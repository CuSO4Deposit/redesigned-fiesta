---
title: An alternative solution to direnv dropping aliases and functions
date: 2025-10-12
lastMod: 2026-09-28
tags:
- Nix
- shell
categories:
summary: "Direnv's inability to export shell-specific aliases and functions, due to its shell-agnostic design, can be addressed in Nix by using pkgs.writeScriptBin to create executable scripts instead."
slug: direnv-aliases
---

Direnv does not support exporting aliases and functions in to the shell, because its works by running through a bash shell and extracting all environment variables from that. It just ignores the aliases and functions. [^1] [^2] This causes aliases defined in `pkgs.mkShell.shellHook` not usable in the development shell.


This is also reasonable and wont-fix because direnv is shell-independent while aliases and functions are shell-dependent, as bbenne10 issued [here](https://web.archive.org/web/20251012023117/https://github.com/nix-community/nix-direnv/issues/245#issuecomment-1961431939).

A solution when using nix to it is to create a `pkgs.writeScriptBin`. This is an example I used as an alternative to an alias `alias mu="......"`:

```nix
{
  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      perSystem = { config, self', inputs', pkgs, system, ... }: {
        devShells = {
          default = pkgs.mkShellNoCC {
            packages = with pkgs; [
              lolcat
              (writeShellScriptBin "mu" ''mv $PUBLICEXPORT_SOURCE/publicExport.zip .; unzip -o -q publicExport.zip; rm publicExport.zip'')
            ];
            shellHook = ''
              echo "use mu to extract \$PUBLICEXPORT_SOURCE/publicExport.zip here and remove source." | lolcat
            '';
          };
        };
      };
    };
}
```

[^1]: https://web.archive.org/web/20251012023117/https://github.com/nix-community/nix-direnv/issues/245
[^2]: https://web.archive.org/web/20251001053401/https://github.com/direnv/direnv/issues/73
