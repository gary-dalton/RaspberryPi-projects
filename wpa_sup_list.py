from subprocess import Popen, PIPE
import errno
import logging
import time
import shlex

def run_command(the_call):
    """
    Runs a program with arguments (e.g. rcmd="ls -lh /var/www")
    Returns output if successful, or None and logs error if not.
    """

    cmd = shlex.split(the_call)
    executable = cmd[0]
    executable_options = cmd[1:]

    try:
        proc = Popen(([executable] + executable_options), stdout=PIPE, stderr=PIPE)
        response = proc.communicate()
        response_stdout, response_stderr = response[0], response[1]
    except OSError as e:
        if e.errno == errno.ENOENT:
            logging.debug("Unable to locate '%s' program. Is it in your path?" % executable)
        else:
            logging.error("O/S error occured when trying to run '%s': \"%s\"" % (executable, str(e)))
    except ValueError as e:
        logging.debug("Value error occured. Check your parameters.")
    else:
        if proc.wait() != 0:
            logging.debug("Executable '%s' returned with the error: \"%s\"" % (executable, response_stderr))
            return response
        else:
            logging.debug("Executable '%s' returned successfully. First line of response was \"%s\"" % (
            executable, response_stdout.split('\n')[0]))
            return response_stdout

def get_networks(iface, retry=10):
    """
    Grab a list of wireless networks within range, and return a list of dicts describing them.
    """
    while retry > 0:
        if "OK" in run_command("wpa_cli -i %s scan" % iface):
            networks = []
            r = run_command("wpa_cli -i %s scan_result" % iface).strip()
            if "bssid" in r and len(r.split("\n")) > 1:
                for line in r.split("\n")[1:]:
                    b, fr, s, f = line.split()[:4]
                    ss = " ".join(line.split()[4:])  # Hmm, dirty
                    networks.append({"bssid": b, "freq": fr, "sig": s, "ssid": ss, "flag": f})
                return networks
        retry -= 1
        logging.debug("Couldn't retrieve networks, retrying")
        time.sleep(0.5)
    logging.error("Failed to list networks")

#wpa_cli -i wlan0 scan
#wpa_cli -i wlan0 scan_result