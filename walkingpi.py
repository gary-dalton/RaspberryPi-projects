#!/bin/python
# Walkingpi main script
# Added Collection mode  and detail record toggle buttons

import RPi.GPIO as GPIO
import time
import os
import datetime
import logging

# Configure logging
logfilename='/home/pi/Downloads/walkingpi.log'
logformat = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logformat, filename = logfilename, level=logging.DEBUG)

# Use the Board Pin numbers
GPIO.setmode(GPIO.BOARD)

# Pins
BUTTON_SHUTDOWN = 11
BUTTON_COLLECTION = 13
BUTTON_RECORD = 15

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
    if pressed_time > 2:
        os.system("sudo shutdown -h now")
    GPIO.add_event_detect(channel, GPIO.FALLING, callback=shutdown, bouncetime=200)
##

##
def collection_toggle():
    global collection_flag
    collection_flag = ~collection_flag
##

##
def record_toggle():
    global record_flag
    record_flag = ~record_flag
##

# Add button pressed event detects
GPIO.add_event_detect(BUTTON_SHUTDOWN, GPIO.FALLING, callback=shutdown, bouncetime=2000)
GPIO.add_event_detect(BUTTON_COLLECTION, GPIO.FALLING, callback=collection_toggle, bouncetime=2000)
GPIO.add_event_detect(BUTTON_RECORD, GPIO.FALLING, callback=record_toggle, bouncetime=2000)

# Main loop
while True:
    if collection_flag:
        # Collect data - fill in later
        # Initiate GPS
        # Log GPS
        # Scan and lof wifi
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
        # Connect to home base
        # Transfer data - fill in later
        # Notify of completion
        pass







from threading import Timer
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

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
