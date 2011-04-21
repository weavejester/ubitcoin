import gobject
import gtk
import appindicator
import authproxy

class Application:
    "Main application class. Use Application.main to start."

    @classmethod
    def main(cls):
        "Create the application and start gtk.main()."
        app = cls()
        gtk.main()

    def __init__(self):
        "Create the application."
        self.setup_indicator()
        self.setup_rpc()

    def setup_indicator(self):
        "Create the indicator applet."
        self.indicator = appindicator.Indicator(
            "example-simple-client",
            "indicator-messages",
            appindicator.CATEGORY_APPLICATION_STATUS)

        self.indicator.set_status(appindicator.STATUS_ACTIVE)
        self.indicator.set_attention_icon("indicator-messages-new")
        self.indicator.set_menu(self.setup_menu())

    def setup_rpc(self):
        self.rpc = authproxy.AuthServiceProxy("http://:secret@localhost:8332")

    def setup_menu(self):
        "Create the main menu on the indicator."
        self.menu = gtk.Menu()
        self.add_balance_item()
        self.add_separator()
        self.add_quit_item()
        return self.menu

    def add_separator(self):
        separator = gtk.SeparatorMenuItem()
        separator.show()
        self.menu.append(separator)

    def add_balance_item(self):
        "Add a balance item to the menu."
        self.balance_item = gtk.MenuItem("Balance: 10 BTC")
        self.balance_item.set_sensitive(False)
        self.balance_item.show()
        self.menu.append(self.balance_item)

    def add_quit_item(self):
        "Add a quit item to the menu."
        quit_item = gtk.MenuItem("Quit uBitcoin")
        quit_item.connect("activate", exit)
        quit_item.show()
        self.menu.append(quit_item)
