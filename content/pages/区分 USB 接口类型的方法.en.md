---
title: How to Distinguish USB Connector Types
date: 2024-08-19
lastMod: 2026-09-28
tags:
categories:
slug: usb-connector-types
ai: translated
---

## Env / Dependency

- Arch Linux, x86_64

- core/usbutils

## Determining Whether a USB Device Supports USB 3.0

- ~~A blue connector generally means USB 3.0~~

- USB 3.0 has five additional pins [Image](https://en.wikipedia.org/wiki/USB_3.0#/media/File:Connector_USB_3_IMGP6024_wp.jpg)

- Using lsusb:

```shell-session
$ lsusb                        
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 002: ID 04f2:b689 Chicony Electronics Co., Ltd TOSHIBA Web Camera - HD
Bus 001 Device 003: ID 8087:0a2b Intel Corp. Bluetooth wireless interface
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 002 Device 004: ID 1058:266e Western Digital Technologies, Inc. Elements SE SSD

$ lsusb -D /dev/bus/usb/002/004 
Device: ID 1058:266e Western Digital Technologies, Inc. Elements SE SSD
Couldn't open device, some information will be missing
Device Descriptor:
  bLength                18
  bDescriptorType         1
  bcdUSB               3.20
```

**In the device descriptor, `bcdUSB` is the USB version supported by this USB device.**

## Distinguishing 2.0/3.0 USB Ports on a Device

- Using the example above:

```shell-session
$ lsusb                        
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 001 Device 002: ID 04f2:b689 Chicony Electronics Co., Ltd TOSHIBA Web Camera - HD
Bus 001 Device 003: ID 8087:0a2b Intel Corp. Bluetooth wireless interface
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 002 Device 004: ID 1058:266e Western Digital Technologies, Inc. Elements SE SSD
```

The 2.0 root hub and the 3.0 root hub have different bus numbers. Plug in a USB device, then check which corresponding bus number the device appears under to determine the type of the port it was plugged into.

- Detailed Explanation from GPT-4-turbo:

  - To determine which USB ports on your device are USB 2.0 and which are USB 3.0 based on the output from `lsusb`, you can look at the Bus IDs and their associated root hub device IDs. Here's how you can interpret the information:

  - ### Understanding the `lsusb` Output

1. **Bus and Device IDs**: Each USB device connected to your system is listed with a Bus ID and a Device ID. For example, `Bus 001 Device 001` indicates the first device on the first USB bus.

2. **Device Description and Vendor IDs**: Each entry includes a vendor and product ID (`ID 1d6b:0002`), followed by a description of the device (e.g., `Linux Foundation 2.0 root hub`).

3. **Root Hubs**:

   - **USB 2.0 Root Hubs**: Typically have a device ID that ends with `0002`. In your output:

     - `Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub` indicates that Bus 001 is a USB 2.0 bus.

   - **USB 3.0 Root Hubs**: Typically have a device ID that ends with `0003`. In your output:

     - `Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub` indicates that Bus 002 is a USB 3.0 bus.

   - ### Determining USB Port Versions
     - **USB 2.0 Ports** are linked to `Bus 001` in your case. Any device listed under this bus, like your webcam and Bluetooth interface, is connected via a USB 2.0 port.

     - **USB 3.0 Ports** are linked to `Bus 002` in your case. The Western Digital SSD connected here is utilizing a USB 3.0 port.

   - ### Physical Identification

To physically identify which ports on your laptop or PC correspond to these bus numbers:

1. **Try Connecting a Device**: Plug a USB device into a port, check `lsusb` or use `dmesg | tail` to see which bus the device appears on. If it appears under `Bus 001`, it's a USB 2.0 port. If it appears under `Bus 002`, it's a USB 3.0 port.

2. **Look for Port Markings**: USB 3.0 ports are sometimes marked with the SuperSpeed USB logo or might have blue plastic inside the port instead of black or white, which is common with USB 2.0 ports.

3. **Check Documentation**: Refer to your device’s user manual or manufacturer's website for detailed information about the port specifications.

Using these methods, you can effectively identify which ports are USB 2.0 and which are USB 3.0 on your Arch Linux system.
