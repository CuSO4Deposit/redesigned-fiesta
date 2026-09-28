---
title: "配置小米 AI 音箱连接电脑（Windows, Linux）"
date: 2025-10-20
lastMod: 2025-10-20
tags:
- Bluetooth
- Linux
- Windows
categories:
summary: 本文介绍了如何在 Windows 11 和 Linux 系统中连接小米 AI 音箱作为电脑音箱，并分享了连接过程中遇到的问题及解决方法，尤其是在 Linux 系统下通过 blueman 和 pavucontrol 实现更稳定的连接。
---

我有一台已经很久没有用过的小米 AI 音箱，大概是初代或者初代过去没多久的。最近想把它拿来当电脑音箱，不用白不用，所以配置下。


## Windows 11

  + Windows 11 下直接在蓝牙界面搜索是找不到小爱音箱的。需要这样做：↓


  + win11的连接小爱音箱方法：蓝牙和其他设备-显示更多设备-下拉有个**“设备设置“-蓝牙设备发现-把”默认“改为高级**，然后添加蓝牙设备就能正常找到小爱音箱正常连接了，无意中发现的，已经连接上了 by https://space.bilibili.com/78499643 at https://www.bilibili.com/opus/712676963114811396

  + 虽然尽管像这样做了之后能连上，还是三天两头就断连，断连之后就连接不上设备了，需要重启 Windows 的蓝牙功能。感觉单纯是 Windows 的锅，没准是什么驱动太新了我老音箱配不上吧。

## Linux

  + 需要用到的包：`blueman`, `pavucontrol`


  + blueman 提供的 Bluetooth Manager GUI 可以直接搜索到小爱音箱。pavucontrol 提供的 Volume Control 则可以控制每一个音频输出从哪一个输出设备走。

  + 这是在 NixOS 25.11 上的示例配置。
```nix
{
  environment.systemPackages = with pkgs; [
    pavucontrol # Pipewire graphical tool
  ];
  
  # https://nixos.wiki/wiki/Bluetooth
  hardware.bluetooth = {
    enable = true;
    powerOnBoot = true;
    settings = {
      General = {
        Experimental = true;
        FastConnectable = true;
      };
      Policy = {
        AntoEnable = true;
      };
    };
  };
  
  services.blueman.enable = true;
}
```
