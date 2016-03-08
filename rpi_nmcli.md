---
title: RPi NetworkManager CLI
subtitle: Raspberry Pi - working with nmcli
author: Gary Dalton
date: 6 March 2016
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html rpi_nmcli.md -o rpi_nmcli.html
tags: rpi, setup, guide, nmcli, NetworkManager
---
[Home](index.html)

# Description

If the Pi will be used from the GUI destop or if it just needs to connect to one network and won't be moving around much, you don't need Network Manager. If you are likely to go mobile with your Pi and need to connect to multiple networks, consider using nmcli.

NetworkManager is a set of tools that make networking simpler. Whether Wi-Fi, wired, bond, bridge, 3G, or Bluetooth, NetworkManager allows you to quickly move from one network to another: once a network has been configured and joined, it can be detected and re-joined automatically the next time its available. Nmcli is just the command line interface, CLI, to NetworkManager.

# Next up?

After reading this guide, you may be interested in reading:

- [RPi WiFi Access Point Guide](rpi_wifi_ap.html)
- [Raspberry Tor](rpi_tor.html)

# Overview

1. [Install NetworkManager CLI](#1)
2. [Using nmcli](#2)
3. [Service control](#3)
4. [Learn more](#4)

# Procedures

## <a name="1"></a>Install NetworkManager CLI

**This procedure will disable your wifi connection until it is reestablished in NetworkManager. So you will need a console or Ethernet connection.**

1. Update your sources, `sudo apt-get update`
2. Install NetworkManager, `sudo apt-get install network-manager`. This will install a number of other packages as well.
3. Install links text-based browser to confirm on captive portals, `sudo apt-get install links`.
4. NetworkManager does not manage any interface defined in /etc/network/interfaces by default. The easiest way to manage some interfaces using NetworkManager is to comment them out. `sudo nano /etc/network/interfaces`.

```
auto lo
iface lo inet loopback

# Managed by NetworkManager
#iface eth0 inet manual

# Managed by NetworkManager
#auto wlan0
#allow-hotplug wlan0
#iface wlan0 inet dhcp
#    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
```

- Review the `sudo nano /etc/NetworkManager/NetworkManager.conf` file. It should look similar to this. The previous _interfaces_ file combined with the _managed=false_ setting, informs NetworkManager to only manage interfaces that are not listed in _interfaces_.

```
[main]
plugins=ifupdown,keyfile

[ifupdown]
managed=false
```

## <a name="2"></a>Using nmcli

1. Reboot, `sudo reboot now`.
2. Check network connection status, `ifconfig wlan0` and verify that the inet addr is empty.
3. Start using nmcli by scanning the manual, `man nmcli`.
4. There are 5 Objects but mainly, this guide uses _connection_ and _device_. Learn more about these by, `nmcli con help` and `nmcli dev help`.
5. `nmcli dev status` displays a table. Notice that wlan0 is disconnected.
6. `nmcli dev wifi` displays a table of available wifi access points.
7. Connects may be added using nmcli, for example `nmcli con add con-name HOMEOFFICE ifname wlan0 type wifi ssid MYSSID`, but I prefer to use nmtui.
8. `sudo nmtui` provides a text user interface that allows easy creation of wifi connection.
9. Edit a connection.
10. Add >> wifi
11. Give your connection a name and set the fields needed for your access point.
12. If you provided all the settings correctly and set the connection to connect automatically, it might already have connected. Check with `ifconfig wlan0`.
13. Notice the changed out put from `nmcli dev status` and `nmcli dev wifi`.
14. Show active connections with `nmcli con show -a`.
15. Take down a connection with `sudo nmcli con down connection_name` and bring it back up with `sudo nmcli con up connection_name`.

## <a name="3"></a>Service control

NetworkManager service control is via systemctl, therefore it may be enabled with `sudo systemctl enable NetworkManager` and disabled with `sudo systemctl disable NetworkManager`. The service may also be monitored using `sudo service NetworkManager [status|start|stop|reload|restart]`.

## <a name="4"></a>Learn more

Learn more about NetworkManager and nmcli from these,

- [Man nmcli](https://www.mankier.com/1/nmcli)
- [Man nmcli examples](https://www.mankier.com/5/nmcli-examples)
- [NetworkManager for Administrators](https://blogs.gnome.org/dcbw/2015/02/16/networkmanager-for-administrators-part-1/)
- [Archlinux](https://wiki.archlinux.org/index.php/NetworkManager)
- [Redhat](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Networking_Guide/sec-Using_the_NetworkManager_Command_Line_Tool_nmcli.html)
