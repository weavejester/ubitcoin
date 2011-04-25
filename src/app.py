import pygtk
pygtk.require("2.0")
import gtk
import appindicator
import os.path
import timer
import bitcoin

from send_coins import SendCoinsDialog
from balance import BalanceDialog
from transactions import TransactionsWindow

class Application(object):
    "Main application class. Use Application.main to start."

    @classmethod
    def main(cls):
        "Create the application and start gtk.main()."
        app = cls()
        gtk.main()

    def __init__(self):
        self.setup_client()
        self.setup_windows()
        self.setup_indicator()
        self.client.poll()

    def update_balance(self):
        balance = self.client.get_balance()
        menu_text = "Balance:  %.2f BTC" % balance
        self.balance_item.child.set_label(menu_text)
        self.refresh_menu()

    def refresh_menu(self):
        """Workaround for a bug in appindicator - menu needs to be reset
        if any menu item changes, otherwise the change won't show up."""
        self.indicator.set_menu(self.menu)
        
    def setup_indicator(self):
        "Create the indicator applet."
        self.indicator = appindicator.Indicator(
            "example-simple-client",
            os.path.abspath("ubitcoin-dark.svg"),
            appindicator.CATEGORY_APPLICATION_STATUS)

        self.indicator.set_status(appindicator.STATUS_ACTIVE)
        self.indicator.set_menu(self.setup_menu())

    def setup_client(self):
        "Setup the Bitcoin RPC client."
        self.client = bitcoin.Client()
        self.client.on_transaction(self.update_balance)
        timer.periodic_timer(2000, self.client.poll)

    def setup_windows(self):
        self.send_coins_dialog = SendCoinsDialog(self.client)
        self.balance_dialog = BalanceDialog(self.client)
        self.transactions_dialog = TransactionsWindow(self.client)

    def open_send_coins(self, _=None):
        "Open the 'Send Coins' dialog."
        self.send_coins_dialog.show()

    def open_balance(self, _=None):
        "Open the 'Balance' dialog."
        self.balance_dialog.show()

    def open_transactions(self, _=None):
        "Open the 'Transactions' dialog."
        self.transactions_dialog.show()
        
    def setup_menu(self):
        "Create the main menu on the indicator."
        self.menu = gtk.Menu()
        self.add_balance_item()
        self.add_menu_item("Send Coins", self.open_send_coins)
        self.add_menu_item("Transaction History", self.open_transactions)
        self.add_separator()
        self.add_menu_item("Quit", gtk.main_quit)
        return self.menu

    def add_separator(self):
        "Add a separator to the menu."
        separator = gtk.SeparatorMenuItem()
        separator.show()
        self.menu.append(separator)

    def add_menu_item(self, label, callback):
        """Add a menu item with a callback function to the menu. Returns the
        newly created menu item."""
        menu_item = gtk.MenuItem(label)
        menu_item.connect("activate", callback)
        menu_item.show()
        self.menu.append(menu_item)
        return menu_item
        
    def add_balance_item(self):
        "Add a balance item to the menu."
        self.balance_item = self.add_menu_item("Balance", self.open_balance)
        self.update_balance()
