---
title: Which WiFi USB
subtitle: Discussion on choice
author: Gary Dalton
date: 30 January 2016
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html rpi_which_wifi_usb.md -o rpi_which_wifi_usb.html
tags: rpi, howto, portal, wifi, hotspot
---

# Which WiFi USB?

## Discussion on choice for the Raspberry Pi

# Overview

Which wifi USB adapter makes the best purchase? The cheapest? The highest rated? The one mentioned in all the tutorials? If only it were that easy. Sections that require special caution are denoted.

1. [Pi compatible.](#1)
2. [Define your needs.](#2)
3. [Range, power suppply, and antenna.](#3)
4. [As an access point.](#4) (caution)
5. [Change a MAC address.](#5)(caution)
6. [Monitor and inject](#6)(caution)
7. [Commands for information.](#7)
8. [Using two wifi adapters.](#8)(caution)
9. [Solution to wlan0 and wlan1 confusion.](#9)
10. [Test the solution.](#10)
11. [Conclusion](#Conclusion)
12. [References](#References)

# Discussion

## <a name="1"></a>Pi compatible

Make certain that whichever adapter you decide upon that it is compatible with the Raspberry Pi. This is not always easy to determine as the compatibility depends more on the maker of the chipset used in the adapter and not on the brand name logoed on the package. This [eLinux RPi USB Wi-Fi Adapters page](http://elinux.org/RPi_USB_Wi-Fi_Adapters) is excellent for knowing what will work and what probably will not work.

The adapters I have used in these guides are:

+ [Edimax EW-7811Un](http://www.amazon.com/Edimax-EW-7811Un-150Mbps-Raspberry-Supports/dp/B003MTTJOY/ref=pd_bxgy_147_2)
+ [CanaKit Raspberry Pi WiFi Wireless Adapter](http://www.amazon.com/CanaKit-Raspberry-Wireless-Adapter-Dongle/dp/B00GFAN498)
+ [TP-Link WN722N](https://smile.amazon.com/dp/B002SZEOLG)

## <a name="2"></a>Define your needs

Before deciding on the right adapter, define your needs and requirements.

+ Do you want it powered directly from the pi or is a powered hub OK?
+ How much range do you require?
+ Do you need to attach an external antenna?
+ Are you going to use it as an access point?
+ Do you need to change its MAC address?
+ Do you need monitor mode?
+ Do you need to inject?

If you have some of these needs, some of them may be answered from the [eLinux page](http://elinux.org/RPi_USB_Wi-Fi_Adapters) or from the manufacturers documentation. Others, you may have to dig for an answer but next I will share my experiences.

## <a name="3"></a>Range, power supply, and antenna

For the most part the issues of range, power supply, and antenna can be determined from eLinux and the documentation. A rule of thumb, however; suggests that larger units with better range and external antennae will require a powered USB hub.

## <a name="4"></a>As an access point

**(caution)** So you want to use your pi as an access point? Take a bit more care in your wifi selection. The [RPi WiFi Access Point Guide](rpi_wifi_ap.html) uses an Edimax adapter. The Edimax adapter is based on the RealTek RTL8188CUS chipset.

This chipset does not work out-of-the-box as an access point with _hostpad_. Instead, downloading or compiling a special hostapd is required to make this chipset work. The guides do assume this adapter though.

## <a name="5"></a>Change a MAC address

**(caution)** The RealTek RTL8188CUS chipset does not support modifying the MAC address. If changing the MAC on your wifi is important, try an adapter based on a Ralink chipset. In fact, the Ralink chipset should be your choice if you need to monitor or inject as well.

Notice that the second wifi card in the [Raspberry Tor Guide](rpi_tor.html) has a Ralink chipset.

## <a name="6"></a>Monitor and inject

**(caution)** If you need to do advanced reconnaissance or security assessment, you will need an adapter capable of monitor and inject modes. Most wifi chipsets do not support this. The _TP-Link WN722N_ supports the full range of wifi modes and is a highly recommended adapter.

I use this adapter in the [WalkingPi](walkingpi.html) and [Kismet on Raspberry Pi](rpi3_kismet.html) guides. The _TP-Link WN722N_ also works well with Kali Linux and aircrack-ng.

How to determine if your wifi is monitor and inject capable. These commands are testing the wlan0 wifi.

+ `sudo ifconfig wlan0 down`
+ `sudo iwconfig wlan0 mode monitor`
    + Error message indicates the monitor mode is not supported

If monitor mode seems supported, install aircrack-ng for further tests.

+ `sudo apt-get install aircrack-ng`
+ `sudo airodump-ng wlan0`
    + If monitor mode is supported, then found wifis will display
+ `sudo aireplay-ng -9 wlan0`
    + Returns result which includes _Injection is working!_

For more injection testing see [Injection test](https://www.aircrack-ng.org/doku.php?id=injection_test).

## <a name="7"></a>Commands for information

There are some basic commands to determine information about your USB devices.

+ List the devices, `lsusb`.
    - Shows a table with chipset manufacturer and model.
+ Show the MAC address of a device, `macchanger -s wlan0`.
    - Lists the current and permanent MAC address of the device.
+ Verbose list of devices, `lsusb -vv`.

## <a name="8"></a>Using two wifi adapters

**(caution)** In order to build a wifi to wifi access point, two wifi adapters are needed. If these adapters are built using the same chipset or have the same capabilities then you should experience no problems.

If wifi adapters with different capabilities are used, you may need to do some extra work. In the [RPi WiFi Access Point Guide](rpi_wifi_ap.html), wlan1 is setup as the access point server. That guide presumes that wlan0 is a RealTek RTL8188CUS chipset adapter and installs a specially compiled hostapd. The guide also sets the _/etc/hostapd/hostapd.conf_ to use _driver=rtl871xdrv_. The guide uses two of the same adapter and therefore avoids problems.

Moving to the [Raspberry Tor Guide](rpi_tor.html), we start with the completed access point but now want to change the MAC address on wlan1. This is not possible with the RealTek chipset. In order to change the MAC address, the wlan1 adapter is changed to a Ralink chipset. This solves the problem of MAC address but introduces the problem of which adapter is assigned by udev to the wlan0 and wlan1 identifiers.

## <a name="9"></a>Solution to wlan0 and wlan1 confusion

To ensure consistency on wlan0 and wlan1, a persistence rule must be generated for udev.

+ Boot you pi with only the Ralink chipset adapter inserted.
+ Edit the file, `sudo nano /lib/udev/rules.d/75-persistent-net-generator.rules`.

```
CHANGE
# device name whitelist
KERNEL!="ath*|msh*|ra*|sta*|ctc*|lcs*|hsi*", \
                                       GOTO="persistent_net_generator_end"

TO
# device name whitelist
KERNEL!="ath*|wlan*[0-9]|msh*|ra*|sta*|ctc*|lcs*|hsi*", \
                                        GOTO="persistent_net_generator_end"
```

+ Reboot.
+ Check the file, `cat /etc/udev/rules.d/70-persistent-net.rules` to make certain a USB device has been assigned to wlan0.
+ Shutdown.
+ Insert the RealTek chipset device.
+ Boot the pi.
+ Check the file, `cat /etc/udev/rules.d/70-persistent-net.rules` to make certain a USB device has been assigned to wlan0 and wlan1.
+ Understand that these specific devices, identified by there hardcode MAC, are tied to the interface. If you later need to replace an adapter, revisit the process of setting persistent rules.

* [Solution source](https://www.raspberrypi.org/forums/viewtopic.php?f=29&t=55527)

## <a name="10"></a>Test the solution

The easiest way to check for persistence is to boot your pi with the wlan0 adapter missing. The `ifconfig` will not display wlan0 but only wlan1.

Also test this by changing the MAC on the Ralink chipset adapter, wlan0.

+ `sudo service network-manager stop`
+ `sudo macchanger -e wlan0`
+ A successful MAC change will not contain the phrase _Network driver didn't actually change to the new MAC!!_
+ `sudo service network-manager start`

# <a name="Conclusion"></a>Conclusion

The gist of this discussion is that one should choose the wifi adapter with care and foresight.

# <a name="References"></a>References

+ [Injection test](https://www.aircrack-ng.org/doku.php?id=injection_test)
