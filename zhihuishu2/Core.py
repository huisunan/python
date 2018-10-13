from Factory import FormFactory, BrowserFactory, Form
from PyQt5 import QtWidgets
import CheckVersion
import sys
import MessageBox
from openBrowserWorker import OpenBrowserWorker
from datetime import datetime
from StartClass import StartClass


class Core(object):
    def __init__(self) -> None:
        super().__init__()
        self.form = None  # type:Form
        self.browser = None

    def show_box(self, s: bool, ss):
        """

        :param s: 是否过期参数
        :return:
        """
        if not s:
            MessageBox.MessageBox(self.form, ss)
            self.form.close()

    def set_browser(self, browser):
        self.browser = browser

        self.form.start_class = StartClass(self.browser, self.form.pushButton_start)
        self.form.pushButton_start.clicked.connect(self.form.start_class.start)
        self.form.start_class.sinOut_str.connect(self.log)
        self.form.start_class.sinOut_int.connect(self.set_bar)
        self.form.start_class.sinOut_class_name.connect(self.set_label)

        self.form.pushButton_start.setEnabled(True)
        self.form.pushButton_open.setEnabled(False)

    def set_label(self, s):
        self.form.label.setText(s)

    def log(self, s: str):
        time = datetime.now().strftime("%H:%M:%S")
        self.form.textBrowser.append("["+time+"] "+s)

    def set_bar(self, value: int):
        if value is not None:
            self.form.progressBar.setValue(value)

    def worker_handle(self):
        #  版本线程启动
        self.form.worker_version = CheckVersion.CheckVersion()
        self.form.worker_version.sinOut.connect(self.show_box)
        self.form.worker_version.start()

        # 启动按钮
        self.form.worker_open_browser = OpenBrowserWorker('chrome')
        self.form.pushButton_open.clicked.connect(self.form.worker_open_browser.start)
        self.form.worker_open_browser.sinOut_browser.connect(self.set_browser)
        self.form.worker_open_browser.sinOut_str.connect(self.log)
        self.form.worker_open_browser.sinOut_bool.connect(self.show_box)

        # # 刷课按钮
        # self.form.start_class = StartClass(self.browser)
        # self.form.pushButton_start.clicked.connect(self.form.start_class.start)
        # self.form.start_class.sinOut_str.connect(self.log)
        # self.form.start_class.sinOut_int.connect(self.set_bar)
        # self.form.start_class.sinOut_class_name.connect(self.set_label)

    def start_main_thread(self):
        app = QtWidgets.QApplication(sys.argv)
        self.form = FormFactory.create_form()
        self.worker_handle()
        self.form.show()
        if app.exec_() == 0:
            if self.browser is not None:
                self.browser.quit()
        sys.exit()
