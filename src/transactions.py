import gtk
import window
from decimal import Decimal
from datetime import datetime

class TransactionsWindow(window.Base):
    "Dialog box for displaying a list of past transactions."

    def __init__(self, client):
        "Creates the window. Takes a bitcoin.Client object as an argument."
        window.Base.__init__(self, "transactions.xml")
        self.client = client
        self.window = self.builder.get_object("window")
        self.setup_table()

    def setup_store(self):
        self.transactions = gtk.ListStore(str, str, str, str, str)
        self.transactions.append(["a", "b", "c", "d", "e"])
        return self.transactions

    def add_transaction(self, transaction):
        pass
    
    def setup_table(self):
        self.transaction_table = self.builder.get_object("transactions_table")
        self.transaction_table.set_model(self.setup_store())
        self.cell_renderer = gtk.CellRendererText()
        self.add_column("Date")
        self.add_column("Description")
        self.add_column("Debit")
        self.add_column("Credit")
        self.add_column("Status")

    def add_column(self, title):
        column = gtk.TreeViewColumn(title, self.cell_renderer, text=0)
        self.transaction_table.append_column(column)
        
    def show(self):
        self.window.show()

    def on_window_delete_event(self, window, data=None):
        self.window.hide()
        return True
