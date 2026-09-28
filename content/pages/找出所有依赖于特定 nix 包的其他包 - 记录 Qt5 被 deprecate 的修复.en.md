---
title: Finding All Other Packages That Depend on a Specific Nix Package - Notes on Fixing the Qt5 Deprecation
date: 2025-08-30
lastMod: 2026-09-28
tags:
  - Nix
  - NixOS
categories:
slug: nix-reverse-deps
ai: translated
---

TL;DR Use the following command to find all other nix packages that depend on a specific package.

```
$ nix-store --query --referrers /nix/store/xxxxx
```

---

Today, while running `nixos-rebuild`, I got the following error:

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

As you can see, during the build the package `qtwebengine-5.15.19` blocked the build. I needed to find which packages depend on it, so I could make the corresponding adjustments to my system configuration.

For now I don't know how to directly generate a dependency tree for a derivation before it has finished building (since the build currently errors out and cannot finish). So I looked for this package directly in the current system.

```
$ nix derivation show -r /run/current-system > derivation.json
$ grep -n "qtwebengine-5.15.9" derivation.json
469148:  "/nix/store/9wkvq3il6idfaifr9wqk79zh1qxirrcn-qtwebengine-5.15.19.drv": {
```

This told me the location of the corresponding package. You can query all referrers of the package; if you use the `--referrers-closure` option instead of `--referrers`, you can query the closure.

```
$ nix-store --query --referrers /nix/store/9wkvq3il6idfaifr9wqk79zh1qxirrcn-qtwebengine-5.15.19
/nix/store/f5bw8y84yzh825hcdkjxkls93vhkmr85-qtwebengine-5.15.19
/nix/store/6ih0mdpllivbnxrmifj0bcbpvvn7gxkj-fcitx5-chinese-addons-5.1.8
/nix/store/7ijasfsclacmnzk2sbkxspdj6sviwcwr-qtwebengine-5.15.19-bin
/nix/store/7cn2m13sq758al60pkczafcc9wbwfimk-zeal-0.7.2
```

This told me the problem was caused by `fcitx5-chinese-addons` and `zeal`.

- A PR was introduced 3 days ago: https://github.com/nix-community/home-manager/pull/7730, which changed the default package of `fcitx5-with-addons` from `pkgs.libsForQt5.fcitx5-with-addons` to `pkgs.qt6Packages.fcitx5-with-addons`.

- Switched `zeal` to its qt6 version: `zeal-qt6`

- Left `fcitx5-chinese-addons` alone; it seemed to have no effect

After rebuilding again, the system rebuilt successfully.
