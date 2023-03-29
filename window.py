import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Pango", "1.0")

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

        # Allow scrolling if too many tabs
        self.browser_window_notebook.set_scrollable(True)

        # Button to add tabs
        self.add_tab_button = Gtk.Button(image=Gtk.Image(stock=Gtk.STOCK_ADD))

        # Register the click event handler to the required function
        self.add_tab_button.connect('clicked', self.add_tab_to_notebook)

        # Action widgets placed after/before tabs for control
        self.browser_window_notebook.set_action_widget(self.add_tab_button, Gtk.PackType.START)

        self.add_tab_button.show()


    
    def add_tab_to_notebook(self, widget):
        
        # Creates a tab and adds it to the notebook
        new_tab = Tab(self.browser_window_notebook)
        

    
    def start_event_loop(self):
        # Starts the event loop
        self.browser_window.show_all()
        Gtk.main()

