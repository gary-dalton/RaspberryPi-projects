#!/bin/python
# wpa_sup_list.py
# Runs and parses 'wpa_cli -i wlan0 scan' and 'wpa_cli -i wlan0 scan_result'
from subprocess import Popen, PIPE
import errno
import logging
import time
import shlex

def run_command(the_call):
    """
    Runs a program with arguments (the_call = 'wpa_cli -i wlan0 scan_result')
    Returns output if successful and logs error if not.
    """

    the_cmd = shlex.split(the_call)
    executable = the_cmd[0]
    executable_args = the_cmd[1:]

    try:
        proc = Popen(([executable] + executable_args), stdout=PIPE, stderr=PIPE)
        response = proc.communicate()
        response_stdout, response_stderr = response[0], response[1]
    except OSError as e:
        if e.errno == errno.ENOENT:
            logging.debug('Unable to locate \'%s\'.' % executable)
        else:
            logging.error('O/S error when trying to run \'%s\': "%s"' % (executable, str(e)))
    except ValueError as e:
        logging.debug("Value error occured.")
    else:
        if proc.wait() != 0:
            logging.debug('Executable \'%s\' returned with the error: "%s"' % (executable, response_stderr))
            return response
        else:
            logging.debug('Executable \'%s\' returned successfully. First line of response was "%s"' % (
            executable, response_stdout.split('\n')[0]))
            return response_stdout

def get_networks(iface, retry=10):
    """
    Grab a list of wireless networks within range, and return a list of dicts describing them.
    """
    while retry > 0:
        if 'OK' in run_command('wpa_cli -i %s scan' % iface):
            networks = []
            r = run_command('wpa_cli -i %s scan_result' % iface).strip()
            if 'bssid' in r and len(r.split('\n')) > 1:
                for line in r.split("\n")[1:]:
                    b, fr, s, f = line.split()[:4]
                    ss = " ".join(line.split()[4:])
                    networks.append({'bssid': b, 'freq': fr, 'sig': s, 'ssid': ss, 'flag': f})
                return networks
        retry -= 1
        logging.debug('Unable to retrieve networks, retrying')
        time.sleep(0.5)
    logging.error('Failed to list networks')

'''
iface = 'wlan0'
networks = get_networks(iface)
if networks:
    networks = sorted(networks, key=lambda k: k['sig'])
    for network in networks:
        print(network)
        logging.info('SSID:%s, Signal:%s, BSSID:%s, Security:%s, Freq:%s', network['ssid'], network['sig'], network['bssid'], network['flag'], network['freq'])
else:
    logging.info('No wireless networks detected')
'''