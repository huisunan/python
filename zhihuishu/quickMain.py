from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread,pyqtSignal
import time
import requests
import sys
from quickWindow import window
from quick import zhihuishu
import os
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

class checkBanben(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)

    def downLoad(self, u):
        r = requests.get(u)
        with open("MicrosoftWebDriver.exe", "wb") as f:
            f.write(r.content)

    def startDown(self):
        rootPath = "c:/WINDOWS/SystemApps/"
        lis = os.listdir(rootPath)
        edgePath = ''
        for s in lis:
            if "Microsoft.MicrosoftEdge" in s:
                edgePath = s
        with open(rootPath + edgePath + "/AppxManifest.xml", "r") as f:
            lines = f.readlines()
            for ll in lines:
                if "17134" in ll:
                    self.downLoad(
                        "https://download.microsoft.com/download/F/8/A/F8AF50AB-3C3A-4BC4-8773-DC27B32988DD/MicrosoftWebDriver.exe")
                elif "16299" in ll:
                    self.downLoad(
                        "https://download.microsoft.com/download/D/4/1/D417998A-58EE-4EFE-A7CC-39EF9E020768/MicrosoftWebDriver.exe")
                elif "15063" in ll:
                    self.downLoad(
                        "https://download.microsoft.com/download/3/4/2/342316D7-EBE0-4F10-ABA2-AE8E0CDF36DD/MicrosoftWebDriver.exe")
                elif "14393" in ll:
                    self.downLoad(
                        "https://download.microsoft.com/download/3/2/D/32D3E464-F2EF-490F-841B-05D53C848D15/MicrosoftWebDriver.exe")
                elif "10586" in ll:
                    self.downLoad(
                        "https://download.microsoft.com/download/C/0/7/C07EBF21-5305-4EC8-83B1-A6FCC8F93F45/MicrosoftWebDriver.exe")
                elif "10240" in ll:
                    self.downLoad(
                        "https://download.microsoft.com/download/8/D/0/8D0D08CF-790D-4586-B726-C6469A9ED49C/MicrosoftWebDriver.exe")

    def run(self):
        if os.path.exists("MicrosoftWebDriver.exe"):
            w.textBrowser.append("驱动已下载")
            pass
        else:
            w.textBrowser.append("正在下载驱动")
            self.startDown()
            w.textBrowser.append("驱动下载完成")
        w.worker.start()




def box(str):
    QtWidgets.QMessageBox.warning(w, "警告", str, QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
    w.close()
app = QtWidgets.QApplication(sys.argv)


w = window()
#工作线程声明
w.worker = worker()
w.start = start()
w.study = study()
w.check = check()
w.banben = checkBanben()


z = zhihuishu()
z.setTextBrower(w.textBrowser)
z.setProgressBar(w.progressBar)
z.setLabel(w.label)

w.check.sinOut.connect(box)
w.pushButton.clicked.connect(w.banben.start)
w.pushButton_2.clicked.connect(w.start.start)
w.check.start()
w.show()




if app.exec_() == 0:
    if z != None:
        z.browser.quit()
sys.exit()