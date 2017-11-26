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


query_url = crawler.ieee_query_url("real-time \"xue liu\"", "2014_2017")
print(query_url)

if not os.path.exists("output"):
    os.makedirs("output")

chrome_options = Options()
# specify headless mode
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.set_page_load_timeout(60)
driver.set_script_timeout(60)

crawler.ieee_search_result(query_url, driver)

paper_info = crawler.paper_url_from_webpage(driver)

print("Crawling finished...")

o_file = open("output/papers.csv","w")
for paper in paper_info:
    # print("{}-{}-{}".format(paper[0], paper[1], paper[2]))
    o_file.write("{},{},{}\n".format(paper[0],paper[1],paper[2]))
o_file.close()

print("Start to download...")
downloader.papers_download(driver, paper_info, "output")

# for paper in paper_info:
#     try:
#         driver.get(paper[2])
#         iframe = driver.find_element_by_xpath("/html/body/iframe[2]")
#         driver.switch_to_frame(iframe)
#         src = iframe.get_attribute("src")
#         # print(src)
#         # downloader.paper_download(src, "output", "{}--{}".format(paper[0],paper[1]))
#     except Exception as e:
#         print("## Err:  {}".format(e.args))


driver.close()