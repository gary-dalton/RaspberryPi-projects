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
# RPi Desktop Mods

## Changes to the packages and defaults of the full Raspian

# Description

The choice of what software to run on a pi is a personal choice. Rarely will two people make the same decisions. The default full Raspbian image includes many packages I will never use and does not include many I use everyday. I make many of the following changes to my installations but, please note, each addition or removal is optional.

# Overview

A good command to see all that is installed on the system is `dpkg -l | grep ii | more`.

1. [Remove LibreOffice](#1)
2. [Remove Wolfram and Mathematica](#2)
3. [Remove Blue Jay Java IDE](#3)
4. [Remove Greenfoot Java IDE](#4)
5. [Install Eric IDE](#5)
6. [Install Adafruit WebIDE](#6)
7. [Install Arduino IDE](#7)
8. [Install GNU Octave](#8)
10. [Conclusion.](#Conclusion)

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
+ Sometimes the menu system does not seem to properly remove uninstalled applications. Force removal of menu item, `sudo rm /usr/share/raspi-ui-overrides/applications/bluej.desktop`

## <a name="4"></a>Remove Greenfoot Java IDE

A Java Integrated Development Environment that is appropriate for learning at the high school or college level. Let's do this from the GUI. Use a monitor connected to your pi or a VNC connection.

+ Run `gksudo pi-packages`
+ In the search box enter _greenfoot_.
+ Uncheck the greenfoot package.
+ Click _Apply_.
+ Force removal of menu item
    - Run `gksudo pcmanfm`
    - Browse to _/usr/share/raspi-ui-overrides/applications_
    - Select _Greenfoot Java IDE_
    - Delete
    - Close File Manager

## <a name="5"></a>Install Eric IDE

The [Eric Python IDE](http://eric-ide.python-projects.org/index.html). Eric is a full featured Python editor and IDE, written in Python.

+ `sudo apt-get install eric`
+ Start Eric and check your version
+ See the latest version at [Eric downloads](http://sourceforge.net/projects/eric-ide/files/eric6/stable/)
+ I often install the latest version at this point. Download the latest version.
+ `sudo apt-get remove eric`
+ The following packages upon which Eric depends will not be removed. _bicyclerepair bluez libmysqlclient18 libqt4-declarative libqt4-designer libqt4-help libqt4-script libqt4-scripttools libqt4-sql libqt4-sql-mysql libqt4-svg libqt4-test libqtassistantclient4 mysql-common ofono python3-pygments python3-pyqt4 python3-pyqt4.qsci python3-pyqt4.qtsql python3-sip vim-addon-manager_
+ Unarchive the latest version of eric
+ CD into its folder
+ Install with `sudo python3 ./install.py`
+ Run it from the Programming menu

## <a name="6"></a>Midnight Commander

Midnight Commander is a text-based file manager. It makes it very easy to work with file structure from the command line.

+ `sudo apt-get install mc`
+ Use with `mc`

## <a name="7"></a>Install Arduino IDE

I like to work with Arduinos and other microcontrollers. When running the GUI on the pi, sometimes it is just more convenient to run the IDE from there. At the time of this writing, the latest version of the Arduino IDE is not in the repositories. Instead, this guide follows the instructions from [ShorTie8](https://github.com/ShorTie8/Arduino_IDE). Also see this [forum topic](https://www.raspberrypi.org/forums/viewtopic.php?f=66&t=92662&start=75)

+ Install an old version, `sudo apt-get install arduino`

Go into the desktop and start the IDE. If this covers all of the boards you use and connects well with your Arduino, you do not need to install a newer version.

## <a name="8"></a>Install GNU Octave

GNU Octave is a high-level interpreted language, primarily intended for numerical computations. It provides capabilities for the numerical solution of linear and nonlinear problems, and for performing other numerical experiments. It also provides extensive graphics capabilities for data visualization and manipulation.

+ `sudo apt-get install octave`
+ Interested in additional Octave packages? Search with `apt-cache search octave-`

## <a name="9"></a>Install Adafruit WebIDE

**I do not typically install this**
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


### References

+ [Adafruit WebIDE on github](https://github.com/adafruit/Adafruit-WebIDE)
+ [Adafruit WebIDE](https://learn.adafruit.com/webide)


# <a name="Conclusion"></a>Conclusion

Save the image file. After all that configuring it is good to make sure you can duplicate it.

The Tor Browser is recommended in addition to using the Raspberry Tor. It has a number of tweaks that improve anonymity. If you like this guide and using Tor, consider supporting the Tor Project. The easiest way to show your support is by setting up a relay. The Tor Project also [accepts donations](https://www.torproject.org/donate/donate.html)

After doing the research needed to make this guide work, I am planning on setting most of my servers as relays or bridges. I would really like to set up an exit node but that requires a bit more effort.
