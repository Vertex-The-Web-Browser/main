import gi
import validators

gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk
from gi.repository import WebKit2

# TODO: use class for window and rendering box

# Global variable section start

rendering_box = WebKit2.WebView()
'''
Global instance of rendering box which is global so that it can be used by various functions
'''

session_history = []
'''
List to manage session history, used to implement the back (and in future, forward) button.
Any new page visits are appended to the end.
TODO: Hide the structure behind a class, in order to prevent accidental manipulations
'''

# Global variable section end


def search(widget):
    '''
    Function called by search button or by pressing enter when address bar is active.
    If entered text is a valid url, load it, otherwise load google search results for it
    '''

    search_text = address_bar.get_text()
    
    if(validators.url(search_text)): 
        rendering_box.load_uri(search_text)
    else:
        rendering_box.load_uri("https://www.google.com/search?q=" + search_text.replace(" ", "+"))
        # TODO: implement proper google querying, perhaps using https://stackoverflow.com/questions/6431061/python-encoding-characters-with-urllib-quote


def back(widget):
    '''
    Function called by back button to go to previous page
    Pops the current url from session history stack, and goes to the 
    url now on top of the stack, unless the stack has only one element.
    '''
    if len(session_history) > 1:
        session_history.pop()
        rendering_box.load_uri(session_history[-1])


def url_requested(current_webview_object, load_event_type):
    '''
    Function called when a new page is loaded. Adds the page to session history if
    it is not already at the top of the stack (to prevent issues with refresh).
    '''
    if load_event_type == WebKit2.LoadEvent.COMMITTED:
        uri = current_webview_object.get_uri()
        if session_history and session_history[-1] == uri:
            pass
        else:
            session_history.append(uri)
        
# Creates the browser GTK window
browser_window = Gtk.Window()

# Registers an event handler to exit event. Can add stuff such as saving, pause downloads, etc before quit
browser_window.connect("destroy", Gtk.main_quit)

# Creates GTK grid on which various UI components are placed, and adds it to the window
browser_window_grid = Gtk.Grid()
browser_window.add(browser_window_grid)

# Creates back button, and registers back() event handler which is invoked when it is clicked
back_button = Gtk.Button.new_with_label("Back")
back_button.connect("clicked", back)

# Creates address bar, and registers search event handler which is invoked when enter is pressed
address_bar = Gtk.Entry()
address_bar.set_hexpand(True)
address_bar.connect("activate", search)

# Creates search button, and registers search event handler which is invoked when button is pressed
search_button = Gtk.Button.new_with_label("Search")
search_button.connect("clicked", search)

# Adds aforementioned buttons and address bar to the display grid
browser_window_grid.add(back_button)
browser_window_grid.add(address_bar)
browser_window_grid.add(search_button)

rendering_box.set_hexpand(True)
rendering_box.set_vexpand(True)

# Registers url_requested() as event handler for page load events
rendering_box.connect('load-changed', url_requested)

# Puts webview object into the grid 
browser_window_grid.attach_next_to(rendering_box, address_bar, Gtk.PositionType.BOTTOM, 100, 100)

# Loads default search engine
rendering_box.load_uri('https://www.google.com')

# Starts the event loop
browser_window.show_all()
Gtk.main()
