# 目标歌曲：https://music.163.com/#/song?id=461525011
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Chrome()
browser.maximize_window() # 窗口最大化
browser.get('https://music.163.com/#/song?id=461525011')
browser.switch_to.frame('contentFrame') # 切换进入框架
time.sleep(5)
browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
coms = []
for i in range(10):
    next_page = browser.find_element_by_css_selector('.znxt')
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@data-type='reply']")))
    comments = browser.find_elements_by_css_selector('.itm')
    for comment in comments:
        tmp = comment.text
        new_comment = tmp.split('\n')
        print(new_comment[0])
        coms.append(new_comment[0])
    next_page.click()
browser.close()
for i in coms:
    with open('网易云音乐评论.txt','a',encoding='utf8') as f:
        f.write(i)
        f.write('\n')




