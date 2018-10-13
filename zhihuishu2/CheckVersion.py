from PyQt5.QtCore import QThread, pyqtSignal
import requests
import time


class CheckVersion(QThread):
    sinOut: pyqtSignal = pyqtSignal(bool, str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        time.sleep(5)
        while True:
            r = requests.get("http://139.199.106.104/zhihuishu.html")
            if r.text.strip() != "1.0":
                self.sinOut.emit(False, '版本过期')
            time.sleep(30)
