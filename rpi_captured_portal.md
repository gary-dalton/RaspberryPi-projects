---
title: Using the WiFi Access Point
subtitle: Connecting through a Captured Portal
author: Gary Dalton
date: 29 January 2016
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html rpi_captured_portal.md -o rpi_captured_portal.html
tags: rpi, howto, portal, wifi, hotspot
---

# Using the WiFi Access Point

## Connecting through a Captured Portal

# Description

Now that you have a wifi access point, how do you use it? It can be used on your home network, a public hotspot, and a captured portal hotspot. This how-to assumes that you have a Raspberry Pi wifi access point as setup in the [RPi Wifi Access Point Guide](rpi_wifi_ap.html).

# Next up?

After reading this guide, you may be interested in reading:

- [Raspberry Tor](rpi-tor.html)

# Overview

This how-to covers the use of nmcli to scan, connect to and disconnect from access points. It also describes how to accept agreements or log into hotspot captive portals. Finally there is a section on troubleshooting.

1. [Start the Access Point](#1)
2. [Connect to the pi.](#2)
3. [Scan for SSIDs.](#3)
4. [Add new connections.](#4)
5. [Connect and disconnect a connection.](#5)
6. [Install links.](#6)
7. [Use links with a captive portal.](#7)
8. [Connect and Test.](#8)
9. [Troubleshooting.](#9)
10. [Shutting down.](#10)
11. [Conclusion](#Conclusion).

# Procedures


## <a name="1"></a>Start the Access Point

Basically, just give the pi power and the access point will start up. I use a simple USB to mini-USB cable and connect it from my laptop to my pi but you could use a dedicated power cord or even a battery pack.

## <a name="2"></a>Connect to the Pi

Once the pi is started it should broadcast its SSID. This is the SSID you gave it in /etc/hostapd/hostapd.conf. Connect to this SSID and provide the password you set in that file. Once connected, your device has an IP address in the same subnet as the AP and the device is using the nameservers you selected in the /etc/hostapd/hostapd.conf. These IP address were assigned via DHCP.

Now SSH into the AP's shell using `ssh user@hostname.local`.

## <a name="3"></a>Scan for SSIDs

Time to find out what SSIDs are nearby and available. The easy command is `nmcli dev wifi` which outputs a table similar to:


X   SSID  MODE   CHAN  RATE      SIGNAL BARS    SECURITY
--  ----  -----  ----  --------- ------ ------  --------
.   ap1   Infra  1     16 Mbit/s 100    ▂▄▆█    WPA2
X   ap2   Infra  6     54 Mbit/s 100    ▂▄▆█    WPA2
.   ap3   Infra  8     54 Mbit/s 100    ▂▄▆█    WPA2
.   ap4   Infra  6     16 Mbit/s  42    ▂▄__     WPA2
------------------------------------------------------

The table shows all nearby broadcasting SSIDs, their signal strength, and their security requirements. This table also shows that there is an active connection to ap2.

## <a name="4"></a>Add new connections

Check to see if you already have a connection to one of these SSIDs by `nmcli con`. This displays a tabled list of saved connections. It is best to name new connections according to the SSID for ease of use. If you need more details on a connection, try `nmcli con connection_name show`

If you have previously added a connection to your desired SSID, then proceed to the next step. I found adding new connections using `sudo nmtui` to be easiest. Choose _Edit a connection_ and then _Add_. The prompts and fields to be completed should be self-explantory.


## <a name="5"></a>Connect and disconnect a connection

Once you have a connection, connecting and disconnection are easy.

+ `sudo nmcli con up connection_name`
+ `sudo nmcli con down connection_name`

## <a name="6"></a>Install links

Links is text browser with layouts, tables, and frames. This makes it easy to browse the Internet from the command line. Links will be used to check and accept terms of a captive portal. `sudo apt-get install links`.

## <a name="7"></a>Use links with a captive portal

A captive portal is a special web page that is shown before using the Internet normally. The portal is often used to present a login page. This is done by intercepting most packets, regardless of address or port, until the user opens a browser and tries to access the web. At that time the browser is redirected to a web page which may require authentication and/or payment, or simply display an acceptable use policy and require the user to agree. Captive portals are used at many Wi-Fi hotspots, and can be used to control wired access (e.g. apartment houses, hotel rooms, business centers, "open" Ethernet jacks) as well. [from Wikipedia](https://en.wikipedia.org/wiki/Captive_portal)

The purpose here is not to circumvent the active portal but to acknowledge its terms and continue with using our personal access point. The easiest way to do this is simply to browse to some well know web site with links, eg. `links google.com`. If the hotspot is using an captive portal, the browser will be redirected to the proper page for login or acceptance.

Once done with the captive portal, your access point should be connecting to the Internet. You may remain connected to the pi but, for now, let's move back to your main computing device.

## <a name="8"></a>Connect

Try opening a browser window to a well known web site. If this works you are connected to the Internet, otherwise; review the _Troubleshooting_ section.

## <a name="10"></a>Shutting down

It is always a good idea to follow a defined shutdown procedure and not just pull the plug on everything.

+ On your pi, `sudo nmcli con down connection_name`.
+ On your pi, `sudo shutdown now`.
+ On you main device, close your SSH session.
+ Shutdown your main device.

## <a name="11"></a>Troubleshooting

I have encountered only a few problems using the above procedures. The main problem has to do with the hotspot blocking certain types of services.

+ **Problem** Able to connect from the pi but not from the main device.
    - **Solution** This is likely due to the hotspot preventing external DNS lookups. The pi DHCP server assigns the _8.8.8.8_ and _8.8.4.4_ nameservers to your main device when it connects. The easiest way to solve this is by editing the configuration file to include the hotspot assigned nameservers.
    - Find the hotspot DNS, `nmcli con show connection_name | grep DNS`
    - Using comments, disable the Google domain-name-servers and make the hotspot domain-name-servers active instead, `sudo nano /etc/dhcp/dhcpd.conf`.
    - Restart the DHCP service, `sudo service isc-dhcp-server restart`.
    - Disconnect and then reconnect your main device's wifi.
+ **Question** I want to connect to the hotspot and click through the captive portal page automatically.
    - **Answer** I may choose to do this in the future but for now, there is no consensus on how a captive portal works and how to have express users on the portal. If you are interested in writing Python as a solution, have a look at [python-networkmanager](https://github.com/seveas/python-networkmanager/tree/master/examples).

# <a name="Conclusion"></a>Conclusion

Verifying Internet connectivity when connected with hotspots is still in flux. Much of this is done by the operating system for the user. Here, we must do some of this work ourselves.

Remember to save your image file.
