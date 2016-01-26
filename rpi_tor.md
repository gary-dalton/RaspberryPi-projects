---
title: Raspberry Tor
subtitle: Raspberry Pi used as a Tor router
author: Gary Dalton
date: 24 January 2016
license: MIT
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html rpi_tor.md -o rpi_tor.html
tags: rpi, tor, howto, router, privacy

---
# Raspberry Tor

## Raspberry Pi used as a Tor router

# Description

The purpose of Raspberry Tor is to securely and anonymously use the Internet.
The Tor Project defends against network surveillance and traffic analysis.
Tor joined with a Raspberry Pi provides a wireless router to ensure that all
network traffic from a computer is automatically either blocked or routed
through the Tor network.

This is a first but insufficient step to online anonymity.

# Parts List

* Raspberry Pi 2
* 4GB MicroSD card
* [Two USB WiFi dongles](http://www.amazon.com/Edimax-EW-7811Un-150Mbps-Raspberry-Supports/dp/B003MTTJOY/ref=pd_bxgy_147_2)
* Pi Case
* Mini-USB power

# Overview

Start with a Raspberry Pi Lite with Wifi Access Point image. This is an image saved after following both the [RPi Initial Setup Guide](rpi_initial_setup.html) and the [RPi Wifi Access Point Guide](rpi_wifi_ap.html). If you do not have such an image, start with a Raspbian Lite image and follow the aforementioned guides before returning here.

1. Write the image to the microSD.
2. Connect to the Pi using either the USB to serial cable or using a keyboard
and monitor.
3. Boot the Pi and run general setup
4. Get the Pi to connect to your WiFi.
5. Get the Pi to act as a WiFi gateway.
6. Install Tor and configure the firewall.
7. Further configure and secure the system
8. Test

# Procedures

## Raspbian

Download the [latest version of Raspbian](https://www.raspberrypi.org/downloads/raspbian/).
I used the Lite version as no GUI or additional software is needed. Unzip the
image and write it to the MicroSD card. On Windows, I used [Win32 Disk Imager](http://sourceforge.net/projects/win32diskimager/). Other OS instructions
may be found on the Raspbian download page.

Insert the MicroSD into the Pi.

## Connect to the Pi

A Raspberry Pi is a computer that may be operated by connecting with a mouse,
keyboard, and monitor. I prefer to connect to it using  the USB to Serial
console cable. This allows me to use my main computers resources while working
on the Pi in a terminal window. See the [Adafruit overiew](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-5-using-a-console-cable) for full
details on using the USB to console cable.
