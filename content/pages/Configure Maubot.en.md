---
title: Configure Maubot
date: 2023-05-18
lastMod: 2026-09-28
tags:
  - Matrix
  - Maunium
categories:
slug: maubot
ai: translated
---

[Maubot](https://github.com/maubot/maubot) is a plugin-based Matrix bot SDK.

Its documentation is not written very well, and it doesn't give a sensible, ordered installation process. In fact, when I installed it I had to jump back and forth between various sections of the docs, so I'm recording a reasonable configuration workflow here.

## Set Up the Environment

Install maubot via pip.

```
$ python3 -m venv maubotVenv
$ source ./maubotVenv/bin/activate
$ pip install --upgrade maubot
```

Add the necessary files and directories, otherwise it will report an error.

```
$ vim config.yaml
$ mkdir plugins, trash, logs
```

It seems `config.yaml` can be written pretty much any way you like (but leaving it out will cause an error). I referred to [maubot/base-config.yaml at master · maubot/maubot · GitHub](https://github.com/maubot/maubot/blob/master/examples/config/base-config.yaml), but in fact it doesn't seem to be meant for this purpose—it's for plugins. Anyway, once it runs it will overwrite this and generate a YAML containing the entries.

## Run to Generate a Fillable config

```
$ python3 -m maubot
```

It runs a web interface on port 29316. When you enter it, you'll find that it requires login, but no credentials have been configured yet. For now, press `<C-C>` to stop it, and open config.yaml to see many configuration entries.

## Configure nginx

If you changed the path in config.yaml, fill in the corresponding new path. If you don't have HTTPS, you can change it to listen 80.

```
# nginx.conf

server {
  listen 443;
  ...
  location /_matrix/maubot/v1/logs {
      proxy_pass http://localhost:29316;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";
      proxy_set_header X-Forwarded-For $remote_addr;
  }

  location /_matrix/maubot {
      proxy_pass http://localhost:29316;
      proxy_set_header X-Forwarded-For $remote_addr;
      }
  ...
}

}
```

Check the config and restart nginx.

## Add credentials

Find the `admins` field in config.yaml and add entries in the `name: password` format. Note that root cannot have a password configured; after running, this will be encrypted (rather than plaintext account and password).

The account and password here are used to administer the maubot system (that is, the web app on port 29316), and have nothing to do with Matrix. The `mbc login` you'll use shortly also uses this same set of credentials.

## Log In and Add Plugins

Run it again; in the GUI it's easy to find how to upload a plugin. You can use the official [Echo](https://github.com/maubot/echo) plugin for testing. After logging in you can upload the plugin. But at this point there is still no client or instance. **Each client is equivalent to a logged-in Matrix account, and each instance is equivalent to a plugin running on a specified account.**

To create a client, we need to obtain the access_token and device required by Matrix's end-to-end encryption mechanism. To get them, we need to use the CLI tool provided by maubot.

## Obtain access_token and device via the CLI

Logging in directly from the CLI cannot do encryption, so it's best to set up the encryption components first:

[Encryption - maubot](https://docs.mau.fi/maubot/usage/encryption.html)

```
$ pip install --upgrade maubot[encryption]
$ pip install python-olm --extra-index-url https://gitlab.matrix.org/api/v4/projects/27/packages/pypi/simple
```

`mbc auth` is the command that obtains these two items, but before that you need to `mbc login` to log in to maubot's admin account.

```
$ mbc login
<interactively login with credenricals in config.yaml...>
```

Before `mbc auth`, you also need to add a homeserver in config.yaml. Here `<your homeserver>` is the dictionary key and can be named arbitrarily, while `url` is the URL displayed when the cursor hovers over the host server item on the register page.

**After updating config.yaml, you must restart maubot for it to take effect.**

```
# config.yaml

#...
homeservers:
  #...
  <your homeserver>:
      url: ...
      secret: ... # can left empty if you don't have
```

Then run `mbc auth`, which is again an interactive login. Note here that the homeserver value you fill in is the dictionary key configured in `config.yaml`, not the dictionary value. For the username, either the full user ID or just the local part works.

```
$ mbc auth --update-client
<interactively login with matrix account>
```

If you don't pass `--update-client`, the access_token and device will be printed to the screen after logging in. Then you can go back to the web page to log in manually. If you do pass that argument, the client is already configured on the web side, and you can configure plugins directly.

If login fails, you can check the log in the window where maubot is running to debug.

## Create client and instance. Verify session

In the GUI, first create a client, then specify a plugin and a client to run an instance. When creating a client, both the display_name and avatar fields can be set to `disable` to mean "do not overwrite"; **if left empty, they will overwrite the existing values with empty values.**

After creating a client, you should verify maubot's corresponding session using a device that is already logged in. Only then can you be sure that it can decrypt end-to-end encrypted messages.
