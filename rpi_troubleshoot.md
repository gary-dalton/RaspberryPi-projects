---
title: RPi Troubleshooting
subtitle: Tips and tricks
author: Gary Dalton
date: 5 March 2016
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html rpi_troubleshoot.md -o rpi_troubleshoot.html
tags: raspberrypi, howto, troubleshoot
---
[Home](index.html)

# Description

Sometimes not everything goes smoothly -- something just goes awry. It might be specific to the hardware setup or the network configuration you are connecting to. The essence of hacking is making a thing work the way you want it to. This How-to will cover some simple fixes I have found and also some general methods to solving a problem.

# Simple fixes

+ [Hiss from the headphone output of the pi](#1)

# Problem solving methods

+ Clearly state the problem
+ Google is your friend
+ Document all your changes
+ Be fearless

## <a name=""></a>Hiss from the headphone output of the pi

This is especially noticeable when using Sonic Pi.

+ `sudo sh -c 'echo "disable_audio_dither=1" >> /boot/config.txt'`
    - [source](https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=85811)
    - [/boot/config settings](http://elinux.org/RPiconfig)
