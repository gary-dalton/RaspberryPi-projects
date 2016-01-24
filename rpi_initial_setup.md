---
title: RPi Initial Setup Guide
subtitle: Raspberry Pi - Image and Initial Setup
author: Gary Dalton
date: 23 January 2016
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: gary-dalton.github.io
  branch: "master"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html InitialSetup.md -o rpi_initial_setup.html
tags: rpi, guide

---

# RPi Initial Setup Guide

# Description

This guides the user through creation of a MicroSD image and then initial setup of the Raspberry Pi. It is necessary to have either a wired or WiFi network to complete this guide. Once a well functioning and secure Pi is completed, the user will save the image.

# Parts List

* Raspberry Pi
* 4GB (or larger) class 10 MicroSD card
* [USB WiFi dongle](http://www.amazon.com/Edimax-EW-7811Un-150Mbps-Raspberry-Supports/dp/B003MTTJOY/ref=pd_bxgy_147_2) _(optional)_
* [USB to serial console cable](https://www.adafruit.com/product/954)  _(optional)_

# Overview

1. Download the Raspbian image and write it to the microSD.
2. Connect to the Pi using either the USB to serial cable or using a keyboard and monitor.
3. Boot the Pi.
4. Run the initial setup.
5. Get the Pi connected to your WiFi.
6. Install some network magic.
7. Connect to the Pi using SSH.
8. Improve SSH security.
9. Firewalling with iptable.
10. Connect to the Pi using VNC. _(optional)_
11. Add the Adafruit Raspberry Pi repository. _(optional)_
12. Install node.js. _(optional)_
13. Install occidentalis. _(optional)_

# Procedures

## 1 Raspbian

Download the [latest version of Raspbian](https://www.raspberrypi.org/downloads/raspbian/).
For general use, download the full version. If you are certain that you want a headless installation with no GUI desktop, download the Lite version. I usually use the Lite version with no desktop.

For the Lite version, a 4Gb MicroSD is likely sufficient but use at least an 8GB card for the full version. The required size of your disk depends a bit on your expected use.

Unzip the image and write it to the MicroSD card. On Windows, I use [Win32 Disk Imager](http://sourceforge.net/projects/win32diskimager/). Other OS instructions may be found on the Raspbian download page.

Insert the MicroSD into the Pi.

## 2 Connect to the Pi

A Raspberry Pi is a computer that may be operated by connecting with a mouse, keyboard, and monitor. I prefer to connect to it using the USB to Serial console cable. This allows me to use my main computer's equipment while working on the Pi in a terminal window. See the [Adafruit overiew](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-5-using-a-console-cable) for full details on using the USB to console cable.

![USB to console connection](images/USB-console-connect.jpg)

## 3 Boot the Pi

As soon as you insert the USB to console cable into your computer, the Pi will start to boot. If you are using a keyboard and monitor, plug in your power to boot the Pi.

This next set of instructions assumes you are using the USB to console cable.

1. Use SSH to connect to the serial COM port of the USB connection
2. Hit enter to show the login screen
3. Login using the default user: pi and the default password: raspberry. (We will change these shortly.)

## 4 Run first boot setup

Start the configuration software to expand the filesystem, change the password, and change the hostname. Enter the configuration with this command, `sudo raspi-config`.

1. Select and execute **Expand Filesystem**
2. Select and execute **Change User Password**
3. Select **Advanced Options** and select and execute **Hostname**. _Pick a unique and easy to remember hostname. This will be used to connect later._
4. Reboot your system `sudo reboot now`.

## 5 WiFi

Time to get your Pi connected to your local network and then to the Internet. This procedure assumes you are using a supported wifi USB dongle, are connecting to a simple shared key access point using DHCP, and are not using the GUI desktop to configure your connections. If you are using the full desktop, connect your wifi using the graphical Network Manager. See the [Debian wiki](https://wiki.debian.org/WiFi) for an excellent discussion.

### Method 1 -  /etc/network/interfaces

If the Pi just needs to connect to one network and won't be moving around much, use Method 1. If you are likely to go mobile with your Pi and need to connect to multiple networks, do the initial setup with Method 1 and then move on to Method 2.

1. `sudo nano /etc/network/interfaces`
2. Add the following to this file
```
auto wlan0
allow-hotplug wlan0
iface wlan0 inet dhcp
    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
```
3. `CTRL-o` to save and `CTRL-x` to exit.
4. `sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`
5. Add the following to this file:
```
network={
ssid="your_wifi_identifier"
psk="your_wifi_password"
proto=RSN
key_mgmt=WPA-PSK
pairwise=CCMP
auth_alg=OPEN
}
```
6. You may need to change the _proto_ or _key mgmt_ values depending on your network. See `man wpa_supplicant.conf` for more information.
7. Restart the wifi interface. If your settings are correct, it should automatically connect.
```
sudo ifdown
sudo ifup
```
8. Check that you are connected with `ifconfig wlan0`. From this output, make note of the **inet addr**. This is your Pi's IP address. Use `iwconfig wlan0` to see which Access Point you are connected to.

### Method 2 -  ConnMan

ConnMan is a daemon for managing Internet connections within embedded devices. It has low memory consumption and reacts well to changing network conditions. See  [ConnMan](https://01.org/connman)

Basically ConnMan will make it easier to connect to and manage multiple connection profiles from the command line interface, CLI.

1. Update your sources, `sudo apt-get update`
2. Apply the updates, `sudo apt-get upgrade`
3. Install ConnMan, `sudo apt-get install connman`. This may also install _bluez_ and _ofono_.
4. Disable the previous network configuration, `sudo nano /etc/network/interfaces` and comment all the lines you previously entered.
```
#auto wlan0
allow-hotplug wlan0
#iface wlan0 inet dhcp
iface wlan0 inet manual
#    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
```
5. Reboot, `sudo reboot now`
6. Check network connection status, `ifconfig wlan0` and verify that the inet addr is empty.

Start using ConnMan. This guide will only cover an initial connection but ConnMan is capable of much more. See additional documentation from [archlinux](https://wiki.archlinux.org/index.php/Connman), [intel](https://01.org/connman/documentation), and [tizen](https://wiki.tizen.org/wiki/IVI/ConnMan_Tips_%26_Tricks). One thing to note is that ConnMan uses tab completion. This means type the first few characters of your command and hit tab.

1. Start ConnMan control, `sudo connmanctl`. Notice that the CLI prompt changes.
2. `enable wifi`
3. Scan for wifi services, `scan wifi`.
4. List the found services, `services`.
5. Register an agent to handle user requests, `agent on`.
6. From the list of services, select the wifi address you wish to connect to. This will start with wifi_, tab completion comes in handy now. Connect to the service, `connect wifi_the_numbers_letters_of_your_service`.
7. If it is a secured access point, the agent should request a password so enter the password.
8. Once authenticated, your credentials are saved for future connections.
9. `quit`.
10. Check your connection, `ifconfig wlan0`.
11. To view all of your saved configurations,
```
sudo -i
cat /var/lib/connman/*/settings
exit
```
12. Start, stop, and view status of ConnMan using `systemctl status connman`

## 6 Network magic

This step does nothing more than make it easier to find your Pi on your network. It uses _Zeroconf_, provided by _Avahi_ on Linux, _Bonjour_ on Windows, and included in Apple.

1. Install `sudo apt-get install avahi-daemon`.
2. Your system can now be found at hostname.local, where the hostname is that which you entered back in _4 Run first boot setup_.
3. For your Windows machine, download and install [Bonjour Print Services](https://support.apple.com/downloads/Bonjour_for_Windows).

## 7 Connect to Pi using SSH

SSH is a safe and efficient way to connect to your Pi over the network or the Internet. It is enabled by default but for highest security, I recommend a few configuration changes and installing your own personal keys. This guide assumes you are connecting from Windows or another Linux system. For Windows use [PuTTY](http://www.putty.org/) and for Linux use [OpenSSH](http://www.openssh.com/). It may be necessary to install PuTTY but OpenSSH comes installed on Linux.

* Verify that SSH is enabled, `sudo raspi-config` then Advanced Options and then SSH.

### Windows

1. Start puTTY
2. Enter _hostname.local_, where hostname is from _6 Network magic_ into the **Host Name (or IP address)** box.
3. Save the session if you wish.
4. The first time you connect, you will get an alert. Click Yes to continue.
5. Enter your username, default _pi_, and password.
6. You are now at the CLI prompt of your pi.
7. When done, end your session with `exit`.

### Linux

1. Connect using `ssh user@hostname.local`, where hostname is from _6 Network magic_ and the default user is _pi_.
2. The first time you connect, you will get an alert. Enter **yes** to continue.
3. You are now at the CLI prompt of your pi.
4. When done, end your session with `exit`.

A good resource is from [archlinux](https://wiki.archlinux.org/index.php/Secure_Shell).

## 8 Improving security

Some general rules to security are:

* Do not use default passwords
* Use multifactor authentication
* Do not provide shell access unless it is needed
* Do not provide services you do not need
* Do not needlessly expose services
* Apply security patches
* Prevent physical access
* Use quality cryptology

### SSHd configuration

There are a few SSHd configuration changes that will improve SSH security. Since SSHd is likely a service you do want to provide and it gives shell access, this is important.

1. Edit the configuration file, `sudo nano /etc/ssh/sshd_config`
2. Change the following:
```
PermitRootLogin no
```
3. Add the following:
```
AllowUsers pi   // Even better if you use a non-default user
```

### SSH key authentication

Using public key authentication will greatly improve your SSHd security but sometimes seems complicated. Do it anyways.

#### Linux

1. Generate a password protected key pair, `ssh-keygen`.
2. You will be asked the name of the key file and the password to unlock the key. I usually name my key file according to the system it is used to connect to. The process should look something like this:
```
Generating public/private rsa key pair.
Enter file in which to save the key (/home/user/.ssh/id_rsa): /home/user/.ssh/id_rsa_hostname
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/user/.ssh/id_rsa_hostname.
Your public key has been saved in /home/user/.ssh/id_rsa_hostname.pub.
The key fingerprint is:
ac:6a:0f:32:2e:bd:aa:3d:46:cc:c0:21:cc:68:47:40 user@computer
The key's randomart image is:
+---[RSA 2048]----+
|=Eo.             |
|o= .             |
|+ o              |
|..     .         |
| +      S        |
|  +    .         |
| oo . .          |
|.o+o.o           |
|++++...          |
+-----------------+
```
3. Copy your public key to the pi, `ssh-copy-id -i ~/.ssh/id_rsa_hostname.pub pi@hostname.local`.
4. You should see something like the following and also be asked for your password.

```
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
pi@hostname.local's password:

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'pi@hostname.local'"
and check to make sure that only the key(s) you wanted were added.
```

* Go ahead and `ssh 'pi@hostname.local`. You should be asked for the password for your key.

An excellent resource for learning more is from [archlinux](https://wiki.archlinux.org/index.php/SSH_keys)

#### Windows PuTTY

1. Start **PuTTYgen**
2. Change the _Number of bits in a generated key_ to 2048.
3. Click **Generate** to generate a new key pair.
4. Add a password to the _Key passphrase_ and _Confirm passphrase_.
5. Save your public and private keys. The private key should not be shared but the public key may be freely shared.
6. On the pi, `nano ~/.ssh/authorized_keys`.
7. Copy the public key from the Windows PuTTYgen box and paste it into the authorized_keys file on your pi. Save the file.
8. Close PuTTYgen.
9. Open PuTTY.
10. Save a new session named _hostname_ and put _hostname.local_ in the Host Name box.
11. From the configuration Categories, select Connection >> SSH >> Auth.
12. Browse to select the private key you created earlier for authentication.
13. Save the session.
14. Test by clicking Open.
15. You should be required to enter in the username to log in with and also the password used to protect the key.

**NOTE: Do not lose your private keys. Once the next configuration steps are complete, your private key and password are required to login remotely.** You will still be able to login from the console or with a keyboard and monitor.

### More SSHd configuration

Time now to only allow remote logins using public key authentication. This configuration is on your pi.

1. Open the file, `sudo nano /etc/ssh/sshd_config`
2. Add the following lines to the file and save:
```
PasswordAuthentication no
ChallengeResponseAuthentication no
UsePAM no
PubkeyAuthentication yes
```
3. Reload the sshd configuration, `sudo service sshd reload`
4. Test by trying to login without the key file.

## 9 Firewall with iptables

At this point, your pi is functional, connected, and reasonably secure. It can be made more secure with iptables which will only allow the types of traffic you permit. Iptables is currently running on your pi but it is set to allow all traffic. We are about to change that. Rules for iptables can sometimes be a bit touchy so make certain that you are able to connect to your pi via console until certain of your settings. Iptables is quite powerful but also sometimes complex, so do try to learn more before blindly applying these rules. See [Iptables How To](https://help.ubuntu.com/community/IptablesHowTo/), [Debian](https://wiki.debian.org/iptables), and [archlinux](https://wiki.archlinux.org/index.php/iptables).

Firewall rules are processed from top to bottom. Once a rule is matched, no more rule checking occurs. So if my first rule allows all traffic and my last rule allows none, then all traffic is allowed. Don't block yourself by creating a bad first rule.

1. List current rules, `sudo iptables -L`
2. Store rules in a file, `sudo apt-get install iptables-persistent`
3. Edit the files, `sudo nano /etc/iptables.test.rules`
4. Add the following to this file:

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
5. Load the rules, `sudo iptables-restore < /etc/iptables.test.rules`.
6. Check that they loaded correctly, `iptables -L`.
7. Verify that you can still establish a connection using SSH.
8. All OK? Save the rules, `sudo iptables-save > /etc/iptables.up.rules`.
9. Force rules to load on reboot, `sudo nano /etc/network/if-pre-up.d/iptables`.
10. Add these lines:
```
#!/bin/sh
/sbin/iptables-restore < /etc/iptables.up.rules
```
11. Make that file executable, `sudo chmod +x /etc/network/if-pre-up.d/iptables`.
12. Reboot and test by connecting with SSH and `iptables -L`.

## 10 Connect to the Pi using VNC (optional)

Virtual Network Connection (VNC) is a way to remotely connect to your pi via the network and access the pi's GUI desktop. I usually do not use a VNC but there are circumstances (educational setting, inexperienced users) where it does prove useful. Good information from [rasperrypi.org](https://www.raspberrypi.org/documentation/remote-access/vnc/).

**Note: VNC should only available on the local network.**

1. Update your sources, `sudo apt-get update`.
2. Install TightVNC Server, `sudo apt-get install tightvncserver`.
3. Start the server, `vncserver :1`.
4. Enter the requested new vnc password. This will be required from the VNC Viewer we install later.
5. Stop the server with `vncserver -kill :1`.
6. The vncserver may be setup to run at boot but I do not recommend it.
7. Update the iptables rule if needed.

### Connect from Linux

1. From the desktop open either _Remote Desktop Viewer_ or the _Remmina Remote Desktop Client_.
2. Change the connection protocol to VNC.
3. Connect to _hostname.local:1_.
4. Enter the vnc password.
5. When done, just close the window.

### Connect from Windows

1. Download the [TightVNC installer](http://www.tightvnc.com/download.php).
2. Start the installer and choose **Custom Setup**.
3. From Custom Setup, use the pull-down next to TightVNC Server to have **Entire feature will be unavailable**.
4. Start the _Tight VNC Viewer_.
5. Connect to the Remote Host, _hostname.local:1_.
6. When done, just close the window.

## 11 Add the Adafruit Raspberry Pi repository (optional)

The [Adafruit repository](https://learn.adafruit.com/apt-adafruit-com/overiew) provides access to the most recent node packages and to a few other goodies useful to makers.

1. Become root, `sudo -i`.
2. Add the repository to the sources file, `echo "deb http://apt.adafruit.com/raspbian/ release main" >> /etc/apt/sources.list`. Replace _release_ with the current stable release. In Jan2016, it is jessie.
3. Add the repository key, `wget -O - -q https://apt.adafruit.com/apt.adafruit.com.gpg.key | apt-key add -`.
4. `apt-get update`.
5. Exit root, `exit`.

## 12 Install node.js (optional)

Node.js is a JavaScript runtime environment for developing server-side Web applications. It uses an asynchronous event driven framework that is designed to build scalable network applications. I install it on nearly all of my pi to provide a framework for building user interfaces that can actually do something.

1. Update, `sudo apt-get update`.
2. Install node, `sudo apt-get install node`.
3. Now go learn more about node from [Node](https://nodejs.org/en/), [Express](http://expressjs.com/en/starter/hello-world.html), [Adafruit](https://learn.adafruit.com/node-embedded-development/events), and [search](https://www.google.com/webhp?q=node.js%20raspberry%20pi).

## 13 Install occidentalis (optional)

Occidentalis is a collection of drivers, configuration utilities, and other useful things for single-board computers from [Adafruit](https://github.com/adafruit/Adafruit-Occidentalis).

1. Update, `sudo apt-get update`.
2. Install occidentalis, `sudo apt-get install occidentalis`.

# Save the image to a file

Now that you have spent all this time getting your Raspberry Pi set up just so, save it to an image for easy reuse. You will still have to change things like usernames, passwords, and hostnames.

Instead of writing a file image to the MicroSD, use the same software to read the MicroSD to a file image. Then when you are ready to spin up your next pi, it will be as easy as, well, pie.
