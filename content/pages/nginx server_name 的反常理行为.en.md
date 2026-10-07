---
title: The Counterintuitive Behavior of nginx server_name
ai: translated
date: 2024-08-24
lastMod: 2024-08-24
tags:
- nginx
categories:
slug: nginx-server-name
---

## TL;DR

> It is important to understand that Nginx will only evaluate the `server_name` directive when it needs to distinguish between server blocks that match to the same level of specificity in the `listen` directive.


---

While configuring a machine with a fresh Nginx installation, I found that the server_name setting did not work:

  + In a server block, server_name and location blocks were configured, and an application was running on local port 3000. `*.internal` and `*.localhost` already pointed to `127.0.0.1` in DNS records:
```nginx
server {
    listen 80;
    server_name sub.internal;

    location / {
        proxy_pass http://127.0.0.1:3000;
    }
}
```


  + Under this configuration, the expected behavior is that accessing `sub.internal` is redirected to `127.0.0.1:3000`, while accessing other domains such as `whatever.internal` or `whatever.localhost` does nothing.

  + But the actual behavior was: not only the specified domain gets redirected, but the domains mentioned in the two examples above, and indeed any `*.internal`, are redirected to `127.0.0.1:3000`.

The problem occurred because this machine's nginx was freshly configured and had only this one server block. According to [this article](https://www.digitalocean.com/community/tutorials/understanding-nginx-server-and-location-block-selection-algorithms), `server_name` is only used to determine which server block is selected when the `listen` directive resolves more than one matching server block. Therefore the solution is to add another server block.
```nginx
server {
    listen 80;
    server_name sub.internal;

    location / {
        proxy_pass http://127.0.0.1:3000;
    }
}

server {
    listen 80;
    server_name *.internal;

    return 404;
}
```
