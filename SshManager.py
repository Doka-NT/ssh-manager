import json
import os
import shutil
import subprocess
from PyQt4 import QtGui

from PyQt4.QtCore import pyqtSlot, SIGNAL, SLOT


class SshManager(QtGui.QWidget):
    layout = None
    text_edit = None
    list_file = 'config.json'
    list_file_template = 'config-dist.json'
    config = None
    list_widget = None

    def __init__(self, parent=None, flags=0):
        QtGui.QWidget.__init__(self, parent)
        # Set up UI
        self.setup_ui()
        # Connect slots
        self.connect_slots()

        # Load connections
        self.connections_load()

        # update connections list
        self.update_connection_list()

    def setup_ui(self):
        """ Setup main UI """
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('SSH Manager')
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        self.layout = QtGui.QVBoxLayout(self)

        add_label = QtGui.QLabel()
        add_label.setText("Add connection:")
        self.layout.addWidget(add_label)
        # new connection box
        self.text_edit = QtGui.QLineEdit(self)
        self.text_edit.setFixedHeight(26)
        self.text_edit.setPlaceholderText("root@example.com")
        self.layout.addWidget(self.text_edit)

        list_label = QtGui.QLabel()
        list_label.setText("Available connections:")
        self.layout.addWidget(list_label)
        # Connections list
        self.list_widget = QtGui.QListWidget(self)
        self.layout.addWidget(self.list_widget)

    def connect_slots(self):
        """ Connect SIGNAL with SLOTS """
        self.text_edit.connect(self.text_edit, SIGNAL("returnPressed()"), self, SLOT("return_pressed()"))
        # self.list_widget.connect(
        #     self.list_widget,
        #     SIGNAL("itemClicked(QListWidgetItem)"),
        #     self,
        #     SLOT("list_widget_item_double_clicked(QListWidgetItem)")
        # )
        self.list_widget.itemDoubleClicked.connect(self.list_widget_item_double_clicked)

    def connections_load(self):
        """ Load saved connections """
        dirname = os.path.dirname(__file__)
        config_file_path = os.path.join(dirname, self.list_file)
        # create default config file if not exists
        if not os.path.isfile(config_file_path):
            shutil.copyfile(os.path.join(dirname, self.list_file_template), os.path.join(dirname, self.list_file))

        with open(config_file_path) as data_file:
            self.config = json.load(data_file)

    def update_connection_list(self):
        """ Update connection list widget """
        for connection in self.config['connections']:
            self.list_widget.addItem(connection['uri'])

    @pyqtSlot("QListWidgetItem")
    def list_widget_item_double_clicked(self, item):
        """

        :param item:QListWidgetItem
        :return:
        """
        # item = QtGui.QListWidgetItem()
        uri = item.text()
        # command = "gnome-terminal"
        subprocess.Popen(["gnome-terminal", "-x", "ssh", uri])

    @pyqtSlot()
    def return_pressed(self):
        """ SLOT text_edit -> return pressed """
        connect_string = self.text_edit.text()
        print connect_string

