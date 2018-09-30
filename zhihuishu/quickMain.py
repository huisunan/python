from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread


import sys
from quickWindow import window
from quick import zhihuishu

class start(QThread):
    def __init__(self, parent=None):
        super(start, self).__init__(parent)
    def run(self):
        handles = z.browser.window_handles
        z.browser.switch_to_window(handles[-1])
        z.closeWarning()
        z.closeTip()
        w.study.start()

class worker(QThread):
    def __init__(self, parent=None):
        super(worker, self).__init__(parent)
    def run(self):
        z.setBrowser()
        w.pushButton.setEnabled(False)
        w.pushButton_2.setEnabled(True)

class study(QThread):
    def __init__(self, parent=None):
        super(study, self).__init__(parent)
    def run(self):
        w.pushButton_2.setEnabled(False)
        z.study()

app = QtWidgets.QApplication(sys.argv)

w = window()

w.worker = worker()
w.start = start()
w.study = study()

z = zhihuishu()
z.setTextBrower(w.textBrowser)
w.pushButton.clicked.connect(w.worker.start)
w.pushButton_2.clicked.connect(w.start.start)
w.show()


if app.exec_() == 0:
    if z != None:
        z.browser.quit()

sys.exit()