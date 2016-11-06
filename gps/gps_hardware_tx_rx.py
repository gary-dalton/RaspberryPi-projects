#!/bin/python3
"""
gps_hardware_tx_rx.py: communicate directly with GPS chip.
Provide a library and a test script to interact with the
MediaTek GPS Chipset MT3339.
"""

import datetime, time, os, serial
import microstacknode.hardware.gps.l80gps as l80gps
import rpi_utils


def basic_nmea(gps):
    """
    Prints a variety of basic NMEA sentences
    :return: none
    """

    # Time, date, position, course and speed data. Recommended Minimum Navigation Information.
    print("GPMRC")
    print(gps.get_gprmc())

    # Time, position and fix type data.
    print("GPGGA")
    print(gps.get_gpgga())

    # GPS receiver operating mode, active satellites used in the position solution and DOP values.
    print("GPGSA")
    print(gps.get_gpgsa())

    # The number of GPS satellites in view satellite ID numbers, elevation, azimuth, and SNR values.
    print("GPGSV")
    print(gps.get_gpgsv())

    # The UTC date and time
    print("GPZDA")
    print(get_gpzda(gps))


def gps_output_spy(gps, duration_seconds=10):
    """
    Watches the data output from the serial device
    :param gps:
    :param duration_seconds: number of seconds to loop
    :return: none
    """
    starttime = datetime.datetime.now()
    duration = 0
    while duration < duration_seconds:
        line = gps.device_tx_rx.readline()
        print(str(line, 'utf-8'))
        dif = datetime.datetime.now() - starttime
        duration = dif.seconds


def get_gpzda(gps_object):
    """
    Returns the latest GPZDA message.
    Based upon similar functions from microstacknode.hardware.gps.l80gps
    :param gps_object:
    :return: GPZDA message as a dictionary
    """
    pkt = gps_object.get_nmea_pkt('GPZDA')
    gpzda_dict, checksum = gpzda_as_dict(pkt)
    return gpzda_dict


def gpzda_as_dict(gpzda_str):
    """
    Returns the GPZDAC as a dictionary and the checksum.
    :param gpzda_str:
    :return: gpzda_as_dict($GPZDA,142930.000,03,11,2016,,*5D)
    ({'message_id': '$GPZDA',
        'date_object':  datetime.datetime(2016, 11, 3, 14, 29, 30)
        },
        0C)
    """
    gpzda, checksum = gpzda_str.split('*')
    message_id, thetime, day, month, year, time_zone_hours, time_zone_minutes = gpzda.split(',')
    thedate = datetime.datetime(int(year), int(month), int(day), int(thetime[:2]),
                                int(thetime[2:4]), int(thetime[4:6]), int(thetime[7:]))
    gpzda_dict = {'message_id': message_id,
                  'date_object': thedate}
    return (gpzda_dict, checksum)


def location_logging_test(gps, duration_minutes=5):
    """
    Queries and then starts the built in locus logger. Stops after a
    preset duration and returns the logged data.
    :param gps:
    :param duration_minutes:
    :return: list of dictionaries representing the logged data
    """
    print("Locus query dictionary")
    print(gps.locus_query())

    print("Locus status = " + gps.locus_query()['status'] + ". Status of 0 means logging, 1 means waiting.")
    if gps.locus_query()['status'] == '0':
        gps.locus_stop()
        print("Stopped logging")
        time.sleep(5)
    gps.locus_start()
    print("Started logging")
    time.sleep(5)

    cycles = 0
    while cycles * 0.25 < duration_minutes:
        cycles += 1
        print("Locus status = " + gps.locus_query()['status'] + ".")
        time.sleep(15)

    gps.locus_stop()
    print("Stopped logging")
    time.sleep(5)

    print("Locus status = " + gps.locus_query()['status'] + ". Status of 0 means logging, 1 means waiting.")
    print("Locus logged points = " + gps.locus_query()['number'] + ".")
    locus_data = gps.locus_query_data()

    print("Erasing locus log")
    gps.locus_erase()

    return locus_data


def get_device_gps():
    """
    Use the hardware revision to determine the serial device used by UART GPS.
    See http://www.raspberrypi-spy.co.uk/2012/09/checking-your-raspberry-pi-board-version/
    :return: device string
    """
    pi1 = ['0002','0003','0004','0005','0006','0007','0008','0009','000d','000e','000f','0010','0011','0012','0013']
    pi2 = ['a01041','a21041']
    pi0 = ['900092']
    pi3 = ['a02082','a22082']
    rpi_revision = rpi_utils.get_revision()
    if rpi_revision in pi1 or rpi_revision in pi2 or rpi_revision in pi0:
        # Pi 2 or lower
        device = '/dev/ttyAMA0'
    else:
        # Pi 3 or higher
        device = '/dev/ttyS0'
    return device


def disconnect_serial_gps(gps):
    """
    Remove the python gps serial connection and reattach gpsd to the device.
    :param gps:
    :return: none
    """
    # global gps
    gps.device_tx_rx.close()
    device = get_device_gps()
    cmd = 'sudo gpsd ' + device + ' -n -F /var/run/gpsd.sock'
    os.system(cmd)
    # rpi_utils.run_program(cmd)

    """
    TODO: Close the serial gps connection
    This may have to be done by extending the L80GPS class
    """


def device_available(device):
    """
    Check to see if the named device is available
    :param device: string identifying device to query
    :return: boolean T or F
    """
    try:
        ser = serial.Serial(port=device)
        ser.close()
        return True
    except serial.SerialException:
        return False


def connect_serial_gps():
    """
    Check if the device is available. If its not, disconnect any currently running gpsd using killall.
    Check availability again. If still not available, raise an error. When device is available, connect
    to the L80GPS object.
    If device does not become available after killall on gpsd, another process such as kismet_server may be
    forcing it to remain connected.
    :return: L80GPS object
    """
    device = get_device_gps()
    if not device_available(device):
        cmd = 'sudo killall gpsd'
        os.system(cmd)
        #rpi_utils.run_program(cmd)
        time.sleep(1)
        if not device_available(device):
            raise serial.SerialException('Device busy ' + device + '. Check your processes.')
    gps = l80gps.L80GPS()
    return gps


if __name__ == '__main__':
    cmd = 'sudo killall kismet_server'
    os.system(cmd)
    gps = connect_serial_gps()
    gps.get_gpgsv()
    disconnect_serial_gps(gps)
    del(gps)
    cmd = '/usr/local/bin/kismet_server --daemonize'
    os.system(cmd)
