---
title: SSH Hints
subtitle: Tricks
author: Gary Dalton
date: 24 February 2016
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html ssh_hints.md -o ssh_hints.html
tags: raspberrypi, howto, ssh
---
[Home](index.html)

# Description

This is just a list of hints and tricks for better leveraging SSH on the various platforms.

# Hints

## <a name="Chrome"></a>Chrome Browser App

+ [Remove SSH known_hosts](#Chrome_01)


### <a name="Chrome_01"></a>Remove SSH known_hosts

When working with pies in a closed network, there are times when the host identification will change. When that happens, attempts to connect using the Secure Shell app will fail with the following message:

    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    @ WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED! @
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
    Someone could be eavesdropping on you right now (man-in-the-middle attack)!
    It is also possible that a host key has just been changed.
    The fingerprint for the ECDSA key sent by the remote host is
    d6:be:12:7e:22:23:c3:e1:56:30:d6:cd:65:b7:ab:42.
    Please contact your system administrator.
    Add correct host key in /.ssh/known_hosts to get rid of this message.
    Offending ECDSA key in /.ssh/known_hosts:7
    ECDSA host key for xxxxxxxxxxxxx.yyy.au has changed and you have requested strict checking.
    Host key verification failed.
    NaCl plugin exited with status code 255.
    (R)econnect, (C)hoose another connection, or E(x)it?

This can only be fixed by removing the offending key. Make note of the number shown at the end of the line, _Offending ECDSA key in /.ssh/known_hosts:7_. That number depends on your system and is the index of the offending key.

+ Open the JavaScript console, `CTRL +Shift +J`
+ Enter `term_.command.removeKnownHostByIndex(INDEX);` into the console. Replace _INDEX_ by the index of your offending key.
+ Clear all host keys with `term_.command.removeAllKnownHosts();`

_from [gaggl](https://www.gaggl.com/2015/07/chromeos-removing-ssh-known_hosts-from-chromebook/)_
