---
title: Building loong64 Docker Images on NixOS
ai: translated
date: 2025-06-20
lastMod: 2026-09-28
tags:
- docker
- loong
- Nix
- NixOS
categories:
slug: nixos-loong64-docker
---

When trying to cross-compile a loong64 image on an x86_64 platform using docker buildx, a problem occurred:


```
1 warning found (use docker --debug to expand):
- InvalidBaseImagePlatform: Base image lcr.loongnix.cn/library/node:22.15-alpine3.21 was pulled with platform "linux/loong64", expected "linux/amd64" for current build

ERROR: failed to solve: process "/bin/sh -c npm run build" did not complete successfully: exit code: 1
```


When trying to build an image for another platform, the build arg that needs to be provided is `--build-arg BUILDPLATFORM=<arch>`. The builder used by docker buildx can be seen with `docker buildx ls`. Find the builder in use and inspect it:

```shell-session
# docker buildx ls
[sudo] password for cuso4d:
NAME/NODE     DRIVER/ENDPOINT   STATUS    BUILDKIT   PLATFORMS
default*      docker
 \_ default    \_ default       running   v0.22.0    linux/amd64, linux/arm64, linux/386
 
# docker buildx inspect default
ame:          default
Driver:        docker
Last Activity: 2025-06-20 09:43:16 +0000 UTC

Nodes:
Name:             default
Endpoint:         default
Status:           running
BuildKit version: v0.22.0
Platforms: linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386
Labels:
 org.mobyproject.buildkit.worker.moby.host-gateway-ip: 172.17.0.1
...
```


As you can see, loong64 is not in Platforms. Therefore the build fails. The solution to this problem is that docker will run a qemu virtual machine to run the build for the corresponding platform. This qemu is usually injected by running a container. Loongson's is here:

```shell-session
# docker run --rm --privileged loongcr.lcpu.dev/multiarch/archlinux --reset -p yes # loong64
```


However, after running this on NixOS, although the runtime produced normal output adding certain binfmt entries, the platforms shown when inspecting the builder did not increase. This is because binfmt_misc was not enabled. In NixOS, this corresponds to an option (currently, nixpkgs 08f22084):

```nix
# configuration.nix

{
  boot.binfmt.emulatedSystems = [ "loongarch64-linux" ];
}
```


After enabling this option and rebuilding the system, run the container that registers binfmt once more, and you will see many more architectures in Platforms; the loong64 container can then be built normally.

```shell-session
# docker run --rm --privileged loongcr.lcpu.dev/multiarch/archlinux --reset -p yes
Setting /usr/bin/qemu-alpha-static as binfmt interpreter for alpha
Setting /usr/bin/qemu-arm-static as binfmt interpreter for arm
Setting /usr/bin/qemu-armeb-static as binfmt interpreter for armeb
Setting /usr/bin/qemu-sparc-static as binfmt interpreter for sparc
Setting /usr/bin/qemu-sparc32plus-static as binfmt interpreter for sparc32plus
Setting /usr/bin/qemu-sparc64-static as binfmt interpreter for sparc64
Setting /usr/bin/qemu-ppc-static as binfmt interpreter for ppc
Setting /usr/bin/qemu-ppc64-static as binfmt interpreter for ppc64
Setting /usr/bin/qemu-ppc64le-static as binfmt interpreter for ppc64le
Setting /usr/bin/qemu-m68k-static as binfmt interpreter for m68k
Setting /usr/bin/qemu-mips-static as binfmt interpreter for mips
Setting /usr/bin/qemu-mipsel-static as binfmt interpreter for mipsel
Setting /usr/bin/qemu-mipsn32-static as binfmt interpreter for mipsn32
Setting /usr/bin/qemu-mipsn32el-static as binfmt interpreter for mipsn32el
Setting /usr/bin/qemu-mips64-static as binfmt interpreter for mips64
Setting /usr/bin/qemu-mips64el-static as binfmt interpreter for mips64el
Setting /usr/bin/qemu-sh4-static as binfmt interpreter for sh4
Setting /usr/bin/qemu-sh4eb-static as binfmt interpreter for sh4eb
Setting /usr/bin/qemu-s390x-static as binfmt interpreter for s390x
Setting /usr/bin/qemu-aarch64-static as binfmt interpreter for aarch64
Setting /usr/bin/qemu-aarch64_be-static as binfmt interpreter for aarch64_be
Setting /usr/bin/qemu-hppa-static as binfmt interpreter for hppa
Setting /usr/bin/qemu-riscv32-static as binfmt interpreter for riscv32
Setting /usr/bin/qemu-riscv64-static as binfmt interpreter for riscv64
Setting /usr/bin/qemu-xtensa-static as binfmt interpreter for xtensa
Setting /usr/bin/qemu-xtensaeb-static as binfmt interpreter for xtensaeb
Setting /usr/bin/qemu-microblaze-static as binfmt interpreter for microblaze
Setting /usr/bin/qemu-microblazeel-static as binfmt interpreter for microblazeel
Setting /usr/bin/qemu-or1k-static as binfmt interpreter for or1k
Setting /usr/bin/qemu-hexagon-static as binfmt interpreter for hexagon
Setting /usr/bin/qemu-loongarch64-static as binfmt interpreter for loongarch64

# docker buildx inspect default
Name:          default
Driver:        docker
Last Activity: 2025-06-20 09:43:16 +0000 UTC

Nodes:
Name:             default
Endpoint:         default
Status:           running
BuildKit version: v0.22.0
Platforms:        linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386, linux/arm64, linux/riscv64, linux/ppc64, linux/ppc64le, linux/s390x, linux/mips64le, linux/mips64, linux/loong64, linux/arm/v7, linux/arm/v6
...
```


## References

  + https://bbs.deepin.org/en/post/263728


  + https://loonguser.github.io/system/install_archlinux/

  + https://nixos-and-flakes.thiscute.world/zh/development/cross-platform-compilation#linux-binfmt-misc

  + https://github.com/lcpu-club/loong64-dockerfiles
