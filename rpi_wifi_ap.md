---
title: RPi Wifi Access Point Guide
subtitle: Adding WiFi Access Point to your Raspberry Pi
author: Gary Dalton
date: 24 January 2016
license: MIT
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html rpi_wifi_ap.md -o rpi_wifi_ap.html
tags: rpi, tor, howto, router, privacy

---
# RPi Wifi Access Point Guide

## Adding WiFi Access Point to your Raspberry Pi

# Description

Turning your pi into an access point is a useful step. It allows the pi to be used as a bridge between networks and allows your pi to be accessed directly from a client device. This is useful for IoT devices.

# Parts List

* Raspberry Pi 2
* 4GB (or larger) class 10 MicroSD card
* [Two USB WiFi dongles](http://www.amazon.com/Edimax-EW-7811Un-150Mbps-Raspberry-Supports/dp/B003MTTJOY/ref=pd_bxgy_147_2) _(second wifi is optional)_
* [USB to serial console cable](https://www.adafruit.com/product/954)  _(optional)_
* Pi Case
* Mini-USB power

# Overview

Start with a Raspberry Pi image. This is an image saved after following the [RPi Initial Setup Guide](rpi_initial_setup.html). The image may be either Lite or Full depending on your needs. If you do not have such an image, start with a Raspbian image and follow the aforementioned guide before returning here.

1. Write the image to the MicroSD.
2. Connect to the Pi.
3. Connect to your WiFi.
4. Install new packages.
5. Setup the DHCP server.
6. Set a static IP on wlan0.
7. Set the Pi as an Access Point.
8. Configure NAT.
Further configure and secure the system.

# Procedures

## 1 Write the image

Write the image to the MicroSD as described in the [RPi Initial Setup Guide](rpi_initial_setup.html). Insert the MicroSD into the Pi.

## 2 Connect to the Pi

Attach the USB to serial console cable and allow the system to boot. Connect to the pi using a PuTTY terminal to the COM port or from Linux using `sudo screen /dev/ttyUSB0 115200`.

## 3 Connect to your WiFi

Unless you are using the same WiFi dongle as in the previous guide, your wifi needs to be told to connect. If you have more than 1 wifi dongle, make note of the HWaddr obtained from `ifconfig wlan1`. This guide assumes that wlan0 is used for the access point. Use ConnMan for managing this.

1. Start ConnMan control, `sudo connmanctl`. Notice that the CLI prompt changes.
2. `enable wifi`
3. Scan for wifi services, `scan wifi`.
4. List the found services, `services`.
5. Register an agent to handle user requests, `agent on`.
6. From the list of services, select the wifi address you wish to connect to. The wifi address is the same hexadecimal sequence as the HWaddr obtained earlier. Connect to the service, `connect wifi_numbers_letters_of_your_service`.
7. If it is a secured access point, the agent should request a password so enter the password.
8. Once authenticated, your credentials are saved for future connections.
9. `quit`.
10. Check your connection using `ifconfig`.

## 4 Install new packages
## 5 Setup the DHCP server
## 6 Set a static IP on wlan0
## 7 Set the Pi as an Access Point
## 8 Configure NAT

For the steps 4 through 8 follow the procedures given by Adafruit's guide to [Setting up a Raspberry Pi as a WiFi access point](https://learn.adafruit.com/setting-up-a-raspberry-pi-as-a-wifi-access-point/install-software). **Read my _Comments and additional references_ before following these steps as there are a few minor changes.**

### Comments and additional references

- [Ubuntu Community isc-dhcp-server](https://help.ubuntu.com/community/isc-dhcp-server)
- The Domain Name Servers are [Google Public DNS](https://developers.google.com/speed/public-dns/)
- A valid private IPv4 address range is 192.168.0.0 - 192.168.255.255
- **iptables rules** Change eth0 to wlan1
- **iptables rules** Add to the current rules table.

```
sudo nano /etc/iptables.test.rules
-----------
# TOP OF FILE ADD

*nat

# Allow Access Point NAT
-A POSTROUTING -o wlan1 -j MASQUERADE

COMMIT
-----------
# BEFORE THE COMMENT # Reject all other inbound # ADD

# Allow forwarded from wlan0 to permit NAT and Access Point
-A FORWARD -i wlan1 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
-A FORWARD -i wlan0 -o wlan1 -j ACCEPT
-----------
# SAVE
# LOAD RULES
sudo iptables-restore < /etc/iptables.test.rules
# VERIFY RULES
sudo iptables -L
# SAVE RULES
sudo -i
iptables-save > /etc/iptables.up.rules
exit
```
- **update hostapd** The binary version available for download from Adafruit is a little old. It will work but I recommend compiling hostapd. The Adafruit tutorial covers this on the last page.
- **Realtek download** The version listed on Adafruit is no longer available. Instead, try the version for Linux found on this [Realtek page](http://www.realtek.com.tw/downloads/downloadsView.aspx?Langid=1&PNid=21&PFid=48&Level=5&Conn=4&DownTypeID=3&GetDown=false&Downloads=true)
- **hostapd compile** File locations are a little different. Try these instead.

```
unzip RTL8188C_8192C_USB_linux_v4.0.2_9000.20130911.zip
mv RTL8188C_8192C_USB_linux_v4.0.2_9000.20130911 rtl
cd rtl
cd wpa_supplicant_hostapd
tar -xzvf wpa_supplicant_hostapd-0.8_rtw_r7475.20130812.tar.gz
cd wpa_supplicant_hostapd-0.8_rtw_r7475.20130812
cd hostapd
make
```
- **Do not remove WPA-Supplicant**
