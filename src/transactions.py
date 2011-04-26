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
        self.client.on_block(self.update_transactions)

    def update_transactions(self):
        print "On block"
        for row in self.transactions:
            transaction = row[0]
            if not transaction.is_confirmed():
                new_transaction = transaction.reload()
                if new_transaction.is_confirmed():
                    self.transactions.set_value(row.iter, 0, new_transaction)

    def setup_store(self):
        "Setup the ListStore that holds the transaction data."
        self.transactions = gtk.ListStore(object)
        return self.transactions

    def add_new_transactions(self):
        "Add any new transactions."
        print "On transaction"
        transactions = list(self.client.get_new_transactions(1000))
        for transaction in reversed(transactions):
            self.transactions.prepend([transaction])

    def setup_table(self):
        "Setup the transactons table."
        self.transaction_table = self.builder.get_object("transactions_table")
        self.transaction_table.set_model(self.setup_store())
        self.text_renderer = gtk.CellRendererText()
        self.add_text_column("Date", self.format_datetime)
        self.add_text_column("Description", self.format_description)
        self.add_text_column("Debit", self.format_debit)
        self.add_text_column("Credit", self.format_credit)
        self.add_text_column("Status", self.format_status)

    def on_scrolled_window_size_allocate(self, window, event, data=None):
        """Ensure scrolled transaction window snaps to top when new transactions
        are added to the table."""
        vadjustment = window.get_vadjustment()
        vadjustment.set_value(vadjustment.get_lower())

    def format_datetime(self, transaction):
        return transaction.datetime.strftime("%Y-%m-%d %H:%m:%S")

    def format_description(self, transaction):
        return transaction.address

    def format_credit(self, transaction):
        return "%.2f" % transaction.amount if transaction.amount >= 0 else ""

    def format_debit(self, transaction):
        return "%.2f" % transaction.amount if transaction.amount < 0 else ""

    def format_status(self, transaction):
        return "Confirmed" if transaction.is_confirmed() else "Unconfirmed"

    def add_text_column(self, title, getter):
        "Add a text table column with a getter function."
        column = gtk.TreeViewColumn(title, self.text_renderer)
        column.set_cell_data_func(
            self.text_renderer,
            self.make_cell_formatter(getter, 0))
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
