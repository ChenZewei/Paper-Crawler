from __future__ import print_function

import shutil
import imghdr
import os
import concurrent.futures
import requests

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Proxy-Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, sdch",
    # 'Connection': 'close',
}


def paper_download(paper_url, dst_dir, file_name, timeout=20, proxy_type=None, proxy=None):
    proxies = None
    if proxy_type is not None:
        proxies = {
            "http": proxy_type + "://" + proxy,
            "https": proxy_type + "://" + proxy
        }

    response = None
    file_path = os.path.join(dst_dir, file_name)
    try_times = 0
    while True:
        try:
            try_times += 1
            response = requests.get(
                paper_url, headers=headers, timeout=timeout, proxies=proxies)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            response.close()
            new_file_name = "{}.pdf".format(file_name)
            new_file_path = os.path.join(dst_dir, new_file_name)
            shutil.move(file_path, new_file_path)
            print("## OK:  {}  {}".format(new_file_name, paper_url))
            break
        except Exception as e:
            if try_times < 3:
                continue
            if response:
                response.close()
            print("## Fail:  {}  {}".format(paper_url, e.args))
            break


def papers_download(driver, paper_info, dst_dir, concurrency=50, timeout=20, proxy_type=None, proxy=None):
    """
    Download image according to given urls and automatically rename them in order.
    :param timeout:
    :param proxy:
    :param proxy_type:
    :param paper_info: paper information
    :param dst_dir: output the downloaded papers to dst_dir
    :param concurrency: number of requests process simultaneously
    :return: none
    """

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        future_list = list()
        count = 0
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for paper in paper_info:
            try:
                driver.get(paper[2])
                iframe = driver.find_element_by_xpath("/html/body/iframe[2]")
                driver.switch_to_frame(iframe)
                src = iframe.get_attribute("src")
                future_list.append(executor.submit(
                    paper_download, src, dst_dir, "{}--{}".format(paper[0], paper[1]), timeout, proxy_type, proxy))
                count += 1
            except Exception as e:
                print("## Err:  {}".format(e.args))
        concurrent.futures.wait(future_list, timeout=180)
