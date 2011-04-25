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
        self.client.on_transaction(self.add_new_transactions)

    def setup_store(self):
        "Setup the ListStore that holds the transaction data."
        self.transactions = gtk.ListStore(long, str, float, int)
        return self.transactions

    def add_new_transactions(self):
        "Add any new transactions."
        transactions = list(self.client.get_new_transactions(1000))
        for transaction in reversed(transactions):
            self.add_transaction(transaction)

    def add_transaction(self, transaction):
        "Add a new transaction dictionary to the transactions table."
        self.transactions.prepend([
                transaction['time'],
                transaction['address'],
                transaction['amount'],
                transaction['confirmations']])

    def setup_table(self):
        "Setup the transactons table."
        self.transaction_table = self.builder.get_object("transactions_table")
        self.transaction_table.set_model(self.setup_store())
        self.text_renderer = gtk.CellRendererText()
        self.add_text_column("Date", 0, self.format_datetime)
        self.add_text_column("Description", 1)
        self.add_text_column("Debit", 2, self.format_debit)
        self.add_text_column("Credit", 2, self.format_credit)
        self.add_text_column("Status", 3, self.format_status)

    def on_scrolled_window_size_allocate(self, window, event, data=None):
        """Ensure scrolled transaction window snaps to top when new transactions
        are added to the table."""
        vadjustment = window.get_vadjustment()
        vadjustment.set_value(vadjustment.get_lower())

    def format_datetime(self, timestamp):
        "Turn a timestamp integer into a formatted date/time string."
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%m:%S")

    def format_credit(self, amount):
        "Format an amount of money if it credits the account."
        return "%.2f" % amount if amount >= 0 else ""

    def format_debit(self, amount):
        "Format an amount of money if it debits the account."
        return "%.2f" % amount if amount < 0 else ""

    def format_status(self, confirmations):
        return "Confirmed" if confirmations >= 6 else "Unconfirmed"

    def add_text_column(self, title, index, formatter=None):
        "Add a text table column with an optional formatter function."
        column = gtk.TreeViewColumn(title, self.text_renderer)
        if formatter is None:
            column.set_attributes(self.text_renderer, text=index)
        else:
            column.set_cell_data_func(
                self.text_renderer,
                self.make_cell_formatter(formatter, index))
        self.transaction_table.append_column(column)

    def make_cell_formatter(self, formatter, index):
        """Create a cell renderer from a formatter function that turns an object
        in a tree model into a string."""
        def cell_renderer(_, cell, model, iter, data=None):
            raw_value = model.get_value(iter, index)
            cell.set_property('text', formatter(raw_value))
        return cell_renderer

    def show(self):
        "Show the window."
        self.window.show()

    def on_window_delete_event(self, window, data=None):
        "Hide the window on close."
        self.window.hide()
        return True
