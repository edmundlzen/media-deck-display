import threading
import time
import pyfirmata

import gi
import firebase_admin
from firebase_admin import db

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

cred_obj = firebase_admin.credentials.Certificate('media-deck-80f66-firebase-adminsdk-rdw0o-912eceec34.json')
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': "https://media-deck-80f66-default-rtdb.asia-southeast1.firebasedatabase.app/"
})


class MyWindow(Gtk.Window):
    def __init__(self):

        Gtk.Window.__init__(self, title="Media Deck")
        self.unmute_sent = None
        self.mute_sent = None
        self.last_analog_read = None
        self.last_read_values = set()
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

        currentPlayingSongTitleRef = db.reference('currentPlayingSong/title')
        currentPlayingSongTitleRef.listen(self.on_current_playing_song_title_changed)
        currentPlayingSongProgressRef = db.reference('currentPlayingSong/progress')
        currentPlayingSongProgressRef.listen(self.on_current_playing_song_progress_changed)
        currentVolumeRef = db.reference('settings/volume')
        currentVolumeRef.listen(self.on_volume_changed)

        port = '/dev/ttyACM0'
        self.board = pyfirmata.ArduinoMega(port)
        board = self.board
        it = pyfirmata.util.Iterator(board)
        it.start()
        for i in range(2, 11):
            board.digital[i].mode = pyfirmata.INPUT
        board.digital[22].mode = pyfirmata.INPUT
        board.analog[0].enable_reporting()

        # Run a loop to read the arduino
        GLib.timeout_add(100, self.read_arduino)
        self.show_all()

    def read_arduino(self):
        board = self.board
        print("\033[2J")
        for i in range(2, 11):
            if board.analog[0].read() is not None:
                if board.analog[0].read() != self.last_analog_read:
                    print("New analog value: " + str(board.analog[0].read()))
                    self.set_volume(board.analog[0].read() * 100)
                    volumeRef = db.reference('settings/volume')
                    volumeRef.set(board.analog[0].read() * 100)
                self.last_analog_read = board.analog[0].read()
            if board.digital[i].read() is True:
                self.last_read_values.add(i)

        for last_on_pin in self.last_read_values.copy():
            if board.digital[last_on_pin].read() is False:
                self.last_read_values.remove(last_on_pin)
                pinNum = last_on_pin - 1
                if pinNum == 1:
                    # Do something with button 1
                    print("Button 1 pressed")
                    commandRef = db.reference('commands/previous')
                    commandRef.set(True)
                elif pinNum == 2:
                    # Do something with button 2
                    print("Button 2 pressed")
                    commandRef = db.reference('commands/playPause')
                    commandRef.set(True)
                elif pinNum == 3:
                    # Do something with button 3
                    print("Button 3 pressed")
                    commandRef = db.reference('commands/next')
                    commandRef.set(True)
                elif pinNum == 4:
                    # Do something with button 4
                    print("Button 4 pressed")
                elif pinNum == 5:
                    # Do something with button 5
                    print("Button 5 pressed")
                elif pinNum == 6:
                    # Do something with button 6
                    print("Button 6 pressed")
                elif pinNum == 7:
                    # Do something with button 7
                    print("Button 7 pressed")
                elif pinNum == 8:
                    # Do something with button 8
                    print("Button 8 pressed")
                elif pinNum == 9:
                    # Do something with button 9
                    print("Button 9 pressed")

        if board.digital[22].read() is True:
            if self.mute_sent is False:
                self.unmute_sent = False
                # Do something
                commandRef = db.reference('commands/mute')
                commandRef.set(True)
                print("Mute button pressed")
                self.mute_sent = True
        else:
            self.mute_sent = False
            if self.unmute_sent is False:
                # Do something
                commandRef = db.reference('commands/unmute')
                commandRef.set(True)
                print("Unmute button pressed")
                self.unmute_sent = True
        return True

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
        GLib.idle_add(self.active_info_title.set_text, title)

    def set_active_song_progress(self, progress):
        print("set_active_song_progress", progress)
        GLib.idle_add(self.active_info_scale.set_value, progress)

    def set_volume(self, volume):
        print("set_volume", volume)
        GLib.idle_add(self.bottom_left_audio_scale.set_value, volume)

    def on_current_playing_song_title_changed(self, event):
        print("on_current_playing_song_title_changed", event.data)
        if event.data is not None:
            self.set_active_song_title(event.data)

    def on_current_playing_song_progress_changed(self, event):
        print("on_current_playing_song_progress_changed", event.data)
        if event.data is not None:
            self.set_active_song_progress(event.data)

    def on_volume_changed(self, event):
        print("on_volume_changed", event.data)
        if event.data is not None:
            self.set_volume(event.data)


win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
