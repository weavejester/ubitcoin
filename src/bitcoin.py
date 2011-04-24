import authproxy
import os.path
import re
import urllib
import json

class Event(object):
    "Functor for event-based programming."
    def __init__(self):
        self.handlers = []

    def __call__(self, handler):
        self.handlers.append(handler)

    def trigger(self, *args):
        for handler in self.handlers:
            handler(*args)

class Client(object):
    "Class for talking to the Bitcoin server via JSONRPC."

    def __init__(self):
        self.setup_config()
        self.setup_rpc()
        self.on_transaction = Event()
        self.last_transaction = None

    def get_balance(self):
        "Get the current bitcoin balance."
        return self.rpc.getinfo()['balance']

    def send_to_address(self, address, amount):
        "Send an amount of bitcoins to a bitcoin address."
        self.rpc.sendtoaddress(address, amount)

    def get_usd_buy_rate(self):
        ticker = self.get_mt_gox_ticker()
        return ticker['buy']

    def get_mt_gox_ticker(self):
        ticker_url = "http://mtgox.com/code/data/ticker.php"
        response = json.load(urllib.urlopen(ticker_url))
        return response['ticker']

    def poll_transactions(self):
        "Poll the Bitcoin server for new transactions."
        last_last_transaction = self.last_transaction
        self.last_transaction = self.get_last_transaction()

        if last_last_transaction != self.last_transaction:
            self.on_transaction.trigger()

    def get_last_transaction(self):
        return self.get_transactions(1)[0]

    def get_transactions(self, n):
        return self.rpc.listtransactions("*", n)
    
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


class ConfigFile(object):
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
