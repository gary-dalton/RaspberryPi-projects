---
title: Node.js on Raspberry Pi
subtitle: Web and Pi
author: Gary Dalton
date: 7 September 2016
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html rpi_nodejs.md -o rpi_nodejs.html
tags: rpi, node.js, guide, iot, web
---
[Home](index.html)

# Description

Node.js is a JavaScript runtime environment for developing server-side Web applications. It uses an asynchronous event driven framework that is designed to build scalable network applications. I install it on nearly all of my pi to provide a framework for building user interfaces that can actually do something.

Learn more about node from [Node.js](https://nodejs.org/en/), [Express](http://expressjs.com/en/starter/hello-world.html), [Adafruit](https://learn.adafruit.com/node-embedded-development/events), and [search](https://www.google.com/webhp?q=node.js%20raspberry%20pi).

# Next up?

After reading this guide, you may be interested in reading:

# Parts List

+ Installed network connected Raspberry Pi 2 or newer

# Overview

Start with a Raspberry Pi image. This is an image saved after following the [RPi Initial Setup Guide](rpi_initial_setup.html). This may be either a lite or a full desktop image.

1. [Write the image to the MicroSD.](#1)
2. [Connect to your Pi](#2)
3. [Download and install the nodejs binaries](#3)
4. [Express framework](#4)
5. [Node-RED](#5)
6. [Conclusion](#Conclusion)
7. [References](#references)

# <a name="1"></a>Write the image

Write the image to the MicroSD as described in the [RPi Initial Setup Guide](rpi_initial_setup.html). Insert the MicroSD into the Pi and boot.

# <a name="2"></a>Connect Pi to your Internet

Use an Ethernet cable to connect the pi to the network. DHCP will assign the pi an IP address. Find the address of your pi from your network's DHCP server.

+ SSH to the pi at that IP address or yourpiname.local

# <a name="3"></a>Download and install the nodejs binaries

The pi uses the ARM processor. Determine which instruction set version is included, `grep 'model name' /proc/cpuinfo`. This output should include ARMv6, ARMv7, and so forth. The Raspberry Pi 3 uses the ARMv7 processor.

Visit the [downloads page](https://nodejs.org/en/download/) and select _LTS Recommended for Most Users_. Now copy the link to the correct ARM binary. In the following steps, replace _node-v4.5.0-linux-armv7l_ with the version for your system.

+ Change to home directory on the pi, `cd ~`
+ Download the binary, `wget https://nodejs.org/dist/v6.5.0/node-v6.5.0-linux-armv7l.tar.xz`, replace the URL with the link you copied above.
+ Extract the binary, `tar -xvf  node-v6.5.0-linux-armv7l.tar.xz`
+ `cd node-v6.5.0-linux-armv7l`
+ Copy the files, `sudo cp -R * /usr/local/`
+ Rehash the shell, `hash -r`
+ Check the version, `node -v`. This should match what you downloaded.
+ Check npm version, `npm -v`.

# <a name="4"></a>Express framework

Express.js is one of the most essential web frameworks for Node.js. It is a minimalist framework for building a host of web and mobile applications as well as application programming interfaces (APIs). Express.js is offers various features, like template engines, simplified multiple routing, database integration and more.

+ Install with `sudo npm install express --save`

# <a name="references"></a>References

+ [Installing Node.js on a Raspberry Pi 3](https://blog.wia.io/installing-node-js-on-a-raspberry-pi-3)
+ [Installing newer version of NodeJS on Pi 3](https://www.raspberrypi.org/forums/viewtopic.php?f=34&t=140747)
