import gi
import validators

gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk
from gi.repository import WebKit2

session_history = []
def search(widget):
    #wv.load_uri(address_bar.get_text())
    search_text = address_bar.get_text()
    #if valid url, load it, otherwise load google search results for it
    if(validators.url(search_text)): 
        wv.load_uri(search_text)
    else:
        wv.load_uri("https://www.google.com/search?q=" + search_text.replace(" ", "+"))
        #TODO: implement proper google querying 

def back(widget):
    #print(session_history)
    if len(session_history) >= 2:
        session_history.pop()
        wv.load_uri(session_history[-1])


def url_requested(current_webview_object, load_event_type):
    #print(load_event_type, current_webview_object.get_uri())
    if load_event_type == WebKit2.LoadEvent.COMMITTED:
        uri = current_webview_object.get_uri()
        if session_history and session_history[-1] == uri:
            pass
        else:
            session_history.append(uri)
    #print(session_history)
        

win = Gtk.Window()
win.connect("destroy", Gtk.main_quit)

grid = Gtk.Grid()
win.add(grid)
back_button = Gtk.Button.new_with_label("Back")
back_button.connect("clicked", back)
address_bar = Gtk.Entry()
address_bar.set_hexpand(True)
address_bar.connect("activate", search)
search_button = Gtk.Button.new_with_label("Search")
search_button.connect("clicked", search)
grid.add(back_button)
grid.add(address_bar)
grid.add(search_button)


wv = WebKit2.WebView()
wv.set_hexpand(True)
wv.set_vexpand(True)
wv.connect('load-changed', url_requested)
grid.attach_next_to(wv, address_bar, Gtk.PositionType.BOTTOM, 100, 100)
wv.load_uri('https://google.com')


win.show_all()
Gtk.main()
