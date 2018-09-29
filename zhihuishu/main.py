from temp import zhiHui
from myWindow import myWindow
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread
def login():
    mw.loginworker.start()
class loginWorker(QThread):
    def __init__(self,parent=None):
        super(loginWorker, self).__init__(parent)
    def run(self):
        mw.pushButton.setEnabled(False)
        username = mw.txtUsername.text()
        password = mw.txtPassword.text()
        if username == "" or password == "":
            QtWidgets.QMessageBox.warning(mw, "警告", "账户密码不为空", QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            mw.pushButton.setEnabled(True)
            return
        z = zhiHui()
        z.turnLoginUrl()
        z.login(username, password)
        if z.isLogin():
            mw.pushButton.setEnabled(True)
            pass
        else:
            QtWidgets.QMessageBox.information(mw, "tip", "登陆失败", QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

print("start")
app = QtWidgets.QApplication(sys.argv)
######界面正式启动
mw = myWindow()
mw.loginworker = loginWorker()
global z
mw.pushButton.clicked.connect(login)
mw.show()
sys.exit(app.exec_())