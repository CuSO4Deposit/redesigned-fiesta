---
title: nginx server_name 的反常理行为
date: 2024-08-24
lastMod: 2025-10-18
tags:
- nginx
categories:
---

## TL;DR

> It is important to understand that Nginx will only evaluate the `server_name` directive when it needs to distinguish between server blocks that match to the same level of specificity in the `listen` directive.


---

在全新安装了 Nginx 的机器上进行配置时，发现 server_name 这一配置失效：

  + 某个 server 块中，配置有 server_name 和 location 块，而本地的 3000 端口运行着应用。`*.internal` 与 `*.localhost` 已在 DNS 记录中指向 `127.0.0.1`。：
```nginx
server {
    listen 80;
    server_name sub.internal;

    location / {
        proxy_pass http://127.0.0.1:3000;
    }
}
```


  + 在这一配置下，期望的行为是 在访问 `sub.internal` 时被重定向到 `127.0.0.1:3000`，访问其他域名如 `whatever.internal` 或 `whatever.localhost` 时，无事发生。

  + 但事实上的行为是：不仅指定的域名会被重定向，上二例所举的域名，以至于任意一个 `*.internal`，都会重定向到 `127.0.0.1:3000`。

问题发生是因为这台机器的 nginx 是全新配置的，只有这一个 server 块。根据[这篇文章](https://www.digitalocean.com/community/tutorials/understanding-nginx-server-and-location-block-selection-algorithms)的解读，只有在 listen 解析出满足符合条件的 server 块不止一个时，`server_name` 才被用于确定哪一个 server 块被选择。因此解决方案是添加一个 server 块。
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
