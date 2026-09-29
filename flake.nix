{
  description = "Description for the project";

  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    pre-commit-hooks.url = "github:cachix/git-hooks.nix";
    logseq-schrodinger = {
      url = "github:CuSO4Deposit/logseq-schrodinger";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [
        inputs.pre-commit-hooks.flakeModule
      ];
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "aarch64-darwin"
        "x86_64-darwin"
      ];
      perSystem =
        {
          config,
          self',
          inputs',
          pkgs,
          system,
          ...
        }:
        {
          packages = {
            schrodinger = inputs.logseq-schrodinger.packages.${system}.default;
            hugo = pkgs.hugo;
            uv = pkgs.uv;
          };
          pre-commit.settings = {
            src = ./.;
            hooks = {
              nixfmt-rfc-style.enable = true;
              ruff.enable = true;
              ruff-format.enable = true;
            };
          };
          devShells = {
            default = pkgs.mkShellNoCC {
              buildInputs = with pkgs; [
                uv
                pythonManylinuxPackages.manylinux2014Package
                just
                hugo
                nodejs
              ];
              NIX_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
                pkgs.stdenv.cc.cc
                pkgs.pythonManylinuxPackages.manylinux2014Package
              ];
              NIX_LD = builtins.readFile "${pkgs.stdenv.cc}/nix-support/dynamic-linker";

              shellHook = ''
                # `nix develop` blanks SSL_CERT_FILE; the uv-managed Python then
                # falls back to /etc/ssl/cert.pem, which NixOS does not provide.
                # Point it at the system bundle so HTTPS (and any local proxy CA)
                # is trusted.
                if [ -e /etc/ssl/certs/ca-bundle.crt ]; then
                  export SSL_CERT_FILE=/etc/ssl/certs/ca-bundle.crt
                fi

                # install pre-commit hooks
                ${config.pre-commit.installationScript}

                uv venv --allow-existing
                . .venv/bin/activate
                uv sync
              '';
            };
          };
        };
    };
}
