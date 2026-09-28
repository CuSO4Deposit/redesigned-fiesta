---
title: 为小米手环配置Zepp Life的开源替代
date: 2023-01-22
lastMod: 2026-09-28
tags:
categories:
slug: gadgetbridge
---

Steps: [https://codeberg.org/Freeyourgadget/Gadgetbridge](https://codeberg.org/Freeyourgadget/Gadgetbridge)


## 下载Gadgetbridge

[Gadgetbridge | F-Droid - Free and Open Source Android App Repository](https://f-droid.org/app/nodomain.freeyourgadget.gadgetbridge)

## 获取auth key

Steps: [Huami Server Pairing - Gadgetbridge - Codeberg.org](https://codeberg.org/Freeyourgadget/Gadgetbridge/wiki/Huami-Server-Pairing)

原来手环绑定的app如果是“小米穿戴”(com.xiaomi.wearable)，则不能返回正常的信息，可以先换用“Zepp Life”(com.xiaomi.hm.health)绑定手环。

```
$ git clone https://codeberg.org/argrento/huami-token.git
$ cd huami-token
$ python3 huami_token.py --method xiaomi --bt_keys
```

按提示操作登录，并粘贴重定向至的链接，返回了类似这样的数据。

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

通过设备的蓝牙地址可以确定是哪一台设备（如果只有一个设备启用中，通过active: Yes也可以），对应的“Key”即为需要的auth key。

## 连接到Gadgetbridge

不要解除手环和"Zepp Life"的绑定，Kill "Zepp Life"，此后在手机的蓝牙设置中就可以看到设备"Mi Smart Band 5"。

使用 *Gadgetbridge* 搜索设备，长按搜索到的设备卡片，在弹出窗口填入对应的"Key"选项。然后返回设备卡片页，单击卡片进行配对和连接。

首页显示了这个设备卡片，说明配对成功，可以直接卸载Zepp Life啦（不可以先解绑再卸载，因为auth key是每次绑定重新生成）。
