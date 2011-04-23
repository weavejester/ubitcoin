import gtk
import os.path

class Base(object):
    "Base window class built from a GTK Builder file."

    def __init__(self, builder_file_path):
        "Create a window given a GTK builder file path."
        current_dir = os.path.dirname(__file__)
        ui_file = os.path.join(current_dir, builder_file_path)
        self.builder = gtk.Builder()
        self.builder.add_from_file(ui_file)
        self.builder.connect_signals(self)
