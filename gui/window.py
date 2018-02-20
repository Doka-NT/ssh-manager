from gi import require_version

from manager.command import AbstractCommand
from manager.config import Window

require_version('Gdk', '3.0')
require_version('Gtk', '3.0')

from gi.repository import Gtk

import application
from manager.manager import Manager


class ConnectionListWindow:
    VERTICAL_MARGIN = 5
    HORIZONTAL_MARGIN = 2

    def __init__(
            self, manager: Manager,
            window_config: Window,
            command_ssh: AbstractCommand,
            command_edit: AbstractCommand
    ):
        self._listbox = None
        self._frame = None
        self._scrollable = None
        self._btn_reload = None
        self._btn_settings = None
        self._list_store = Gtk.ListStore(str)

        self.__command_ssh = command_ssh
        self.__command_edit = command_edit
        self._manager = manager
        self._window_config = window_config

    def show(self):
        win = self.__create_window()

        self.__setup_ui(win)
        self.__setup_ui_listeners(win)

        win.show_all()
        Gtk.main()

    def __setup_ui_listeners(self, win):
        self._btn_settings.connect("clicked", self.__btn_settings_click)
        self._btn_reload.connect("clicked", self.__btn_reload_click)
        win.connect("delete-event", Gtk.main_quit)

    def __setup_ui(self, win):
        self._btn_settings = Gtk.Button("Settings")
        self._btn_settings.set_margin_right(self.HORIZONTAL_MARGIN)
        self._btn_reload = Gtk.Button("Reload")
        btn_box = Gtk.HBox()
        btn_box.add(self._btn_settings)
        btn_box.add(self._btn_reload)
        self._listbox = Gtk.TreeView(self._list_store)
        self._listbox.set_headers_visible(False)
        self._listbox.connect("row-activated", self.__row_activated)
        self._scrollable = Gtk.ScrolledWindow()
        self._scrollable.add(self._listbox)
        self.__fill_listbox()
        self._frame = Gtk.Frame()
        self._frame.add(self._scrollable)
        self._frame.set_border_width(1)
        self._frame.set_margin_bottom(self.VERTICAL_MARGIN)
        vbox = Gtk.VBox()
        vbox.pack_start(self._frame, 1, 1, 1)
        vbox.pack_end(btn_box, 0, 0, 0)
        vbox.set_margin_top(self.VERTICAL_MARGIN)
        vbox.set_margin_bottom(self.VERTICAL_MARGIN)
        vbox.set_margin_left(self.VERTICAL_MARGIN)
        vbox.set_margin_right(self.VERTICAL_MARGIN)
        win.add(vbox)
        return self._btn_reload, self._btn_settings

    def __create_window(self):
        win = Gtk.Window()
        win.set_size_request(self._window_config.width, self._window_config.height)
        win.move(self._window_config.x, self._window_config.y)
        win.set_resizable(False)
        win.set_title("SshManager GTK")

        return win

    # noinspection PyUnusedLocal
    def __btn_settings_click(self, target):
        self.__command_edit.run(application.GtkApplication.get_config_file_path())

    # noinspection PyUnusedLocal
    def __btn_reload_click(self, target):
        self._manager = application.GtkApplication.create_default_manager()
        self.__fill_listbox()

    def __fill_listbox(self):
        self._list_store.clear()
        connections = self._manager.get_connections()
        for connection in connections:
            self._list_store.append([connection.label])

        renderer = Gtk.CellRendererText()
        column = self._listbox.get_column(0)
        if not column:
            column = Gtk.TreeViewColumn(None, renderer, text=0)
            self._listbox.append_column(column)
        self._listbox.show_all()

    # noinspection PyUnusedLocal
    def __row_activated(self, target: Gtk.TreeView, path: Gtk.TreePath, column: Gtk.TreeViewColumn):
        i = path.get_indices()[0]
        connection = self._manager.get_connection(i)
        self.__command_ssh.run(connection, connection.args)
