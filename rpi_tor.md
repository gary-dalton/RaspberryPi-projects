---
title: Raspberry Tor
subtitle: Raspberry Pi used as a Tor router
author: Gary Dalton
date: 24 January 2016
license: MIT
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html rpi_tor.md -o rpi_tor.html
tags: rpi, tor, guide, router, privacy

---
# Raspberry Tor

## Raspberry Pi used as a Tor router

# Description

The purpose of Raspberry Tor is to securely and anonymously use the Internet.
The Tor Project defends against network surveillance and traffic analysis.
Tor joined with a Raspberry Pi provides a wireless router to ensure that all
network traffic from a computer is automatically either blocked or routed
through the Tor network.

This is a first but insufficient step to online anonymity.

# Parts List

+ Raspberry Pi 2
+ 4GB MicroSD card
+ [Edimax EW-7811Un](http://www.amazon.com/Edimax-EW-7811Un-150Mbps-Raspberry-Supports/dp/B003MTTJOY/ref=pd_bxgy_147_2)
+ [CanaKit Raspberry Pi WiFi Wireless Adapter](http://www.amazon.com/CanaKit-Raspberry-Wireless-Adapter-Dongle/dp/B00GFAN498)
    - See the discussion [Which Wifi USB adapters](rpi_which_wifi_usb.html).
+ Pi Case
+ Mini-USB power
+ [DS3231 RTC Module](http://www.sunfounder.com/index.php?c=downloadscs&a=Manualdetails&id=64) avilable from [Amazon](http://www.amazon.com/DS3231-Precision-Module-Arduino-Raspberry/dp/B00SSQAUHG/ref=sr_1_3?qid=1454019152)

# Overview

Start with a Raspberry Pi Lite with Wifi Access Point image. This is an image saved after following both the [RPi Initial Setup Guide](rpi_initial_setup.html) and the [RPi Wifi Access Point Guide](rpi_wifi_ap.html). If you do not have such an image, start with a Raspbian Lite image and follow the aforementioned guides before returning here.

1. [Write the image to the microSD.](#1)
2. [Connect to the Pi.](#2)
3. [Configure I2C.](#3)
4. [Real Time clock.](#4)
5. [Disable Internet date checking.](#5)
6. [Install macchanger.](#6)
7. [Add the Tor repository.](#7)
8. [Install Tor.](#8)
9. [Tor configuration.](#9)
10. [Iptables configuration.](#10)
11. [Create the log file.](#11)
12. [Set Tor to start at boot.](#12)
13. [Test the Raspberry Tor.](#13)
14. [Conclusion.](#Conclusion)

# References

+ [Installing Tor on Debian](https://www.torproject.org/docs/debian.html.en)
+ [Tor wiki](https://trac.torproject.org/projects/tor/wiki)
+ [Adafruit Onion Pi](https://learn.adafruit.com/onion-pi/install-tor)
+ [breadtk onion_pi](https://github.com/breadtk/onion_pi/blob/master/setup.sh)
+ [AnonymizingMiddlebox](https://trac.torproject.org/projects/tor/wiki/doc/TransparentProxy#AnonymizingMiddlebox)
+ [Archlinux](https://wiki.archlinux.org/index.php/tor)

# Procedures

## <a name="1"></a>Write the image

Write the image to the MicroSD as described in the [RPi Initial Setup Guide](rpi_initial_setup.html). Insert the MicroSD into the Pi.

## <a name="2"></a>Connect to the Pi

Connect to the pi using SSH over the network connection. Your wlan0 connection should be fully functional unless you are not on the same access point.

## <a name="3"></a>Configure I2C

Follow the [Adafruit Guide](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c).

## <a name="4"></a>Adding a real time clock

Tor network require accurate time keeping and, for anonymity, time keeping over the Internet should be disabled. Follow the [PiHut Guide](Adding a Real Time Clock to your Raspberry Pi).

## <a name="5"></a>Disable Internet date checking

Having an accurate time is important for synchronized communications and for log filing. Linux, and most computers, use Network Time Protocol to check and validate the date/time. Remove the NTP package is an option, `sudo apt-get remove ntp`. NTP can always be easily reinstalled if it is later needed.

## <a name="6"></a>Install macchanger

Media Access Control (MAC) address is a hardware address that uniquely identifies each node of a network. Each of your network interfaces have a MAC address. Macchanger makes it easy to spoof your network node's MAC. See [archlinux](https://wiki.archlinux.org/index.php/MAC_address_spoofing) and [debianadmin](http://www.debianadmin.com/change-your-network-card-mac-media-access-control-address.html).

**Note: See the discussion [Which Wifi USB adapters](rpi_which_wifi_usb.html)**

+ `sudo apt-get install macchanger`.
+ Choose Yes to the question _Please specify whether macchanger should be set up to run automatically every time a network device is brought up or down. This gives a new MAC address whenever you attach an ethernet cable or reenable wifi. Change MAC automatically?_.
+ Verify that the MAC is automaticaly changed by
    - checking your current MAC, `ifconfig wlan0`, make note of the _HWaddr_
    - take the interface down, `sudo service network-manager stop`
    - bring the interface up, `sudo service network-manager start`
    - check the new MAC, `ifconfig wlan0`

### The MAC did not automatically change

If the MAC address did not automatically change, there are two options.

+ `sudo nano /etc/init/macchanger.conf` and add the following:

```
# macchanger - set MAC addresses
#
# Set the MAC addresses for the network interfaces.

description	"change mac addresses"

start on starting network-manager

pre-start script
        /usr/bin/macchanger -e wlan0
        #/usr/bin/macchanger -e eth0
        #/usr/bin/macchanger -e wmaster0
        #/usr/bin/macchanger -e pan0
        #/usr/bin/logger wlan0 `/usr/bin/macchanger -s wlan0`
        #/usr/bin/logger eth0 `/usr/bin/macchanger -s eth0`
end script
```

+ Test it
+ If it still is not changing, `/etc/init/network-manager.conf` and add the following:

```
# network-manager - network connection manager
#
# The Network Manager daemon manages the system's network connections,
# automatically switching between the best available.

description "network connection manager"

start on (local-filesystems
          and started dbus)
stop on stopping dbus

expect fork
respawn
pre-start script
        /usr/bin/macchanger -e wlan0
        #/usr/bin/macchanger -e eth0
        #/usr/bin/macchanger -e wmaster0
        #/usr/bin/macchanger -e pan0
        #/usr/bin/logger wlan0 `/usr/bin/macchanger -s wlan0`
        #/usr/bin/logger eth0 `/usr/bin/macchanger -s eth0`
end script
```

+ Test it
+ Sources are [comment 32](https://bugs.launchpad.net/ubuntu/+source/network-manager/+bug/336736/comments/32) and [comment 31](https://bugs.launchpad.net/ubuntu/+source/network-manager/+bug/336736/comments/31)

## <a name="7"></a>Add the Tor repository

1. Become root, `sudo -i`.
2. Add the repository to the sources file, `echo "deb http://deb.torproject.org/torproject.org release main" >> /etc/apt/sources.list`. Replace _release_ with the current stable release. In Jan2016, it is jessie.
3. Add the repository key,
    - `gpg --keyserver keys.gnupg.net --recv 886DDD89`
    - `gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | apt-key add -`
4. `apt-get update`.
5. Exit root, `exit`.


## <a name="8"></a>Install Tor

Installation is an easy one line command.

+ `sudo apt-get install tor deb.torproject.org-keyring`
+ Stop Tor, `sudo service tor stop`

## <a name="9"></a>Tor configuration

Configuration takes place in a number of service files. Let's start with Tor.

+ `sudo nano /etc/tor/torrc`
+ Scan over this configuration and try to understand as much as you can. Combine this with documents and FAQs from the [Tor Project](https://www.torproject.org).

```
###############  Raspberry Tor Configuration ###
## dated 31JAN2016

VirtualAddrNetworkIPv4 10.192.0.0/10

# Transparent proxy port
TransPort 192.168.83.1:9040
#DEPRECATED
#TransListenAddress 192.168.83.1

# Explicit SOCKS port for local applications.
#SocksPort 9050
SOCKSPort 0

# Port that Tor will output 'info' level logs to.
Log notice file /var/log/tor/notices.log

# Have Tor run in the background
#Conflicts with systemd
#RunAsDaemon 1

# Only ever run as a client. Do not run as a relay or an exit.
ClientOnly

# Ensure resolution of .onion and .exit domains happen through Tor.
AutomapHostsSuffixes .onion,.exit
AutomapHostsOnResolve 1

# Serve DNS responses
DNSPort 192.168.83.1:53
#DEPRECATED
#DNSListenAddress 192.168.83.1

# Firewall will be blocking most outgoing ports
FascistFirewall 1

## End Raspberry Tor Configuration
```

+ Validate the configuration, `tor --verify-config`.

Some important configuration settings from the [Tor manual](https://www.torproject.org/docs/tor-manual.html.en) are:

+ **TransPort [address:]port|auto [isolation flags]**
    - Open this port to listen for transparent proxy connections. Set this to 0 if you don’t want to allow transparent proxy connections. Set the port to "auto" to have Tor pick a port for you. This directive can be specified multiple times to bind to multiple addresses/ports. See SOCKSPort for an explanation of isolation flags.
    - TransPort requires OS support for transparent proxies, such as BSDs' pf or Linux’s IPTables. If you’re planning to use Tor as a transparent proxy for a network, you’ll want to examine and change VirtualAddrNetwork from the default setting. You’ll also want to set the TransListenAddress option for the network you’d like to proxy. (Default: 0)
+ **VirtualAddrNetworkIPv4 Address/bits**
    - When Tor needs to assign a virtual (unused) address because of a MAPADDRESS command from the controller or the AutomapHostsOnResolve feature, Tor picks an unassigned address from this range. (Defaults: 127.192.0.0/10 and /10 respectively.)
    - When providing proxy server service to a network of computers using a tool like dns-proxy-tor, change the IPv4 network to "10.192.0.0/10" or "172.16.0.0/12" and change the IPv6 network to "[FC00]/7". The default VirtualAddrNetwork address ranges on a properly configured machine will route to the loopback or link-local interface. For local use, no change to the default VirtualAddrNetwork setting is needed.
+ **DNSPort [address:]port|auto [isolation flags]**
    - If non-zero, open this port to listen for UDP DNS requests, and resolve them anonymously. This port only handles A, AAAA, and PTR requests---it doesn’t handle arbitrary DNS request types. Set the port to "auto" to have Tor pick a port for you. This directive can be specified multiple times to bind to multiple addresses/ports. See SOCKSPort for an explanation of isolation flags. (Default: 0)
+ **FascistFirewall 0|1**
    - If 1, Tor will only create outgoing connections to ORs running on ports that your firewall allows (defaults to 80 and 443; see FirewallPorts). This will allow you to run Tor as a client behind a firewall with restrictive policies, but will not allow you to run as a server behind such a firewall. If you prefer more fine-grained control, use ReachableAddresses instead.

## <a name="10"></a>Iptables configuration

From earlier guides, the file /etc/iptables.test.rules /etc/iptables.test.rules was used to load the iptables rules. Here, a new file with some torrified rules added to the old rules will be used instead.

+ `sudo nano /etc/iptables.tortest.rules`

```
*nat

# Allow SSH to access point
-A PREROUTING -i wlan1 -p tcp --dport 22 -j REDIRECT --to-ports 22

# DNS routing
-A PREROUTING -i wlan1 -p udp --dport 53 -j REDIRECT --to-ports 53

# All other TCP traffic
-A PREROUTING -i wlan1 -p tcp --syn -j REDIRECT --to-ports 9040

COMMIT

*filter

# Allows all loopback (lo0) traffic and drop all traffic to 127/8 that
# doesn't use lo0
-A INPUT -i lo -j ACCEPT
-A INPUT ! -i lo -d 127.0.0.0/8 -j REJECT

# Allows all local traffic from wlan1
# This may be tweaked to deny some traffic on wlan1
-A INPUT -i wlan1 -j ACCEPT

# Accepts all established inbound connections
#-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
-A INPUT -i wlan0 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Prevent transproxy packet leak
-A OUTPUT -m conntrack --ctstate INVALID -j LOG --log-prefix "Transproxy ctstate leak blocked: " --log-uid
-A OUTPUT -m conntrack --ctstate INVALID -j DROP

# On wlan1
# Allow all outgoing traffic
# This may be tweaked to limit wlan1 traffic
-A OUTPUT -o wlan1 -j ACCEPT

# On wlan0
# Only allows outbound traffic to ports 80 and 443
# Also allow DNS traffic (needed for captive portal connection)
-A OUTPUT -o wlan0 -p tcp --dport 80 -j ACCEPT
-A OUTPUT -o wlan0 -p tcp --dport 443 -j ACCEPT
# Also allow DNS traffic (needed for captive portal connection)
# If needed, this rule may be dropped once connected to the portal
-A OUTPUT -o wlan0 -p udp --dport 53 -j ACCEPT

# Deny all other outbound traffic on wlan0
-A OUTPUT -o wlan0 -j REJECT

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

# Allow Zeroconf connections. (Bonjour and Avahi)
-A INPUT -p udp -m state --state NEW --dport 5353 -j ACCEPT

# Allow ping
# note that blocking other types of icmp packets is considered a bad idea
# by some
#  remove -m icmp --icmp-type 8 from this line to allow all kinds of icmp:
#  https://security.stackexchange.com/questions/22711
-A INPUT -p icmp -m icmp --icmp-type 8 -j ACCEPT

# log iptables denied calls (access via 'dmesg' command)
-A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables denied: " --log-level 7

# Allow forwarded from wlan1 to permit NAT and Access Point
-A FORWARD -i wlan0 -o wlan1 -m state --state RELATED,ESTABLISHED -j ACCEPT
-A FORWARD -i wlan1 -o wlan0 -j ACCEPT

# Reject all other inbound - default deny unless explicitly allowed policy:
-A INPUT -j DROP
-A FORWARD -j DROP

COMMIT
```
+ Become root, `sudo -i`.
+ Load the new rules, `iptables-restore < /etc/iptables.tortest.rules`.
+ Visually verify the new rules, `iptables -t nat -S` and `iptables -S`.
+ Save the new rules `iptables-save > /etc/iptables.up.rules`.
+ `exit`

## <a name=11></a>Create the log file

+ Create the file, `sudo touch /var/log/tor/notices.log`.
+ Set the owner and permissions.
    - `sudo chown debian-tor /var/log/tor/notices.log`
    - `sudo chmod 644 /var/log/tor/notices.log`

## <a name=12></a>Set Tor to start at boot

+ It Tor already enabled on boot, `sudo systemctl is-enabled tor.service`?
+ Enable Tor for boot start, `sudo systemctl enable tor.service`
+ Start Tor now, `sudo service tor start`


## <a name=13></a>Test the Raspberry Tor

The final product is near. Let's do a little testing to make sure everything is performing as it should. (It is possible to tweak the iptables rules if needed.)

+ Start the pi, connect to it, and connect it to the network. Let the [Using the WiFi Access Point with captured portal](rpi_captured_portal.html) be your guide.
+ On the pi, `links check.torproject.org`. Should show _Sorry. You are not using Tor._
+ From your connected device, use a standard browser to **check.torproject.org**. Should show _Congratulations. This browser is configured to use Tor._
+ All connections from your connected device are routed through Tor.
+ The pi only allows outgoing connections to ports 80, 433, and 53.
+ Once connected to a captive portal, port 53 may be blocked.
    - Deny with `sudo iptables -D OUTPUT -o wlan0 -p udp --dport 53 -j ACCEPT`
    - Reallow with `sudo iptables -A OUTPUT -o wlan0 -p udp --dport 53 -j ACCEPT`

### Some helpful commands for troubleshooting

+ `sudo nano /etc/dhcp/dhcpd.conf`
+ `sudo service isc-dhcp-server restart`
+ `sudo nano /etc/hostapd/hostapd.conf`
+ `sudo service hostapd start`
+ `sudo service network-manager stop`
+ `sudo nmcli con up connection_name`
+ `sudo nano /etc/tor/torrc`
+ `sudo service tor status`
+ `sudo nano /etc/iptables.tortest.rules`
+ `sudo iptables-restore < /etc/iptables.tortest.rules`
+ `sudo iptables -t nat -S`
+ `sudo iptables -L`
+ `tail -F /var/log/tor/notices.log`

# <a name="Conclusion"></a>Conclusion

Save the image file. After all that configuring it is good to make sure you can duplicate it.

The Tor Browser is recommended in addition to using the Raspberry Tor. It has a number of tweaks that improve anonymity. If you like this guide and using Tor, consider supporting the Tor Project. The easiest way to show your support is by setting up a relay. The Tor Project also [accepts donations](https://www.torproject.org/donate/donate.html)

After doing the research needed to make this guide work, I am planning on setting most of my servers as relays or bridges. I would really like to set up an exit node but that requires a bit more effort.
