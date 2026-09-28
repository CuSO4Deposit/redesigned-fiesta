---
title: "Markdown - Syntaxes that I don't Know"
date: 2025-02-25
lastMod: 2026-09-28
tags:
- Markdown
categories:
slug: markdown-syntax
---

# Syntaxes


  + ## Line Break


    + End a line with 2 or more trailing spaces for a line break (\<br\> tag in HTML).


  + ## Bold and Italic

    + Use `***` to warp the text you want to ***Bold and Italic***.


  + ## Nest Another Element in a List

    + Indent the element 4 spaces in the list environment.
```markdown
- list 0
- list 1
    > This is a blockquote nested in a list
- list 2
```


  + ## Escape Backticks in a Code Element

    + Wrap the code element that includes one or more backticks with double backticks.

```markdown
``This is a code element with a backtick(`) inside.``
```


  + ## Adding a Title for a Link

    + Add a title enclosed in quotation marks after the link url.

```markdown
My favorite search engine is [DuckDuckGo](https://duckduckgo.com "The best search engine for privacy").
```


  + ## Automatic Links

    + Enclose a url or email address with angle brackets if they do not need a link text.


  + ## Formatting Links

    + To emphasize links, add asterisks before and after the brackets and parentheses. To denote links as code, add backticks in the brackets.

```markdown
I love supporting the **[EFF](https://eff.org)**.
This is the *[Markdown Guide](https://www.markdownguide.org)*.
See the section on [`code`](#code).
```


  + ## Reference-style Links

```markdown
This is a [text with link][1].

...

[1]: https://some.domain.tld/path#hashtag "title shown when hovering"
```


  + ## Linking Images

```markdown
[![An old rock in the desert](/static/assets/shiprock.jpg)](https://www.flickr.com/photos/beaurogers/31833779864/in/photolist-Qv3rFw-34mt9F-a9Cmfy-5Ha3Zi-9msKdv-o3hgjr-hWpUte-4WMsJ1-KUQ8N-deshUb-vssBD-6CQci6-8AFCiD-zsJWT-nNfsgB-dPDwZJ-bn9JGn-5HtSXY-6CUhAL-a4UTXB-ugPum-KUPSo-fBLNm-6CUmpy-4WMsc9-8a7D3T-83KJev-6CQ2bK-nNusHJ-a78rQH-nw3NvT-7aq2qf-8wwBso-3nNceh-ugSKP-4mh4kh-bbeeqH-a7biME-q3PtTf-brFpgb-cg38zw-bXMZc-nJPELD-f58Lmo-bXMYG-bz8AAi-bxNtNT-bXMYi-bXMY6-bXMYv)
```


  + ## Verbatim Code Blocks

    + Aside from fenced code blocks, many implementations support **verbatim text**. Indent all lines in a block 4 spaces will make it treated as a code block.

```markdown
    this {
        is treated as
        a code block.
    }
```


# Pandoc's Markdown Best Practices

  + **Warning**: The following syntaxes may not be supported by all implementations.


  + ## Put Black Lines before and after Elements

    + Always put blank lines before and after **horizontal rules**.


    + Put a blank line before **headings**.

    + Put a blank line before **blockquotes**.

  + ## Put a space between the Hashtags and Headers

```markdown
## Headers should be like this

###Never do this
```


  + ## Headers can be Assigned Attributes

```markdown
# My heading {#identifier .class .class key=value key=value}
```


  + ## Line Blocks

    + Use a vertical bar to start a line block. Pandoc's Markdown will preserve all leading spaces, line breaks and so on in the line block.

```markdown
| 200 Main St.
| Berkeley, CA 94718
```


  + ## Sidenotes

    + Pandoc's Markdown allows footnotes:

```markdown
Here is a footnote reference,[^1] and another.[^longnote]

[^1]: Here is the footnote.

[^longnote]: Here's one with multiple blocks.

    Subsequent paragraphs are indented to show that they
belong to the previous footnote.

        { some.code }

    The whole paragraph can be indented, or just the first
    line.  In this way, multi-paragraph footnotes work like
    multi-paragraph list items.

This paragraph won't be part of the note, because it
isn't indented.
```


    + Pandoc's Markdown allows inline notes:

```markdown
Here is an inline note.^[Inline notes are easier to write, since
you don't have to pick an identifier and move down to type the
note.]
```
