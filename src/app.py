import gobject
import gtk
import appindicator
import os.path
import bitcoin
import send_coins

class Application(object):
    "Main application class. Use Application.main to start."

    @classmethod
    def main(cls):
        "Create the application and start gtk.main()."
        app = cls()
        gtk.main()

    def __init__(self):
        self.client = bitcoin.Client()
        self.set_timer()
        self.setup_indicator()
        self.setup_dialogs()
        self.client.on_transaction(self.update_balance)

    def tick(self):
        self.client.poll()

    def update_balance(self):
        text = u"Balance:  %.2f \u0E3F" % self.client.balance
        self.balance_item.child.set_label(text)
        self.refresh_menu()

    def refresh_menu(self):
        """Workaround for a bug in appindicator - menu needs to be reset
        if any menu item changes, otherwise the change won't show up."""
        self.indicator.set_menu(self.menu)

    def open_send_coins(self, _ = None):
        "Open the 'Send Coins' dialog."
        self.send_coins_dialog.show()

    def setup_indicator(self):
        "Create the indicator applet."
        self.indicator = appindicator.Indicator(
            "example-simple-client",
            os.path.abspath("ubitcoin-dark.svg"),
            appindicator.CATEGORY_APPLICATION_STATUS)

        self.indicator.set_status(appindicator.STATUS_ACTIVE)
        self.indicator.set_menu(self.setup_menu())
        
    def set_timer(self):
        self.tick()
        gobject.timeout_add(2000, self.set_timer)

    def setup_dialogs(self):
        self.send_coins_dialog = send_coins.SendCoinsDialog()

    def setup_menu(self):
        "Create the main menu on the indicator."
        self.menu = gtk.Menu()
        self.add_balance_item()
        self.add_send_coins_item()
        self.add_separator()
        self.add_quit_item()
        return self.menu

    def add_separator(self):
        "Add a separator to the menu."
        separator = gtk.SeparatorMenuItem()
        separator.show()
        self.menu.append(separator)

    def add_send_coins_item(self):
        "Add a 'Send Coins' item to the menu."
        send_coins_item = gtk.MenuItem("Send Coins")
        send_coins_item.connect("activate", self.open_send_coins)
        send_coins_item.show()
        self.menu.append(send_coins_item)

    def add_balance_item(self):
        "Add a balance item to the menu."
        self.balance_item = gtk.MenuItem("Balance")
        self.update_balance()
        self.balance_item.show()
        self.menu.append(self.balance_item)

    def add_quit_item(self):
        "Add a quit item to the menu."
        quit_item = gtk.MenuItem("Quit uBitcoin")
        quit_item.connect("activate", gtk.main_quit)
        quit_item.show()
        self.menu.append(quit_item)
