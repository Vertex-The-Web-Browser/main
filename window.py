import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Pango", "1.0")

from gi.repository import Gtk
from gi.repository import Pango

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

        # Allow scrolling if too many tabs
        self.browser_window_notebook.set_scrollable(True)


    def add_tab_to_notebook(self):
        '''
        Creates a new tab object, and adds the tab as a page in the notebook
        Sets the tab to be reorderable
        Creates a label object for labelling a page, and passes it to 
        tab
        '''

        # Creates a new laebl with text Loading
        tab_label = Gtk.Label("Loading")

        # Sets width of label to MAX_WIDTH chars, so that all pages have same width
        tab_label.set_width_chars(20)

        # Adds ellipses to the end of label if text is too long
        tab_label.set_ellipsize(Pango.EllipsizeMode.END)

        new_tab = Tab(tab_label)

        self.browser_window_notebook.append_page(new_tab.get_container())

        self.browser_window_notebook.set_tab_label(new_tab.get_container(), tab_label)

        self.browser_window_notebook.set_tab_reorderable(new_tab.get_container(), True)

    
    def start_event_loop(self):
        # Starts the event loop
        self.browser_window.show_all()
        Gtk.main()