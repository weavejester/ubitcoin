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
        self.transactions = gtk.ListStore(long, str, float, int)
        self.add_all_transactions()
        return self.transactions

    def add_all_transactions(self, n=1000):
        for transaction in self.client.get_transactions(n):
            self.add_transaction(transaction)

    def add_transaction(self, transaction):
        "Add a new transaction dictionary to the transactions table."
        self.transactions.append([
                transaction['time'],
                transaction['address'],
                transaction['amount'],
                transaction['confirmations']])
    
    def setup_table(self):
        self.transaction_table = self.builder.get_object("transactions_table")
        self.transaction_table.set_model(self.setup_store())
        self.cell_renderer = gtk.CellRendererText()
        self.add_column("Date", 0)
        self.add_column("Description", 1)
        self.add_column("Amount", 2)
        self.add_column("Status", 3)

    def add_column(self, title, index):
        column = gtk.TreeViewColumn(title, self.cell_renderer, text=index)
        self.transaction_table.append_column(column)
        
    def show(self):
        self.window.show()

    def on_window_delete_event(self, window, data=None):
        self.window.hide()
        return True
