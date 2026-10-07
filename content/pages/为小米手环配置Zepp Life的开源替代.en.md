---
title: Configuring an Open-Source Alternative to Zepp Life for a Xiaomi Mi Band
date: 2023-01-22
lastMod: 2023-01-22
tags:
categories:
slug: gadgetbridge
ai: translated
---

Steps: [https://codeberg.org/Freeyourgadget/Gadgetbridge](https://codeberg.org/Freeyourgadget/Gadgetbridge)

## Download Gadgetbridge

[Gadgetbridge | F-Droid - Free and Open Source Android App Repository](https://f-droid.org/app/nodomain.freeyourgadget.gadgetbridge)

## Obtain the auth key

Steps: [Huami Server Pairing - Gadgetbridge - Codeberg.org](https://codeberg.org/Freeyourgadget/Gadgetbridge/wiki/Huami-Server-Pairing)

If the app the band was originally bound to is “Mi Wear” (com.xiaomi.wearable), it will not return normal information. You can first switch to binding the band with “Zepp Life” (com.xiaomi.hm.health).

```
$ git clone https://codeberg.org/argrento/huami-token.git
$ cd huami-token
$ python3 huami_token.py --method xiaomi --bt_keys
```

Log in by following the prompts, and paste the redirect link. It returned data like this.

```
Token: ['C3_xxxxxxxxxxxxxxxxxxx']
Logging in...
Logged in! User id: 10xxxxxxx
Getting linked wearables...

╓───Device 0
║  MAC: 11:22:33:44:55:66, active: No
║  Key: 0x11111111111111111111111111111111
╙────────────

╓───Device 1
║  MAC: F4:11:22:33:44:55, active: Yes
║  Key: 0xfe000000000000000000000000000000
╙────────────

Logged out.
```

You can identify which device it is via the device's Bluetooth address (if only one device is active, active: Yes also works). The corresponding “Key” is the auth key you need.

## Connect to Gadgetbridge

Do not unbind the band from “Zepp Life”; kill “Zepp Life”. After that, the device “Mi Smart Band 5” will appear in your phone's Bluetooth settings.

Use _Gadgetbridge_ to search for devices, long-press the device card found, and fill in the corresponding “Key” in the pop-up window. Then return to the device card page and tap the card to pair and connect.

Once the device card appears on the home page, pairing was successful, and you can go ahead and uninstall Zepp Life (do not unbind before uninstalling, because the auth key is regenerated on every binding).
