from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtWidgets
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
import time


class StartClass(QThread):
    sinOut_str = pyqtSignal(str)  # 字符串信号变量
    sinOut_int = pyqtSignal(int)  # 进度变量
    sinOut_class_name = pyqtSignal(str)  # 课程名

    def switch_window_by_url(self, url):
        handles = self.browser.window_handles
        for i in handles:
            self.browser.switch_to_window(i)
            if url in self.browser.current_url:
                return True
        return False

    def __close_warning(self):
        try:
            self.browser.find_element_by_class_name("wrap_popboxes")
            self.browser.find_element_by_class_name("popbtn_yes").click()
            return "true"
        except NoSuchElementException:
            return "false"

    def __close_tip(self):
        try:
            style = self.browser.find_element_by_id("j-assess-criteria_popup").get_attribute('style')
            if "none" not in style:
                self.browser.find_element_by_class_name("popup_delete").click()
                return "true"
            return "false"
        except NoSuchElementException:
            return "exception"

    def __get_class_name(self):
        return self.browser.find_element_by_id("lessonOrder").text

    def __open_bar(self):
        element = self.browser.find_element_by_class_name("controlsBar")
        style = element.get_attribute("style")
        if "none" in style:
            self.browser.execute_script('document.querySelector(".controlsBar").style.display="block"')

    def __get_play_state(self):
        try:
            state = self.browser.find_element_by_id("playButton").get_attribute("class")
            if state == "playButton":
                return "pause"
            else:
                return "play"
        except NoSuchElementException:
            return "exception"

    def __get_pause_condition(self):
        if self.browser.find_element_by_class_name("currentTime").text == self.browser.find_element_by_class_name("duration").text or ("100%" in self.browser.find_element_by_class_name("passTime").get_attribute("style")) or ("100%" in self.browser.find_element_by_class_name("progressbar").get_attribute("style")):
            return "end"
        else:
            return "pause"

    def __jump_next(self):
        if self.type == 'chrome':
            self.__open_bar()

            try:
                self.browser.find_element_by_id("nextBtn").click()
            except ElementNotVisibleException:
                self.__open_bar()
                self.browser.find_element_by_id("nextBtn").click()

        elif self.type == 'MicrosoftEdge':
            self.browser.execute_script('document.querySelector("#nextBtn").click()')

    def __close_volume(self):
        self.__open_bar()
        try:
            if "volumeNone" not in self.browser.find_element_by_class_name("volumeBox").get_attribute("class"):
                self.browser.find_element_by_class_name("volumeIcon").click()
                return "have"
        except:
            if "volumeNone" not in self.browser.find_element_by_class_name("volumeBox").get_attribute("class"):
                self.__open_bar()
                self.browser.find_element_by_class_name("volumeIcon").click()
                return "have"
        return "had"

    def __start_accelerate(self):
        self.__open_bar()
        try:
            if "0.5" in self.browser.find_element_by_class_name("speedBox").get_attribute("style"):
                self.browser.execute_script('document.querySelector(".speedList").style.display="block";')
                self.__open_bar()
                self.browser.find_element_by_class_name("speedTab15").click()
                return "have"
        except Exception as err:
            print(err)
        return "had"

    def __get_percent(self):
        try:
            current_time: str = self.browser.find_element_by_class_name("currentTime").text
            total_time: str = self.browser.find_element_by_class_name("duration").text
            cArr = current_time.split(':')
            tArr = total_time.split(':')
            c = int(cArr[0]) * 60 * 60 + int(cArr[1]) * 60 + int(cArr[2])
            t = int(tArr[0]) * 60 * 60 + int(tArr[1]) * 60 + int(tArr[2])
            percent = c * 100 / t
            if percent == 0:
                return None
            else:
                return percent
        except:
            return None

    def __get_select_condition(self):
        try:
            self.browser.find_element_by_class_name("popboxes_close")
            return "have"
        except NoSuchElementException:
            return "not"

    def __close_select(self):
        self.browser.find_element_by_class_name("popboxes_close").click()

    def __play(self):
        try:
            self.browser.find_element_by_id("playButton").click()
        except:
            self.__open_bar()
            self.browser.find_element_by_id("playButton").click()

    def __get_last_lesson(self):
        if "none" in self.browser.find_element_by_class_name("next_lesson_bg").get_attribute("style"):
            return True
        else:
            return False

    def __write_cookies(self):
        with open('cookie.coo', 'w', encoding='utf-8') as f:
            s = str(self.browser.get_cookies())
            s.replace('null', 'None')
            s.replace('false', 'False')
            f.write(s)

    def __init__(self, browser:webdriver.Remote, btn:QtWidgets.QPushButton,parent=None):
        super().__init__(parent)
        self.browser = browser
        self.type = self.browser.capabilities.get('browserName')
        self.btn = btn

    def run(self):
        self.btn.setEnabled(False)
        if self.switch_window_by_url('http://study.zhihuishu.com/learning/videoList') is False:
            self.sinOut_str.emit("未正常打开页面")
            return
        # self.__write_cookies()
        if self.__close_warning() == "true":
            self.sinOut_str.emit("关闭警告框")
        time.sleep(2)
        if self.__close_tip() == "true":
            self.sinOut_str.emit("关闭提示卡")
        time.sleep(2)

        lastName = self.__get_class_name()
        newName = self.__get_class_name()
        while True:
            if self.__get_play_state() == "pause":
                if self.__get_pause_condition() == "end":
                    if self.__get_last_lesson():
                        self.sinOut_str.emit("已结束")
                        break
                    else:
                        self.__jump_next()
                        self.sinOut_str.emit(self.__get_class_name() + "已完成")
                        self.sinOut_str.emit("跳转到下一节")
                        newName = self.__get_class_name()
                        while True:
                            if newName != lastName:
                                lastName = newName
                                break
                            newName = self.__get_class_name()
                            time.sleep(0.5)
                else:
                    if self.__get_select_condition() == "have":
                        time.sleep(2)
                        self.__close_select()
                        self.sinOut_str.emit("关闭选择题")
            elif self.__get_play_state() == "play":
                self.__open_bar()
                if self.__close_volume() == "have":
                    self.sinOut_str.emit("关闭声音")
                if self.__start_accelerate() == "have":
                    self.sinOut_str.emit("开启加速")
                self.sinOut_class_name.emit(self.__get_class_name())
                self.sinOut_int.emit(self.__get_percent())
            elif self.__get_play_state() == "exception":
                self.sinOut_str.emit("异常")
            time.sleep(1)
