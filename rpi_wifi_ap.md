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
tags: rpi, howto, router, iot, accesspoint

---
# RPi Wifi Access Point Guide

## Adding WiFi Access Point to your Raspberry Pi

# Description

Turning your pi into an access point is a useful step. It allows the pi to be used as a bridge between networks and allows your pi to be accessed directly from a client device. This is useful for IoT devices.

This guide assumes that 2 WiFi adapters will be used, one for access point service and one for Internet access. The information presented, with minor modifications, would also apply for an Ethernet Internet connected and for a non-Internet connected access point.

# Next up?

After reading this guide, you may be interested in reading:

- [Raspberry Tor](rpi-tor.html)
- [Using the WiFi Access Point with captured portal](rpi_captured_portal.html)

# Parts List

* Raspberry Pi 2
* 4GB (or larger) class 10 MicroSD card
* [Two USB WiFi dongles](http://www.amazon.com/Edimax-EW-7811Un-150Mbps-Raspberry-Supports/dp/B003MTTJOY/ref=pd_bxgy_147_2) _(second wifi is optional)_
* [USB to serial console cable](https://www.adafruit.com/product/954)  _(optional)_
* Pi Case
* Mini-USB power

# Overview

Start with a Raspberry Pi image. This is an image saved after following the [RPi Initial Setup Guide](rpi_initial_setup.html). The image may be either Lite or Full depending on your needs. If you do not have such an image, start with a Raspbian image and follow the aforementioned guide before returning here.

1. [Write the image to the MicroSD.](#1)
2. [Connect to the Pi.](#2)
3. [Connect to your WiFi.](#3)
4. [Install new packages.](#4)
5. [Setup the DHCP server.](#4)
6. [Set a static IP on wlan1.](#4)
7. [Set the Pi as an Access Point.](#4)
8. [Configure NAT.](#4)
9. [Connect and Test.](#4)
10. [Conclusion](#Conclusion).

# Procedures

## <a name="1"></a>Write the image

Write the image to the MicroSD as described in the [RPi Initial Setup Guide](rpi_initial_setup.html). Insert the MicroSD into the Pi.

## <a name="2"></a>Connect to the Pi

Attach the USB to serial console cable and allow the system to boot. Connect to the pi using a PuTTY terminal to the COM port or from Linux using `sudo screen /dev/ttyUSB0 115200`.

It should also be possible to connect to the pi using SSH over the network connection. Your wlan0 connection should be fully functional unless you are not on the same access point.

## <a name="3"></a>Connect to your WiFi

This guide assumes that wlan1 is used for the access point and wlan0 is used for the network connection. If your pi is not currently connected on the network, use NetworkManager, nmcli. See the [RPi Initial Setup Guide](rpi_initial_setup.html#12). Check your connection using `ifconfig`.

## <a name="4"></a>4 Install new packages
## 5 Setup the DHCP server
## 6 Set a static IP on wlan1
## 7 Set the Pi as an Access Point
## 8 Configure NAT
## 9 Connect and Test

For the steps 4 through 9 follow the procedures given by Adafruit's guide to [Setting up a Raspberry Pi as a WiFi access point](https://learn.adafruit.com/setting-up-a-raspberry-pi-as-a-wifi-access-point/install-software). **Read my _Comments and additional references_ before following these steps as there are a few minor changes.**

### Comments and additional references

- [Ubuntu Community isc-dhcp-server](https://help.ubuntu.com/community/isc-dhcp-server)
- The Domain Name Servers are [Google Public DNS](https://developers.google.com/speed/public-dns/)
- A valid private IPv4 address range is 192.168.0.0 - 192.168.255.255
- **File /etc/default/isc-dhcp-server** The setting is INTERFACES="wlan1"
- **Static IP on wlan1** not on wlan0
- **iptables rules** Change eth0 to wlan0 and wlan0 to wlan1
- **iptables rules** Add to the current rules table.

```
sudo nano /etc/iptables.test.rules
-----------
# TOP OF FILE ADD

*nat

# Allow Access Point NAT
-A POSTROUTING -o wlan0 -j MASQUERADE

COMMIT
-----------
# BEFORE THE COMMENT # Reject all other inbound # ADD

# Allow forwarded from wlan1 to permit NAT and Access Point
-A FORWARD -i wlan0 -o wlan1 -m state --state RELATED,ESTABLISHED -j ACCEPT
-A FORWARD -i wlan1 -o wlan0 -j ACCEPT
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

# <a name="Conclusion"></a>Conclusion

Well done, you now have a working wifi access point. From here you could turn it into a hotspot, a Tor router, or an IoT controller.

Remember to save your image file.
