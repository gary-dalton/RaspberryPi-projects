---
title: Basic GPIO on the Raspberry Pi
subtitle: I/O, Interrupts, and notifications
author: Gary Dalton
date: 15 May 2016
license: Creative Commons BY-SA
github:
  user: gary-dalton
  repo: RaspberryPi-projects
  branch: "gh-pages"
framework: minimal
css: stylesheets/stylesheet.css
pandoc: pandoc -t html5 --standalone --section-divs --template=template_github.html rpi_gpio.md -o rpi_gpio.html
tags: raspberrypi, guide, gpio, aws, rtc
---
[Home](index.html)

# Description

This guide demonstrates basic use of Raspberry Pi GPIO. Our inputs will be a simple push button and temperature data read from an I2C DS3231 device (RTC). Our outputs will be LEDs and an Amazon Web Services - Simple Notification Services (SNS) endpoint.

# Parts List

+ Raspberry Pi 2
+ MicroSD card
+ [DS3231M RTC Module](http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=ds3231)
+ [Pushbutton](http://www.amazon.com/s/ref=sr_nr_n_1?fst=as%3Aoff&rh=n%3A5739464011%2Ck%3Apushbutton&keywords=pushbutton&ie=UTF8&qid=1463408857&rnid=2941120011)
+ [LEDs](http://www.amazon.com/s/ref=sr_nr_n_2?fst=as%3Aoff&rh=n%3A16310091%2Cn%3A306760011%2Ck%3Aled&keywords=led&ie=UTF8&qid=1463409024&rnid=16310161)

# Overview

This guide assumes you have an installed and functioning Raspberry Pi with an installed RTC. If not please see the [RPi Initial Setup Guide](rpi_initial_setup.html) and [RTC DS3231 on the Raspberry Pi](rpi_RTCds3231). It also assumes you are using SNS for notifications. If you do not have SNS, that portion may be easily skipped. Programs will be written in Python.

The steps to follow are:

1. [Using GPIO for input and output](#1)
2. [Using a GPIO interrupt](#2)
3. [LEDs](#3)
4. [Amazon Web Services - Simple Notification Services](#4)
5. [Full example](#5)

6. [Connect with VNC](#6)
7. [Personalize your desktop](#7)
8. [Conclusion](#Conclusion)
9. [References](#References)

## <a name="1"></a>Using GPIO for input and output

**WARNING: The pi must be powered down whenever you are connecting or disconnecting pins.**

Python's RPi.GPIO library supports using the GPIO pins on the pi. This library is installed by default on recent versions of Raspbian. It is a good idea to review the [documentation for this library](https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/).

The layout of the pins is shown below. Note that there are two numbering schemes and for programming you MUST choose either BOARD or BCM.

![Pi GPIO pinouts](images/pi_gpio.jpg)

To use a channel (pin), you must set it up. Output channels have fewer options than input channels.

### Basic channel setup

In the python example below, _channel_ should be replaced by the appropriate pin number.

```
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
# or
# GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Output with an optional initial GPIO.HIGH
GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH)

# Multiple channels with 1 call (Use your own pin numbers)
channel_list = [31,32,33]
GPIO.setup(channel_list, GPIO.OUT)

# Inputs with pull-up resistors
GPIO.setup(channel_list, GPIO.IN, pull_up_down=GPIO.PUD_UP

```

Pull-up or pull-down resistors are needed to prevent the input from floating. Instead of using a physical resistor, this may by set as port of the GPIO.

## <a name="2"></a>Using a GPIO interrupt

Interrupts are used to detect and act upon events. For example, you may wish to run a loop until a button is pressed. If the loop runs for 5 seconds, checking for the button press in the loop, called polling, would probably miss the button press. Instead, use event detection to capture the button press and check that status in the loop. Here is an example:

```
import RPi.GPIO as GPIO
import smbus
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(channel, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(channel, GPIO.RISING, bouncetime=200)

while not GPIO.event_detected(BUTTON):
    Celsius = getTemp(address)
    Fahrenheit = 9.0/5.0 * Celsius + 32
    print Fahrenheit, "*F /", Celsius, "*C"
    time.sleep(10)
```

## <a name="3"></a>LEDs

Turning a light on with a circuit is a simple and effective way to check functioning and often leads directly to a product. LEDs have an anode and a cathode, meaning that current can only flow in one direction. LEDs also have very little resistance, meaning that they should be placed in series with a resistor in most circuits. LEDs have different specifications but a good resistor to place in series is 330 ohms.

On LEDs the longer lead is the anode and should be connected to the positive side of the circuit. If you don't recall and an easy way to check the functioning and color of an LED is to use a 3 volt button battery.

+ View this[ Sparkfun LED Tutorial](https://learn.sparkfun.com/tutorials/light-emitting-diodes-leds)

## <a name="4"></a>Amazon Web Services - Simple Notification Services

Amazon SNS is a fast, flexible, fully managed publication-subscription messaging service. Use it as a cloud-based mobile app notification service to send push notifications, email, and SMS messages; or as an enterprise-messaging infrastructure.

This guide will not go into the details of SNS but assume that you have a functioning subscribed endpoint. Instead this guide will use boto3 to publish a message. The purpose of this is to demonstrate the connection of the virtual with the physical with the remote in the next section.

+ Install boto3, `sudo pip install boto3`
+ Enter your credentials into the configuration as shown in the [Boto3 Quickstart](https://boto3.readthedocs.io/en/latest/guide/quickstart.html)
+ Publish a message as shown:

```
import boto3
client =  boto3.client('sns')

# use your endpoint from Amazon
endpoint = 'arn:aws:sns:us-east-1:234567890:Alarms'

#Send alert via SNS
response = client.publish(
    TopicArn=endpoint,
    Message='My Alert Message!')
```

Those who have subscribed with an SMS phone number with receive and SMS text message. There are many other possible notifications that may be received.

## <a name="5"></a>Full example

![the circuit](images/clk_temp_lites_bb.png)

The DS3231M has an operating temperature range of -45 C to 85 C. The RTC stores its temperature data in two registers. The upper 8 bits, representing an integer, are stored in two's complement form in register 11h. The lower 2 bits, representing the fractional portion, are in register 12h.

The RTC converts the temperature (updates the registers) every 64s. The maximum allowed by the chip is once every second. A convert may be forced by setting the CONV bit of the Control register (0Eh) to 1. Once the convert is completed, the CONV is set to 0 and the temperature may be read.

```
## python
import smbus
import os
import RPi.GPIO as GPIO
import time
import random
import boto3

# Pins
LED_FLASH_LOW = 40
LED_GREEN = 38
LED_YELLOW = 37
LED_RED = 35
LED_FLASH_HIGH = 36
BUTTON = 33
LDR = 31

# Release RTC 3231
os.system('sudo rmmod rtc_ds1307')

# Setup RTC 3231 for temperature reading
bus = smbus.SMBus(1)
address = 0x68

# Force a conversion and wait until it completes
def convTemp(address):
    byte_control = bus.read_byte_data(address,0x0E)
    if byte_control & 32 == 0:
        bus.write_byte_data(address, 0x0E, byte_control|32)
    byte_control = bus.read_byte_data(address,0x0E)
	while byte_control & 32 != 0:
		time.sleep(1)
		byte_control = bus.read_byte_data(address,0x0E)
    return True

# Get temperature in degrees C
def getTemp(address):
    convTemp(address)
    byte_tmsb = bus.read_byte_data(address,0x11)
    byte_tlsb = bus.read_byte_data(address,0x12)
    tinteger = (byte_tmsb & 0x7f) + ((byte_tmsb & 0x80) >> 7) * -2**8
    tdecimal = (byte_tmsb >> 7) * 2**(-1) + ((byte_tmsb & 0x40) >> 6) * 2**(-2)
    return tinteger + tdecimal

# Setup the AWS SNS client
client =  boto3.client('sns')
endpoint = 'arn:aws:sns:us-east-1:234567890:Alarm'

##
#Work with LEDs
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

leds = [LED_FLASH_LOW,LED_GREEN,LED_YELLOW,LED_RED,LED_FLASH_HIGH]

# Temp in Fahrenheit
ALARM_LOW = 70
ALARM_OK = 80
ALARM_CAUTION = 90
ALARM_HIGH = 100

GPIO.setup(leds, GPIO.OUT)

#Use button to stop monitoring temperature
GPIO.setup(BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(BUTTON, GPIO.RISING, bouncetime=200)

counter = 0
alert_low_clear = False
alert_high_clear = False
alert_critical_clear = False

while not GPIO.event_detected(BUTTON) and counter < 100:
    Celsius = getTemp(address)
    Fahrenheit = 9.0/5.0 * Celsius + 32
    print Fahrenheit, "*F /", Celsius, "*C"
    temperature = Fahrenheit
    if temperature < ALARM_LOW:
        GPIO.output(leds, GPIO.LOW)
        GPIO.output(LED_FLASH_LOW, GPIO.HIGH)
        if alert_low_clear:
            #Send notification via AWS SNS
            response = client.publish(
                TopicArn=endpoint,
                Message='Temperature is low!')
            alert_low_clear = False
    elif temperature < ALARM_OK:
        GPIO.output(leds, GPIO.LOW)
        GPIO.output(LED_GREEN, GPIO.HIGH)
        alert_low_clear = False
        alert_high_clear = False
        alert_critical_clear = False
    elif temperature < ALARM_CAUTION:
        GPIO.output(leds, GPIO.LOW)
        GPIO.output(LED_YELLOW, GPIO.HIGH)
    elif temperature < ALARM_HIGH:
        GPIO.output(leds, GPIO.LOW)
        GPIO.output(LED_RED, GPIO.HIGH)
        if alert_high_clear:
            #Send notification via AWS SNS
            response = client.publish(
                TopicArn=endpoint,
                Message='Temperature Alert!')
            alert_high_clear = False
    else:
        GPIO.output(leds, GPIO.LOW)
        GPIO.output([LED_RED, LED_FLASH_HIGH], GPIO.HIGH)
        if alert_critical_clear:
            #Send notification via AWS SNS
            response = client.publish(
                TopicArn=endpoint,
                Message='Temperature Critical! Meltdown Imminent')
            alert_critical_clear = False

	counter = counter + 1
	time.sleep(5)

#Run cleanup routines
print "LEDs off"
GPIO.output(leds, GPIO.LOW)
GPIO.cleanup()
os.system('sudo modprobe rtc_ds1307')
```

## <a name="Conclusion"></a>Conclusion

Your pi now as a battery backed, accurate RTC installed and working. This allows quality data-logging and other applications. Additionally, the temperature data from the RTC is available for your use.

## <a name="References"></a>References

+ [RTC DS3231 on the Raspberry Pi](rpi_RTCds3231)
+ [RPi.GPIO module basics](https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/)
+ [Boto3 SNS](https://boto3.readthedocs.io/en/latest/reference/services/sns.html)
+ [Adding a Shutdown Button to the Raspberry Pi B+](https://www.element14.com/community/docs/DOC-78055/l/adding-a-shutdown-button-to-the-raspberry-pi-b)
