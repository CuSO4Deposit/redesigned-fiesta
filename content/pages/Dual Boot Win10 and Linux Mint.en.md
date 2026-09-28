---
title: Dual Boot Win10 and Linux Mint
date: 2022-01-22
lastMod: 2026-09-28
tags:
  - Linux
  - Windows
categories:
slug: dual-boot
ai: translated
---

## Introduction

I already have Windows 10 installed on my computer, and want to install Linux to dual boot.

## Preparation

I don't have any experience on installing a new OS. So I have to investigate enough to minimize the probability that emergencies happen.

### Distro

I choose Linux Mint 20.03(Edge). This stable edition is distributed on Jan. 17, 2022. Some videos that helps to choose a distro (provided by @Erik):

[Linux HATES Me – Daily Driver CHALLENGE Pt.1 - YouTube](https://www.youtube.com/watch?v=0506yDSgU7M)

[Linus BREAKS Linux! - Daily Driver Challenge Reaction - YouTube](https://www.youtube.com/watch?v=D8j1n05s9-w)

### Creating a bootable USB Stick

[Create the bootable media](https://linuxmint-installation-guide.readthedocs.io/en/latest/burn.html)
[Create the bootable media](https://linuxmint-installation-guide.readthedocs.io/en/latest/burn.html#create-the-bootable-media)

Download the iso image from [mirrors](https://www.linuxmint.com/mirrors.php). I chose [the one](https://mirror.sjtu.edu.cn/linuxmint-cd/) the SJTUG site provided. Download the iso file.

Remember to check the file integrity using SHA256.
[Verify your ISO image](https://linuxmint-installation-guide.readthedocs.io/en/latest/verify.html#verify-your-iso-image)
As I am now operating on Windows, call cmd and type command:

CertUtil -hashfile <filename.iso> SHA256

where the <filename.iso> is the file name of the iso file.

([How to verify the ISO image on Windows](https://forums.linuxmint.com/viewtopic.php?f=42&t=291093&sid=5a96f0c51c745ca15875f8c818af15df))

![](/static/assets/sha256-1.png)

screenshot of my SHA256 check

Download [Etcher](https://etcher.io/), install and run it.

16GB UDisk, after flashing

### Fundamental Knowledges

[Partitioning — Linux Mint Installation Guide documentation](https://linuxmint-installation-guide.readthedocs.io/en/latest/partitioning.html)

[C.4. Device Names in Linux](https://www.debian.org/releases/wheezy/amd64/apcs04.html.en)

[Understanding the Linux File System :: Chapter 7: Red Hat Linux Basics :: Part II: Exploring Red Hat Linux :: Red Hat Linux 9 Professional Secrets :: Linux systems :: eTutorials.org](http://etutorials.org/Linux+systems/red+hat+linux+9+professional+secrets/Part+II+Exploring+Red+Hat+Linux/Chapter+7+Red+Hat+Linux+Basics/Understanding+the+Linux+File+System/)

[A beginner’s guide to disks and disk partitions in Linux – LinuxBSDos.com](https://linuxbsdos.com/2014/11/08/a-beginners-guide-to-disks-and-disk-partitions-in-linux/)

### Backup data

There's not a lot of things to say here. In case of emergencies, always remember to backup your important data!

## Installation

A full [tutorial](https://youtu.be/IzVnTSklWa0) by LearnLinuxTV:

Choose my USB stick as boot device (rather than "Windows boot manager").

Actually, this process is really easy. Everything is pre-configured. I just need to choose a few options.

My computer only has one hard drive. I give Linux Mint 50GB space. At first I am afraid that: as it automatically re-partition the drive, the C:(the partition where my Windows system is put) of my Windows may be full, and Windows can't run. But finally it turns out that it doesn't touch the system partition, and my D: (partition that saves data, with 175GB free) reduced to 125GB free. Meaning the re-partition process takes its 50GB all frm D: .

After configuring, the system tells me to restart. Then a blue screen "Perform MOK management" jumps out, which i have never seen in other tutorials. Some websites say it has something to do with graphics cards. They say I should choose "Enroll MOK" to load the graphic card's driver properly, but at this time my keyboard doesn't work. I can't gain control of anything on my computer. Then it automatically enters "continue boot". So my graphic card may be misconfigured. I will try to fix this in the future.

## Configuration

### A problem - packagekitd

After some time (about 1 hour) I installed Linux, something went wrong. I can't access anything about packages, including installing applications, updating cache, and so on.

All the things above were stuck. Waiting for them for a long time, I came to know that packagekitd must have run into a loop. This is an error. So I have to stop it:

sudo kill -9 43984

where 43984 is the process id of packagekitd. After doing this, the command line still told me that the file that installation needed was still locked by "aptd". Then after a while, system jumped out a window, asking me to set a secure boot password. Then after several minutes, when I was randomly trying, I found the process was no longer locked. Then everything stuck was solved. But I still don't know whether the system heals itself after "packagekitd" was killed, or setting that password worked.

### Driver Manager

Some websites recommended this option.

Some websites recommend the NVIDIA official driver, but **[later it gave me a lot of trouble](#Blurred-Screen)**. Next time when I install a Linux system on a computer with NVIDIA, I will directly choose "Xserver driver".

### Another problem - Can't shut down

Each time when i press "shut down", it just restarts the system, doesn't give me a chance to boot into Windows.

Solution[Fix: Linux Mint Won't Shut Down (Shutting Down Automatically Restarts)](https://zhuanlan.zhihu.com/p/378106182):

sudo apt-get install laptop-mode-tools

Problem solved.

### 3rd problem - too much buffer/cache memory

The free memory is very little. My laptop has 16GB RAM, but memory are almost all buffered/cached, making the free mem less then 1GB:

I tried a lot, but nothing works. Then the blurred screen(mentioned later) happened, and I changed the driver of graphic cards. And now I suddenly find it is solved, even though I don't know when and how:

Maybe it was because of the driver, I don't know. That is the only thing changed that I can think of.

### Emergency - Blurred screen

When I get almost everything done, I choose to restart the machine. Then the blue interface comes out again, and I still cannot control the keyboard. Then following this tutorial:

[Lenovo Legion R7000: Keyboard Not Responding on the "Perform MOK management" Screen When Installing the NVIDIA Driver (Solved)](https://blog.csdn.net/weixin_51449137/article/details/114462411)

Disable the secure root, and choose the switching mode. Next time the keyboard does work, but the meau is a little different:

The second option is no longer "enroll MOK" as [every tutorial says](https://www.cnblogs.com/yutian-blogs/p/13019226.html). It becomes "**reset MOK**".

In normal case

Then I dare not choose reset, I let it "continue boot", and then the whole screen became blurred. It really scared me that I didn't take a picture, so here is no pictures.

According to [some tutorials](https://www.cnblogs.com/real010/p/14678546.html), I entered the settings of the Advanced Options for Linux Mint, searching for this line:

ash $vt\_handoff

Sadly I did not find this line. Maybe it's because mine is Linux Mint 20.04, this line has been removed.

The next tutorial helped me:

[Pitfalls and Fixes When Installing Linux Mint: Blurred Screen, Can't Enter the Installation Boot Screen, Driver Errors, Can't Connect to Wi-Fi...](https://blog.csdn.net/m0_61536749/article/details/121673359)

Enter recovery mode, connect to the network(before the screen is blurred, we have connected to network), choose "root" and type:

ubuntu-drivers devices

It will retiurn a lot of drivers. Choose one to install:

sudo apt install nvidia-driver-470

After installing, input

reboot

and the system will restart. Boot into the normal Linux system, there is no more blurred screen, but the display is still not right. The brightness isn't modifiable. No matter where I put the "brightness percent" to, the actual brightness is fixed at 100%. Too bright, making me nearly blind.

Once I have met this problem when on Windows, it was because I chose the wrong mode of the graphic card. Discrete mode is OK, switchable mode is "fixed at 100% brightness". But this time I find the graphic card's settings is correct, in Windows the brightness is still modifiable. So this is just some problem for this driver of Linux. Then I decide to directly change the driver of graphic cards.

After applying on this driver, the brightness is modifiable now.

Here are some other possible ways to solve this problem, but I didn't try:

[A Simple and Reliable Solution for Not Being Able to Adjust Screen Brightness on Ubuntu 20.04 (Brightness Slider Has No Effect), and My Pitfall-Filled Journey](https://blog.csdn.net/weixin_44120025/article/details/118875998?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522163463823816780357241251%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=163463823816780357241251&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-1-118875998.first_rank_v2_pc_rank_v29&utm_term=ubuntu%E5%B1%8F%E5%B9%95%E4%BA%AE%E5%BA%A6%E8%B0%83%E8%8A%82%E6%97%A0%E6%95%88%E8%A7%A3%E5%86%B3%E6%96%B9%E6%B3%95&spm=1018.2226.3001.4187)

[Linux / Ubuntu + Win10 Dual-Boot Installation Log (2): Problems Caused by the AMD Integrated GPU Driver](https://zhuanlan.zhihu.com/p/397952249)

[The Ultimate Solution for Screen Brightness Adjustment After Installing Ubuntu 20.04 on a Lenovo Legion R7000](https://zhuanlan.zhihu.com/p/348624522)

### Configure VPN with valid \*.conf file using WireGuard

reference:

[How to Set Up a WireGuard Client on Linux with .conf File](https://engineerworkshop.com/blog/how-to-set-up-a-wireguard-client-on-linux-with-conf-file/)

[Let's Talk About WireGuard in the Kernel](https://zhuanlan.zhihu.com/p/147377961)

[Use wg-quick to make your Wireguard tunnels easy and persistent on Linux.](https://www.adamintech.com/use-wg-quick-to-make-your-wireguard-tunnels-easy-and-persistent-on-linux/)

Move the \*.conf to /etc/wireguard/, and type(in the following, I use the filename "Depoze\_Laptop.conf"):

sudo wg-quick up Depoze\_Laptop

It returns this message.

```
\[#\] ip link add Depoze\_Laptop type wireguard
\[#\] wg setconf Depoze\_Laptop /dev/fd/63
\[#\] ip -4 address add 10.6.0.22/24 dev Depoze\_Laptop
\[#\] ip link set mtu 1420 up dev Depoze\_Laptop
\[#\] resolvconf -a Depoze\_Laptop -m 0 -x
/usr/bin/wg-quick: line 32: resolvconf: command not found
\[#\] ip link delete dev Depoze\_Laptop
```

We should install resolvconf
[/usr/bin/wg-quick: line 31: resolvconf: command not found \[WireGuard Debian\]](https://superuser.com/questions/1500691/usr-bin-wg-quick-line-31-resolvconf-command-not-found-wireguard-debian).

sudo apt-get install resolvconf

After installing, execute:

sudo wg-quick up Depoze\_Laptop

Then check if success:

sudo wg

it returns an interface, establishing connection successfully.

If want to quit the connection, use

sudo wg-quick down Depoze\_laptop
