import gi
import validators

gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk
from gi.repository import WebKit2

def search(widget):
    #wv.load_uri(address_bar.get_text())
    search_text = address_bar.get_text()
    #if valid url, load it, otherwise load google search results for it
    if(validators.url(search_text)): 
        wv.load_uri(search_text)
    else:
        wv.load_uri("https://www.google.com/search?q=" + search_text.replace(" ", "+"))
        #TODO: implement proper google querying 

win = Gtk.Window()
win.connect("destroy", Gtk.main_quit)

grid = Gtk.Grid()
win.add(grid)
address_bar = Gtk.Entry()
address_bar.set_hexpand(True)
address_bar.connect("activate", search)
search_button = Gtk.Button.new_with_label("Search")
search_button.connect("clicked", search)
grid.add(address_bar)
grid.add(search_button)


wv = WebKit2.WebView()
wv.set_hexpand(True)
wv.set_vexpand(True)
grid.attach_next_to(wv, address_bar, Gtk.PositionType.BOTTOM, 100, 100)
wv.load_uri('https://google.com')

win.show_all()
Gtk.main()
