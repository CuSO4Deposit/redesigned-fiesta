---
title: Configure Maunium Stickerpicker for Element
date: 2024-05-05
lastMod: 2025-10-18
tags:
- Element
- Matrix
- Maunium
categories:
---

[GitHub - maunium/stickerpicker: A fast and simple Matrix sticker picker widget](https://github.com/maunium/stickerpicker)


## Maintainer side

### Install

```
% cd stickerpicker
% pip install .
```

If encountered env KeyError in Windows, refer to [issue #52](https://github.com/maunium/stickerpicker/issues/52):

```
# setup.py
long_desc = open("README.md", encoding="utf-8").read()
```

```
% $env:HOME = $env:USERPROFILE
% pip install .
```

### Create decks

Put the stickers into an arbitory folder. Call `sticker-import /path/to/dir --add-to-index ./web/packs`. (`python3 -m sticker.import ...` if in Windows)

The script will prompt for homeserver and access_token, both can be found in `All Settings > Help & About`.

### Host on GitHub pages

Push the `./web/packs` folder to your GitHub fork repo.

In repo settings > pages, select source being `Deploy from a branch` and branch being `Master`, `/(root)`. Save settings and check `<username>.github.io/<forked-repo-name>/web/`.

## User side

### Enable the widget

Input `/devtools` in any chat in Element Web. Select `Other > Explore Account Data`.

Edit the `m.widgets` event (if there is not this event, simply create one) to have the following:

```
{
  "stickerpicker": {
      "content": {
          "type": "m.stickerpicker",
          "url": "https://your.sticker.picker.url/?theme=$theme",
          "name": "Stickerpicker",
          "creatorUserId": "@you:matrix.server.name",
          "data": {}
      },
      "sender": "@you:matrix.server.name",
      "state_key": "stickerpicker",
      "type": "m.widget",
      "id": "stickerpicker"
  }
}
```

And remeber to substitute the `url` to the server hosting stickers. (e.g. `<username>.github.io/stickerpicker/web/`)

Send event. Enjoy!

---

## 用户侧

### 开启部件

在 Element Web 端任意聊天框发送 `/devtools`. 选择 "其他 > 查看账户数据"。

修改 `m.widgets` 事件（如果没有，就创建一个），数据：

```
{
  "stickerpicker": {
      "content": {
          "type": "m.stickerpicker",
          "url": "https://your.sticker.picker.url/?theme=$theme",
          "name": "Stickerpicker",
          "creatorUserId": "@you:matrix.server.name",
          "data": {}
      },
      "sender": "@you:matrix.server.name",
      "state_key": "stickerpicker",
      "type": "m.widget",
      "id": "stickerpicker"
  }
}
```

其中把 `url` 栏换成托管表情的服务器（如 `<username>.github.io/stickerpicker/web/`）。
