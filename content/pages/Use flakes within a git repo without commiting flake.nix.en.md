---
title: Use flakes within a git repo without commiting flake.nix
date: 2025-09-12
lastMod: 2026-09-28
tags:
  - Flakes
  - Nix
categories:
sunmary: "This article demonstrates how to use `direnv` and Flakes to start a development environment without committing `flake.nix` to the repository, which is useful for teams not using Nix."
slug: flakes-in-git-repo
ai: translated
---

Doing the following allows you to use flakes to start a development environment without commit the `flake.nix` to the repo, for cases when your team does not use nix. [^1]

```shell
[1:user@hostname:~/project-name on main]
$ nvim .envrc
direnv: error /home/user/project-name/.envrc is blocked. Run `direnv allow` to approve its content
[1:user@hostname:~/project-name on main]
$ direnv allow
direnv: loading ~/project-name/.envrc
direnv: using flake ~/flake-project
direnv: nix-direnv: Renewed cache
git-hooks.nix: updating /home/user/project-name repo
/home/user/project-name/.pre-commit-config.yaml
pre-commit installed at .git/hooks/pre-commit
direnv: export +CONFIG_SHELL +HOST_PATH +IN_NIX_SHELL +NIX_BUILD_CORES +NIX_CFLAGS_COMPILE +NIX_ENFORCE_NO_NATIVE +NIX_LDFLAGS +NIX_STORE +NODE_PATH +SOURCE_DATE_EPOCH +__structuredAttrs +buildInputs +buildPhase +builder +cmakeFlags +configureFlags +depsBuildBuild +depsBuildBuildPropagated +depsBuildTarget +depsBuildTargetPropagated +depsHostHost +depsHostHostPropagated +depsTargetTarget +depsTargetTargetPropagated +doCheck +doInstallCheck +dontAddDisableDepTrack +mesonFlags +name +nativeBuildInputs +out +outputs +patches +phases +preferLocalBuild +propagatedBuildInputs +propagatedNativeBuildInputs +shell +shellHook +stdenv +strictDeps +system ~PATH ~XDG_DATA_DIRS
[1:user@hostname:~/project-name on main]
$ gs
?? .direnv/
?? .envrc
?? .pre-commit-config.yaml
[1:user@hostname:~/project-name on main]
$ cat .envrc
use flake ~/flake-project
watch_file ~/flake-project/flake.nix
[1:user@hostname:~/project-name on main]
$ nvim ./.git/info/exclude
[1:user@hostname:~/project-name on main]
$ gs
[1:user@hostname:~/project-name on main]

```

[^1]: https://discourse.nixos.org/t/can-i-use-flakes-within-a-git-repo-without-committing-flake-nix/18196
