---
title: RPi Desktop Mods
subtitle: Changes to the packages and defaults of the full Raspian
author: Gary Dalton
date: 3 February 2016
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html rpi_gui_changes.md -o rpi_gui_changes.html
tags: rpi, desktop, guide, packages
---
# Description

The choice of what software to run on a pi is a personal choice. Rarely will two people make the same decisions. The default full Raspbian image includes many packages I will never use and does not include many I use everyday. I make many of the following changes to my installations but, please note, each addition or removal is optional.

# Overview

A good command to see all that is installed on the system is `dpkg -l | grep ii | more`.

1. [Remove LibreOffice](#1)
2. [Remove Wolfram and Mathematica](#2)
3. [Remove Blue Jay Java IDE](#3)
4. [Remove Greenfoot Java IDE](#4)
5. [Menu icon removal](#5)
6. [Install Eric IDE](#6)
7. [Install Midnight Commander](#7)
8. [Install Arduino IDE](#8)
9. [Install GNU Octave](#9)
10. [Install Coder](#10)
11. [Install Adafruit WebIDE](#11)
12. [Conclusion.](#Conclusion)

# Procedures

## <a name="1"></a>Remove LibreOffice

LibreOffice is a great suite of programs for those using the pi as a traditional office computer. I do not use my pi thusly, therefore; I remove it.

+ `sudo apt-get remove --purge libreoffice*`
+ `sudo apt-get clean`
+ `sudo apt-get autoremove`

## <a name="2"></a>Remove Wolfram and Mathematica

Although Wolfram's Mathematica seems like an excellent programming environment, it is not the one I choose to use. `sudo apt-get remove --purge wolfram-engine`

## <a name="3"></a>Remove Blue Jay Java IDE

A Java Integrated Development Environment that is appropriate for learning at the high school or college level.

+ `sudo apt-get remove --purge bluej`

## <a name="4"></a>Remove Greenfoot Java IDE

A Java Integrated Development Environment that is appropriate for learning at the high school or college level. Let's do this from the GUI. Use a monitor connected to your pi or a VNC connection.

+ Run `gksudo pi-packages`
+ In the search box enter _greenfoot_.
+ Uncheck the greenfoot package.
+ Click _Apply_.
+ Click _Close_.

## <a name="5"></a>Menu icon removal

Sometimes the menu system does not seem to properly remove uninstalled applications. Force removal of menu item icons.

+ From the command line,
    - `cd /usr/share/raspi-ui-overrides/applications`
    - List the items, `ls -al`
    Remove with `sudo rm /appname.desktop`. Replace appname as needed.
+ From the desktop,
    - Run `gksudo pcmanfm`
    - Browse to _/usr/share/raspi-ui-overrides/applications_
    - Select _Greenfoot Java IDE_
    - Delete
    - Close File Manager

## <a name="6"></a>Install Eric IDE

The [Eric Python IDE](http://eric-ide.python-projects.org/index.html). Eric is a full featured Python editor and IDE, written in Python.

+ `sudo apt-get install eric`
+ Start Eric and check your version
+ See the latest version at [Eric downloads](http://sourceforge.net/projects/eric-ide/files/eric6/stable/)
+ I often install the latest version at this point. Download the latest version.
+ `sudo apt-get remove eric`
+ The following packages upon which Eric depends will not be removed. _bicyclerepair bluez libmysqlclient18 libqt4-declarative libqt4-designer libqt4-help libqt4-script libqt4-scripttools libqt4-sql libqt4-sql-mysql libqt4-svg libqt4-test libqtassistantclient4 mysql-common ofono python3-pygments python3-pyqt4 python3-pyqt4.qsci python3-pyqt4.qtsql python3-sip vim-addon-manager_
+ Assuming you downloaded the file into _Downloads_, `cd ~/Downloads`
+ Unarchive the latest version of eric, `tar -xzvf eric*.gz`
+ CD into its folder
+ Install with `sudo python3 ./install.py`
+ Run it from the Programming menu

## <a name="7"></a>Midnight Commander

Midnight Commander is a text-based file manager. It makes it very easy to work with file structure from the command line.

+ `sudo apt-get install mc`
+ Use with `mc`

## <a name="8"></a>Install Arduino IDE

I like to work with Arduinos and other microcontrollers. When running the GUI on the pi, sometimes it is just more convenient to run the IDE from there. At the time of this writing, the latest version of the Arduino IDE is not in the repositories. Instead, this guide follows the instructions from [ShorTie8](https://github.com/ShorTie8/Arduino_IDE). Also see this [forum topic](https://www.raspberrypi.org/forums/viewtopic.php?f=66&t=92662&start=75)

+ Install an old version, `sudo apt-get install arduino`

Go into the desktop and start the IDE. If this covers all of the boards you use and connects well with your Arduino, you do not need to install a newer version.

## <a name="9"></a>Install GNU Octave

GNU Octave is a high-level interpreted language, primarily intended for numerical computations. It provides capabilities for the numerical solution of linear and nonlinear problems, and for performing other numerical experiments. It also provides extensive graphics capabilities for data visualization and manipulation.

+ `sudo apt-get install octave`
+ Add the manual, ` sudo apt-get install octave-info`
+ Edit a local config file to make sure plotting works, `sudo nano ~/.octaverc`
    - Add the line, _graphics_toolkit('gnuplot')_
+ Interested in additional Octave packages? Search with `apt-cache search octave-`

## <a name="10"></a>Install Coder

Coder is a simple way to make web stuff on Raspberry Pi. New coders can craft small projects in HTML, CSS, and Javascript, right from the web browser. From [Coder on Github](https://github.com/googlecreativelab/coder).

+ Node.js and npm must be installed prior to coder. See [RPi Initial Setup Guide - Install node.js](rpi_initial_setup.html#14)
+ `cd`
+ Download, `git clone https://github.com/googlecreativelab/coder.git`
+ `cd coder/coder-apps`
+ Install apps, `./install_common.sh ../coder-base`
    - You may ignore messages like _cp: cannot stat ‘./common//auth/static/media/*’: No such file or directory_
+ `cd ../coder-base`
+ Preinstall bcrypt, `npm install bcrypt`
+ Node install for required packages, `npm install`

### Configure Coder

This will base the configuration on config.js.localhost.

+ Backup original config, `mv config.js config.js.datestamp`
+ Copy localhost config, `cp config.js.localhost config.js`
+ Get your IP, `ifconfig`
+ Edit config, `nano config.js`
    - exports.commonName = "hostname.local";
    - exports.subjectAltName = "DNS:yourIP";

### Use Coder locally

+ `cd ~/coder/coder-base`
+ Start it, `node localserver.js`
+ Test from the pi desktop by openning a browser to **http://127.0.0.1:8080**
+ You should a see page to set your password, enter one
+ Now login and start coding. It will run very slowly from the pi desktop.
+ Stop coder with `CTRL-c`
+ Learn more about usage and projects to try at:
    - [Coder for Raspberry Pi](https://googlecreativelab.github.io/coder/)
    - [Coder Projects](https://googlecreativelab.github.io/coder-projects/)

### Use Coder from the network

+ Some firewall rules must be added to route the connections.
    - `sudo iptables -t nat -A PREROUTING -p tcp -m tcp --dport 80 -j REDIRECT --to-ports 8080`
    - `sudo iptables -t nat -A PREROUTING -p tcp -m tcp --dport 443 -j REDIRECT --to-ports 8081`
+ Update the config, `nano config.js`
    - _exports.listenIP = null;_
+ Test by pointing your browser, not from pi, to **http://hostname.local:8080**

### Start coder as a service

A service runs in the background and is started and monitored by a standard set of commands. A service may also be set to run at boot. (Good guide to [deploy a node app](https://certsimple.com/blog/deploy-node-on-linux))

+ Become root, `sudo -i`
+ Make the folder structure, `mkdir -p /var/www/coderapp`
+ Copy the files, `cp -R /home/pi/coder/coder-base/* /var/www/coderapp`
+ Create and edit the launch script, `nano /var/www/coderapp/start_coder.sh`

```
#!/bin/sh
/usr/local/bin/node /var/www/coderapp/server.js
```

+ Make it executable, `chmod +x /var/www/coderapp/start_coder.sh`
+ Change folder ownership, `chown -R www-data:www-data /var/www/coderapp`
+ Create the service file, `touch /etc/systemd/system/coderapp.service`
+ Edit file, `nano /etc/systemd/system/coderapp.service` thusly

```
[Unit]
Description=coderapp

[Service]
ExecStart=/var/www/coderapp/start_coder.sh
Restart=always
User=www-data
Group=www-data
Environment=PATH=/usr/bin:/usr/local/bin
Environment=NODE_ENV=production
WorkingDirectory=/var/www/coderapp

[Install]
WantedBy=multi-user.target
```

+ Exit root, `exit`
+ Reload system control, `sudo systemctl daemon-reload`
+ Start Coder, `sudo systemctl start coderapp`
+ View log file, `sudo journalctl -u coderapp`
+ (optional) Enable it to run on boot, `sudo systemctl enable coderapp`
+ Test by pointing your browser, not from pi, to **http://hostname.local:8080**

## <a name="11"></a>Install Adafruit WebIDE

**I do not typically install this.**

The Adafruit WebIDE is easy way to run code on your Raspberry Pi or BeagleBone. Just connect your Pi or BeagleBone to your local network, and log on to the WebIDE in your web browser to edit Python, Ruby, JavaScript, or anything and easily send it over to your Pi. The WebiDE includes a terminal, so you can easily send various commands to your Pi right from the browser. Also, your code will be versioned in a local git repository, and pushed remotely out to bitbucket so you can access it from anywhere, and any time.

+ Download and install the WebIDE

```
curl -O http://adafruit-download.s3.amazonaws.com/adafruitwebide-0.3.12-Linux.deb
sudo dpkg -i adafruitwebide-0.3.12-Linux.deb
sudo apt-get -f install
```

+ Once this completes, you should receive a message similar to:

```
**** The Adafruit WebIDE is installed and running! ****
**** Commands: sudo service adafruit-webide.sh {start,stop,restart} ****
**** Navigate to http://_hostname.local to use the WebIDE
```

+ Some good to know options:
    - Redo the bitbucket setup, `http://_hostname.local/setup`
    - Access some configuration options, `http://_hostname.local/config`

### Uninstall

+ `sudo apt-get remove --purge adafruitwebide`
+ `apt-get autoremove`
+ Start Midnight Commander,`sudo mc` to remove these folders:
    - /usr/share/adafruit
    - /home/webide
+ `sudo apt-get autoremove`


### References

+ [Adafruit WebIDE on github](https://github.com/adafruit/Adafruit-WebIDE)
+ [Adafruit WebIDE](https://learn.adafruit.com/webide)


# <a name="Conclusion"></a>Conclusion

Save the image file. After all that configuring it is good to make sure you can duplicate it.

The newly configured pi has many fun and functional packages installed. Explore your pi from the desktop and from the command line. This guide has not informed you how to use any of the packages. For that information use help files, the `man` command and search techniques.
