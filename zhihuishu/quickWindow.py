from quickForm import Ui_MainWindow
from PyQt5 import QtWidgets
class window(Ui_MainWindow,QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(window, self).__init__(parent)
        self.setupUi(self)