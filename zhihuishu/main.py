from temp import zhiHui
from myWindow import myWindow
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
def login():
    mw.loginworker.start()

class loginWorker(QThread):
    sinOut = pyqtSignal(str)
    def __init__(self,parent=None):
        super(loginWorker, self).__init__(parent)
    def run(self):
        mw.pushButton.setEnabled(False)
        username = mw.txtUsername.text()
        password = mw.txtPassword.text()
        if username == "" or password == "":
            # QtWidgets.QMessageBox.information(mw, "tip", "账号密码不为空", QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            self.sinOut.emit("账号密码不为空")
            mw.pushButton.setEnabled(True)
            return
        if mw.radioButton.isChecked():
            z.setBrowser("no")
        else:
            z.setBrowser("1")
        z.setTextBrower(mw.textBrowser)
        z.turnLoginUrl()
        z.login(username, password)


        if z.isLogin():
            mw.pushButton_2.setEnabled(False)
            mw.txtUsername.setEnabled(False)
            mw.txtPassword.setEnabled(False)
            z.setStudyList()
            z.log("检测到的学习列表")
            j = 0
            for i in z.sutdyListName:

                z.log(i.text+"----科目代号:"+str(j))
                j += 1


        else:
            self.sinOut.emit("登陆失败")
            return

def box(str):
    QtWidgets.QMessageBox.information(mw, "tip",str, QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

def study():
    mw.studyworker.start()

class studyWorker(QThread):
    sinOut = pyqtSignal(str)
    def __init__(self, parent=None):
        super(studyWorker, self).__init__(parent)
    def run(self):
        id = int(mw.spinBox.text())
        if id >= len(z.sutdyListName):
            self.sinOut.emit("请输入有效代号")
        else:
            if id > 1:
                z.click(z.btns[1])
                z.sleep(2,4)
                mw.pushButton_3.setEnabled(False)
            z.click(z.studyList[id])
            w = z.getWindows()
            z.switchWindow(w[-1])
            while True:
                if z.isUrlSearch("http://study.zhihuishu.com/learning/"):
                    z.sleep(3, 5)
                    z.closeWarning()
                    z.sleep(3, 5)
                    z.closeTip()
                    break

'''
"18860825826", "liyin780816"
'''
print("start")
app = QtWidgets.QApplication(sys.argv)
######界面正式启动
mw = myWindow()
z = zhiHui()
#注册线程

mw.loginworker = loginWorker()
mw.loginworker.sinOut.connect(box)

mw.studyworker = studyWorker()
mw.studyworker.sinOut.connect(box)

mw.pushButton.clicked.connect(login)
mw.pushButton_3.clicked.connect(study)


mw.show()
if app.exec_() == 0:
    if z != None:
        z.quit()
    sys.exit()


