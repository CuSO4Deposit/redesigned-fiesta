---
title: 找出所有依赖于特定 nix 包的其他包 - 记录 Qt5 被 deprecate 的修复
date: 2025-08-30
lastMod: 2025-10-18
tags:
- Nix
- NixOS
categories:
---

TL;DR 使用以下命令可以找到所有依赖于特定包的其他 nix 包。

```
$ nix-store --query --referrers /nix/store/xxxxx
```


---

今天在执行 `nixos-rebuild` 时，出现了如下报错：

```
$ nrbt                                                                          M A
warning: Git tree '/home/cuso4d/.nixos' is dirty
building the system configuration...
warning: Git tree '/home/cuso4d/.nixos' is dirty
error:
       … while calling the 'head' builtin
         at /nix/store/4hm8lf740i8qvyg5pzdqfm0rpshwb7vn-source/lib/attrsets.nix:1544:13:
         1543|           if length values == 1 || pred here (elemAt values 1) (head values) then
         1544|             head values
             |             ^
         1545|           else

       … while evaluating the attribute 'value'
         at /nix/store/4hm8lf740i8qvyg5pzdqfm0rpshwb7vn-source/lib/modules.nix:1118:7:
         1117|     // {
         1118|       value = addErrorContext "while evaluating the option `${showOption loc}':" value;
             |       ^
         1119|       inherit (res.defsFinal') highestPrio;

       … while evaluating the option `system.build.toplevel':

       … while evaluating definitions from `/nix/store/4hm8lf740i8qvyg5pzdqfm0rpshwb7vn-source/nixos/modules/system/activation/top-level.nix':

       … while evaluating the option `warnings':

       … while evaluating definitions from `/nix/store/4hm8lf740i8qvyg5pzdqfm0rpshwb7vn-source/nixos/modules/system/boot/systemd.nix':

       … while evaluating the option `systemd.services.home-manager-cuso4d.serviceConfig':

       … while evaluating definitions from `/nix/store/7wkrw49sgffqpd9vm7dfa4ngbh4n2fk5-source/nixos':

       … while evaluating the option `home-manager.users.cuso4d.home.file."/home/cuso4d/.config/fontconfig/conf.d/10-hm-fonts.conf".source':

       … while evaluating definitions from `/nix/store/7wkrw49sgffqpd9vm7dfa4ngbh4n2fk5-source/modules/files.nix':

       … while evaluating the option `home-manager.users.cuso4d.home.file."/home/cuso4d/.config/fontconfig/conf.d/10-hm-fonts.conf".text':

       … while evaluating definitions from `/nix/store/7wkrw49sgffqpd9vm7dfa4ngbh4n2fk5-source/modules/misc/xdg.nix':

       … while evaluating the option `home-manager.users.cuso4d.xdg.configFile."fontconfig/conf.d/10-hm-fonts.conf".text':

       … while evaluating definitions from `/nix/store/7wkrw49sgffqpd9vm7dfa4ngbh4n2fk5-source/modules/misc/fontconfig.nix':

       (stack trace truncated; use '--show-trace' to show the full, detailed trace)

       error: Package ‘qtwebengine-5.15.19’ in /nix/store/4hm8lf740i8qvyg5pzdqfm0rpshwb7vn-source/pkgs/development/libraries/qt-5/modules/qtwebengine.nix:442 is marked as insecure, refusing to evaluate.


       Known issues:
        - qt5 qtwebengine is unmaintained upstream since april 2025.
       It is based on chromium 87.0.4280.144, and supposedly patched up to 135.0.7049.95 which is outdated.

       Security issues are frequently discovered in chromium.
       The following list of CVEs was fixed in the life cycle of chromium 138 and likely also affects qtwebengine:
       - CVE-2025-8879
       - CVE-2025-8880
       - CVE-2025-8901
       - CVE-2025-8881
       - CVE-2025-8882
       - CVE-2025-8576
       - CVE-2025-8577
       - CVE-2025-8578
       - CVE-2025-8579
       - CVE-2025-8580
       - CVE-2025-8581
       - CVE-2025-8582
       - CVE-2025-8583
       - CVE-2025-8292
       - CVE-2025-8010
       - CVE-2025-8011
       - CVE-2025-7656
       - CVE-2025-6558 (known to be exploited in the wild)
       - CVE-2025-7657
       - CVE-2025-6554
       - CVE-2025-6555
       - CVE-2025-6556
       - CVE-2025-6557

       The actual list of CVEs affecting qtwebengine is likely much longer,
       as this list is missing issues fixed in chromium 136/137 and even more
       issues are continuously discovered and lack upstream fixes in qtwebengine.


       You can install it anyway by allowing this package, using the
       following methods:

       a) To temporarily allow all insecure packages, you can use an environment
          variable for a single invocation of the nix tools:

            $ export NIXPKGS_ALLOW_INSECURE=1

          Note: When using `nix shell`, `nix build`, `nix develop`, etc with a flake,
                then pass `--impure` in order to allow use of environment variables.

       b) for `nixos-rebuild` you can add ‘qtwebengine-5.15.19’ to
          `nixpkgs.config.permittedInsecurePackages` in the configuration.nix,
          like so:

            {
              nixpkgs.config.permittedInsecurePackages = [
                "qtwebengine-5.15.19"
              ];
            }

       c) For `nix-env`, `nix-build`, `nix-shell` or any other Nix command you can add
          ‘qtwebengine-5.15.19’ to `permittedInsecurePackages` in
          ~/.config/nixpkgs/config.nix, like so:

            {
              permittedInsecurePackages = [
                "qtwebengine-5.15.19"
              ];
            }
Command 'nix --extra-experimental-features 'nix-command flakes' build --print-out-paths '/home/cuso4d/.nixos#nixosConfigurations."nightcord-dynamica".config.system.build.toplevel' --no-link' returned non-zero exit status 1.
```

可以看出，在构建的过程中，`qtwebengine-5.15.19` 这个包阻碍了构建。我需要找到是哪些包依赖了这个，从而进行对系统配置相对应的调整。

我暂时不知道如何直接生成一个 derivation 的依赖树，在它被构建完成之前（因为目前构建会遇到错误，无法构建完成）。因此我直接在目前系统中寻找这个包。

```
$ nix derivation show -r /run/current-system > derivation.json
$ grep -n "qtwebengine-5.15.9" derivation.json
469148:  "/nix/store/9wkvq3il6idfaifr9wqk79zh1qxirrcn-qtwebengine-5.15.19.drv": {
```

这样我就知道了对应的包的位置。可以查询包的所有依赖者，如果使用 `--referrers-closure` 选项而不是 `--referrers` 则可以查询闭包。

```
$ nix-store --query --referrers /nix/store/9wkvq3il6idfaifr9wqk79zh1qxirrcn-qtwebengine-5.15.19
/nix/store/f5bw8y84yzh825hcdkjxkls93vhkmr85-qtwebengine-5.15.19
/nix/store/6ih0mdpllivbnxrmifj0bcbpvvn7gxkj-fcitx5-chinese-addons-5.1.8
/nix/store/7ijasfsclacmnzk2sbkxspdj6sviwcwr-qtwebengine-5.15.19-bin
/nix/store/7cn2m13sq758al60pkczafcc9wbwfimk-zeal-0.7.2
```

这样我知道问题是由 `fcitx5-chinese-addons` 和 `zeal` 造成的。

  + 3 天前引入了 PR:  https://github.com/nix-community/home-manager/pull/7730，将 `fcitx5-with-addons` 的 default package 从 `pkgs.libsForQt5.fcitx5-with-addons` 换为了 `pkgs.qt6Packages.fcitx5-with-addons`。


  + `zeal` 换为它的 qt6 版本: `zeal-qt6`

  + 没管 `fcitx5-chinese-addons`，好像没影响

再次 rebuild，系统就成功 rebuild 了。
