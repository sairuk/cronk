#!/usr/bin/python3

import os
import yaml

class ConfigFile():
    def __init__(self):
        self.configfile = os.path.expanduser("~/cronk.yaml")
        return

    def readConfig(self):
        if os.path.exists(self.configfile):
            with open(self.configfile, 'r') as f:
                return yaml.safe_load(f)
            try:
                with open(self.configfile, 'r') as f:
                    return yaml.safe_load(f)
            except:
                return None
        else:
            print("Config not found")
            return None

