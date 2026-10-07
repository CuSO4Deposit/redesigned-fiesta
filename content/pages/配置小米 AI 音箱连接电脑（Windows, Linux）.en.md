---
title: "Configuring a Xiaomi AI Speaker to Connect to a Computer (Windows, Linux)"
date: 2025-10-20
lastMod: 2025-10-20
tags:
  - Bluetooth
  - Linux
  - Windows
categories:
summary: This article explains how to connect a Xiaomi AI Speaker to a computer as a speaker in Windows 11 and Linux, and shares the problems encountered during connection and their solutions, especially achieving a more stable connection under Linux via blueman and pavucontrol.
slug: mi-ai-speaker
ai: translated
---

I have a Xiaomi AI Speaker that hasn't been used for a long time, probably the first generation or not long after it. Recently I wanted to use it as a computer speaker—might as well—so I set it up.

## Windows 11

- Under Windows 11, searching directly in the Bluetooth interface will not find the Xiao Ai Speaker. You need to do this: ↓

- How to connect the Xiao Ai Speaker on Win11: Bluetooth & devices - Show more devices - scroll down to **"Device settings" - Bluetooth device discovery - change "Default" to Advanced**, then add a Bluetooth device and you can find the Xiao Ai Speaker and connect normally. Discovered by accident; already connected. by https://space.bilibili.com/78499643 at https://www.bilibili.com/opus/712676963114811396

- Although it can connect after doing this, it still disconnects every few days, and after disconnecting it cannot connect to the device again; you need to restart Windows' Bluetooth. I feel it's simply Windows' fault—maybe some driver is too new for my old speaker.

## Linux

- Packages needed: `blueman`, `pavucontrol`

- The Bluetooth Manager GUI provided by blueman can directly find the Xiao Ai Speaker. The Volume Control provided by pavucontrol lets you control which output device each audio stream goes to.

- Here is an example configuration on NixOS 25.11.

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
