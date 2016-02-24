---
title: Using Core Pi
subtitle: What is Core Pi used for?
author: Gary Dalton
date: 20 February 2016
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html using_core_pi.md -o using_core_pi.html
tags: rpi, howto, router, iot, accesspoint
---
# Description

Core Pi acts as the central point in providing Internet and initial setup for other pies in a wifi only environment. Core Pi connects to the Internet via wifi, provides a wifi access point, and acts as a DHCP router for a pi direct connected with Ethernet cable.

# Next up?

After reading this guide, you may be interested in reading:

# Overview

This how-to covers the various uses of a Core Pi. Of course, in order to use the Core Pi, one must be connected to it.

1. [Connect the Core Pi](#1)
2. [Setup other pies](#2)

## <a name="1"></a>Connect the Core Pi

Since your pi already acts as a wifi access point, connect to its SSID.

### SSH

Now use SSH to connect to it using either _hostname.local_ or its IP address. If you used the settings given in [RPi WiFi Access Point Guide](rpi_wifi_ap.html), the IP address is _192.168.42.1_.

### VNC

VNC was discussed in [RPi Initial Setup Guide - Connect to the Pi using VNC](rpi_initial_setup.html#11).

+ `vncserver :1`
+ From your browser connect to the pi's VNC

### Connect Core Pi to your WiFi Internet

From the VNC desktop, use the dialogs to connect to your Internet wifi SSID.

## <a name="2"></a>Setup other pies

Core Pi makes it easy to set up a new pi, starting with an image written to a microSD card inserted into the new pi.

+ Connect an Ethernet cable between the Core Pi and the new pi
+ Power up the new pi

### From Core Pi's command line

+ `arp -i eth0`, which will list IP addresses served by DHCPd on eth0.
+ Use the IP address to connect to the new pi, `ssh pi@192.168.84.10`
+ **Note:** If you receive _WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!_, it is because the IP address is now associated with a different pi.
    - To remove the stored key, `ssh-keygen -f "/home/pi/.ssh/known_hosts" -R 192.168.84.10`
    - To prevent Core Pi from storing the key edit or create a config file
        - `nano ~/.ssh/config` with the following lines (see [ssh config](http://linux.die.net/man/5/ssh_config) for full details)

```
Host raspberrypi
  StrictHostKeyChecking no
  UserKnownHostsFile=/dev/null
```

+ Run the setup as you usually would
