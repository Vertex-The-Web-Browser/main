import gi
import validators
import sqlite3
import  os
import pandas as pd



gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk
from gi.repository import WebKit2

from history import SessionHistory


class Tab:

    def __init__(self, tab_label):
        '''
        Intialises a tab, including a webview rendering engine,
        search bar, search button and back button
        '''
        self.tab_grid = Gtk.Grid()
        self.session_history = SessionHistory()
        self.rendering_box = WebKit2.WebView()
        
        # Creates back button, and registers back() event handler which is invoked when it is clicked
        self.back_button = Gtk.Button.new_with_label("Back button ")
        self.back_button.connect("clicked", self.back)

        # Creates forward button, and registers forward() event handler which is invoked when it is clicked
        self.forward_button = Gtk.Button.new_with_label("Forward")
        self.forward_button.connect("clicked", self.forward)

        # Creates address bar, and registers search event handler which is invoked when enter is pressed
        self.address_bar = Gtk.Entry()
        self.address_bar.set_hexpand(True)
        self.address_bar.connect("activate", self.search)



        con = sqlite3.connect('bookmarks.db')
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS bookmark_table(id integer primary key autoincrement, uri varchar(2000))")
        con.commit()
        con.close()


        self.bookmark_button = Gtk.Button.new_from_icon_name("bookmark-new-symbolic", Gtk.IconSize.BUTTON)
        self.bookmark_button.connect("clicked", self.bookmark)

      


        # Creates search button, and registers search event handler which is invoked when button is pressed
        self.search_button = Gtk.Button.new_with_label("Search")
        self.search_button.connect("clicked", self.search)



      


        # Adds aforementioned buttons and address bar to the display grid
        self.tab_grid.add(self.back_button)
        self.tab_grid.add(self.forward_button)
        self.tab_grid.add(self.address_bar)
        self.tab_grid.add(self.search_button)
        self.tab_grid.add(self.bookmark_button)


        self.rendering_box.set_hexpand(True)
        self.rendering_box.set_vexpand(True)

        # Registers url_load_handler() as event handler for page load events
        self.rendering_box.connect('load-changed', self.url_load_handler)

        # Puts webview object into the grid 
        self.tab_grid.attach_next_to(self.rendering_box, self.address_bar, Gtk.PositionType.BOTTOM, 100, 100)

        # Loads default search engine
        self.rendering_box.load_uri('https://www.google.com')

        self.tab_label = tab_label

    
    def get_container(self):
        # Returns the gui container of the tab
        return self.tab_grid


    def search(self, widget):
        '''
        Function called by search button or by pressing enter when address bar is active.
        If entered text is a valid url, load it, otherwise load google search results for it
        '''

      

        search_text = self.address_bar.get_text()

        if(validators.url(search_text)): 
            self.rendering_box.load_uri(search_text)
        elif(search_text == "vertex::bookmark"):
            conn = sqlite3.connect('bookmarks.db')
            cur = conn.cursor()

            cur.execute("SELECT * FROM bookmark_table")
            data = cur.fetchall()
   
            html = "<table border='1' style='width:100%;'>"
            html += "<tr><th>ID</th><th>URI</th></tr>"
            for row in data:
               html += "<tr><td>" + str(row[0]) + "</td><td>" + row[1] + "</td></tr>"
            html += "</table>"




            with open("bookmarks.html","w") as f:
             f.write(html)

            self.rendering_box.load_uri("file://"+os.getcwd()+"/bookmarks.html")
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


    def add_uri_to_history(self, uri):
        '''
        Function to add uri to tab history
        '''

        if self.session_history.curr_uri() != uri:
            self.session_history.add_uri(uri)

    
    def update_address_bar(self, address):
        self.address_bar.set_text(address)


    def update_tab_title(self, title):
        self.tab_label.set_label(title)
        

    
    def bookmark(self, widget):
        '''
        Function called by bookmark button to add current URI to bookmarks database.
        '''

        conn = sqlite3.connect('bookmarks.db')
        c = conn.cursor()

        uri = self.rendering_box.get_uri()

        # Check if bookmark already exists
        c.execute('SELECT * FROM bookmark_table WHERE uri=?', (uri,))
        bookmark = c.fetchone()

        if bookmark is None:
            # Add bookmark to database
            c.execute('INSERT INTO bookmark_table (uri) VALUES (?)', (uri,))
            conn.commit()

        conn.close()        





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
            self.update_address_bar(uri)
            self.update_tab_title(uri)

        elif load_event_type == WebKit2.LoadEvent.COMMITTED:
            self.add_uri_to_history(uri)

        elif load_event_type == WebKit2.LoadEvent.FINISHED:
            self.update_tab_title(current_webview_object.get_title())
            
                