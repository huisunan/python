from PyQt5 import QtWidgets


def MessageBox(w: QtWidgets.QMainWindow, s:str):
    QtWidgets.QMessageBox.warning(w, "警告",  s, QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)