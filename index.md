---
title: Raspberry Pi Projects
subtitle: Documentation
author: Gary Dalton
date: 26 February 2016
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html index.md -o index.html
tags: rpi, index
---

# Guides

- [RPi Initial Setup Guide](rpi_initial_setup.html), Raspberry Pi - Image and Initial Setup
- [RPi WiFi Access Point Guide](rpi_wifi_ap.html), Adding WiFi Access Point to your Raspberry Pi
- [Raspberry Tor Guide](rpi_tor.html), Raspberry Pi used as a Tor router
- [RPi Desktop Mods](rpi_gui_changes.html), Changes to the packages and defaults of the full Raspian
- [Core Pi v2](core_pi_v2.html), Pi as a wifi bridge providing safe subnet to wifi and Ethernet
- [RPi Voice Recognition and Command](rpi_vr_command.html)
- [Beginner Guide via Core Pi v2](beginner_guide_via_core_pi_v2.html), This guides a beginner to perform an initial setup of a Raspberry Pi.

# How-tos

- [Using the WiFi Access Point with captured portal](rpi_captured_portal.html)
- [Using CorePi v2](using_core_pi_v2.html)
- [Resize the SD image](resize_sd_image.html), Using GParted to shrink the disk size

# Discussions

- [Which Wifi USB adapters](rpi_which_wifi_usb.html)
- [SSH Hints](ssh_hints.html), hints and tricks for better leveraging SSH on the various platforms

## Deprecated

- [Core Pi](core_pi.html), superceded by Core Pi v2
