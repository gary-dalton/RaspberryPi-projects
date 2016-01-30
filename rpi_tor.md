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

# STATUS - NOT COMPLETE

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
* [DS3231 RTC Module](http://www.sunfounder.com/index.php?c=downloadscs&a=Manualdetails&id=64) avilable from [Amazon](http://www.amazon.com/DS3231-Precision-Module-Arduino-Raspberry/dp/B00SSQAUHG/ref=sr_1_3?qid=1454019152)

# Overview

Start with a Raspberry Pi Lite with Wifi Access Point image. This is an image saved after following both the [RPi Initial Setup Guide](rpi_initial_setup.html) and the [RPi Wifi Access Point Guide](rpi_wifi_ap.html). If you do not have such an image, start with a Raspbian Lite image and follow the aforementioned guides before returning here.

1. Write the image to the microSD.
2. Connect to the Pi.
3. Configure I2C
4. Real Time clock
5. Disable Internet date checking


6. Install Tor and configure the firewall.
7. Further configure and secure the system
8. Test

# Procedures

## <a name="1"></a>Write the image

Write the image to the MicroSD as described in the [RPi Initial Setup Guide](rpi_initial_setup.html). Insert the MicroSD into the Pi.

## <a name="2"></a>Connect to the Pi

Connect to the pi using SSH over the network connection. Your wlan0 connection should be fully functional unless you are not on the same access point.

## Configure I2C

Follow the [Adafruit Guide](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c).

## Adding a real time clock

Tor network require accurate time keeping and, for anonymity, time keeping over the Internet should be disabled. Follow the [PiHut Guide](Adding a Real Time Clock to your Raspberry Pi).

## Disable Internet date checking

Having an accurate time is important for synchronized communications and for log filing. Linux, and most computers, use Network Time Protocol to check and validate the date/time. Remove the NTP package is an option, `sudo apt-get remove ntp`. NTP can always be easily reinstalled if it is later needed.
