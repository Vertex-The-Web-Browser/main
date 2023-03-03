import gi
import validators

gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk
from gi.repository import WebKit2

from history import SessionHistory


class Tab:

    def __init__(self, notebook):
        '''
        Intialises a tab, including a webview rendering engine,
        search bar, search button and back button
        '''
        self.tab_grid = Gtk.Grid()
        self.session_history = SessionHistory()
        self.rendering_box = WebKit2.WebView()

        
        # Creates back button, and registers back() event handler which is invoked when it is clicked
        self.back_button = Gtk.Button.new_with_label("Back")
        self.back_button.connect("clicked", self.back)

        # Creates forward button, and registers forward() event handler which is invoked when it is clicked
        self.forward_button = Gtk.Button.new_with_label("Forward")
        self.forward_button.connect("clicked", self.forward)

        #Creates refresh button
        self.refresh_button= Gtk.Button.new_with_label("Refresh")
        self.refresh_button.connect("clicked", lambda x: self.rendering_box.reload())

        # Creates address bar, and registers search event handler which is invoked when enter is pressed
        self.address_bar = Gtk.Entry()
        self.address_bar.set_hexpand(True)
        self.address_bar.connect("activate", self.search)

        # Creates search button, and registers search event handler which is invoked when button is pressed
        self.search_button = Gtk.Button.new_with_label("Search")
        self.search_button.connect("clicked", self.search)

        # Adds aforementioned buttons and address bar to the display grid
        self.tab_grid.add(self.back_button)
        self.tab_grid.add(self.forward_button)
        self.tab_grid.add(self.refresh_button)

        self.tab_grid.add(self.address_bar)
        self.tab_grid.add(self.search_button)
        
        self.rendering_box.set_hexpand(True)
        self.rendering_box.set_vexpand(True)

        # Registers url_requested() as event handler for page load events
        self.rendering_box.connect('load-changed', self.url_requested)

        # Puts webview object into the grid 
        self.tab_grid.attach_next_to(self.rendering_box, self.address_bar, Gtk.PositionType.BOTTOM, 100, 100)

        # Loads default search engine
        self.rendering_box.load_uri('https://www.google.com')

        # Appends this tab to the passed notebook 
        notebook.append_page(self.tab_grid)


    def search(self, widget):
        '''
        Function called by search button or by pressing enter when address bar is active.
        If entered text is a valid url, load it, otherwise load google search results for it
        '''

        search_text = self.address_bar.get_text()
    
        if(validators.url(search_text)): 
            self.rendering_box.load_uri(search_text)
        else:
            self.rendering_box.load_uri("https://www.google.com/search?q=" + search_text.replace(" ", "+"))
            # TODO: implement proper google querying, perhaps using https://stackoverflow.com/questions/6431061/python-encoding-characters-with-urllib-quote

    
    def back(self, widget):
        '''
        Function called by back button to go to previous page
        Requests the previous uri from the session history
        '''
        
        uri = self.session_history.prev_uri()
        if uri is not None:
            self.rendering_box.load_uri(uri)

    
    def forward(self, widget):
        '''
        Function called by forward button to go to next page
        Requests the next uri from the session history
        '''

        uri = self.session_history.next_uri()
        if uri is not None:
            self.rendering_box.load_uri(uri)

    
    def url_requested(self, current_webview_object, load_event_type):
        '''
        Function called when a new page is loaded. Adds the page to session history if
        it is not already at the top of the stack (to prevent issues with refresh).
        '''

        if load_event_type == WebKit2.LoadEvent.COMMITTED:
            uri = current_webview_object.get_uri()
            if self.session_history.curr_uri() != uri:
                self.session_history.add_uri(uri)
                
