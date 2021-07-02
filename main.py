from selenium import webdriver
from bs4 import BeautifulSoup
import bs4
import time
import re
import requests
import os
#无头浏览器
# options.add_argument('-headless')
# driver=webdriver.Firefox(firefox_options=options)
# driver.get("http://night2.fun")

page0="https://mn4.fun"
file = open('hw.txt', mode='a+', encoding='utf-8')
file2= open('nav.txt',mode='a+',encoding='utf-8')
file3= open('app.txt',mode='a+',encoding='utf-8')
link_all=["https://mn4.fun"]
option = webdriver.FirefoxOptions()
option.add_argument('-headless')
driver = webdriver.Firefox(options=option)
def sele(link): #这个参数是一个网址连接
    try:
        driver.get(link)
        driver.refresh()
        time.sleep(10)
    except Exception as e:
        print(e)
        pass
    #time.sleep(2)
    a = driver.page_source
    return a  #a即是我想要的异步加载完成后的html文件

#小范围初阶版本：只爬取那些有关键词特征的网站

#一个普通黄网

#一个黄网导航页面
##获取网址，并且对网站状态进行检测，只收录能正常访问的网页
###获取网页的名称 title
def getname(page):
    name=page.title.string
    return name
#通过网页的title标签内容，对网页进行分类：导航、app、视频网站
def judge(page):
    linkname=getname(page)
    nav_judge = re.search("导航", linkname)
    app_judge = re.search("下载", page.text)
    if nav_judge:
        return 0
    elif app_judge:
        return 1
    elif not linkname:
        return 3
    else:
        return 2
def getBroNode(node):
    k=0
    node_sib = node.next_sibling
    #获得为tag类型的兄弟节点，同时获得她的list
    while type(node_sib)!=bs4.element.Tag and k<5 and node_sib:
        node_sib= node_sib.next_sibling
        k+=1
        print(type(node_sib))
    if type(node_sib)==bs4.element.Tag:
        node_sib_list=node_sib.find_all("a")
    elif not node_sib:
        node_sib_list=[]

    return node_sib

def write(m,k,linkname):
    if m == 0 and not (k in link_all):
        file2.write(linkname + "   ")
        file2.write(k + "\n")
    elif m == 1 and not (k in link_all):
        file3.write(linkname + "   ")
        file3.write(k + "\n")
    elif m == 2 and not (k in link_all):
        file.write(linkname + "   ")
        file.write(k + "\n")
###获取导航页内的黄网网址
####获得页面一块下的网址
def getchunklink(node):
    global link_all
    num=0
    n=0
    k=0
    node_sib_list=[]
    node_sib = node.next_sibling
    nodelist=node.find_all("a")
    #以下皆为定位，先确定好链接所在位置，才能继续挖掘
    #获得的兄弟标签
    node_sib=getBroNode(node)
    if len(node_sib_list)>3 and len(nodelist)<3:#如果兄弟节点的比目前节点的链接link多，就用兄弟节点的
        nodelist=node_sib_list
        node=node_sib
    #获得父母的
    while len(nodelist)<3 and n<5 and len(node_sib_list)<3:
        node=node.parent
        if type(node)==bs4.element.Tag:
            nodelist=node.find_all("a")
        node_sib=getBroNode(node)
        n+=1
    if len(node_sib_list)>3 and len(nodelist)<3:#如果兄弟节点的比目前节点的链接link多，就用兄弟节点的
        nodelist=node_sib_list

    #获取链接
    for i in nodelist:
        #要以http开头，来保证是外链
        print(i.get("href"))
        if re.match("http",str(i.get("href"))):
            try:
                r=requests.get(i["href"]).status_code
                print(r)
            except:
                r=404
            if r==200:
                new_link=sele(i["href"])
                new_html=BeautifulSoup(new_link,"html.parser")
                linkname = getname(new_html)
                m=judge(new_html)
                print(m)
                print(i["href"])
                write(m,i["href"],linkname)
            print(num)
            num+=1
            link_all+=[i[href]] #去重
            link_key+=[re.search("([a-z]*://)(www.)*(\w*)\.*.*",i[href])
]
#对整个网站进行滚动获取
# def getlink(page):
#     #通过每个导航页都会存在一个"推荐"这个分类，来进行定位
#     links=page.find_all("a")
#     for i in links:

    # m=text_tj[0]
    # print(m)
    # while m:
    #     getchunklink(m)
    #     while m!=bs4.element.Tag:
    #         m=m.next_sibling
#对hw的友情链接进行获取
def getfrilink(page):
    #文字
    print(page)
    friend=page.find_all(text=re.compile("友情链接"))
    footer=page.find_all(attrs={"class":"footer"})
    nav=page.find_all(text=re.compile("导航"))
    coo=page.find_all(text=re.compile("合作"))
    if friend:
        getchunklink(friend[0])
    elif footer:
        getchunklink(footer[0])
    elif nav:
        getchunklink(nav[0])
    elif coo:
        getchunklink(coo[0])




def main():
    for i in link_all:
        bs = BeautifulSoup(sele(i), "html.parser") #BeautifulSoup是对html文本进行解析的，而获取html文本，则需要selenium或者requests等
        m=judge(bs)
        if m==0:
            getchunklink(bs.find("html"))
        elif m==2:
            getfrilink(bs)


main()

driver.close()

file.close()
file2.close()
