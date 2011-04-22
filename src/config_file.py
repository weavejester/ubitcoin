import os.path
import re

class ConfigFile:
    "Class for reading Bitcoin config files."
    
    def __init__(self, path = None):
        """Creates an object for reading the config file specified as an
        argument. If no argument is specified, the default Bitcoin config
        file is used."""
        if path is None:
            self.path = os.path.expanduser("~/.bitcoin/bitcoin.conf")
        else:
            self.path = path
            
    def read(self):
        "Returns a dictionary of configuration values."
        settings = {}
        if os.path.exists(self.path):
            for line in file(self.path):
                if self.is_whitespace(line): continue
                if self.is_comment(line): continue
                key, value  = self.parse_setting(line)
                settings[key] = value
        return settings

    def is_whitespace(self, line):
        return line.strip() == ""

    def is_comment(self, line):
        return re.match(r"^\s*#", line)

    def parse_setting(self, line):
        key, value = line.split("=", 1)
        return key.strip(), value.strip()
