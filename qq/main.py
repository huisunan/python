import getChrome
import time
#from selenium import webdriver

w = getChrome.getChrome()
w.get("https://i.qq.com/")
time.sleep(10)
with open("qq.html","w",encoding="utf-8") as f:
    f.write(w.page_source)
print(w.page_source)


input()
w.quit()
