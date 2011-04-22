import gobject
import gtk
import appindicator
import authproxy
import os.path

class Application:
    "Main application class. Use Application.main to start."

    @classmethod
    def main(cls):
        "Create the application and start gtk.main()."
        app = cls()
        gtk.main()

    def __init__(self):
        "Create the application."
        self.setup_rpc()
        self.setup_indicator()
        self.setup_timer()

    def tick(self):
        self.refresh_balance()

    def refresh_balance(self):
        balance = self.rpc.getinfo()['balance']
        self.balance_item.child.set_text(u"Balance:  %.2f \u0E3F" % balance)
        
    def setup_indicator(self):
        "Create the indicator applet."
        self.indicator = appindicator.Indicator(
            "example-simple-client",
            os.path.abspath("ubitcoin-dark.svg"),
            appindicator.CATEGORY_APPLICATION_STATUS)

        self.indicator.set_status(appindicator.STATUS_ACTIVE)
        self.indicator.set_menu(self.setup_menu())

    def setup_rpc(self):
        self.rpc = authproxy.AuthServiceProxy("http://:secret@localhost:8332")
        
    def setup_timer(self):
        gobject.timeout_add(2000, self.__tick)

    def __tick(self):
        self.tick()
        self.setup_timer()
        
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
        send_coins_item.show()
        self.menu.append(send_coins_item)

    def add_balance_item(self):
        "Add a balance item to the menu."
        self.balance_item = gtk.MenuItem("Balance")
        self.refresh_balance()
        self.balance_item.show()
        self.menu.append(self.balance_item)

    def add_quit_item(self):
        "Add a quit item to the menu."
        quit_item = gtk.MenuItem("Quit uBitcoin")
        quit_item.connect("activate", exit)
        quit_item.show()
        self.menu.append(quit_item)
