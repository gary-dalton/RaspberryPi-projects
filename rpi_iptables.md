---
title: RPi iptables
subtitle: Using iptables for firewall with various configuration examples
author: Gary Dalton
date: 6 March 2016
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html rpi_iptables.md -o rpi_iptables.html
tags: rpi, setup, guide, secure, iptables, firewall
---
[Home](index.html)

# Description

iptables is used to control packet filtering, Network Address Translation (masquerading, portforwarding, transparent proxying), and special effects such as packet mangling. It is an important and effective part of your pi's security and in some use cases is required.

# Overview

Without a firewall, your pi is functional and connected. It can be made more secure with iptables which will only allow the types of traffic you permit. Iptables is currently running on your pi but it is set to allow all traffic. We are about to change that. Rules for iptables can sometimes be a bit touchy so make certain that you are able to connect to your pi via console until certain of your settings. Iptables is quite powerful but also sometimes complex, so do try to learn more before blindly applying these rules.

1. [Learn more](#1)
2. [Persistant iptables](#2)
3. [Basic rule set](#3)
4. [CorePi rule set](#4)
5. [WiFi Access Point rule set](#5)


# Procedures

## <a name="1"></a>Learn more

 See [Iptables How To](https://help.ubuntu.com/community/IptablesHowTo/), [Debian](https://wiki.debian.org/iptables), and [archlinux](https://wiki.archlinux.org/index.php/iptables).

Firewall rules are processed from top to bottom. Once a rule is matched, no more rule checking occurs. So if my first rule allows all traffic and my last rule allows none, then all traffic is allowed. Don't block yourself by creating a bad first rule.

List the current rules with, `sudo iptables -L`.

## <a name="2"></a>Persistant iptables

iptables-persistent makes it easier to load and save iptables settings. We also create a script to load the rules on boot.

+ Install, `sudo apt-get install iptables-persistent`
+ Create the file, `sudo nano /etc/iptables.test.rules`, with whatever rules you wish to use. (this guide covers various rule sets later)
+ Load the rules, `sudo iptables-restore < /etc/iptables.test.rules`
+ Check that they loaded correctly, `sudo iptables -L`
+ All OK? Save the rules, `sudo sh -c 'iptables-save > /etc/iptables.up.rules'`
+ Force rules to load on reboot, `sudo nano /etc/network/if-pre-up.d/iptables`
+ Add these lines:

```
#!/bin/sh
/sbin/iptables-restore < /etc/iptables.up.rules
```

+ Make that file executable, `sudo chmod +x /etc/network/if-pre-up.d/iptables`.


## <a name="3"></a>Basic rule set

Rule set for a standard pi with nothing extra or unusual

+ Edit the file, `sudo nano /etc/iptables.test.rules`
+ Set the file to:

```
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

# Now you should read up on iptables rules and consider whether ssh access
# for everyone is really desired. Most likely you will only allow access
# from certain IPs.

# Allows TightVNC connections. Uncomment this to allow VNC. Again, this is
# best restricted to certain IPs
#-A INPUT -p tcp -m state --state NEW --dport 5901 -j ACCEPT

# Allows RDP connections. Uncomment this to allow RDP.
#-A INPUT -p tcp -m state --state NEW --dport 3389 -j ACCEPT

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

# Reject all other inbound - default deny unless explicitly allowed policy:
-A INPUT -j DROP
-A FORWARD -j DROP

COMMIT
```

+ Load the rules, `sudo iptables-restore < /etc/iptables.test.rules`.
+ Check that they loaded correctly, `sudo iptables -L`.
+ Verify that you can still establish a connection using SSH.
+ All OK? Save the rules, `sudo sh -c 'iptables-save > /etc/iptables.up.rules'`.
+ Reboot and test by connecting with SSH and `iptables -L`.

## <a name="4"></a>CorePi rule set

Rule set for [CorePi V2](core_pi_v2.html)

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

# For Apt-Cacher-NG
-A PREROUTING -p tcp -m tcp --dport 3142 -j REDIRECT --to-ports 3142

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

# Allows Apt-Cacher-NG
-A INPUT -p tcp --dport 3142 -j ACCEPT

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

# Allows RDP connections. Uncomment this to allow RDP.
#-A INPUT -p tcp -m state --state NEW --dport 3389 -j ACCEPT

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

## <a name="5"></a>WiFi Access Point rule set

Rule set for [RaspberryPi3 easy WiFi access point](rpi3_simple_wifi_ap.html)

+ Update iptables rules, `sudo nano /etc/iptables.test.rules`
+ Update the file to this:

```
*nat

# Allow Access Point NAT
-A POSTROUTING -o eth0 -j MASQUERADE

# Redirect SSH to local
# -A PREROUTING -p tcp -m tcp --dport 22 -j REDIRECT --to-ports 22

COMMIT

*filter

# Allows all loopback (lo0) traffic and drop all traffic to 127/8 that
# doesn't use lo0
-A INPUT -i lo -j ACCEPT
-A INPUT ! -i lo -d 127.0.0.0/8 -j REJECT

# Accepts all established inbound connections
-A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allows all inbound traffic from wlan0
-A INPUT -i wlan0 -j ACCEPT

# Allows all outbound traffic
# You could modify this to only allow certain traffic
-A OUTPUT -j ACCEPT

# Allows HTTP and HTTPS connections from anywhere (the normal ports
# for websites)
-A INPUT -p tcp --dport 80 -j ACCEPT
-A INPUT -p tcp --dport 443 -j ACCEPT

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
#-A INPUT -p tcp -m state --state NEW --dport 5901 -j ACCEPT

# Allows RDP connections. Uncomment this to allow RDP.
#-A INPUT -p tcp -m state --state NEW --dport 3389 -j ACCEPT

# Allow Zeroconf connections. (Bonjour and Avahi)
-A INPUT -p udp -m state --state NEW --dport 5353 -j ACCEPT

# Allow ping
# note that blocking other types of icmp packets is considered a bad idea
# by some
#  remove -m icmp --icmp-type 8 from this line to allow all kinds of icmp:
#  https://security.stackexchange.com/questions/22711
-A INPUT -p icmp -m icmp --icmp-type 8 -j ACCEPT

# Allow forwarded from eth0 to permit NAT and Access Point
-A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
-A FORWARD -i wlan0 -o eth0 -j ACCEPT

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
# Block an IP address

Sometimes, it is neccessary to block an IP address or range of addresses. There are many ways to use IP blacklists but that will not be covered.

+ Block a single IP
    + CLI `iptables -I INPUT -s 216.58.216.206 -j DROP`
    + Config `-A INPUT -s 216.58.216.206/32 -j DROP`

See, [Blocking IP addresses in Linux with iptables](https://linux-audit.com/blocking-ip-addresses-in-linux-with-iptables/)

# <a name="Conclusion"></a>Save the image to a file

Now that you have spent all this time getting your Raspberry Pi set up just so, **save it to an image** for easy reuse. You will still have to change things like usernames, passwords, and hostnames.

Instead of writing a file image to the MicroSD, use the same software to read the MicroSD to a file image. Then when you are ready to spin up your next pi, it will be as easy as, well, pie.
