---
title: RPi Initial Setup Guide
subtitle: Raspberry Pi - Image and Initial Setup
author: Gary Dalton
date: 21 February 2017
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html rpi_initial_setup.md -o rpi_initial_setup.html
tags: rpi, setup, guide, secure
---
[Home](index.html)

# Description

This guides the user through creation of a MicroSD image and then initial setup of the Raspberry Pi. It is necessary to have either a wired or WiFi network to complete this guide. Once a well functioning and secure Pi is completed, the user will save the image. Notice that a large part of this guide deals with security. Security is a primary concern when connecting things to the Internet.

# Next up?

After reading this guide, you may be interested in reading:

- [RPi WiFi Access Point Guide](rpi_wifi_ap.html)
- [Raspberry Tor](rpi_tor.html)
- [RPi Desktop Mods](rpi_gui_changes.html), Changes to the packages and defaults of the full Raspian


# Parts List

* Raspberry Pi 2 or newer
* 4GB (or larger) class 10 MicroSD card
* [USB WiFi dongle](http://www.amazon.com/Edimax-EW-7811Un-150Mbps-Raspberry-Supports/dp/B003MTTJOY/ref=pd_bxgy_147_2) _(optional)_
* [USB to serial console cable](https://www.adafruit.com/product/954)  _(optional)_

# Overview

1. [Download the Raspbian image and write it to the microSD.](#1)
2. [Connect to the Pi.](#2)
3. [Boot the Pi.](#3)
4. [Run the initial setup.](#4)
5. [Connect to the Internet.](#5)
6. [Update and upgrade the Pi.](#6)
7. [Install some network magic.](#7)
8. [Connect to the Pi using SSH.](#8)
9. [Improving security.](#9)
10. [Firewalling with iptables.](#10)
11. [Connect remotely to the Pi's desktop.](#11) _(optional)_
12. [Advanced network management with nmcli.](#12) _(optional)_
13. [Adafruit Raspberry Pi repository.](#13) _(deprecated)_
14. [Node.js.](#14) _(optional)_
15. [Occidentalis.](#15) _(deprecated)_
16. [Conclusion](#Conclusion).

The estimated time to complete each step is given. This time is for a novice performing the procedures for the first time. If you are familiar with some of the topics or have completed these procedures before, you should expect to use less time.

Not sure where things are on your Pi? Review [this diagram](http://www.techweekeurope.co.uk/wp/wp-content/gallery/raspberry-pi-b/b__infographic_web.jpg).

# Procedures

## <a name="1"></a>Raspbian

_Time to complete this is about 1 hour 20 minutes. If you already have an image, the required software, and have done it before it will go much faster._

Download the [latest version of Raspbian](https://www.raspberrypi.org/downloads/raspbian/).
For general use, download the full version. If you are certain that you want a headless installation with no GUI desktop, download the Lite version. I usually use the Lite version with no desktop.

For the Lite version, a 4Gb MicroSD is likely sufficient but use at least an 8GB card for the full version. The required size of your disk depends a bit on your expected use. In early 2016, the sweet spot in pricing for these cards is 16GB.

Unzip the image and write it to the MicroSD card. On Windows, I use [Win32 Disk Imager](http://sourceforge.net/projects/win32diskimager/). More detailed instructions and instructions for other operating systems may be found on [Raspberrypi.org's Installing Images](https://www.raspberrypi.org/documentation/installation/installing-images/README.md).

Insert the MicroSD into the Pi.

**NOTE: Versions of Raspbian later than December 2016 ship with SSH disabled. SSH may be enabled by adding a file named _ssh_ to the boot directory of the SD card. See https://www.raspberrypi.org/blog/a-security-update-for-raspbian-pixel/**


## <a name="2"></a>Connect to the Pi

_Time to complete is about 15 minutes._

From the initial boot, there are three ways to connect to the pi.

1. A Raspberry Pi is a computer that may be operated by connecting with a mouse, keyboard, and monitor.
2. Using SSH over an Ethernet connection. If you are not familiar with SSH, we will review it later in this guide.
3. Often, I find it easiest to connect to it using the USB to Serial console cable. This allows me to use my main computer's equipment while working on the Pi in a terminal window. See the [Adafruit overiew](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-5-using-a-console-cable) for full details on using the USB to console cable.
    - If you use the Adafruit guide and wish to install PuTTY, this [PuTTY page](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html) instead. Also, don't download just the putty.exe but the **A Windows installer for everything except PuTTYtel** instead.

![USB to console connection](images/USB-console-connect.jpg)

## <a name="3"></a>Boot the Pi

_Time to complete is about 5 minutes._

As soon as you insert the USB to console cable into your computer, the Pi will start to boot. If you are using a keyboard and monitor, plug in your power to boot the Pi.

This next set of instructions assumes you are using the USB to console cable.

1. Use PuTTY to connect to the serial COM port of the USB connection
2. Hit enter to show the login screen
3. Login using the default user: pi and the default password: raspberry. (We will change these shortly.)

**Hint**, putty allows easy copy/paste. To copy from the putty session to the clipboard, just highlight the required text using the mouse. To paste into the putty session from the clipboard, press the _Shift and Insert_ keys.

## <a name="4"></a>Run first boot setup

_Time to complete is about 10 minutes._

Start the configuration software to expand the filesystem, change the password, and change the hostname. Enter the configuration with this command, `sudo raspi-config`.

+ Select and execute **Expand Filesystem**
+ Select and execute **Change User Password**
+ Select and execute **Internationalization Options**
    - **Change Locale** to your locale.
        - Use spacebar to select/deselect
        - Deselect en_GB.UTF-8 UTF-8
        - Select en_US.UTF-8 UTF-8
        - OK
        - Select en_US.UTF-8 UTF-8 as default and then OK
    - **Change Timezone** to UTC.
+ Select **Advanced Options** and select and execute **Hostname**. _Pick a unique and easy to remember hostname. This will be used to connect later._
+ Reboot your system `sudo reboot now`.

**The pi may be shutdown from the command line with, `sudo shutdown now`. Wait about a minute and remove power.**

## <a name="5"></a>Connect to the Internet

_Time to complete is about 40 minutes._

### Ethernet

The easiest way to do this is via Ethernet. Check if you are connected with `ifconfig eth`. From this output, make note of the **inet addr**. This is your Pi's IP address.

### WiFi

If you do not have an Ethernet connection, you will have to set up your wifi.
This procedure assumes you are using a supported wifi USB dongle, are connecting to a simple shared key access point using DHCP, and are not using the GUI desktop to configure your connections. If you are using the full desktop, connect your wifi using the graphical Network Manager. See the [Debian wiki](https://wiki.debian.org/WiFi) for an excellent discussion.

+ Before connecting any USB dongle, shutdown the pi
+ `sudo nano /etc/network/interfaces`
+ Find the section within this file starting with `allow hotplug wlan0`. Replace that section with the following.

```
auto wlan0
allow-hotplug wlan0
iface wlan0 inet dhcp
    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
```
+ `CTRL-o` to save and `CTRL-x` to exit.
+ `sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`
+ Add the following to this file (remember to change replace _your_wifi_identifier_ and _your_wifi_password_ with your real values):

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
+ Try continuing with these setting but make note that you may need to change the _proto_ or _key mgmt_ values depending on your network. See `man wpa_supplicant.conf` for more information.
+ Restart the wifi interface. If your settings are correct, it should automatically connect.

```
sudo ifdown wlan0
sudo ifup wlan0
```
+ Check that you are connected with `ifconfig wlan0`. From this output, make note of the **inet addr**. This is your Pi's IP address. Use `iwconfig wlan0` to see which Access Point you are connected to.


## <a name="6"></a>Update and upgrade

_Time to complete is about 5 minutes. This does not include the amount of time required to upgrade. Upgrading your system may take an hour with a slow connection and many upgrades._

It is important to keep your pi's software up to date. This is commonly done using apt-get. The main keywords to know are _update_, _upgrade_, _install_, and _remove_. So let's make the system current.

+ Update the packages list, `sudo apt-get update`.
+ Upgrade software packages to the current version, `sudo apt-get upgrade`.
+ Relax, this might take a while. Maybe grab lunch.


## <a name="7"></a>Network magic

_Time to complete is about 5 minutes._

This step does nothing more than make it easier to find your Pi on your network. It uses _Zeroconf_, provided by _Avahi_ on Linux, _Bonjour_ on Windows, and included in Apple.

1. Install `sudo apt-get install avahi-daemon`. (**Note,** on recent versions of Raspbian this is already installed and working.)
2. Your system can now be found at hostname.local, where the hostname is that which you entered back in _[Run first boot setup](#4)_.
3. For your Windows machine, download and install [Bonjour Print Services](https://support.apple.com/downloads/Bonjour_for_Windows).


## <a name="8"></a>Connect to Pi using SSH

_Time to complete is about 30 minutes._

SSH is a safe and efficient way to connect to your Pi over the network or the Internet. It is enabled by default but for highest security, I recommend a few configuration changes and installing your own personal keys. This guide assumes you are connecting from Windows or another Linux system. For Windows use [PuTTY](http://www.putty.org/) and for Linux use [OpenSSH](http://www.openssh.com/). It may be necessary to install PuTTY but OpenSSH comes installed on Linux.

* Verify that SSH is enabled, `sudo raspi-config` then Advanced Options and then SSH. (**Note,** on recent versions of Raspbian this is enabled by default.)

### Browser

If you are using the Chrome browser, there is an app that makes SSH easy. Add to Chrome by visiting the [Web Store](https://chrome.google.com/webstore/detail/secure-shell/pnhechapfaindjhompbnflcldabbghjo). Once installed, launch it from the [apps page](chrome://apps/).

+ Select a _New connection_
+ In the free form text box enter a name for your pi connection. I usually give it the same name as my pi.
+ Username is the user to connect to your pi as. Default it _pi_
+ Hostname is  _hostname.local_ or the IP address you made note of earlier.
+ Port is 22
+ Click _Connect_
+ When done `exit`

### Windows

1. Start puTTY
2. Enter _hostname.local_, where hostname is from _Network magic_ into the **Host Name (or IP address)** box.
    - If you are not able to connect with _hostname.local_, try connecting using the IP address instead. If this works, then somehow the network magic is being blocked.
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


## <a name="9"></a>Improving security

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

_Time to complete is about 5 minutes._

There are a few SSHd configuration changes that will improve SSH security. Since SSHd is likely a service you do want to provide and it gives shell access, this is important.

+ Edit the configuration file, `sudo nano /etc/ssh/sshd_config`
+ Change the following:
```
PermitRootLogin no
```
+ Add the following:
```
AllowUsers pi
# Even better if you use a non-default user
```

### Additional SSH configuration

SSH is very important for improved security when connecting to your pi. The [SSH Hints and Advanced](ssh.html) provides guidance to some more advanced SSH settings and methods. Some of these are for improved security and should not be considered optional for an Internet connected device.

## <a name="10"></a>Firewall with iptables

(advanced) At this point, your pi is functional, connected, and reasonably secure. It can be made more secure with iptables which will only allow the types of traffic you permit. See [RPi iptables](rpi_iptables) sections 1-3, start through Basic rule set.


## <a name="11"></a>Connect remotely to the Pi's desktop

_Time to complete is about 20 minutes._

Sometimes, it is necessary to view the desktop interface of a Raspberry Pi from a remote location or without an attached keyboard and monitor. Both VNC and RDP are available to help. VNC and RDP are client-server remote desktop protocols.

Moved to [Connect to the Raspberry Pi using VNC or RDP](rpi_vnc_rdp.html)


## <a name="12"></a>NetworkManager CLI (advanced)

Moved to [RPi NetworkManager CLI](rpi_nmcli.html).


## <a name="13"></a>Add the Adafruit Raspberry Pi repository

(deprecated) See [Adafruit Raspberry Pi repository](rpi_ada_repo.html)

## <a name="14"></a>Install node.js

See [Node.js on Raspberry Pi](rpi_nodejs.html)

(optional) Node.js is a JavaScript runtime environment for developing server-side Web applications. It uses an asynchronous event driven framework that is designed to build scalable network applications. I install it on nearly all of my pi to provide a framework for building user interfaces that can actually do something.

Learn more about node from [Node.js](https://nodejs.org/en/), [Express](http://expressjs.com/en/starter/hello-world.html), [Adafruit](https://learn.adafruit.com/node-embedded-development/events), and [search](https://www.google.com/webhp?q=node.js%20raspberry%20pi).


## <a name="15"></a>Occidentalis

(deprecated) See [Occidentalis](occidentalis.html)


# <a name="Conclusion"></a>Save the image to a file

Now that you have spent all this time getting your Raspberry Pi set up just so, **save it to an image** for easy reuse. You will still have to change things like usernames, passwords, and hostnames.

Instead of writing a file image to the MicroSD, use the same software to read the MicroSD to a file image. Then when you are ready to spin up your next pi, it will be as easy as, well, pie.
