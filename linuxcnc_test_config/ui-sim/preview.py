import sys
from PyQt5 import QtWidgets, uic

app = QtWidgets.QApplication(sys.argv)

# Change filename to your UI file
window = uic.loadUi("linuxcnc_test_config/ui-sim/ui_panel.ui")

window.show()
sys.exit(app.exec_())
