---
title: Connect to the Raspberry Pi using VNC or RDP
subtitle: View the Pi's desktop remotely
author: Gary Dalton
date: 7 September 2016
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html rpi_vnc_rdp.md -o rpi_vnc_rdp.html
tags: rpi, guide, vnc, rdp, desktop
---
[Home](index.html)

# Description

Sometimes, it is necessary to view the desktop interface of a Raspberry Pi (RPi) from a remote location or without an attached keyboard and monitor. Both VNC and RDP are available to help. VNC and RDP are client-server remote desktop protocols.

# Next up?

After reading this guide, you may be interested in reading:

# Parts List

+ Installed network connected Raspberry Pi

# Overview

Start with a Raspberry Pi image. This is an image saved after following the [RPi Initial Setup Guide](rpi_initial_setup.html). This must be a full desktop image.

1. [Write the image to the MicroSD.](#1)
2. [Connect to your Pi](#2)
3. [Choose VNC or RDP](#3)
4. [RDP](#4)
    + [Installing RDP](#4.1)
    + [The xrdp service](#4.2)
    + [Connecting from Windows](#4.3)
5. [VNC](#5)
    + [Installing VNC](#5.1)
    + [Connect from Linux](#5.2)
    + [Connect from a browser](#5.3)
    + [Connect from Windows](#5.4)
6. [Conclusion](#Conclusion)

# <a name="1"></a>Write the image

Write the image to the MicroSD as described in the [RPi Initial Setup Guide](rpi_initial_setup.html). Insert the MicroSD into the Pi and boot.

# <a name="2"></a>Connect Pi to your Internet

Use an Ethernet cable to connect the pi to the network. DHCP will assign the pi an IP address. Find the address of your pi from your network's DHCP server.

+ SSH to the pi at that IP address or yourpiname.local

# <a name="3"></a>Choose VNC or RDP

There are benefits and drawbacks to each protocol. RDP is faster but is mostly available from Windows. VNC is universal but has lower security. Some other opinions from [Coding Horror](https://blog.codinghorror.com/vnc-vs-remote-desktop/) and [TheTechVoid](http://www.thetechvoid.com/rdp-vs-vnc-which-is-better-for-your-needs/).

It is reasonable to install both but not have them run on boot. This would require SSHing into the pi and starting the protocol of your choice. This guide covers the installation and connection to both VNC and RDP.

# <a name="4"></a>RDP

## <a name="4.1"></a>Installing RDP

Installation is a breeze.

+ Update your sources, `sudo apt-get update`
+ Install, `sudo apt-get install xrdp`
+ At this point RDP is ready to use on the pi

If you are using the iptables firewall, see [RPi iptables](rpi_iptables.html), make certain the port is open.

```
# Allows RDP connections. Uncomment this to allow RDP.
-A INPUT -p tcp -m state --state NEW --dport 3389 -j ACCEPT
```

## <a name="4.2"></a>The xrdp service

xrdp installs itself as a running service which may be controlled via the following commands:

+ `sudo service xrdp status`
+ `sudo service xrdp start`
+ `sudo service xrdp stop`
+ `sudo service xrdp restart`
+ Disable xrdp from starting at boot, `sudo update-rc.d xrdp disable`
+ Enable xrdp to start at boot, `sudo update-rc.d xrdp enable`

## <a name="4.3"></a>Connecting from Windows

An RDP client is a built-in feature of Windows. Just launch the client and enter the connection settings. Connection settings may be saved for easier reconnection. There are also some advanced options available.

+ `Windows-key r`
+ Enter `mstsc`
+ Connect to your pi
+ Enter your pi's login credentials
+ Shortly, you will see the desktop of your pi

*When done with the session, just close the window.*

# <a name="5"></a>VNC

## <a name="5.1"></a>Installing VNC

Virtual Network Connection (VNC) is a way to remotely connect to your pi via the network and access the pi's GUI desktop. I usually do not use a VNC but there are circumstances (educational setting, inexperienced users) where it does prove useful. Generally, I connect using the Browser method. Good information from [rasperrypi.org](https://www.raspberrypi.org/documentation/remote-access/vnc/).

**NOTE: There are many security problems in current vnc implementations. Permit access to vnc servers on the local network only.**

If you feel you need to run an Internet accessible VNC Server, at a minimum, use SSH tunneling for all connections. Also view [About VNC Servers](https://help.ubuntu.com/community/VNC/Servers)

1. Update your sources, `sudo apt-get update`.
2. Install TightVNC Server, `sudo apt-get install tightvncserver`.
3. Start the server, `vncserver -nolisten tcp -nevershared -dontdisconnect :1`.
    + Learn more with `man vncserver`, `man Xvnc`, and `Xvnc -help`
4. Enter the requested new vnc password, a view-only password is not needed. This will be required from the VNC Viewer we install later.
    + If you later wish to set a different password simply `rm .vnc/passwd`
5. Stop the server with `vncserver -kill :1`.
6. The vncserver may be setup to run at boot but I do not recommend it.
7. Update the iptables rule if needed. [RPi iptables](rpi_iptables#3)]

## <a name="5.2"></a>Connect from Linux

+ From the desktop open either _Remote Desktop Viewer_ or the _Remmina Remote Desktop Client_.
    - `sudo apt-get install remmina`
+ Change the connection protocol to VNC.
+ Connect to _hostname.local:1_.
+ Enter the vnc password.
+ When done, just close the window.

## <a name="5.3"></a>Connect from a browser

Browser based VNC makes it easy for anyone to use this technology. I use the Google Chrome App from [RealVNC](https://www.realvnc.com/products/chrome/).

+ From the RealVNC page click _available in the chrome web store_
+ Add to Chrome
+ Launch the extension from Chrome Apps
+ Enter the address, _hostname.local:1_
+ Click _Connect_
+ Enter the vnc password.
+ When done, just close the window.

## <a name="5.4"></a>Connect from Windows

1. Download the [TightVNC installer](http://www.tightvnc.com/download.php).
2. Start the installer and choose **Custom Setup**.
3. From Custom Setup, use the pull-down next to TightVNC Server to have **Entire feature will be unavailable**.
4. Start the _Tight VNC Viewer_.
5. Connect to the Remote Host, _hostname.local:1_.
6. When done, just close the window.

# <a name="Conclusion"></a>Conclusion

Viewing your desktop remotely is cool but remember, this may reduce security. VNC especially, should not be used unprotected over the Internet.
