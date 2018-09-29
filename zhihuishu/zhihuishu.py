# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'zhihuishu'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets
from selenium import webdriver
import re
import time
import random
from selenium.webdriver.common.action_chains import ActionChains


def textInput(element, txt):
    element.clear()
    element.send_keys(txt)


# "18860825826"
def login(user, password):
    textInput(browser.find_element_by_id("lUsername"), user)
    time.sleep(2)
    textInput(browser.find_element_by_id("lPassword"), password)


def mousemove(element):
    ActionChains(browser).move_to_element(element)


if __name__ == "__main__":
    browser = webdriver.Chrome()
    browser.get("https://www.zhihuishu.com")
    btn = browser.find_elements_by_css_selector("#login-register li a")
    mousemove(btn[0])
    btn[0].click()  # 登录按钮
    # print(browser.current_url)

    loginUrl = browser.current_url
    if re.match("https://passport.zhihuishu.com/login?", loginUrl):
        login("18860825826", "liyin780816")
        browser.find_elements_by_css_selector("input[name=rememberMe]")[0].click()
        browser.find_elements_by_css_selector("#f_sign_up div span")[0].click()

    time.sleep(5)
    print(browser.current_url)
    studyList = browser.find_elements_by_css_selector(".speedPromote_btn")  # 学习按钮
    time.sleep(random.randint(5, 10))

    studyList[1].click()  # 在新窗口打开的链接
    time.sleep(random.randint(5, 10))
    windows = browser.window_handles
    browser.switch_to_window(windows[-1])
    print(browser.current_url)
    time.sleep(5)
    currentTime = ''
    totalTime = ''  # duration  id:playButton{playButton,pauseButton}   id:nextBtn   .speedBox{.speedTab15}  popup_delete推出  popboxes_close

    js = 'document.querySelector(".controlsBar").style.display="block"'


    def openBar():
        if re.search("none", browser.find_elements_by_css_selector(".controlsBar")[0].get_attribute("style")) != None:
            browser.execute_script(js)


    # 关闭警告框
    if len(browser.find_elements_by_class_name("wrap_popboxes")) > 0:
        btn_yes = browser.find_element_by_class_name("popbtn_yes")
        mousemove(btn_yes)
        btn_yes.click()
        print("关闭提示框")
        time.sleep(random.randint(1, 2))

    # 关闭提示卡
    tip1 = browser.find_elements_by_css_selector("#j-assess-criteria_popup")[0].get_attribute("style")
    if re.search("none", tip1) == None:
        mousemove(browser.find_elements_by_css_selector(".popup_delete")[0])
        browser.find_elements_by_css_selector(".popup_delete")[0].click()
        print("关闭显示卡")
        time.sleep(random.randint(1, 2))

    while True:

        openBar()
        time.sleep(random.randint(1, 2))
        currentTime = browser.find_elements_by_css_selector(".currentTime")[0].text

        totalTime = browser.find_elements_by_css_selector(".duration")[0].text

        print("%s/%s" % (currentTime, totalTime))

        # 自动跳转
        if re.search("100%", browser.find_elements_by_css_selector(".progressbar_box>div")[0].get_attribute("style")) \
                or (currentTime == totalTime and currentTime != "" and currentTime != ""):
            openBar()
            try:
                browser.find_elements_by_css_selector("#nextBtn")[0].click()
            except:
                openBar()
                browser.find_elements_by_css_selector("#nextBtn")[0].click()
            print("下一节")
            time.sleep(10)
            lastLesson = browser.find_elements_by_css_selector(".next_lesson_bg")[0].get_attribute("style")
            if re.search("none", lastLesson) != None and currentTime == totalTime:
                print("success")
                break
            continue

        # 最后一节 .next_lesson_bg

        # 自动播放
        playStat = browser.find_elements_by_css_selector("#playButton")[0].get_attribute("class")
        if playStat == "playButton":
            if len(browser.find_elements_by_css_selector(".popboxes_close")) > 0:
                mousemove(browser.find_elements_by_css_selector(".popboxes_close")[0])
                browser.find_elements_by_css_selector(".popboxes_close")[0].click()
                print("关闭选择题")
                time.sleep(random.randint(1, 2))
            else:
                openBar()
                try:
                    browser.find_elements_by_css_selector("#playButton")[0].click()
                except:
                    openBar()
                    browser.find_elements_by_css_selector("#playButton")[0].click()
                print("开始播放")

        beishu = ''
        try:
            beishu = browser.find_elements_by_css_selector(".speedBox")[0].get_attribute("style")
        except:
            openBar()
            beishu = browser.find_elements_by_css_selector(".speedBox")[0].get_attribute("style")
        if re.search("0.5", beishu) != None:
            openBar()
            try:
                mousemove(browser.find_elements_by_css_selector(".speedBox")[0])
                browser.execute_script('document.querySelector(".speedList").style.display="block";')
                openBar()
                browser.find_elements_by_css_selector(".speedTab15")[0].click()
            except:
                browser.execute_script('document.querySelector(".speedList").style.display="block";')
                openBar()
                mousemove(browser.find_elements_by_css_selector(".speedBox")[0])
                browser.find_elements_by_css_selector(".speedTab15")[0].click()
            browser.execute_script('document.querySelector(".speedList").style.display="none";')
            print("启动加速")



