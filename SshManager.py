import json
import os
import shutil
import subprocess
from PyQt4 import QtGui

from PyQt4.QtCore import pyqtSlot, SIGNAL, SLOT
from PyQt4.QtGui import QListWidgetItem


class SshManager(QtGui.QWidget):
    # Config
    list_file = 'config.json'
    list_file_template = 'config-dist.json'
    config = None

    # UI
    layout = None
    text_edit = None
    list_widget = None
    settings_btn = None

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        # Load configuration
        self.load_config_file()

        # Set up UI
        self.setup_ui()
        # Connect slots
        self.connect_slots()

        # update connections list
        self.update_connection_list()

    def setup_ui(self):
        """ Setup main UI """
        pos = self.config["window"]  # type: dict
        self.setGeometry(pos["x"], pos["y"], pos["width"], pos["height"])
        self.setWindowTitle('SSH Manager')
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        # setup main layout
        self.layout = QtGui.QVBoxLayout(self)

        # Setup list label
        list_label = QtGui.QLabel()
        list_label.setText("Available connections:")
        self.layout.addWidget(list_label)

        # Connections list
        self.list_widget = QtGui.QListWidget(self)
        self.layout.addWidget(self.list_widget)

        # Settings button
        self.settings_btn = QtGui.QPushButton()
        self.settings_btn.setText("Settings")
        self.layout.addWidget(self.settings_btn)

    def connect_slots(self):
        """ Connect SIGNAL with SLOTS """
        self.settings_btn.connect(self.settings_btn, SIGNAL("clicked()"), self, SLOT("settings_button_clicked()"))

        self.list_widget.connect(
            self.list_widget,
            SIGNAL("itemDoubleClicked(QListWidgetItem*)"),
            self,
            SLOT("list_widget_item_double_clicked(QListWidgetItem*)")
        )

    def load_config_file(self):
        """ Load saved connections """
        config_file_path = self._get_config_file_path()
        # create default config file if not exists
        if not os.path.isfile(config_file_path):
            shutil.copyfile(os.path.join(self._get_app_dir(), self.list_file_template), config_file_path)

        with open(config_file_path) as data_file:
            self.config = json.load(data_file)

    def update_connection_list(self):
        """ Update connection list widget """
        for connection in self.config['connections']:
            self.list_widget.addItem(connection['label'])

    @pyqtSlot(QListWidgetItem)
    def list_widget_item_double_clicked(self):
        """ ListWidget Double click listener """
        index = self.list_widget.selectedIndexes()[0].row()

        connection = self.config['connections'][index]  # type: dict

        if "port" in connection:
            port = connection["port"]
        else:
            port = 22

        self._run("ssh", connection['host'], "-p", str(port))

    @pyqtSlot()
    def return_pressed(self):
        """ SLOT text_edit -> return pressed """
        connect_string = self.text_edit.text()
        print connect_string

    @pyqtSlot()
    def settings_button_clicked(self):
        """ Settings button click listener"""
        self._run("edit", self._get_config_file_path())

    def _run(self, command_name, *args):
        """ Run command with args """
        command = self.config['command'][command_name] + list(args)
        subprocess.Popen(command)

    def _get_config_file_path(self):
        """ Return config file path"""
        return os.path.join(self._get_app_dir(), self.list_file)

    @staticmethod
    def _get_app_dir():
        """ Return base application directory """
        return os.path.dirname(__file__)
