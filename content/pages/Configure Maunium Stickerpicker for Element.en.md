---
title: Configure Maunium Stickerpicker for Element
date: 2024-05-05
lastMod: 2024-05-05
tags:
  - Element
  - Matrix
  - Maunium
categories:
slug: element-stickerpicker
ai: translated
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

## User side

### Enable the widget

Send `/devtools` in any chat input in Element Web. Select "Other > Explore Account Data".

Edit the `m.widgets` event (if it doesn't exist, create one) with the following data:

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

Replace the `url` field with the server hosting the stickers (e.g. `<username>.github.io/stickerpicker/web/`).
