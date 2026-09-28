---
title: Configure Maubot
date: 2023-05-18
lastMod: 2026-09-28
tags:
- Matrix
- Maunium
categories:
slug: maubot
---

[Maubot](https://github.com/maubot/maubot) 是一款基于插件的Matrix-Bot SDK。

它的说明文档写得并不是很好，也没有给出一个合理的顺序安装过程，事实上在我安装时需要在文档的各节反复跳跃，因此我在此记录一个合理的配置流程。


## 配置环境

通过pip安装maubot。

```
$ python3 -m venv maubotVenv
$ source ./maubotVenv/bin/activate
$ pip install --upgrade maubot
```

添加必要的文件和目录，否则会报错

```
$ vim config.yaml
$ mkdir plugins, trash, logs
```

config.yaml似乎怎么写都可以（但是不写就会报错），我参考了[maubot/base-config.yaml at master · maubot/maubot · GitHub](https://github.com/maubot/maubot/blob/master/examples/config/base-config.yaml)，但事实上它好像并不是给这里用的，而是给插件用的。总之过一会运行起来之后会覆盖它生成含有表项的yaml。

## 运行以生成可填写的config

```
$ python3 -m maubot
```

它会在29316端口运行一个web界面。进入会发现需要登录，而此时还没有配置credential。不过现在按`<C-C>`停止运行，打开config.yaml就会看到很多配置项。

## 配置nginx

如果在config.yaml更改了路径，则填写对应的新路径。没有https的可以改为listen 80.

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

检查conf，重启nginx。

## 添加credentials

在config.yaml中找到`admins`字段，添加`name: password`的格式。注意root不可以配置密码，在运行后，这里将会被加密（而不是明文的账号密码）。

这里的账号密码，是管理maubot这个系统（也就是29316的webapp）使用的，与matrix无关。过一会的`mbc login`，使用的也是这一套账号密码。

## 登录、添加插件

再次运行，在GUI很容易找到如何上传插件。这里可以使用官方提供的[Echo](https://github.com/maubot/echo)插件做测试。登录之后就可以上传插件。但这时还没有client和instance。**每个client相当于一个登录着的matrix账号，而每个instance相当于在一个指定账号上运行着的一个插件。**

为了创建一个client，我们需要获取Matrix的端到端加密机制要求的access_token和device。获取需要使用maubot提供的CLI工具。

## 在CLI获取access_token和device

直接在CLI登录会做不到加密，最好先搞好加密的组件：

[Encryption - maubot](https://docs.mau.fi/maubot/usage/encryption.html)

```
$ pip install --upgrade maubot[encryption]
$ pip install python-olm --extra-index-url https://gitlab.matrix.org/api/v4/projects/27/packages/pypi/simple
```

`mbc auth`是获取这两项的命令，但在这之前需要先`mbc login`登录maubot的管理账户。

```
$ mbc login
<interactively login with credenricals in config.yaml...>
```

在`mbc auth`之前，还需要在config.yaml添加homeserver，这里的`<your homeserver>`是字典的键，可以任意取名，`url` 是register页面光标悬停在host server项上时显示的url。

**更新config.yaml后需要重启maubot才会生效。**

```
# config.yaml

#...
homeservers:
  #...
  <your homeserver>:
      url: ...
      secret: ... # can left empty if you don't have
```

然后执行`mbc auth`，又是交互式登录。这里需要注意的是，homeserver项填写的是在`config.yaml`中配置的字典键而不是字典值。username使用全称和用户名都可。

```
$ mbc auth --update-client
<interactively login with matrix account>
```

如果不带`--update-client`，登录后屏幕上就会打印access_token和device。接下来就可以回到web页面操作手动登录。如果带了上面的参数，则web端已经配置好这个client，可以直接配置插件。

登录失败时，可以在maubot运行的窗口查看log来debug。

## 创建client和instance. Verify session

在GUI先创建client，再指定插件和client运行instance。创建client时，display_name和avatar字段都可以设为`disable`表示不覆盖，**如果留空则会使用空值覆盖原有的**。

创建过client后，应当用已经登录的设备对maubot对应的session作验证。这样才能确保它可以解密端对端加密的消息。
