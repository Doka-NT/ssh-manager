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

    __command_ssh = None
    __command_edit = None

    _listbox = None
    _frame = None
    _scrollable = None
    _list_store = Gtk.ListStore(str)

    def __init__(
            self, manager: Manager,
            window_config: Window,
            command_ssh: AbstractCommand,
            command_edit: AbstractCommand
    ):
        self.__command_ssh = command_ssh
        self.__command_edit = command_edit
        self._manager = manager
        self._window_config = window_config

    def show(self):
        win = Gtk.Window()
        win.set_size_request(self._window_config.width, self._window_config.height)
        win.move(self._window_config.x, self._window_config.y)
        win.set_resizable(False)

        btn_setting = Gtk.Button("Settings")
        btn_setting.set_margin_right(self.HORIZONTAL_MARGIN)
        btn_reload = Gtk.Button("Reload")

        btn_box = Gtk.HBox()
        btn_box.add(btn_setting)
        btn_box.add(btn_reload)

        self._listbox = Gtk.TreeView(self._list_store)
        self._listbox.set_headers_visible(False)
        self._listbox.connect("row-activated", self.row_activated)

        self._scrollable = Gtk.ScrolledWindow()
        self._scrollable.add(self._listbox)
        self._fill_listbox()

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

        btn_setting.connect("clicked", self.btn_settings_click)
        btn_reload.connect("clicked", self.btn_reload_click)

        win.add(vbox)

        win.set_title("SshManager GTK")
        win.connect("delete-event", Gtk.main_quit)
        win.show_all()
        Gtk.main()

    # noinspection PyUnusedLocal
    def btn_settings_click(self, target):
        self.__command_edit.run(application.GtkApplication.get_config_file_path())

    # noinspection PyUnusedLocal
    def btn_reload_click(self, target):
        self._manager = application.GtkApplication.create_default_manager()
        self._fill_listbox()

    def _fill_listbox(self):
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
    def row_activated(self, target: Gtk.TreeView, path: Gtk.TreePath, column: Gtk.TreeViewColumn):
        i = path.get_indices()[0]
        connection = self._manager.get_connection(i)
        self.__command_ssh.run(connection, connection.args)
