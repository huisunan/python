from window import Ui_MainWindow
from PyQt5 import QtWidgets
import sys
class myWindow(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(myWindow, self).__init__(parent)
        self.setupUi(self)

# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     w = myWindow()
#     w.show()
#     sys.exit(app.exec_())