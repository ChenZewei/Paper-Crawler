""" Crawl image urls from image search engine. """
# -*- coding: utf-8 -*-
# author: Yabin Zheng
# Email: sczhengyabin@hotmail.com

# from __future__ import print_function

# import re
# import time
# import sys
# import os
# import json
# import codecs

# from urllib.parse import unquote, quote
# from selenium import webdriver
# from selenium.webdriver import DesiredCapabilities
# import requests
# from concurrent import futures

# if getattr(sys, 'frozen', False):
#     bundle_dir = sys._MEIPASS
# else:
#     bundle_dir = os.path.dirname(os.path.abspath(__file__))

# if sys.platform.startswith("win"):
#     phantomjs_path = os.path.join(bundle_dir + "/bin/phantomjs.exe")
# else:
#     phantomjs_path = "phantomjs"

# dcap = dict(DesiredCapabilities.PHANTOMJS)
# dcap["phantomjs.page.settings.userAgent"] = (
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100"
# )


def my_print(msg, quiet=False):
    if not quiet:
        print(msg)


def ieee_query_url(queryText, yearRange = "2014_2017", isNewSearch = False):
    base_url = "http://ieeexplore.ieee.org/search/searchresult.jsp?"
    yearRange_str = "ranges=" + yearRange + "_Year&"
    queryText_str = "queryText=" + queryText
    query_url = base_url + yearRange_str + queryText_str
    if isNewSearch:
        query_url += "&newsearch=true"
    return query_url

def ieee_query_by_author_url(firstName, lastName = "", yearRange = "2014_2017", isNewSearch = False):
    base_url = "http://ieeexplore.ieee.org/search/searchresult.jsp?"
    yearRange_str = "ranges=" + yearRange + "_Year&"
    firstName_str = "searchWithin=\"First%20Name\":" + firstName
    lastNamt_str = "&searchWithin=\"Last%20Name\":" + lastName
    query_url = base_url + yearRange_str + firstName_str + lastNamt_str
    if isNewSearch:
        query_url += "&newsearch=true"
    return query_url

def ieee_query_conference_url(title, yearRange = "2014_2017", isNewSearch = False):
    base_url = "http://ieeexplore.ieee.org/search/searchresult.jsp?"
    yearRange_str = "ranges=" + yearRange + "_Year&"
    title_str = "searchWithin=%22Publication%20Title%22:" + title
    query_url = base_url + yearRange_str + title_str + "&contentType=conferences"
    if isNewSearch:
        query_url += "&newsearch=true"
    return query_url

# my_print(ieee_query_url("real-time systems"))

# my_print(ieee_query_by_author_url("xue", "liu"))

# my_print(ieee_query_conference_url("real-time systems"))

def paper_url_from_webpage(driver):
    paper_elements = driver.find_elements_by_class_name("List-results-items")
    paper_info = list()
    count = 0
    for paper_element in paper_elements:
        try:
            count += 1
            # print("Element{}:".format(count))
            year = paper_element.find_element_by_css_selector("div:nth-child(3) > div:nth-child(2) > span:nth-child(1)").text.split(': ')[1]
            # print(year)
            title = paper_element.find_element_by_css_selector("h2:nth-child(1) > a:nth-child(1)").text
            # print(title)
            paper_url = paper_element.find_element_by_class_name("icon-pdf").get_attribute("href")
            # print(paper_url)
            paper_info.append([year, title, paper_url])
        except Exception as e:
            print("## Fail:  {}".format(e.args))
    return paper_info

def downloader_test(proxy=None, proxy_type="http", quiet=False, browser="phantomjs"):
    phantomjs_args = []
    if proxy is not None and proxy_type is not None:
        phantomjs_args += [
            "--proxy=" + proxy,
            "--proxy-type=" + proxy_type,
        ]
    driver = webdriver.PhantomJS(executable_path=phantomjs_path,
                                    service_args=phantomjs_args, desired_capabilities=dcap)
    query_url = ieee_query_url("real-time")
    driver.get(query_url)
