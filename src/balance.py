import gtk
import window

class BalanceDialog(window.Base):
    "Dialog box for displaying the account balance."

    def __init__(self, client):
        "Creates the dialog. Takes a bitcoin.Client object as an argument."
        window.Base.__init__(self, "balance.xml")
        self.client = client
        self.window = self.builder.get_object("window")

    def show(self):
        self.window.show()
        
    def on_window_close(self, window, data=None):
        self.window.hide()
        return True

    def on_close_pressed(self, button, data=None):
        self.window.hide()
