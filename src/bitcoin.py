import authproxy
import os.path
import re

class Client:
    def __init__(self):
        self.setup_config()
        self.setup_rpc()

    def get_balance(self):
        "Return the current balance held in Bitcoin's wallet."
        return self.rpc.getinfo()['balance']

    def setup_config(self):
        config_path = os.path.expanduser("~/.bitcoin/bitcoin.conf")
        self.config = ConfigFile(config_path).read()
        
    def setup_rpc(self):
        rpc_url = "http://%s:%s@%s:%s" % (
            self.config.get('rpcuser', ''),
            self.config['rpcpassword'],
            self.config.get('rpcconnect', '127.0.0.1'),
            self.config.get('rpcport', '8332'))
        self.rpc = authproxy.AuthServiceProxy(rpc_url)


class ConfigFile:
    "Class for reading Bitcoin config files."

    def __init__(self, path = None):
        "Creates an object for reading the config file at path."
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
