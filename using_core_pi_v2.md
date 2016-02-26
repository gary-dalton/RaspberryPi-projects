---
title: Using Core Pi v2
subtitle: What is Core Pi used for?
author: Gary Dalton
date: 26 February 2016
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html using_core_pi_v2.md -o using_core_pi_v2.html
tags: rpi, howto, router, corepi, accesspoint
---
[Home](index.html)

# Description

Core Pi provides a local network for working with pies. This eases initial setup and provides a safe environment for novice learning.

# Next up?

After reading this guide, you may be interested in reading:

+ [Beginner Guide via Core Pi v2](beginner_guide_via_core_pi_v2.html)

# Overview

This how-to covers the various uses of a Core Pi. Of course, in order to use the Core Pi, one must be connected to it.

1. [Connect the Core Pi](#1)
2. [Setup other pies](#2)

## <a name="1"></a>Connect the Core Pi

Since corepiv2 already acts as a wifi access point, connect to its SSID.

### SSH

Now use SSH to connect to its IP address. If you used the settings given in [Core Pi v2](core_pi_v2.html), the IP address is _192.168.84.1_.

+ Connect to the pi using an SSH session with _192.168.84.1_
    - If this fails, check your network connections. If the wifi to corepiv2 is not the only connection then maybe the OS is trying to route through the other connection. Disconnect the other connections.

### VNC

VNC was discussed in [RPi Initial Setup Guide - Connect to the Pi using VNC](rpi_initial_setup.html#11).

+ On the pi, `vncserver -nolisten tcp -nevershared -dontdisconnect :1`
+ From your VNC Viewer, connect to VNC at _192.168.84.1:1_
+ If not already connected, connect the pi to your wifi access point.
+ Once connected to wifi, disconnect VNC and kill the service, `vncserver -kill :1`.

### Connect Core Pi to your WiFi Internet

From the VNC desktop, use the dialogs to connect to your Internet wifi SSID.

## <a name="2"></a>Setup other pies

Core Pi makes it easy to set up a new pi, starting with an image written to a microSD card inserted into the new pi.

+ Connect an Ethernet cable between the Core Pi and router's WAN port
+ Connect an Ethernet cable from the router to the new pi
+ Power up the new pi
+ Begin your setup
