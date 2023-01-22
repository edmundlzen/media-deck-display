import time

import gi
# import pyfirmata
import firebase_admin
from firebase_admin import db

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

cred_obj = firebase_admin.credentials.Certificate('media-deck-80f66-firebase-adminsdk-rdw0o-912eceec34.json')
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': "https://media-deck-80f66-default-rtdb.asia-southeast1.firebasedatabase.app/"
})


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Media Deck")
        self.fullscreen()
        self.set_size_request(480, 320)
        self.set_resizable(False)
        self.outer_column = Gtk.Box(orientation="vertical", spacing=0)
        self.add(self.outer_column)

        self.active_info_box = Gtk.Box(orientation="vertical", spacing=0)
        self.active_info_box_frame = Gtk.Frame()
        self.active_info_box_frame.add(self.active_info_box)
        self.outer_column.pack_start(self.active_info_box_frame, True, True, 0)

        self.active_info_title = Gtk.Label(label="Title")
        self.active_info_scale = Gtk.Scale(orientation="horizontal")
        self.active_info_scale.set_range(0, 100)
        self.active_info_scale.set_margin_start(10)
        self.active_info_scale.set_margin_end(10)
        # Hide the label
        self.active_info_scale.set_draw_value(False)
        # Call progress_scale_clicked when the scale is clicked
        # self.active_info_scale_event_box = Gtk.EventBox()
        # self.active_info_scale_event_box.add(self.active_info_scale)
        # self.active_info_scale_event_box.set_above_child(True)
        self.active_info_scale.connect("button-release-event", self.progress_scale_clicked)
        self.active_info_box.pack_start(self.active_info_title, True, True, 0)
        self.active_info_box.pack_start(self.active_info_scale, True, True, 0)

        self.bottom_info_box = Gtk.Box(orientation="horizontal", spacing=0)
        self.outer_column.pack_start(self.bottom_info_box, True, True, 0)

        self.bottom_left_box = Gtk.Box(orientation="vertical", spacing=0)
        self.bottom_left_box_border = Gtk.Frame()
        self.bottom_left_box_border.add(self.bottom_left_box)
        self.bottom_info_box.pack_start(self.bottom_left_box_border, True, True, 0)

        self.bottom_left_audio_scale = Gtk.Scale(orientation="horizontal")
        self.bottom_left_audio_scale.set_range(0, 100)
        self.bottom_left_audio_scale.set_margin_start(10)
        self.bottom_left_audio_scale.set_margin_end(10)
        # Hide the label
        self.bottom_left_audio_scale.set_draw_value(False)
        # Call volume_scale_clicked when the scale is clicked
        self.bottom_left_audio_scale.connect("button-release-event", self.volume_scale_clicked)
        self.bottom_left_box.pack_start(self.bottom_left_audio_scale, True, True, 0)

        self.bottom_left_time = Gtk.Label(label="00:00")
        self.bottom_left_box.pack_start(self.bottom_left_time, True, True, 0)

        self.bottom_left_date = Gtk.Label(label="31/12/2019")
        self.bottom_left_box.pack_start(self.bottom_left_date, True, True, 0)

        self.bottom_right_box = Gtk.Label(label="Right")
        self.bottom_right_box.set_margin_start(10)
        self.bottom_right_box.set_margin_end(10)
        self.bottom_right_box_border = Gtk.Frame()
        self.bottom_right_box_border.add(self.bottom_right_box)
        self.bottom_info_box.pack_start(self.bottom_right_box_border, True, True, 0)

    def progress_scale_clicked(self, widget, event):
        print("progress_scale_clicked", widget.get_value())
        currentPlayingSongProgressRef = db.reference('commands/progress')
        currentPlayingSongProgressRef.set(widget.get_value())

    def volume_scale_clicked(self, widget, event):
        print("volume_scale_clicked", widget.get_value())
        volumeRef = db.reference('settings/volume')
        volumeRef.set(widget.get_value())

    def btn_clicked(self, widget):
        if widget == self.bottom_left_button:
            print("bottom_left_button clicked")
            self.currentValue.set_text(str(int(self.currentValue.get_text()) - 1))
        elif widget == self.bottom_right_button:
            print("bottom_right_button clicked")
            self.currentValue.set_text(str(int(self.currentValue.get_text()) + 1))

    def set_active_song_title(self, title):
        print("set_active_song_title", title)
        self.active_info_title.set_text(title)

    def set_active_song_progress(self, progress):
        print("set_active_song_progress", progress)
        self.active_info_scale.set_value(progress)

    def set_volume(self, volume):
        print("set_volume", volume)
        self.bottom_left_audio_scale.set_value(volume)


win = MyWindow()


def on_current_playing_song_title_changed(event):
    print("on_current_playing_song_title_changed", event.data)
    if event.data is not None:
        win.set_active_song_title(event.data)


def on_current_playing_song_progress_changed(event):
    print("on_current_playing_song_progress_changed", event.data)
    if event.data is not None:
        win.set_active_song_progress(event.data)


def on_volume_changed(event):
    print("on_volume_changed", event.data)
    if event.data is not None:
        win.set_volume(event.data)


currentPlayingSongTitleRef = db.reference('currentPlayingSong/title')
currentPlayingSongTitleRef.listen(on_current_playing_song_title_changed)
currentPlayingSongProgressRef = db.reference('currentPlayingSong/progress')
currentPlayingSongProgressRef.listen(on_current_playing_song_progress_changed)
currentVolumeRef = db.reference('settings/volume')
currentVolumeRef.listen(on_volume_changed)

win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

# port = '/dev/ttyACM0'
# board = pyfirmata.Arduino(port)
# while True:
#     board.digital[13].write(0)
#     time.sleep(0.5)
#     board.digital[13].write(1)
#     time.sleep(0.2)
