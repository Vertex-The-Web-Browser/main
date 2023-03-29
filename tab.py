import gi
import validators
import urllib.parse
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk
from gi.repository import WebKit2
from gi.repository import Pango
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

        # The notebook where the tabs are added, required
        # for tab close
        self.notebook = notebook
        
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

        # Registers url_load_handler() as event handler for page load events
        self.rendering_box.connect('load-changed', self.url_load_handler)

        # Puts webview object into the grid 
        self.tab_grid.attach_next_to(self.rendering_box, self.address_bar, Gtk.PositionType.BOTTOM, 100, 100)

        # Loads default search engine
        self.rendering_box.load_uri('https://www.google.com')

        self.close_button = Gtk.Button()
        self.close_button_icon = Gtk.Image(stock=Gtk.STOCK_CLOSE)
        self.close_button.set_image(self.close_button_icon)
        self.close_button.connect("clicked", self.close_tab)

        # Tab label widget
        self.label = Gtk.Label("Loading")
        
        # Sets width of label to MAX_WIDTH chars, so that all pages have same width
        self.label.set_width_chars(20)

        # Adds ellipses to the end of label if text is too long
        self.label.set_ellipsize(Pango.EllipsizeMode.END)
        
        self.loading_spinner = Gtk.Spinner()

        # The tab header is a box containing the tab title (label) and
        # the tab close button
        self.tab_header = Gtk.Box(spacing=20)
        self.tab_header.add(self.loading_spinner)
        self.tab_header.add(self.label)
        self.tab_header.add(self.close_button)

        # Show all tab header components
        self.tab_header.show_all()

        # Adds the tab_grid to the notebook
        notebook.append_page(self.tab_grid)

        # Set tab label
        notebook.set_tab_label(self.tab_grid, self.tab_header)

        # Sets the tab to be reorderable
        notebook.set_tab_reorderable(self.tab_grid, True)

        # Show new notebook components
        notebook.show_all()

    
    def get_container(self):
        # Returns the gui container of the tab
        return self.tab_grid


    def search(self, widget):
        '''
        Function called by search button or by pressing enter when address bar is active.
        If entered text is a valid url, load it, otherwise load google search results for it
        '''

        search_text = self.address_bar.get_text()

        if not search_text.startswith("https://") and validators.url("https://"+search_text):
            search_text = "https://"+search_text
    
        if(validators.url(search_text)): 
            self.rendering_box.load_uri(search_text)
        else:
            self.rendering_box.load_uri("https://www.google.com/search?q=" + urllib.parse.quote(search_text, safe= "!~*'()"))
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


    def add_uri_to_history(self, uri):
        '''
        Function to add uri to tab history
        '''

        if self.session_history.curr_uri() != uri:
            self.session_history.add_uri(uri)

    
    def update_address_bar(self, address):
        self.address_bar.set_text(address)


    def update_tab_title(self, title):
        self.label.set_label(title)

    
    def url_load_handler(self, current_webview_object, load_event_type):
        '''
        Function called when a page load event occurs. 
        If a page has started loading, sets the address bar and tab title to url.
        If page has finished loading, sets tab title to title of html page.
        Adds the page to session history if load is committed, and
        it is not already at the top of the stack (to prevent issues with refresh).
        '''
                
        uri = current_webview_object.get_uri()

        if load_event_type == WebKit2.LoadEvent.STARTED:
            self.loading_spinner.start()
            self.update_address_bar(uri)

        elif load_event_type == WebKit2.LoadEvent.COMMITTED:
            self.add_uri_to_history(uri)
            self.update_tab_title(uri)
            self.update_address_bar(uri)

        elif load_event_type == WebKit2.LoadEvent.FINISHED:
            self.loading_spinner.stop()
            self.update_tab_title(current_webview_object.get_title())
    
    def close_tab(self, widget):
        self.notebook.remove_page(self.notebook.page_num(self.tab_grid))  