---
title: Core Pi v2
subtitle: Pi as a wifi bridge providing safe subnet to wifi and Ethernet
author: Gary Dalton
date: 25 February 2016
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html core_pi_v2.md -o core_pi_v2.html
tags: rpi, guide, router, iot, accesspoint
---
[Home](index.html)

# Description

Core Pi v2 joins a pi used as a wifi to eth0 bridge with a spare wifi access point to provide easy setup of new pies. It also provides a local network for working with pies. Core Pi connects to the Internet via wifi, provides a wifi access point, and acts as a DHCP router for a pies direct connected with Ethernet cable.

Recent Raspbian versions are ready for SSH connection over Ethernet cable. Core Pi takes advantage of that to ease initial connection and setup. I am using this in a learning lab environment with Chromebooks.

# Next up?

After reading this guide, you may be interested in reading:

- [Using CorePi](using_core_pi_v2.html)
- [Beginner Guide via Core Pi v2](beginner_guide_via_core_pi v2.html)

# Parts List

+ Raspberry Pi 2
+ 8GB (or larger) class 10 MicroSD card
+ USB WiFi
+ Pi Case
+ Mini-USB power
+ Ethernet cable
+ Wireless router with at least 4 port Ethernet switch
    - I used a spare [Linksys WRT54GL](http://www.linksys.com/us/p/P-WRT54GL/)
    - This router already had [dd-wrt](https://www.dd-wrt.com) installed.
    - The specific router and dd-wrt are not required but this guide's instructions may be specific to them

# Overview

Start with a Raspberry Pi image. This is an image saved after following the [RPi Initial Setup Guide](rpi_initial_setup.html) and [RPi Desktop Mods](rpi_gui_changes.html). The image should not be Lite. If you do not have such an image, start with a Raspbian image and follow the aforementioned guides before returning here.

## Wireless router

1. [Reset the router](#wr1)
2. [Connect to the router](#wr2)
3. [Router settings - Basic Setup](#wr3)
4. [Router settings - Wireless Basic Setup](#wr4)
5. [Router settings - Wireless Security](#wr5)
6. [Router settings - Apply Settings](#wr6)

## Pi

1. [Write the image to the MicroSD.](#1)
2. [Connect Pi to the router](#2)
3. [Connect to your WiFi.](#3)
4. [Setup the DHCP server.](#4)
5. [Set a static IP on eth0.](#5)
6. [Configure NAT.](#6)
7. [Shutdown and reconfigure](#7)
8. [Connect and test.](#8)
9. [Verify security](#9)
10. [Conclusion](#Conclusion).

# Procedures for wireless router

The router will serve the subnet of pies but has no Internet access of its own. If you prefer, you may do away with the pi part of this configuration and hook the router up directly to a WAN or broadband modem.

## <a name="wr1"></a>Reset the router

Power up the router and then press the reset button on the back of the router. Hold the button for about 20 second or until the power light on the front begins to flash.

![Linksys WRT54GL](images/linksys.jpg)

## <a name="wr2"></a> Connect to the router

After a few moments, you should notice a new unsecured wifi access point names dd-wrt. Connect to it.

The router, by default assigns IP addresses in the 192.168.1.0/24 subnet. It also holds the 192.168.1.1 address. Browse to [192.168.1.1](http://192.168.1.1). You are directed to a username and password reset page. Set a secure username and password. For the password, I used the Ownership ID found on the bottom of the router.

## <a name="wr3"></a>Router settings - Basic Setup

There are only a few settings we need to perform. These include WAN connection, router IP address, DHCP services, WiFi SSID, and WiFi security. See the image for WAN connection, router IP address, and DHCP services settings. Click _Save_ after making the changes.

![Router Basic Settings](images/router_basic.png)

## <a name="wr4"></a>Router settings - Wireless Basic Setup

Here we set the Wireless Mode, SSID, and Channel. Click _Save_ after making the changes.

![Router Basic Settings](images/router_wifi_basic.png)

## <a name="wr5"></a>Router settings - Wireless Security

Here we set the Security Mode, the Algorithm, and the shared key. Click _Save_ after making the changes.

![Router Basic Settings](images/router_wifi_security.png)

## <a name="wr6"></a>Router settings - Apply Settings

Click  _Apply Settings_. This should cause the router to reboot. If it does not automatically reboot, reboot it manually.

The SSID and IP addresses are changed, therefore; you will need to connect with the new settings. Connect to the SSID, _corepiv2_, using the shared key, _raspberry_. Connect to the router at [192.168.42.1](http://192.168.42.1). You should be directed to the status page which provides unprotected general information. To view any other settings page, the username/password is required.

# Procedures for pi

The pi is needed in this configuration to provide Internet access to the router. The pi gains Internet access by connecting to a wifi access point and NATing eth0 to wlan0.

## <a name="1"></a>Write the image

Write the image to the MicroSD as described in the [RPi Initial Setup Guide](rpi_initial_setup.html). Insert the MicroSD into the Pi and boot.

## <a name="2"></a>Connect Pi to the router

Use an Ethernet cable to connect the pi to the router. DHCP will assign the pi an IP address. This address may be seen at the bottom in the _DHCP Clients_ section of [router information page](http://192.168.42.1/Info.htm).

+ SSH to the pi at that IP address

## <a name="3"></a>Connect the Pi to your WiFi Internet

In this guide, I will use the desktop but nmcli may be used as discussed in the [RPi Initial Setup Guide - NetworkManager CLI](rpi_initial_setup.html#12). VNC was discussed in [RPi Initial Setup Guide - Connect to the Pi using VNC](rpi_initial_setup.html#11)

**NOTE: There are many security problems in current vnc implementations. Permit  access to vnc servers on the local network only.**

+ On the pi, `vncserver -nolisten tcp -nevershared -dontdisconnect :1`
+ From your browser connect to the pi's VNC
+ Using the dialogs, connect to your Internet wifi SSID

## <a name="4"></a>Setup the DHCP server

+ Install with, `sudo apt-get install isc-dhcp-server`
+ `sudo nano /etc/default/isc-dhcp-server`
+ `INTERFACES="eth0"`
+ Now edit the DHCP configuration file, `sudo nano /etc/dhcp/dhcpd.conf`

```
# ADD THE BELOW TO CONFIG FOR ETH0
subnet 192.168.84.0 netmask 255.255.255.0 {
	interface eth0;
	range 192.168.84.10 192.168.84.50;
	option broadcast-address 192.168.84.255;
	option routers 192.168.84.1;
	default-lease-time 600;
	max-lease-time 7200;
	option domain-name "local";
	option domain-name-servers 8.8.8.8, 8.8.4.4;
}
```

## <a name="5"></a>Set a static IP on eth0

+ `sudo nano /etc/network/interfaces`
+ Comment `#iface eth0 inet manual`
+ Add

```
iface eth0 inet static
  address 192.168.84.1
  netmask 255.255.255.0
```

## <a name="6"></a>Configure NAT

+ Enable IP Forwarding
    - `sudo nano /etc/sysctl.conf` at bottom add _net.ipv4.ip_forward=1_
    - `sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"`
+ If you have not already completed [Firewall with iptables]((rpi_initial_setup.html#10), do so now
+ Update iptables rules, `sudo nano /etc/iptables.test.rules`
+ Update the file to this:

```
*nat

# Allow Access Point NAT
-A POSTROUTING -o wlan0 -j MASQUERADE

# For Coder access
#-A PREROUTING -p tcp -m tcp --dport 8080 -j REDIRECT --to-ports 8080
#-A PREROUTING -p tcp -m tcp --dport 8081 -j REDIRECT --to-ports 8081

# Force all SSH to stay on Core Pi
-A PREROUTING -p tcp -m tcp --dport 22 -j REDIRECT --to-ports 22

COMMIT

*filter

# Allows all loopback (lo0) traffic and drop all traffic to 127/8 that
# doesn't use lo0
-A INPUT -i lo -j ACCEPT
-A INPUT ! -i lo -d 127.0.0.0/8 -j REJECT

# Accepts all established inbound connections
#-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
-A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allows all outbound traffic
# You could modify this to only allow certain traffic
-A OUTPUT -j ACCEPT

# Allows HTTP and HTTPS connections from anywhere (the normal ports
# for websites)
-A INPUT -p tcp --dport 80 -j ACCEPT
-A INPUT -p tcp --dport 443 -j ACCEPT
# Coder
#-A INPUT -p tcp --dport 8080 -j ACCEPT
#-A INPUT -p tcp --dport 8081 -j ACCEPT

# Allows SSH connections
# The --dport number is the same as in /etc/ssh/sshd_config
-A INPUT -p tcp -m state --state NEW --dport 22 -j ACCEPT

# Limit SSH abuse
# The first rule records the IP address of each new attempt to access
# port 22 using the recent module. The second rule checks to see if that
# IP address has attempted to connect 4 or more times within the last
# 60 seconds, and if not then the packet is accepted.
-A INPUT -p tcp -m state --state NEW -m recent --dport 22 --set --name ssh --rsource
-A INPUT -p tcp -m state --state NEW -m recent --dport 22 ! --rcheck --seconds 60 --hitcount 4 --name ssh --rsource -j ACCEPT

# Allows vncserver connections. Uncomment this to allow VNC. Again, this is
# best restricted to certain IPs
-A INPUT -p tcp -m state --state NEW --dport 5901 -j ACCEPT

# Allow Zeroconf connections. (Bonjour and Avahi)
#-A INPUT -p udp -m state --state NEW --dport 5353 -j ACCEPT

# Allow ping
# note that blocking other types of icmp packets is considered a bad idea
# by some
#  remove -m icmp --icmp-type 8 from this line to allow all kinds of icmp:
#  https://security.stackexchange.com/questions/22711
-A INPUT -p icmp -m icmp --icmp-type 8 -j ACCEPT

# Allow forwarded from wlan1 to permit NAT and Access Point
#-A FORWARD -i wlan0 -o wlan1 -m state --state RELATED,ESTABLISHED -j ACCEPT
#-A FORWARD -i wlan1 -o wlan0 -j ACCEPT

# Allow forwarded from eth0 to permit NAT and Core Pi
-A FORWARD -i wlan0 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT
-A FORWARD -i eth0 -o wlan0 -j ACCEPT

# log iptables denied calls (access via 'dmesg' command)
-A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables denied: " --log-level 7

# Reject all other inbound - default deny unless explicitly allowed policy:
-A INPUT -j DROP
-A FORWARD -j DROP

COMMIT
```

+ Load the rules, `sudo iptables-restore < /etc/iptables.test.rules`
+ Verify rules, `sudo iptables -L`, `sudo iptables -S`, `sudo iptables -S -t nat`
+ Save rules for booting,

```
sudo -i
iptables-save > /etc/iptables.up.rules
exit
```
## <a name="7"></a>Shutdown and reconfigure

Now the Core Pi v2 must be shutdown and physically reconfigured. If some of the pi settings are incorrect, you may have to connect to it using a console cable unless the wifi automatically connects to an access point.

+ `sudo shutdown now`
+ Remove power
+ Connect the Ethernet cable from the pi to the WAN port on the router
+ Boot up the pi

## <a name="8"></a>Connect and Test

Connect to the SSID corpiv2 and browse to the [router information page](http://192.168.42.1/Info.htm). You should notice a WAN IP in the 192.168.84.0/24 subnet and LAN IP of 192.168.42.1. The IP address of the pi is _192.168.84.1_.

+ Connect to the pi using an SSH session with _192.168.84.1_
    - If this fails, check your network connections. If the wifi to corepiv2 is not the only connection then maybe the OS is trying to route through the other connection. Disconnect the other connections.
+ On the pi, `vncserver -nolisten tcp -nevershared -dontdisconnect :1`
+ Connect to VNC at _192.168.84.1:1_
+ If not already connected, connect the pi to your wifi access point.
+ Once connected to wifi, disconnect VNC and kill the service, `vncserver -kill :1`.

If SSH and VNC connected properly, well done. Otherwise, begin some troubleshooting.

## <a name="9"></a>Verify security

Core Pi may be accessed as a via point for novices. Novices should not gain shell or VNC access.

+ The pi user should have a strong password. If it is not, change it now with `sudo raspiconfig`.
+ Use SSH key authentication. This was covered in [SSH key authentication](rpi_initial_setup.html#9)
+ Set a strong password for VNC
    - If you need to change the VNC password, simply `rm .vnc/passwd`
+ Once the pi is connedted to wifi, `vncserver -kill :1`

# <a name="Conclusion"></a>Conclusion

CorePiv2 is ready to use for serving as a wifi router, network master, and pi setup station. It would be relatively easy to write some scripts to automatically set up any unconfigured pi connected to eth0. I do not plan on writing such scripts since my CorePi will be used in learning how to set up a pi.

Remember to save your image file as CorePi.
