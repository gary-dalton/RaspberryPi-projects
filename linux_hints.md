---
title: Linux General Hints
subtitle: How to use Linux
author: Gary Dalton
date: 11 September 2016
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html linux_hints.md -o linux_hints.html
tags: linux, hints, samba, mount, guide
---
[Home](index.html)

# Description

General hints and how-tos for Linux systems.

# Contents

1. [Mount a Windows share](#1)

# Procedures

## <a name="1"></a>Mount a Windows share

+ `sudo apt-get install  samba-common smbclient samba-common-bin smbclient  cifs-utils`
+ `sudo mkdir /mnt/yourmount`, replace yourmount
+ To proceed, you need the server's IP address and the name of your share.
+ If the share requires credentials, those are also needed.
+ `sudo mount -t cifs //server_IP/share /mnt/yourmount`, no credentials
+ `sudo mount -t cifs //server_IP/share /mnt/yourmount -o user=username`, credentialed
+ Your share is now available at _/mnt/yourmount_
+ Unmount with `umount /mnt/yourmount`

### Auto mount on boot

## Apt and Aptitude

* List obsolete packages `aptitude search '~o'`
