import os
import requests
from bs4 import BeautifulSoup
# Selenium import
from selenium import webdriver
import re
import config

# webdriver 설정하기
#browswer = webdriver.Chrome('./chromedriver/chromedriver.exe')

list = []

if __name__ == "__main__":
    root_dir = "./ska1018-1-1/"
    for (root, dirs, files) in os.walk(root_dir):
        if len(files) > 0:
            for file_name in files:
                rootpath = root.replace('\\', '/').replace(root_dir, '')
                list.append(rootpath + '/' + file_name)
# print("# root : " + root)
# if len(dirs) > 0:
#     for dir_name in dirs:
#         if (dir_name.isdigit() == False):
#             print("dir: " + dir_name)


# 파일명이 .html인건 인덱스가 -1보다 큼
# ====html이 아닌 파일(이미지 파일)을 찾아 파일명.png로 변경해주는 소스 ========

# if (file_name.find('.html') < 0 and file_name.find('.') < 0):
#     rename = file_name + '.png'
#     # 원래 파일도 os.path.join으로 지정해줘야 인식 잘 함
#     old_name = os.path.join(root, file_name)
#     new_name = os.path.join(root, rename)
#     # print(new_name)

#     os.rename(old_name, new_name)
# take the second element for sort
# def findslash(elem):
#     return elem[:2]

#list = [3, 21, 32, 31]
# for item in list:
#     if (item[:item.find('/')].isdigit() == False):
#         print(item)
def printpost(title, date, imglist):
    print(title + '(' + date + ') and')
    print(imglist[0])
    # for img in imglist:
    #     print(img)

title = ''
imglist = []

for li in sorted(list, key=lambda item: (int(item[:item.find('/')]))):
    folder = int(li[:li.find('/')])
    if (folder == 261): #첫번째 글자부터 / 까지를 숫자로 변환했을 때 뭐인지(하위폴더명)
        firstindex = int(li.find('/') + 1)
        if (li[firstindex: (firstindex + int(li[firstindex:].find('/')))] == ''):
            if title != '':
                printpost(title, date, imglist)
                title = ''
                date = ''
                imglist = []

            html_file = open(root_dir + li, 'r', encoding='utf-8') #, encoding='UTF8'
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
printpost(title, date, imglist)
        
# ==== end ========
# filepath = './ska1018-1-1/2/2-2011년-12월-30일-오후-09_21.html'

# src_file = open(filepath, 'r', encoding='UTF8')
# data = src_file.read()
# print(data)
# src_file.close()
