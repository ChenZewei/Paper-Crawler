# Crawling paper urls from paper librarys

import time

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

def ieee_search_result(query_url, driver):
    driver.get(query_url)
    time.sleep(5)
    try_connt = 0
    count = 0
    while True:
        try:
            temp = len(driver.find_elements_by_class_name("icon-pdf"))
            print("element count:{}".format(count))
            if try_connt == 3:
                # print("break the loop")
                break
            if count == temp:
                try_connt += 1
            if temp < 25:
                count = temp
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # time.sleep(2)
            else:
                break
        except Exception as e:
            print("## Err:  {}".format(e.args))
            time.sleep(2)

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
