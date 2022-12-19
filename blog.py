from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

import ait
#from pandas.core.frame import DataFrame
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import quote
import os
import config


chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
browser = webdriver.Chrome(config.chrome_driver, options=chrome_options)
action = ActionChains(browser)

list = []

if __name__ == "__main__":
    root_dir = "./ska1018-1-1/"
    for (root, dirs, files) in os.walk(root_dir):
        if len(files) > 0:
            for file_name in files:
                rootpath = root.replace('\\', '/').replace(root_dir, '')
                list.append(rootpath + '/' + file_name)

title = ''
date = ''
content = ''
imglist = []


def post(title, date, content, imglist):
    browser.get(config.BLOG_URL)
    browser.switch_to.frame("mainFrame")
    time.sleep(2)
    browser.find_element_by_xpath(
        '//*[@id="post-admin"]/a[1]').send_keys(Keys.ENTER)
    time.sleep(3)

    # browser.find_element_by_xpath('//span[contains(text(),"제목")]').click()
    action = ActionChains(browser)
    action.send_keys(title + '(' + date + ')').perform()

# se-placeholder __se_placeholder se-ff-nanumgothic se-fs15 se-placeholder-focused
    # browser.find_element_by_xpath('//span[contains(text(),"본문에")]').click()
    # print(browser.find_element_by_xpath('//span[contains(text(),"본문에")]').find_element_by_xpath('..').get_attribute("innerHTML"))
    # browser.find_element_by_xpath('//span[contains(text(),"본문에")]').find_element_by_xpath('..').set_attribute("innerHTML", content)

    if (len(imglist) > 0):
        for img in imglist:
            # 사진 버튼 클릭
            browser.find_element_by_xpath(
                '//button[contains(@class,"se-")]').click()

            # 5초 대기
            time.sleep(2)

            # Basic Window info 값 handle 변수에 저장
            handle = "[CLASS:#32770; TITLE:열기]"

            # 이름이 '열기'인 창이 나올 때까지 3초간 대기
            ait.win_wait_active("열기", 3)

            img_path = img  # 'C:\\Users\\saelim\\Downloads\\ska1018-1-1-article1-488\\ska1018-1-1\\262\\img\\221A13475709A5E812.png'

            # 사진 클릭시 나오는 윈도우 창에서 파일이름(N)에 이미지 경로값 전달
            ait.control_send(handle, "Edit1", img_path)
            time.sleep(1)

            # 사진 클릭시 나오는 윈도우 창에서 Button1 클릭
            ait.control_click(handle, "Button1")
            time.sleep(1)

    # se-text-paragraph se-text-paragraph-align-left

    # bon = (browser.find_element(By.XPATH,'//span[contains(text(),"본문에")]'))
    bon = browser.find_element(
        By.XPATH, '//div[@class="se-component-content"]')
    # .find_element_by_xpath('..')
    # print(str(content))
    #browser.execute_script("arguments[0].innerHTML = arguments[1]", bon, content)
    browser.execute_script("arguments[0].innerHTML = arguments[1];", bon, re.sub(
        '<img.*/>', '', str(content)))
    # se-placeholder __se_placeholder se-ff-nanumgothic se-fs15 se-placeholder-focused
    # browser.find_element_by_xpath('//span[contains(text(),"본문에")]') = content
    # time.sleep(1)
    # action = ActionChains(browser)
    # time.sleep(1)
    # action.send_keys(Keys.ENTER).perform()
    # time.sleep(1)

    # 발행 팝업창 오픈 클릭
    browser.find_element_by_xpath('//span[contains(text(),"발행")]').click()
    # 비공개 클릭
    browser.find_element_by_xpath('//label[contains(text(),"비공개")]').click()
    # 발행 클릭
    # browser.find_element_by_xpath('//button[@class="confirm_btn__Dv9du"]').click()
    # confirm_btn__Dv9du


for li in sorted(list, key=lambda item: (int(item[:item.find('/')]))):
    folder = int(li[:li.find('/')])
    if (folder == 261):  # 첫번째 글자부터 / 까지를 숫자로 변환했을 때 뭐인지(하위폴더명)
        firstindex = int(li.find('/') + 1)
        if (li[firstindex: (firstindex + int(li[firstindex:].find('/')))] == ''):
            if title != '':
                post(title, date, content, imglist)
                title = ''
                date = ''
                imglist = []

            # , encoding='UTF8'
            html_file = open(root_dir + li, 'r', encoding='utf-8')
            data = html_file.read()
            title = BeautifulSoup(data, 'html.parser').select_one(
                'h2.title-article').text
            date = BeautifulSoup(data, 'html.parser').select_one(
                'p.date').text
            content = BeautifulSoup(
                data, 'html.parser').select_one('div.article-view')

            html_file.close()
        elif (li[firstindex: (firstindex + int(li[firstindex:].find('/')))] == 'img'):
            imglist.append(config.img_root_path + re.sub('\\/', '\\\\', li))
post(title, date, content, imglist)
# post(title, date, content)
# print(re.sub('<img.*/>', '', content))
