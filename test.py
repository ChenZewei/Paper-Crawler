from __future__ import print_function
from selenium import webdriver
from bs4 import BeautifulSoup

import unittest
import shutil
import imghdr
import os
import time
import concurrent.futures
import requests
import downloader
from urllib.parse import unquote, quote
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# import crawler

ieee_header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Host": "ieeexplore.ieee.org",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
}

def ieee_query_url(queryText, yearRange = "2014_2017", isNewSearch = False):
    base_url = "http://ieeexplore.ieee.org/search/searchresult.jsp?"
    yearRange_str = "ranges=" + yearRange + "_Year&"
    queryText_str = "queryText=" + queryText
    query_url = base_url + yearRange_str + queryText_str
    query_url += "&newsearch=true"
    return query_url

def paper_url_from_webpage(driver):
    paper_elements = driver.find_elements_by_class_name("List-results-items")
    paper_info = list()
    size = len(paper_elements)
    print("Size:{}".format(size))
    count = 0
    for paper_element in paper_elements:
        try:
            count += 1
            print("Element{}:".format(count))
            year = paper_element.find_element_by_css_selector("div:nth-child(3) > div:nth-child(2) > span:nth-child(1)").text.split(': ')[1]
            print(year)
            title = paper_element.find_element_by_css_selector("h2:nth-child(1) > a:nth-child(1)").text
            print(title)
            paper_url = paper_element.find_element_by_class_name("icon-pdf").get_attribute("href")
            # print(paper_url)
            paper_info.append([year, title, paper_url])
        except Exception as e:
            print("## Fail:  {}".format(e.args))
    return paper_info

def ieee_paper_downloader(paper_url, dst_dir, file_name, timeout = 20, proxy_type = None, proxy = None):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    page = webdriver.Chrome(chrome_options=chrome_options)
    page.get(paper_url)
    time.sleep(10)
    page.save_screenshot('page.png')
    element = page.find_element_by_xpath("//*[@id=\"plugin\"]")
    src = element.get_attribute("src")
    print(src)

query_url = ieee_query_url("real-time", "2014_2017")

print(query_url)

if not os.path.exists("output"):
    os.makedirs("output")

response = requests.get(query_url, headers=ieee_header, timeout=20, proxies=None)

with open("output/test", 'wb') as f:
    f.write(response.content)

response.close()

chrome_options = Options()
# specify headless mode
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.set_page_load_timeout(60)    #设置超时时间
driver.set_script_timeout(60)       #这两种设置都进行才有效

# driver.set_window_size(1920, 1080)
# driver.get("file:///home/hadoop/works/Paper-Crawler/IEEE%20Xplore%20Search%20Results.html")
driver.get("http://ieeexplore.ieee.org/search/searchresult.jsp?reload=true&newsearch=true&queryText=real-time")
time.sleep(5)

while True:
    try:
        count = len(driver.find_elements_by_class_name("icon-pdf"))
        print("element count:{}".format(count))
        if count < 25:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        else:
            break
    except Exception as e:
        print("wait")
        time.sleep(2)


driver.save_screenshot("screen_shot.png")
# print(driver.page_source)
# elements = driver.find_element_by_xpath("//*[@id=\"xplMainContent\"]/section[3]/div/div/div[1]/xpl-result/div/div[2]/h2/a")
paper_info = paper_url_from_webpage(driver)

o_file = open("output/papers.csv","w")
for paper in paper_info:
    print("{}-{}-{}".format(paper[0], paper[1], paper[2]))
    o_file.write("{},{},{}\n".format(paper[0],paper[1],paper[2]))
o_file.close()


# ieee_paper_downloader("http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8116677", "download", "test.pdf")
src = ""
for paper in paper_info:
    try:
        paper_test = paper_info[0]
        driver.get(paper[2])
        time.sleep(5)
        iframe = driver.find_element_by_xpath("/html/body/iframe[2]")
        driver.switch_to_frame(iframe)
        src = iframe.get_attribute("src")
        print(src)
        downloader.paper_download(src, "output", "{}--{}".format(paper[0],paper[1]))
    except Exception as e:
        print("## Err:  {}".format(e.args))


driver.close()



# soup = BeautifulSoup(driver.page_source, 'xml')
# print(driver.title)
# driver.quit()
# print(333)
# paper_urls = paper_url_from_webpage(driver)

