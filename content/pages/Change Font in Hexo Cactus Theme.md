---
title: Change Font in Hexo Cactus Theme
date: 2023-04-06
lastMod: 2025-10-18
tags:
- font
- Hexo
categories:
---

Modify `themes/cactus/source/layout/_partial/header.ejs`.

```
<!-- styles -->
    <link rel="stylesheet" href="https://cdn.bootcdn.net/ajax/libs/lxgw-wenkai-webfont/1.6.0/style.min.css" />
    <%- css('css/style') %>
```

[https://github.com/chawyehsu/lxgw-wenkai-webfont](https://github.com/chawyehsu/lxgw-wenkai-webfont)

Modify `_variables.styl`

```
// Fonts
$font-family-body = "Menlo", "Meslo LG", "LXGW WenKai", monospace
$font-family-mono = "Menlo", "Meslo LG", "LXGW WenKai Mono", monospace
$font-size = 14px
...
```


## Deprecated

**Deprecated because ttf file is too big for users to load from this source. Use a CDN is better.**

[how to change the font size ? · Issue #311 · probberechts/hexo-theme-cactus · GitHub](https://github.com/probberechts/hexo-theme-cactus/issues/311)

Move font file to `themes/cactus/source/font/<filename>`. In my case <filename>="LXGWWenKaiMono-Regular.ttf".

Modify `_fonts.styl`:

```
# themes/cactus/source/css/_fonts.styl

...
@font-face
font-style: normal
font-family: "lxgw"
src: url("../font/LXGWWenKaiMono-Regular.ttf") format("truetype")
```

Modify `_variables.styl`

```
// Fonts
$font-family-body = "Menlo", "Meslo LG", "lxgw", monospace
$font-family-mono = "Menlo", "Meslo LG", "lxgw", monospace
$font-size = 14px
...
```

Reload website, fonts will load in left-to-right order.
