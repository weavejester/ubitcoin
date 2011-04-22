import gtk
import os.path

class SendCoinsDialog(object):
    "Dialog box for sending Bitcoins to other accounts."
    
    def __init__(self):
        self.setup_ui()
        self.window = self.builder.get_object("window")

    def show(self):
        self.window.show()

    def setup_ui(self):
        current_dir = os.path.dirname(__file__)
        ui_file = os.path.join(current_dir, "send_coins.xml")
        self.builder = gtk.Builder()
        self.builder.add_from_file(ui_file)
        self.builder.connect_signals(self)

    def on_window_delete_event(self, window, data=None):
        self.window.hide()
        return True

    def on_cancel_pressed(self, button, data=None):
        self.window.hide()

    def on_send_pressed(self, button, data=None):
        pass
