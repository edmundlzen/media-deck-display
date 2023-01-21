import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Say something")
        self.fullscreen()

        self.box = Gtk.Box(orientation="vertical", spacing=2)
        self.add(self.box)

        self.currentValue = Gtk.Label(label="0")

        self.bottom = Gtk.Box(orientation="horizontal", spacing=2)
        self.bottom_left_button = Gtk.Button(label="-1")
        self.bottom_right_button = Gtk.Button(label="+1")
        self.bottom.pack_start(self.bottom_left_button, True, True, 0)
        self.bottom.pack_start(self.bottom_right_button, True, True, 0)

        self.bottom_left_button.connect("clicked", self.btn_clicked)
        self.bottom_right_button.connect("clicked", self.btn_clicked)

        self.box.pack_start(self.currentValue, True, True, 0)
        self.box.pack_start(self.bottom, True, True, 0)

    def btn_clicked(self, widget):
        if widget == self.bottom_left_button:
            self.currentValue.set_text(str(int(self.currentValue.get_text()) - 1))
        elif widget == self.bottom_right_button:
            self.currentValue.set_text(str(int(self.currentValue.get_text()) + 1))


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()