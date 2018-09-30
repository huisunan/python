from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread,pyqtSignal
import time
import requests
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

class check(QThread):
    sinOut = pyqtSignal(str)
    def __init__(self, parent=None):
        super(check, self).__init__(parent)
    def run(self):
        while True:
            html = requests.get("http://www.juweinan.top/zhihuishu.html")
            if html.status_code != 200:
                self.sinOut.emit("版本失效")
            time.sleep(30)

# class box(QThread):
#     def __init__(self, parent=None):
#         super(box, self).__init__(parent)
#     def run(self):
#         QtWidgets.QMessageBox.warning(w,"警告",str,QtWidgets.QMessageBox.Ok,QtWidgets.QMessageBox.Ok)
#         w.close()
def box(str):
    QtWidgets.QMessageBox.warning(w, "警告", str, QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
    w.close()
app = QtWidgets.QApplication(sys.argv)


w = window()
w.worker = worker()
w.start = start()
w.study = study()
w.check = check()
w.check.start()


z = zhihuishu()
z.setTextBrower(w.textBrowser)

w.check.sinOut.connect(box)
w.pushButton.clicked.connect(w.worker.start)
w.pushButton_2.clicked.connect(w.start.start)
w.show()


if app.exec_() == 0:
    if z != None:
        z.browser.quit()

sys.exit()