---
title: Beginner Guide via Core Pi
subtitle: RPi Initial setup using a Core Pi
author: Gary Dalton
date: 20 February 2016
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html beginner_guide_via_core_pi.md -o beginner_guide_via_core_pi.html
tags: raspberrypi, guide, beginner, corepi, accesspoint
---
# Description

This guides a beginner to perform an initial setup of a Raspberry Pi. A coach should be nearby to assist when needed.

# Next up?

After reading this guide, you may be interested in reading:

# Overview

A coach provides:

+ a connected Core Pi
+ a MicroSD with Raspbian image installed
+ a Chrome browser with the Secure Shell and VNC Viewer apps installed

Some useful information is:

+ SSID to connect to is _corepi_
+ corepi wifi password is _raspberry_
+ Core Pi username/password is _guest/raspberry_
+ New pi username/password is _pi/raspberry_
+ Core Pi IP address is _192.168.42.1_

The steps to follow for easy setup are:

1. [Connect to Core Pi](#1)
2. [Setup other pies](#2)

## <a name="1"></a>Connect the Core Pi

### Wifi access point

Using standard methods connect your computer to the corepi access point. The name is _corepi_ and the password is _raspberry_.

### SSH

Use the Secure Shell app to connect to corepi. Start a [New Connection] and then then name your connection _Core PI_. The username is _guest_, the hostname is _192.168.42.1_, and the port is _22_. No other information is needed and you may click _Connect_. Your information should appear similar to this image.

![Secure Shell to Core Pi](images/ssh_corepi.jpg)
