---
title: Setup remote server pubkey login
date: 2024-08-18
lastMod: 2026-09-28
tags:
categories:
slug: ssh-pubkey-login
---

create pubkey pair locally: `ssh-keygen`


send key to server `authorized_keys`:
```shell-session
$ ssh-copy-id -p 22 -i <path_to_public_key> <username>@<host>
```

generate PuTTY-compatible private key format (`*.ppk`):
```shell-session
$ puttygen <path_to_private_key> -O private <path_to_ppk>
```
