import gtk
import os.path

class SendCoinsDialog(object):
    "Dialog box for sending Bitcoins to other accounts."
    
    def __init__(self):
        self.setup_ui()
        self.window = self.builder.get_object("window")
        self.pay_to = self.builder.get_object("pay_to")
        self.amount = self.builder.get_object("amount")

    def show(self):
        self.window.show()

    def hide(self):
        self.window.hide()
        self.clear()

    def clear(self):
        self.pay_to.set_text("")
        self.amount.set_text("")

    def setup_ui(self):
        current_dir = os.path.dirname(__file__)
        ui_file = os.path.join(current_dir, "send_coins.xml")
        self.builder = gtk.Builder()
        self.builder.add_from_file(ui_file)
        self.builder.connect_signals(self)

    def on_window_delete_event(self, window, data=None):
        self.hide()
        return True

    def on_cancel_pressed(self, button, data=None):
        self.hide()

    def on_send_pressed(self, button, data=None):
        pass

    def on_paste_pressed(self, button, data=None):
        clipboard = gtk.clipboard_get()
        clipboard.request_text(self.paste_pay_to)

    def paste_pay_to(self, _, address, data=None):
        self.pay_to.set_text(address)
