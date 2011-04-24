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
        "Setup the ListStore that holds the transaction data."
        self.transactions = gtk.ListStore(long, str, float, int)
        self.add_all_transactions()
        return self.transactions

    def add_all_transactions(self, n=1000):
        "Add all of the transactions the client has listed, up to a max of n."
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
        "Setup the transactons table."
        self.transaction_table = self.builder.get_object("transactions_table")
        self.transaction_table.set_model(self.setup_store())
        self.text_renderer = gtk.CellRendererText()
        self.add_date_column("Date", 0)
        self.add_text_column("Description", 1)
        self.add_number_column("Amount", 2)
        self.add_text_column("Status", 3)

    def add_date_column(self, title, index):
        "Add a table column for displaying a datetime from a timestamp."
        column = gtk.TreeViewColumn(title, self.text_renderer)
        column.set_cell_data_func(self.text_renderer, self.render_datetime, index)
        self.transaction_table.append_column(column)

    def render_datetime(self, _, renderer, model, iter, index):
        "Render a timestamp as a formatted datetime table cell."
        timestamp = model.get_value(iter, index)
        dt = datetime.fromtimestamp(timestamp)
        renderer.set_property('text', dt.strftime("%Y-%m-%d %H:%m:%S"))

    def add_number_column(self, title, index):
        "Add a table column for displaying numerical data."
        column = gtk.TreeViewColumn(title, self.text_renderer)
        column.set_cell_data_func(self.text_renderer, self.render_number, index)
        self.transaction_table.append_column(column)

    def render_number(self, _, renderer, model, iter, index):
        "Render a floating point number as a table cell."
        number = model.get_value(iter, index)
        renderer.set_property('text', "%.2f" % number)

    def add_text_column(self, title, index):
        "Add a plain-text table column."
        column = gtk.TreeViewColumn(title, self.text_renderer, text=index)
        self.transaction_table.append_column(column)

    def show(self):
        "Show the window."
        self.window.show()

    def on_window_delete_event(self, window, data=None):
        "Hide the window on close."
        self.window.hide()
        return True
