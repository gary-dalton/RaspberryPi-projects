---
title: Raspberry Pi 3 as a Simple WiFi Access Point
subtitle: Pi as a wifi bridge providing safe subnet to wifi and Ethernet
author: Gary Dalton
date: 1 September 2016
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html rpi3_simple_wifi_ap.md -o rpi3_simple_wifi_ap.html
tags: rpi3, guide, router, accesspoint, wifi, iot
---
[Home](index.html)

# Description

The Raspberry Pi 3 has a built in WiFi radio. This makes using it easier than ever. This guide will start with a basic Raspbian build, connected to a wired network, and add WiFi access point capabilities. I sometimes use this approach for building an IoT subnet.

# Next up?

After reading this guide, you may be interested in reading:

- [IoT hub](rpi3_iot_hub.html)

# Parts List

+ Raspberry Pi 3
+ 16GB (or larger) class 10 MicroSD card
+ Mini-USB power
+ Ethernet cable

# Overview

Start with a Raspberry Pi image. This is an image saved after following the [RPi Initial Setup Guide](rpi_initial_setup.html). This may be either a Lite image or a full desktop image.

1. [Write the image to the MicroSD.](#1)
2. [Connect Pi to your Internet](#2)
3. [Install dnsmasq and hostapd](#3)
4. [Configure wlan0](#4)
5. [Configure hostapd](#5)
6. [Configure dnsmasq](#6)
7. [Iptables forwarding](#7)
8. [Load, Test and Reboot](#8)
9. [Conclusion](#Conclusion).


# Procedures

This guide mostly follows the guide from [frillip](https://frillip.com/using-your-raspberry-pi-3-as-a-wifi-access-point-with-hostapd/). If this is not available, [try this PDF version](reference-docs/RaspberryPi3WiFiAccessPoint.pdf).

## <a name="1"></a>Write the image

Write the image to the MicroSD as described in the [RPi Initial Setup Guide](rpi_initial_setup.html). Insert the MicroSD into the Pi and boot.

## <a name="2"></a>Connect Pi to your Internet

Use an Ethernet cable to connect the pi to the network. DHCP will assign the pi an IP address. Find the address of your pi from your network's DHCP server.

+ SSH to the pi at that IP address or yourpiname.local

## <a name="3"></a>Install dnsmasq and hostapd

More about [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq) and [hostapd](https://en.wikipedia.org/wiki/Hostapd).

+ `sudo apt-get  update`
+ `sudo apt-get upgrade`
+ `sudo apt-get install dnsmasq hostapd`


## <a name="4"></a>Configure wlan0

+ Inform dhcpd to ignore wlan0 by editing `sudo nano /etc/dhcpcd.conf`
    - To the end add `denyinterfaces wlan0`
    - This must be ABOVE any interface lines you may have added
+ Configure the wlan IP, `sudo nano /etc/network/interfaces`
    - the wlan0 section should be changed to:

```
allow-hotplug wlan0  
iface wlan0 inet static  
    address 192.168.220.1
    netmask 255.255.255.0
    network 192.168.220.0
    broadcast 192.168.220.255
```

+ Restart dhcpcd with `sudo service dhcpcd restart`
+ Reload wlan0 with `sudo ifdown wlan0; sudo ifup wlan0`

## <a name="5"></a>Setup hostapd

+ `sudo nano /etc/hostapd/hostapd.conf`
    - add the following

```
interface=wlan0
driver=nl80211

hw_mode=g
channel=6
ieee80211n=1
wmm_enabled=1
ht_capab=[HT40][SHORT-GI-20][DSSS_CCK-40]
macaddr_acl=0
ignore_broadcast_ssid=0

# Use WPA2
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP

# Change these to your choice
# This is the name of the network
ssid=Pi3-AP
# The network passphrase
wpa_passphrase=raspberry
```

+ Now edit the default configuration, `sudo nano /etc/default/hostapd`
    - Replace _#DAEMON_CONF=""_ with `DAEMON_CONF="/etc/hostapd/hostapd.conf"`

## <a name="6"></a>Configure dnsmasq

+ Rename the current configuration, `sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig `
+ Create and edit the new configuration, `sudo nano /etc/dnsmasq.conf`
    - Add the following

```
interface=wlan0       # Use interface wlan0  
listen-address=192.168.220.1   # Specify the address to listen on  
bind-interfaces      # Bind to the interface
server=8.8.8.8       # Use Google DNS  
domain-needed        # Don't forward short names  
bogus-priv           # Drop the non-routed address spaces.  
dhcp-range=192.168.220.50,192.168.220.150,12h # IP range and lease time  
```

## <a name="7"></a>Iptables forwarding

*(Optional)* Forwarding is required if any devices connected to your this access point need to connect to the Internet. I do not forward for many IoT devices which I expect to act as an isolated network.

+ Enable IP Forwarding
    - `sudo nano /etc/sysctl.conf` at bottom add _net.ipv4.ip_forward=1_
    - `sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"`
+ If you have not already completed [Persistant iptables](rpi_iptables.html#2), do so now
+ **Required** View [WiFi Access Point rule set](rpi_iptables.html#5) to complete iptables setup

## <a name="8"></a>Load, Test and Reboot

Load the services and test availability, connection and forwarding.

+ `sudo service hostapd start`
+ `sudo service dnsmasq start`
+ Use any WiFi client to connect to your new rpi3 access point
+ Verify connection of various services such as SSH
+ If you chose IP Forwarding, verify that your connected device is able to connect to the Internet
+ Once you have verified everything, `sudo reboot now`
+ Retest everything with the rebooted pi

# <a name="Conclusion"></a>Conclusion

You now have a working WiFi access point which may be used to extend your wired network or as a hub for local IoT devices.
