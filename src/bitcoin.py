import authproxy
import os.path
import re
import urllib
import json
import event
from datetime import datetime

class Transaction(object):
    "Class representing a Bitcoin transaction."

    def __init__(self, client, attrs):
        self.client = client
        self.update(attrs)

    def update(self, attrs):
        self.id = attrs['txid']
        self.timestamp = attrs['time']
        self.address = attrs['address']
        self.amount = attrs['amount']
        self.confirmations = attrs['confirmations']

    def reload(self):
        return self.client.get_transaction_by_id(self.id)

    @property
    def datetime(self):
        return datetime.fromtimestamp(self.timestamp)

    def is_confirmed(self):
        return self.confirmations >= 6


class Client(object):
    "Class for talking to the Bitcoin server via JSONRPC."

    def __init__(self):
        "Create a new Bitcoin client class."
        self.setup_config()
        self.setup_rpc()
        self.on_transaction = event.Event()
        self.on_block = event.Event()
        self.setup_polling()

    def get_balance(self):
        "Get the current bitcoin balance."
        return self.rpc.getinfo()['balance']

    def send_to_address(self, address, amount):
        "Send an amount of bitcoins to a bitcoin address."
        self.rpc.sendtoaddress(address, amount)

    def get_usd_buy_rate(self):
        "Get the amount of USD that 1 BTC is being bought for."
        ticker = self.get_mt_gox_ticker()
        return ticker['buy']

    def get_mt_gox_ticker(self):
        "Return ticker information from Mt. Gox."
        ticker_url = "http://mtgox.com/code/data/ticker.php"
        response = json.load(urllib.urlopen(ticker_url))
        return response['ticker']

    def get_block_number(self):
        "Get the current block number."
        return self.rpc.getblocknumber()

    def get_last_transaction_id(self):
        "Get the last transaction made."
        return self.get_transactions(1)[0].id

    def get_new_transactions(self, n):
        """Get all new transactions since the last time poll_transactions was
        called, up to a maximum of n."""
        for transaction in reversed(self.get_transactions(n)):
            if transaction != self.poll_transactions.last_value:
                yield transaction
            else:
                break

    def get_transaction_by_id(self, txid):
        "Get a transaction by its transaction ID."
        response = self.rpc.gettransaction(txid)
        response.update(response['details'][0])
        return Transaction(self, response)

    def get_transactions(self, n):
        "Get the last n transactions."
        return [Transaction(self, t) for t in self.rpc.listtransactions("*", n)]
    
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

    def setup_polling(self):
        self.poll_transactions = event.OnChange(
            self.get_last_transaction_id, self.on_transaction)
        self.poll_blocks = event.OnChange(
            self.get_block_number, self.on_block)

    def poll(self):
        "Poll the Bitcoin server for new transactions or blocks."
        self.poll_transactions()
        self.poll_blocks()


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
