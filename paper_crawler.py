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
import crawler
import downloader
from urllib.parse import unquote, quote
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


ieee_header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Host": "ieeexplore.ieee.org",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
}


query_url = crawler.ieee_query_url("real-time \"xue liu\"", "2014_2017")
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
driver.set_page_load_timeout(60)
driver.set_script_timeout(60)

driver.get(query_url)
time.sleep(5)


try_connt = 0
count = 0
while True:
    try:
        temp = len(driver.find_elements_by_class_name("icon-pdf"))
        print("element count:{}".format(count))
        if try_connt == 3:
            print("break the loop")
            break
        if count == temp:
            try_connt += 1
        if temp < 25:
            count = temp
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        else:
            break
    except Exception as e:
        print("## Err:  {}".format(e.args))
        time.sleep(2)

paper_info = crawler.paper_url_from_webpage(driver)

o_file = open("output/papers.csv","w")
for paper in paper_info:
    print("{}-{}-{}".format(paper[0], paper[1], paper[2]))
    o_file.write("{},{},{}\n".format(paper[0],paper[1],paper[2]))
o_file.close()

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