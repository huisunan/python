from selenium import webdriver
from form import Ui_MainWindow
from PyQt5 import QtWidgets


class BrowserFactory(object):
    @staticmethod
    def create_browser(b):
        if b == 'edge':
            return webdriver.Edge()
        if b == 'ie':
            return webdriver.Ie()
        if b == 'chrome':
            return webdriver.Chrome()


class Form(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setupUi(self)


class FormFactory(object):
    @staticmethod
    def create_form():
        return Form()
