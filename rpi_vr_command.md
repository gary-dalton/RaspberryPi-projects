---
title: RPi Voice Recognition and Command
subtitle: With Jasper and PocketSphinx
author: Gary Dalton
date: 21 February 2016
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html rpi_vr_command.md -o rpi_vr_command.html
tags: rpi, guide, iot, voice, command, jasper, pocketsphinx
---
# Description

Voice recognition and command is one of the modules useful for interacting with robotic systems. There are many voice recognition (VR) systems available but my requirements are:

+ No Internet connection required,
+ Open source license that permits commercial use,
+ Still being developed,
+ Supports Linux,
+ Able to run on the Raspberry Pi,
+ Balance between speed and accuracy

Out of the [possible VR engines](https://en.wikipedia.org/wiki/List_of_speech_recognition_software), the best candidates seem to be PocketSphinx or Julius running under Jasper. I removed Kaldi as a candidate due to its RAM and CPU requirements. Simon was removed as a candidate since it seems very focused on the desktop.

# Next up?

After reading this guide, you may be interested in reading:

# Parts List

+ Raspberry Pi 2
+ 16GB (or larger) class 10 MicroSD card
+ USB microphone or webcam, preferrably listed at [elinux](http://elinux.org/RPi_VerifiedPeripherals)
    - I am using a Logitech Webcam C525
+ Headphones or powered computer speakers
    - In a separate guide, the sound output will be replaced with an amplifier and passive speakers.

# Overview

Start with a Raspberry Pi image. This is an image saved after following the [RPi Initial Setup Guide](rpi_initial_setup.html), [RPi WiFi Access Point Guide](rpi_wifi_ap.html), and [RPi Desktop Mods](rpi_gui_changes.html). The image should not be Lite. If you do not have such an image, start with a Raspbian image and follow the aforementioned guides before returning here. This guide assumes you have an appropriate image and are connected to your running pi.

1. [Setup sound I/O](#1)
2. [Test sound I/O](#2)
3. [Virtual Environments](#3)
4. [Install Jasper](#4)
5. [Install PocketSphinx and requirements](#5)
6. [](#6)
7. [Connect and test.](#7)
10. [Conclusion](#Conclusion).

# Procedures

## <a name="1"></a>Setup sound I/O

Much of the documentation for setting up a USB microphone refer to Raspbian versions prior to Jessie. Since our base distribution is Jessie or newer, those do not apply. This guide follows the stackexchange, [How do I configure my sound for Jasper on Raspbian Jessie?](https://raspberrypi.stackexchange.com/questions/40831/how-do-i-configure-my-sound-for-jasper-on-raspbian-jessie).

+ Power down your pi and insert your USB webcam/microphone
+ Boot the pi and connect to the cli
+ Check the order in which your sound cards have been loaded, `cat /proc/asound/modules`. With output similar to:

        0 snd_bcm2835
        1 snd_usb_audio

+ Create a file, `sudo nano /etc/modprobe.d/alsa-base.conf` with these lines

        # This sets the index value of the cards but doesn't reorder.
        options snd_usb_audio index=0
        options snd_bcm2835 index=1

        # Does the reordering.
        options snd slots=snd-usb-audio,snd-bcm2835

+ Reboot the pi
+ Check the sound card order, `cat /proc/asound/modules`
    - The order should have changed

## <a name="2"></a>Test sound I/O

Settings may be viewed and changed using: amixer, a _command-line mixer for ALSA soundcard driver_ and alsamixer, a _soundcard mixer for ALSA soundcard driver, with ncurses interface_.

+ View settings of microphone, `amixer -c 0`
+ View settings of playback, `amixer -c 1`
+ Adjust settings using `alsamixer -c 0` and `alsamixer -c 1`

Recording is done with arecord, a _command-line sound recorder for ALSA soundcard driver_ and aplay, a _command-line sound player for ALSA soundcard driver_.

+ Record something with (**stop recording with CTRL-c**) `arecord -D plughw:0,0 -f cd test.wav`
+ Play it back with `aplay test.wav`
+ If you receive error messages or no sound record and playback occurs, please troubleshoot before continuing

## <a name="4"></a>Virtual Environments

A Virtual Environment is a tool to keep the dependencies required by different projects in separate places, by creating virtual Python environments for them. Jasper, a python project which helps convert voice recognition into commands, has a number of dependencies that may conflict with the OS installed Linux. A virtual environment will help greatly with this. See [The Hitchhiker's Guide to Python](http://docs.python-guide.org/en/latest/dev/virtualenvs/) and [Virtualenv Documentation](https://virtualenv.readthedocs.org/en/latest/index.html).

+ Install virtualenv, `sudo apt-get install virtualenv`
+ Some basic commands are:
    - `cd my_project_folder`
    - Create the virtual environment, `virtualenv venv`. Only needs to be created once.
    - Activate the environment, `. venv/bin/activate`. The prompt will change.
    - Perform tasks as usual
    - When done, deactivate the environment, `deactivate`    

## <a name="4"></a>Install Jasper

+ Install prerequisites, `sudo apt-get install vim git-core python-dev python-pip bison libasound2-dev libportaudio-dev python-pyaudio`
+ Add to `nano ~/.bash_profile`
    export LD_LIBRARY_PATH="/usr/local/lib"
    source .bashrc
+ Add to `nano ~/.bashrc`
    LD_LIBRARY_PATH="/usr/local/lib"
    export LD_LIBRARY_PATH
    PATH=$PATH:/usr/local/lib/
    export PAT
+ Clone Jasper, `git clone https://github.com/jasperproject/jasper-client.git jasper`
+ `cd jasper`
+ Create virtualenv, `virtualenv venv`
+ Activate the environment, `. venv/bin/activate`
+ Install Jasper requirements, `pip install -r client/requirements.txt`. _This might take a while to compile_

## <a name="5"></a>Install PocketSphinx and requirements

This follows the [Jasper guide](https://jasperproject.github.io/documentation/installation/#installing-dependencies) closely.

+ Install PocketSphinx, `sudo apt-get install pocketsphinx`
+ Installing CMUCLMTK
    - `sudo apt-get install subversion autoconf libtool automake gfortran g++`
    - `svn co https://svn.code.sf.net/p/cmusphinx/code/trunk/cmuclmtk/`
    - `cd cmuclmtk/`
    - `./autogen.sh && make`, Check for errors prior to next step
    - `sudo make install`
    - `cd ~`
+ Installing OpenFST, Phonetisaurus, m2m-aligner and MITLM
    - `sudo su -c "echo 'deb http://ftp.debian.org/debian experimental main contrib non-free' > /etc/apt/sources.list.d/experimental.list"`
    - `sudo apt-get update`
    - `sudo apt-get -t experimental install phonetisaurus m2m-aligner mitlm libfst-tools`
+ Building the Phonetisaurus FST model
    - `wget https://www.dropbox.com/s/kfht75czdwucni1/g014b2b.tgz`
    - `tar -xvf g014b2b.tgz`
    - `cd g014b2b`
    - `./compile-fst.sh`
    - `cd ..`
    - `mv ~/g014b2b ~/phonetisaurus`


# References

+ [virtualenv](https://virtualenv.readthedocs.org/en/latest/userguide.html)
+ [Raspberry Pi 2 – Speech Recognition on device](https://wolfpaulus.com/journal/embedded/raspberrypi2-sr/)
+ [CMUSphinx](http://cmusphinx.sourceforge.net/wiki/raspberrypi)
+ [Jasper install](https://jasperproject.github.io/documentation/installation/)
+ [VoxForge](http://www.voxforge.org/home/downloads)
+ https://jasperproject.github.io/
