import gtk
import window

class BalanceDialog(window.Base):
    "Dialog box for displaying the account balance."

    def __init__(self, client):
        "Creates the dialog. Takes a bitcoin.Client object as an argument."
        window.Base.__init__(self, "balance.xml")
        self.client = client
        self.window = self.builder.get_object("window")
        self.balance = self.builder.get_object("balance")
        self.client.on_transaction(self.update_balance)

    def update_balance(self):
        "Update the balance label to show the current balance."
        if self.is_visible():
            btc  = self.client.get_balance()
            rate = self.client.get_usd_buy_rate()
            usd  = float(btc) * rate
            label_text = "<b>%.2f BTC</b>\n(%.2f USD @ %.4f)" % (btc, usd, rate)
            self.balance.set_label(label_text)

    def is_visible(self):
        "Returns true if the dialog is visible to the user."
        return self.window.get_property("visible")

    def show(self):
        "Show the dialog box to the user."
        self.window.show()
        self.update_balance()
        
    def on_window_close(self, window, data=None):
        self.window.hide()
        return True

    def on_close_pressed(self, button, data=None):
        self.window.hide()
