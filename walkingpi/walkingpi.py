#!/bin/python
# Walkingpi main script
# Added Collection mode  and detail record toggle buttons

import RPi.GPIO as GPIO
import time
import os
import datetime
import logging
import wpa_sup_list
from threading import Timer

# Configure logging
logfilename='/home/pi/Downloads/walkingpi.log'
logformat = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logformat, filename = logfilename, level=logging.DEBUG)

# Use the Board Pin numbers
GPIO.setmode(GPIO.BOARD)

# Pins
BUTTON_SHUTDOWN = 12
BUTTON_COLLECTION = 16
BUTTON_RECORD = 18

IFACE = 'wlan0'
WIFI_SCAN_DELAY = 15
INTERFACES_CONFIG = '/etc/network/interfaces.base'

collection_flag = True
record_flag = False
recording = False

# Setup the Pin with Internal pullups enabled and PIN in reading mode.
GPIO.setup(BUTTON_SHUTDOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_COLLECTION, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_RECORD, GPIO.IN, pull_up_down=GPIO.PUD_UP)

##
def shutdown(channel): # Change to lowercase function name
    # Modify function to require the shutdown button to be pressed and held
    # for at least 2 seconds before shutting down.
    GPIO.remove_event_detect(channel)
    pressed_time = datetime.datetime.now()
    while not GPIO.input(channel):
        time.sleep(.5)
    dif = datetime.datetime.now() - pressed_time
    pressed_time = dif.seconds
    logging.debug('Pressed time = %s', pressed_time)
    if pressed_time > 2:
        pass
        #os.system("sudo shutdown -h now")
    GPIO.add_event_detect(channel, GPIO.FALLING, callback=shutdown, bouncetime=200)
##

##
def collection_toggle(channel):
    global collection_flag

    collection_flag = ~collection_flag
    if collection_flag:
        wpa_sup_list.down_iface(IFACE)
        wpa_sup_list.up_iface(IFACE)
        collection_timer.start()
    else:
        collection_timer.stop()
        wpa_sup_list.up_iface(IFACE, INTERFACES_CONFIG)
##

##
def record_toggle(channel):
    global record_flag
    record_flag = ~record_flag
##

##
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        #self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
##

##
def scan_log_wifi(iface):
    networks = wpa_sup_list.get_networks(iface)
    if networks:
        networks = sorted(networks, key=lambda k: k['sig'])
        for network in networks:
            print(network)
            logging.info('SSID:%s, Signal:%s, BSSID:%s, Security:%s, Freq:%s', network['ssid'], network['sig'], network['bssid'], network['flag'], network['freq'])
    else:
        logging.info('No wireless networks detected')
##

# Add button pressed event detects
GPIO.add_event_detect(BUTTON_SHUTDOWN, GPIO.FALLING, callback=shutdown, bouncetime=2000)
GPIO.add_event_detect(BUTTON_COLLECTION, GPIO.FALLING, callback=collection_toggle, bouncetime=2000)
GPIO.add_event_detect(BUTTON_RECORD, GPIO.FALLING, callback=record_toggle, bouncetime=2000)

# Main loop
collection_timer = RepeatedTimer(WIFI_SCAN_DELAY, scan_log_wifi, IFACE)

# Start state
wpa_sup_list.down_iface(IFACE)
wpa_sup_list.up_iface(IFACE)
collection_timer.start()

while True:
    if collection_flag:
        # Collect data - fill in later
        # Initiate GPS
        # Log GPS
        # Scan and log wifi
            # handled by collection_toggle()
        # Interval photos
        if record_flag > recording:
            # Stop interval photos
            # Start detail recording
            record_flag = False
            pass
        if record_flag & recording:
            # Stop detail recording
            # Start interval photos
            record_flag = False
            pass
        pass
    else:
        # Stop collection
            # handled by collection_toggle()
        # Connect to home base
        # Transfer data - fill in later
        # Notify of completion
        pass








'''
from time import sleep

def hello(name):
    print "Hello %s!" % name

print "starting..."
rt = RepeatedTimer(1, hello, "World") # it auto-starts, no need of rt.start()
try:
    sleep(5) # your long-running job goes here...
finally:
    rt.stop() # better in a try/finally block to make sure the program ends!

'''