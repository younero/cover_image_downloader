import requests
import re
import os
import time
import pandas as pd
from bs4 import BeautifulSoup


# 获取文章源代码
def get_content(url):
    return requests.get(url).content


# 获取文章标题
def get_title(content):
    bs = BeautifulSoup(content, 'lxml')
    text = bs.find(id='activity-name').text
    return text.strip()


# 获取封面图链接
def get_image_url(content):
    match_obj = re.search(r'var msg_cdn_url = "(.*?)";', str(content))
    if match_obj:
        return match_obj.group().replace('var msg_cdn_url = "', '').replace('";', '')
    else:
        return ''


# 保存封面图
def save_image(item):
    content = requests.get(item['image_url']).content
    if not os.path.exists('images'):
        os.mkdir('images')
    with open('images/%d.jpeg' % item['id'], 'wb') as img_f:
        img_f.write(content)
    print('id %d 爬取成功' % item['id'])


if __name__ == '__main__':
    recorder = []
    # 读取urls
    with open('urls.txt', 'r', encoding='utf8') as f:
        image_urls = []
        for line in f.readlines():
            url = line.strip()
            content = get_content(url)
            # 记录id、url
            recorder.append({
                'id': int(time.time() * 1000000),
                'article_url': url,  # 文章url
                'title': get_title(content),  # 文章标题
                'image_url': get_image_url(content)  # 保存微信头图的url
            })
        # for item in recorder:
        #     save_image(item)
        pd.DataFrame(recorder).to_csv('recorder.csv')
