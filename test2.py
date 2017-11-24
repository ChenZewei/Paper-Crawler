from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

import time

# dcap = dict(DesiredCapabilities.PHANTOMJS)
# dcap["phantomjs.page.settings.userAgent"] = (
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
# )
# dcap["phantomjs.page.settings.loadImages"] = False



chrome_options = Options()
# specify headless mode
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.set_page_load_timeout(50)    #设置超时时间
driver.set_script_timeout(50)       #这两种设置都进行才有效
# driver.set_window_size(1024, 768)
# driver.get('http://www.baidu.com')   #加载网页
driver.get("http://ieeexplore.ieee.org/search/searchresult.jsp?reload=true&newsearch=true&queryText=real-time")
time.sleep(15)
data = driver.page_source   #获取网页文本
driver.save_screenshot('1.png')   #截图保存
# print(data)
driver.quit()



# from __future__ import print_function
# from selenium import webdriver
# from bs4 import BeautifulSoup

# import unittest
# import shutil
# import imghdr
# import os
# import time
# import concurrent.futures
# import requests
# from urllib.parse import unquote, quote
# from selenium import webdriver
# from selenium.webdriver import DesiredCapabilities

# dcap = dict(DesiredCapabilities.PHANTOMJS)
# dcap["phantomjs.page.settings.userAgent"] = (
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
# )

# page = webdriver.PhantomJS(executable_path="phantomjs", desired_capabilities=dcap)
# page.get("http://ieeexplore.ieee.org/search/searchresult.jsp?reload=true&newsearch=true&queryText=real-time")
# time.sleep(20)
# # page.save_screenshot('page.png')
# # page.close()