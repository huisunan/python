import re

from PyQt5.QtWidgets import QProgressBar, QLabel
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import time
import random
class zhihuishu():
    def __init__(self):
        pass
    def setBrowser(self,s=None):
        self.browser = webdriver.Edge()
        self.browser.get("https://www.zhihuishu.com")
    def __mousemove(self, element):
        ActionChains(self.browser).move_to_element(element)

    def click(self, element):
        self.__mousemove(element)
        element.click()

    def setLabel(self,label1:QLabel):
        self.label = label1

    def setProgressBar(self,bar1:QProgressBar):
        self.bar = bar1


    def setTextBrower(self, brow):
        self.textBrower = brow

    def sleep(self,a,b):
        time.sleep(random.randint(a, b))

    def log(self,txt):
        tim = datetime.now().strftime("%H:%M:%S")
        if self.textBrower != None:
            self.textBrower.append("[" + tim + "] " + txt)
        else:
            print(txt)

    def openBar(self):
        if re.search("none", self.browser.find_elements_by_css_selector(".controlsBar")[0].get_attribute("style")) != None:
            self.browser.execute_script('document.querySelector(".controlsBar").style.display="block"')

    # 关闭警告框
    def closeWarning(self):
        if len(self.browser.find_elements_by_class_name("wrap_popboxes")) > 0:
            self.click(self.browser.find_element_by_class_name("popbtn_yes"))
            self.log("关闭提示框")
            self.sleep(1, 3)

    #关闭学习卡片
    def closeTip(self):
        tip1 = self.browser.find_elements_by_css_selector("#j-assess-criteria_popup")[0].get_attribute("style")
        #tip1 = self.browser.find_elements_by_css_selector("#j-assess-criteria_popup")[0].get_attribute("style")
        if re.search("none", tip1) == None:
            self.click(self.browser.find_elements_by_css_selector(".popup_delete")[0])
            self.log("关闭显示卡")
            self.sleep(1, 3)


    # 开始自动刷课
    def study(self):
        name = None
        currentTime = ''
        totalTime = ''
        while True:
            if re.search("http://study.zhihuishu.com/learning/videoList", self.browser.current_url) == None:
                self.log("没有正确打开页面")
                break
            if name is None:
                try:
                    name = self.browser.find_element_by_id("lessonOrder").text
                    self.log(name)
                    self.label.setText(name)
                except:
                    print('异常')
                    continue
            self.openBar()
            time.sleep(1)
            try:
                self.openBar()
                currentTime = self.browser.find_elements_by_css_selector(".currentTime")[0].text
                totalTime = self.browser.find_elements_by_css_selector(".duration")[0].text
                cArr = currentTime.split(':')
                tArr = totalTime.split(':')
                ic = int(cArr[0]) * 60 * 60 + int(cArr[1]) * 60 + int(cArr[2])
                it = int(tArr[0]) * 60 * 60 + int(tArr[1]) * 60 + int(tArr[2])
                # self.bar.valueChanged(int(ic * 100 / it))
                if it != 0 and ic != 0:
                    try:
                        value = int((ic * 100) / it)
                        self.bar.setValue(value)
                    except Exception:
                        print("工具条异常")


            except :
                self.log('异常')
            # 自动跳转
            if re.search("100%",self.browser.find_elements_by_css_selector(".progressbar_box>div")[0].get_attribute("style")) or ((currentTime == totalTime) and currentTime != "" and currentTime != ""):
                self.openBar()
                try:
                    self.click(self.browser.find_elements_by_css_selector("#nextBtn")[0])
                except:
                    self.openBar()
                    self.click(self.browser.find_elements_by_css_selector("#nextBtn")[0])
                self.log("下一节")
                lastLesson = self.browser.find_elements_by_css_selector(".next_lesson_bg")[0].get_attribute("style")
                if re.search("none", lastLesson) is not None:
                    self.log("success")
                    break
                name = None
                time.sleep(5)
                continue

            # 最后一节 .next_lesson_bg

            if re.search("volumeNone", self.browser.find_element_by_class_name("volumeBox").get_attribute("class")) == None:
                self.openBar()
                self.click(self.browser.find_element_by_class_name("volumeIcon"))
                self.log("关闭声音")
            # 自动播放
            playStat = self.browser.find_elements_by_css_selector("#playButton")[0].get_attribute("class")
            if playStat == "playButton":
                if len(self.browser.find_elements_by_css_selector(".popboxes_close")) > 0:
                    self.click(self.browser.find_elements_by_css_selector(".popboxes_close")[0])
                    self.log("关闭选择题")
                    self.sleep(1,2)
                else:
                    self.openBar()
                    try:
                        self.click(self.browser.find_elements_by_css_selector("#playButton")[0])
                    except:
                        self.openBar()
                        self.click(self.browser.find_elements_by_css_selector("#playButton")[0])
                    self.log("开始播放")

            beishu = ''
            try:
                beishu = self.browser.find_elements_by_css_selector(".speedBox")[0].get_attribute("style")
            except:
                self.openBar()
                beishu = self.browser.find_elements_by_css_selector(".speedBox")[0].get_attribute("style")
            if re.search("0.5", beishu) != None:
                self.openBar()
                try:
                    self.__mousemove(self.browser.find_elements_by_css_selector(".speedBox")[0])
                    self.browser.execute_script('document.querySelector(".speedList").style.display="block";')
                    self.openBar()
                    self.click(self.browser.find_elements_by_css_selector(".speedTab15")[0])
                except:
                    self.browser.execute_script('document.querySelector(".speedList").style.display="block";')
                    self.openBar()
                    self.click(self.browser.find_elements_by_css_selector(".speedTab15")[0])
                self.browser.execute_script('document.querySelector(".speedList").style.display="none";')
                self.log("启动加速")


