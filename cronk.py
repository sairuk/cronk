#!/usr/bin/python3
#
# hacky cron wannabe
# 
#
import os
import subprocess
import time
from config import ConfigFile
import modules.pycron as pycron

ui = False
verbose = False
clock = 60


def log(s):
    if verbose:
        print(s)

def main():
    # Config
    configfile = ConfigFile()
    procs = {}

    # main loop
    try:
        while True:

            # read the config each loop
            config = configfile.readConfig()
            hostName = config['server']['address']
            serverPort = config['server']['port']

            ui = config['general']['ui']
            verbose = config['general']['verbose']
            clock = config['general']['clock']

            for item in config["watch"]:

                buildcmd = os.path.expanduser(config["watch"][item]['buildcmd'])
                workingdir = os.path.expanduser(config["watch"][item]['workingdir'])
                cron = config['watch'][item]['cron']
                branch = config['watch'][item]['branch']
                tag = config['watch'][item]['tag']

                access = config['watch'][item]['access']
                path = os.path.expanduser(config['watch'][item]['path'])

                active = config['watch'][item]['active']
                if active: 
                    if pycron.is_now(cron):
                        try:
                            cmd = buildcmd.split()
                            run = True
                            for pid in procs.keys():
                                if cmd == procs[pid].args:
                                    d = procs[pid]
                                    if d.poll() is not None:
                                        log(f"Process is complete pid: {pid}")
                                        procs.pop(pid, None)
                                        run = False
                                    else:
                                        log(f"Already running as pid: {pid}")
                                        run = False
                                    break
                            if run:
                                log(f"Run {buildcmd}")
                                if not verbose:
                                    p = subprocess.Popen(cmd, cwd=workingdir, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                                else:
                                    p = subprocess.Popen(cmd, cwd=workingdir)
                                procs[p.pid] = p
                        except:
                            log(f"Could not run {buildcmd}")       
                    else:
                        log("Not due to run yet")

            time.sleep(clock)
    except KeyboardInterrupt:
        log("Interrupted, attempting to clean up running processes")
        for pid in procs.keys():
            d = procs[pid]
            d.kill()
        exit()

if __name__ == "__main__":
    main()
