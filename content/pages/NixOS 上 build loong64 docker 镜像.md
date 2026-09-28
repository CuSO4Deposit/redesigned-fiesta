---
title: NixOS 上 build loong64 docker 镜像
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

在 x86_64 平台上使用 docker buildx 尝试交叉编译 loong64 的镜像时，出现问题：


```
1 warning found (use docker --debug to expand):
- InvalidBaseImagePlatform: Base image lcr.loongnix.cn/library/node:22.15-alpine3.21 was pulled with platform "linux/loong64", expected "linux/amd64" for current build

ERROR: failed to solve: process "/bin/sh -c npm run build" did not complete successfully: exit code: 1
```


在尝试 build 其他平台上的镜像的时候，需要提供的 build arg 是 `--build-arg BUILDPLATFORM=<arch>`。docker buildx 使用的 builder 可以通过 `docker buildx ls` 来看到。找到正在使用的 builder 并 inspect：

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


可以看到 Platforms 里是没有 loong64 的。因此 build 会失败。对这个问题的解决方案，是 docker 将会跑一个 qemu 虚拟机来运行对应平台上的 build。这个 qemu 通常的注入的方式是跑一个容器。龙芯的在这里：

```shell-session
# docker run --rm --privileged loongcr.lcpu.dev/multiarch/archlinux --reset -p yes # loong64
```


但是 NixOS 上跑过这个之后，虽然运行时有正常的输出添加了某些 binfmt，但 inspect builder 看到的 platform 并没有增加。这是因为 binfmt_misc 并没有被启动。在 NixOS 中，这对应着一个选项（目前，nixpkgs 08f22084）：

```nix
# configuration.nix

{
  boot.binfmt.emulatedSystems = [ "loongarch64-linux" ];
}
```


启用这个选项并 rebuild 系统之后，再去跑刚才的用于注册 binfmt 的容器，就可以看见 Platforms 里多了很多架构，loong64 的容器也可以正常构建了。

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
