import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Say something")
        self.set_size_request(300, 190)

        self.box = Gtk.Box(orientation="vertical", spacing=2)
        self.add(self.box)

        self.text = Gtk.Label("Hello")

        self.bottom = Gtk.Box(orientation="horizontal", spacing=2)
        self.bottom_text1 = Gtk.Label("Left")
        self.bottom_text2 = Gtk.Label("Right")
        self.bottom.pack_start(self.bottom_text1, True, True, 0)
        self.bottom.pack_start(self.bottom_text2, True, True, 0)

        self.box.pack_start(self.text, True, True, 0)
        self.box.pack_start(self.bottom, True, True, 0)

    def btn_clicked(self, widget):
        txt = self.ent.get_text()
        print(txt)


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()