---
title: Raspberry Pi Projects
subtitle: Documentation
author: Gary Dalton
date: 23 February 2017
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html index.md -o index.html
tags: rpi, raspberrypi, guide, howto
---

# Beginner

- [Beginner Guide via Core Pi v2](beginner_guide_via_core_pi_v2.html), This guides a beginner to perform an initial setup of a Raspberry Pi
- [RPi Initial Setup Guide](rpi_initial_setup.html), Raspberry Pi - Image and Initial Setup


# Guides

- [RPi WiFi Access Point Guide](rpi_wifi_ap.html), Adding WiFi Access Point to your Raspberry Pi
- [Raspberry Tor Guide](rpi_tor.html), Raspberry Pi used as a Tor router
- [RPi Desktop Mods](rpi_gui_changes.html), Changes to the packages and defaults of the full Raspian
- [Core Pi v2](core_pi_v2.html), Pi as a wifi bridge providing safe subnet to wifi and Ethernet
- [RPi Voice Recognition and Command](rpi_vr_command.html)
- [RPi NGINX Webserver](rpi_nginx.html), Using the NGINX to serve static pages
- [RTC DS3231 on the Raspberry Pi](rpi_RTCds3231), Hardware clock, temperature, and alarms
- [Basic GPIO on the Raspberry Pi](rpi_gpio.html), I/O, interrupts, and notifications
- [Raspberry Pi 3 as a Simple WiFi Access Point](rpi3_simple_wifi_ap.html)
- [Dnsmasq Whitelist](dnsmasq_whitelist.html), Simple DNS domain whitelister
- [GPS on Raspberry Pi 3](rpi3_gps.html), Installation and basic use of the Adafruit Ultimate GPS breakout on a Raspberry Pi 3
- [Kismet on Raspberry Pi](rpi3_kismet.html), Installation and basic use of Kismet on a Raspberry Pi. Kismet is a wireless network detector, sniffer, and intrusion detection system.
- [Python 2 and Python 3 on Raspbian](python.html)
- [Connect to the Raspberry Pi using VNC or RDP](rpi_vnc_rdp.html), view the GUI desktop interface of a Raspberry Pi from a remote location or without an attached keyboard and monitor.


# How-tos

- [RPi Troubleshooting](rpi_troubleshoot.html), Tips and tricks
- [Linux General Hints](linux_hints.html), General hints and how-tos for Linux systems
- [Using the WiFi Access Point with captured portal](rpi_captured_portal.html)
- [Using CorePi v2](using_core_pi_v2.html)
- [Resize the SD image](resize_sd_image.html), Using GParted to shrink the disk size
- [SSH Hints and Advanced](ssh.html), Advanced usage with hints and tricks for leveraging SSH
- [RPi NetworkManager CLI](rpi_nmcli.html), the command line interface, CLI, to NetworkManager
- [RPi iptables](rpi_iptables.html), Using iptables for firewall with various configuration examples

# Discussions

- [Which Wifi USB adapters](rpi_which_wifi_usb.html)

# Links to other guides

- [Add a Shutdown Button](https://www.element14.com/community/docs/DOC-78055/l/adding-a-shutdown-button-to-the-raspberry-pi-b), [local pdf](reference-docs/adding-a-shutdown-button-to-the-raspberry-pi-b.pdf)

## On Hold

- [Walking Pi](walkingpi.html)
- [Timeserver on Raspberry Pi](timeserver.html)

## Deprecated

- [Core Pi](core_pi.html), superceded by Core Pi v2
- [Connect to the Raspberry Pi using VNC or RDP V1](rpi_vnc_rdp_v1.html), superceded by newer version
