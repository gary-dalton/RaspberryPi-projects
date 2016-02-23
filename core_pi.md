---
title: Core Pi
subtitle: Pi as an access point providing dhcp to eth0
author: Gary Dalton
date: 24 January 2016
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html core_pi.md -o core_pi.html
tags: rpi, guide, router, iot, accesspoint
---
# Description

Core Pi may seem an odd exercise but the point is to use a pi as the central point in providing Internet and initial setup for other pies in a wifi only environment. Core Pi connects to the Internet via wifi, provides a wifi access point, and acts as a DHCP router for a pi direct connected with Ethernet cable.

Recent Raspbian versions are ready for SSH connection over Ethernet cable. Core Pi takes advantage of that to ease initial connection and setup. I am using this in a learning lab environment with Chromebooks.

This guide assumes that 2 WiFi adapters will be used, one for access point service and one for Internet access. It also assumes that another pi, not fuly set up, may be connected to it via eth0.

# Next up?

After reading this guide, you may be interested in reading:

- [Using the WiFi Access Point with captured portal](rpi_captured_portal.html)
- [Using CorePi](using_core_pi.html)

# Parts List

+ Raspberry Pi 2
+ 8GB (or larger) class 10 MicroSD card
+ [Two USB WiFi dongles](http://www.amazon.com/Edimax-EW-7811Un-150Mbps-Raspberry-Supports/dp/B003MTTJOY/ref=pd_bxgy_147_2) _(second wifi is optional)_
    - See the discussion [Which Wifi USB adapters](rpi_which_wifi_usb.html)
+ Pi Case
+ Mini-USB power
+ Ethernet cable

# Overview

Start with a Raspberry Pi image. This is an image saved after following the [RPi Initial Setup Guide](rpi_initial_setup.html), [RPi WiFi Access Point Guide](rpi_wifi_ap.html), and [RPi Desktop Mods](rpi_gui_changes.html). The image should not be Lite. If you do not have such an image, start with a Raspbian image and follow the aforementioned guides before returning here.

1. [Write the image to the MicroSD.](#1)
2. [Connect to the Pi.](#2)
3. [Connect to your WiFi.](#3)
4. [Setup the DHCP server.](#4)
5. [Set a static IP on eth0.](#5)
6. [Configure NAT.](#6)
7. [Connect and test.](#7)
10. [Conclusion](#Conclusion).

# Procedures

## <a name="1"></a>Write the image

Write the image to the MicroSD as described in the [RPi Initial Setup Guide](rpi_initial_setup.html). Insert the MicroSD into the Pi and boot.

## <a name="2"></a>Connect to the Pi

Since your pi already acts as a wifi access point, connect to its SSID. Now use SSH to connect to it using either _hostname.local_ or its IP address. If you used the settings given in [RPi WiFi Access Point Guide](rpi_wifi_ap.html), the IP address is _192.168.42.1_.

## <a name="3"></a>Connect the Pi to your WiFi Internet

In this guide, I will use the desktop but nmcli may be used as discussed in the [RPi Initial Setup Guide - NetworkManager CLI](rpi_initial_setup.html#12). VNC was discussed in [RPi Initial Setup Guide - Connect to the Pi using VNC](rpi_initial_setup.html#11)

+ `vncserver :1`
+ From your browser connect to the pi's VNC
+ Using the dialogs, connect to your Internet wifi SSID

## <a name="4"></a>Setup the DHCP server

+ `sudo nano /etc/default/isc-dhcp-server`
+ `INTERFACES="eth0 wlan1"`
+ Now edit the DHCP configuration file, `sudo nano /etc/dhcp/dhcpd.conf`

```
# ADD interface wlan1; TO WIFI ACCESS POINT CONFIG
subnet 192.168.42.0 netmask 255.255.255.0 {
	interface wlan1;
	range 192.168.42.10 192.168.42.50;
	option broadcast-address 192.168.42.255;
	option routers 192.168.42.1;
	default-lease-time 600;
	max-lease-time 7200;
	option domain-name "local";
	option domain-name-servers 8.8.8.8, 8.8.4.4;
}

# ADD THE BELOW TO CONFIG FOR ETH0
subnet 192.168.84.0 netmask 255.255.255.0 {
	interface eth0;
	range 192.168.84.10 192.168.84.50;
	option broadcast-address 192.168.42.255;
	option routers 192.168.84.1;
	default-lease-time 600;
	max-lease-time 7200;
	option domain-name "local";
	option domain-name-servers 8.8.8.8, 8.8.4.4;
}
```

## <a name="5"></a>Set a static IP on eth0

+ Take the interface down, `sudo ifdown eth0`
+ `sudo nano /etc/network/interfaces`
+ Comment `#iface eth0 inet manual`
+ Add

```
iface eth0 inet static
  address 192.168.84.1
  netmask 255.255.255.0
```

## <a name="6"></a>Configure NAT

+ Verify IP Forwarding was enabled earlier
    - `cat /etc/sysctl.conf` should contain _net.ipv4.ip_forward=1_
    - `cat /proc/sys/net/ipv4/ip_forward` shoule be _1_

+ Update iptables rules, `sudo nano /etc/iptables.test.rules`

```
# BEFORE THE COMMENT # Reject all other inbound # ADD

# Allow forwarded from eth0 to permit NAT and Core Pi
-A FORWARD -i wlan0 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT
-A FORWARD -i eth0 -o wlan0 -j ACCEPT
```
+ Load the rules, `sudo iptables-restore < /etc/iptables.test.rules`
+ Verify rules, `sudo iptables -L` and `sudo iptables -S`
+ Save rules for booting,

```
sudo -i
iptables-save > /etc/iptables.up.rules
exit
```
## <a name="7"></a>Connect and Test

First, down and up the interfaces then restart the services.

+ Down and then up the interfaces,
    - `sudo ifdown wlan1`
    - `sudo ifdown eth0`
    - `sudo ifup eth0`
    - `sudo ifup wlan1`
+ Restart the DHCP server, `sudo service isc-dhcp-server restart`
+ Restart hostapd, `sudo service hostapd restart`
+ Check their statuses
+ View logged output from the DHCP server and also from iptables, `tail -F /var/log/syslog`. This may be helpful if troubleshooting is needed.

Next, connect to the interfaces and verify proper functioning of hostapd and dhcp.

+ Connect to the wifi ap
+ Connect with an Ethernet cable to the pi
+ View the active DHCP leases with, `cat /var/lib/dhcp/dhcpd.leases`.
+ Use arp to more easily view active addresses, `arp`.
+ Verify that VNC and SSH work as expected with the DHCP assigned addresses.

# <a name="Conclusion"></a>Conclusion

CorePi is ready to use for serving as a wifi router, network master, and pi setup station. It would be relatively easy to write some scripts to automatically set up any unconfigured pi connected to eth0. I do not plan on writing such scripts since my CorePi will be used in learning how to set up a pi.

Remember to save your image file as CorePi.
