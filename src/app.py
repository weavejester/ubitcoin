import gobject
import gtk
import appindicator

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

    def setup_indicator(self):
        "Create the indicator applet."
        self.indicator = appindicator.Indicator(
            "example-simple-client",
            "indicator-messages",
            appindicator.CATEGORY_APPLICATION_STATUS)

        self.indicator.set_status(appindicator.STATUS_ACTIVE)
        self.indicator.set_attention_icon("indicator-messages-new")
        self.indicator.set_menu(self.setup_menu())

    def setup_menu(self):
        "Create the main menu on the indicator."
        self.menu = gtk.Menu()
        self.add_quit_item()
        return self.menu

    def add_quit_item(self):
        "Add a quit item to the menu."
        quit_item = gtk.MenuItem("Quit uBitcoin")
        self.menu.append(quit_item)
        quit_item.connect("activate", exit)
        quit_item.show()
