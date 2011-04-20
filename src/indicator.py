import gobject
import gtk
import appindicator

def append_quit_item(menu):
    quit_item = gtk.MenuItem("Quit uBitcoin")
    menu.append(quit_item)
    quit_item.connect("activate", exit)
    quit_item.show()

def indicator_menu():
    "The menu on the indicator applet."
    menu = gtk.Menu()
    append_quit_item(menu)
    return menu

def indicator():
    "The main indicator applet."
    indicator = appindicator.Indicator(
        "example-simple-client",
        "indicator-messages",
        appindicator.CATEGORY_APPLICATION_STATUS)

    indicator.set_status(appindicator.STATUS_ACTIVE)
    indicator.set_attention_icon("indicator-messages-new")
    indicator.set_menu(indicator_menu())
    gtk.main()

if __name__ == "__main__":
    indicator()
