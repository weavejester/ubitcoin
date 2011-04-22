import gobject

def periodic_timer(interval, callback):
    "Creates a periodic timer using GTK timeouts."
    def repeating_callback():
        callback()
        periodic_timer(interval, callback)
    gobject.timeout_add(interval, repeating_callback)
