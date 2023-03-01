import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from tab import Tab

class Window:

    def __init__(self):
        # Creates the browser GTK window
        self.browser_window = Gtk.Window()

        # Registers an event handler to exit event. Can add stuff such as saving, pause downloads, etc before quit
        self.browser_window.connect("destroy", Gtk.main_quit)

        # Creates GTK grid on which various UI components are placed, and adds it to the window
        self.browser_window_notebook = Gtk.Notebook()
        self.browser_window.add(self.browser_window_notebook)

        self.tab_list = []       


    def add_tab_to_notebook(self):

        new_tab = Tab(self.browser_window_notebook)
        self.tab_list.append(new_tab)

    
    def start_event_loop(self):
        # Starts the event loop
        self.browser_window.show_all()
        Gtk.main()