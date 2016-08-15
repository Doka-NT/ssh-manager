#!/usr/bin/python
# simple.py

import sys
from PyQt4 import QtGui

from SshManager import SshManager

app = QtGui.QApplication(sys.argv)

sshManager = SshManager()
sshManager.show()

sys.exit(app.exec_())