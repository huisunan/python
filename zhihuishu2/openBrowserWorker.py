from PyQt5.QtCore import QThread, pyqtSignal
from selenium import webdriver
from Factory import BrowserFactory
import os
import requests
import zipfile
from webbrowser import open as web_open

def check_browser_version(s):
    """
    检测浏览器版本
    :return:
    """
    if s == 'edge':
        root_path = 'c:/WINDOWS/SystemApps/'
        lis = os.listdir(root_path)
        edge_path = ''
        for s in lis:
            if "Microsoft.MicrosoftEdge" in s:
                edge_path = s
        with open(root_path + edge_path + "/AppxManifest.xml", "r") as f:
            lines = f.readlines()
            for ll in lines:
                if "17134" in ll:
                    down_load(
                        "https://download.microsoft.com/download/F/8/A/F8AF50AB-3C3A-4BC4-8773-DC27B32988DD"
                        "/MicrosoftWebDriver.exe", "MicrosoftWebDriver.exe")
                    break
                elif "16299" in ll:
                    down_load(
                        "https://download.microsoft.com/download/D/4/1/D417998A-58EE-4EFE-A7CC-39EF9E020768"
                        "/MicrosoftWebDriver.exe", "MicrosoftWebDriver.exe")
                    break
                elif "15063" in ll:
                    down_load(
                        "https://download.microsoft.com/download/3/4/2/342316D7-EBE0-4F10-ABA2-AE8E0CDF36DD"
                        "/MicrosoftWebDriver.exe", "MicrosoftWebDriver.exe")
                    break
                elif "14393" in ll:
                    down_load(
                        "https://download.microsoft.com/download/3/2/D/32D3E464-F2EF-490F-841B-05D53C848D15"
                        "/MicrosoftWebDriver.exe", "MicrosoftWebDriver.exe")
                    break
                elif "10586" in ll:
                    down_load(
                        "https://download.microsoft.com/download/C/0/7/C07EBF21-5305-4EC8-83B1-A6FCC8F93F45"
                        "/MicrosoftWebDriver.exe", "MicrosoftWebDriver.exe")
                    break
                elif "10240" in ll:
                    down_load(
                        "https://download.microsoft.com/download/8/D/0/8D0D08CF-790D-4586-B726-C6469A9ED49C"
                        "/MicrosoftWebDriver.exe", "MicrosoftWebDriver.exe")
                    break
    if s == 'chrome':
        try:
            root_path = 'C:\Program Files (x86)\Google\Chrome\Application'
            lis = os.listdir(root_path)
            down_path = 'http://npm.taobao.org/mirrors/chromedriver/'
            version = 0
            w_version = 0
            for i in lis:
                if i.count('.') == 3:
                    version = int(i.split('.')[0])
                    break
            if 68 <= version <= 70:
                w_version = '2.42'
            elif version == 66:
                w_version = '2.41'
            elif version == 65:
                w_version = '2.38'
            elif version == 64:
                w_version = '2.37'
            elif version == 63:
                w_version = '2.36'
            elif version == 62:
                w_version = '2.35'

            down_load(down_path+w_version+'/'+'chromedriver_win32.zip','chromedriver_win32.zip')
            f = zipfile.ZipFile('chromedriver_win32.zip', 'r')
            f.extractall()
        except:
            return 'not'


def check_file(filename):
    """
    检测文件是否存在
    :param filename: 文件名
    :return:
    """

    lis = os.listdir('.')
    for i in lis:
        if filename in i:
            return True
    return False


def down_load(url, filename):
    """
    :param url: 下载地址
    :param filename: 保存文件名
    :return:
    """

    r = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(r.content)


# class LoadCookiesWorker(QThread):
#
#     def __init__(self, browser, parent=None):
#         super().__init__(parent)
#         self.browser = browser
#
#     def run(self):
#


class OpenBrowserWorker(QThread):
    sinOut_browser = pyqtSignal(webdriver.Remote)
    sinOut_str = pyqtSignal(str)
    sinOut_bool = pyqtSignal(bool)
    # def __add_cookies(self):
    #     if check_file('cookie.coo'):
    #         with open('cookie.coo', 'r', encoding='utf-8') as f:
    #             lis = list(f.readlines())
    #             dic = eval(lis[0])
    #             for d in dic:
    #                 self.browser.add_cookie(cookie_dict=d)
    #             return True
    #     return False

    def __init__(self, type, parent=None):
        super().__init__(parent)
        self.browser = None
        self.type = type

    def run(self):
        if self.type == 'edge':
            if check_file('MicrosoftWebDriver.exe'):
                self.sinOut_str.emit('驱动已下载')
                pass
            else:
                self.sinOut_str.emit('正在下载驱动')
                check_browser_version(self.type)
                self.sinOut_str.emit('驱动下载完成')

            self.browser = BrowserFactory.create_browser('edge')

            self.sinOut_str.emit('打开浏览器')
            self.browser.get("http://www.zhihuishu.com")
            self.sinOut_browser.emit(self.browser)

        if self.type == 'chrome':
            if check_file('chromedriver.exe'):
                self.sinOut_str.emit('驱动已下载')
            else:
                self.sinOut_str.emit('正在下载驱动')
                if check_browser_version(self.type) == 'not':
                    self.sinOut_str.emit('chrome浏览器尚未下载')
                    web_open('https://www.google.cn/chrome/', 0, autoraise=True)
                    self.sinOut_bool.emit(False, '请安装chrome浏览器，并重启软件')
                    return
                self.sinOut_str.emit('驱动下载完成')

            self.browser = BrowserFactory.create_browser('chrome')

            self.sinOut_str.emit('打开浏览器')
            self.browser.get("http://www.zhihuishu.com")
            try:
                self.sinOut_browser.emit(self.browser)
            except Exception as err:
                print(err)
