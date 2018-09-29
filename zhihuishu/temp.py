from selenium import webdriver
import getChrome
import re
import time
import random
from selenium.webdriver.common.action_chains import ActionChains

class zhiHui():
    def __init__(self):
        self.browser = webdriver.Chrome()
        #self.browser = getChrome.getChrome()
    def openUrl(self, url):
        self.browser.get(url)

    def __mousemove(self, element):
        ActionChains(self.browser).move_to_element(element)

    def input(self,element,txt):
        self.__mousemove(element)
        element.clear()
        element.send_keys(txt)

    def click(self,element):
        self.__mousemove(element)
        element.click()

    def sleep(self,a,b):
        time.sleep(random.randint(a, b))

    def turnLoginUrl(self):
        self.openUrl("https://www.zhihuishu.com")
        self.click(self.browser.find_elements_by_css_selector("#login-register li a")[0])
        self.log("正在打开登陆页面")
        self.sleep(3,5)

    def login(self,username,password):
        if self.isUrlMatch("https://passport.zhihuishu.com/login?"):
            self.input(self.browser.find_element_by_id("lUsername"), username)
            self.sleep(1, 2)
            self.input(self.browser.find_element_by_id("lPassword"), password)
            self.sleep(1, 2)
            self.click(self.browser.find_elements_by_css_selector("input[name=rememberMe]")[0])
            self.click(self.browser.find_elements_by_css_selector("#f_sign_up div span")[0])
            self.log("登录中...")
            self.sleep(3,5)
        else:
            self.log("地址错误")

    def isLogin(self):
        if self.isUrlSearch("http://online.zhihuishu.com/onlineSchool/student/index"):
            return True
        else:
            return False

    def setStudyList(self):
        if self.isUrlSearch("http://online.zhihuishu.com/onlineSchool/student/index"):
            self.studyList = self.browser.find_elements_by_css_selector(".speedPromote_btn")
        else:
            self.log("登陆错误")
    def getWindows(self):
        self.windows = self.browser.window_handles
        return self.windows

    def switchWindow(self, window):
        self.browser.switch_to_window(window)
        self.log("切换窗口")



    def openBar(self):
        if re.search("none", self.browser.find_elements_by_css_selector(".controlsBar")[0].get_attribute("style")) != None:
            self.browser.execute_script('document.querySelector(".controlsBar").style.display="block"')

    # 关闭警告框
    def closeWarning(self):
        if len(self.browser.find_elements_by_class_name("wrap_popboxes")) > 0:
            self.click(self.browser.find_element_by_class_name("popbtn_yes"))
            self.log("关闭提示框")

    #关闭学习卡片
    def closeTip(self):
        tip1 = self.browser.find_elements_by_css_selector("#j-assess-criteria_popup")[0].get_attribute("style")
        if re.search("none", tip1) == None:
            self.click(self.browser.find_elements_by_css_selector(".popup_delete")[0])
            self.log("关闭显示卡")

    #开始自动刷课
    def study(self):
        while True:
            self.browser.save_screenshot("a.png")
            self.openBar()
            time.sleep(random.randint(1, 2))
            currentTime = self.browser.find_elements_by_css_selector(".currentTime")[0].text

            totalTime = self.browser.find_elements_by_css_selector(".duration")[0].text

            self.log("%s/%s" % (currentTime, totalTime))

            # 自动跳转
            if re.search("100%",
                         self.browser.find_elements_by_css_selector(".progressbar_box>div")[0].get_attribute("style")) \
                    or (currentTime == totalTime and currentTime != "" and currentTime != ""):
                self.openBar()
                try:
                    self.click(self.browser.find_elements_by_css_selector("#nextBtn")[0])
                except:
                    self.openBar()
                    self.click(self.browser.find_elements_by_css_selector("#nextBtn")[0])
                self.log("下一节")
                time.sleep(10)
                lastLesson = self.browser.find_elements_by_css_selector(".next_lesson_bg")[0].get_attribute("style")
                if re.search("none", lastLesson) != None and currentTime == totalTime:
                    self.log("success")
                    break
                continue

            # 最后一节 .next_lesson_bg

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



       #####工具
    def log(self,txt):
        print(txt)

    def isUrlMatch(self,url):
        if re.match(url, self.browser.current_url):
            return True
        else:
            return False

    def isUrlSearch(self,url):
        if re.search(url, self.browser.current_url):
            return True
        else:
            return False

if __name__ == "__main__":
    z = zhiHui()
    z.turnLoginUrl()
    z.login("18860825826", "liyin780816")
    while True:
        if z.isLogin():
            z.setStudyList()
            break
    z.click(z.studyList[1])
    w = z.getWindows()
    z.switchWindow(w[-1])
    while True:
        if z.isUrlSearch("http://study.zhihuishu.com/learning/"):
            z.sleep(3,5)
            z.closeWarning()
            z.sleep(3,5)
            z.closeTip()
            break
    z.study()
