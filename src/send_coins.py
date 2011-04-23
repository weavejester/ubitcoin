import gtk
import window

class SendCoinsDialog(window.Base):
    "Dialog box for sending Bitcoins to other accounts."
    
    def __init__(self, client):
        "Creates the dialog. Takes a bitcoin.Client object as an argument."
        window.Base.__init__(self, "send_coins.xml")
        self.client = client
        self.window = self.builder.get_object("window")
        self.pay_to = self.builder.get_object("pay_to")
        self.amount = self.builder.get_object("amount")

    def show(self):
        "Show the window."
        self.window.show()

    def close(self):
        "Close and clear the window."
        self.window.hide()
        self.clear()

    def clear(self):
        self.pay_to.set_text("")
        self.amount.set_text("")

    def on_window_close(self, window, data=None):
        self.close()
        return True

    def on_cancel_pressed(self, button, data=None):
        self.close()

    def on_send_pressed(self, button, data=None):
        address = self.pay_to.get_text()
        amount = float(self.amount.get_text())
        self.client.send_to_address(address, amount)
        self.close()

    def on_paste_pressed(self, button, data=None):
        clipboard = gtk.clipboard_get()
        clipboard.request_text(self.paste_pay_to)

    def paste_pay_to(self, _, address, data=None):
        self.pay_to.set_text(address)
