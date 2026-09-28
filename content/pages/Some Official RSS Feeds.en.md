---
title: Some Official RSS Feeds
date: 2025-10-13
lastMod: 2026-09-28
tags:
  - RSS
categories:
summary: "Some services provide their official RSS feeds so you don't have to use services like RSSHub. This page lists some."
slug: official-rss-feeds
ai: translated
---

## GitHub

- A private feed can be retrieved with a query parameter `?token=:secret` where `:secret` is a personal access token. [Official Documentation](https://docs.github.com/en/rest/activity/feeds)

- Repo releases[^1]

  - https://github.com/:owner/:repo/releases.atom

- Repo commits[^2]

  - https://github.com/:owner/:repo/:branch.atom

- User activities[^1]

  - https://github.com/:user.atom

- Wiki history[^1]

  - https://github.com/:owner/:repo/wiki.atom

- File updates[^2], this interface is not officially documented

  - https://github.com/:owner/:repo/commits/:branch/:path-to-file.atom

## Discourse

- There are a lot of other official feed interfaces tracking categories, groups, posts, tags, topics, users and so on, please check [this topic](https://meta.discourse.org/t/finding-discourse-rss-feeds/264134)!

- Topic updates[^3]

  - https://discourse.example.org/t/-/:id.rss

## Youtube

- Playlist history

  - https://youtube.com/feeds/video.xml?playlist_id=:playlist-id

- Channel history[^4]

  - https://youtube.com/feeds/video.xml?channel_id=:channel-id

[^1]: https://web.archive.org/web/20251010135905/https://docs.rsshub.app/routes/programming

[^2]: https://web.archive.org/web/20250930150059/https://stackoverflow.com/questions/7353538/setting-up-a-github-commit-rss-feed

[^3]: https://web.archive.org/web/20250929221835/https://meta.discourse.org/t/finding-discourse-rss-feeds/264134

[^4]: https://web.archive.org/web/20250923163519/https://chuck.is/yt-rss/
