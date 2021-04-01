import sys
import re
import requests
from bs4 import BeautifulSoup


class Downloader(object):

    def __init__(self):
        self.server = 'http://www.bqkan.com/'
        self.target = 'http://www.bqkan.com/1_1094/'
        self.chapter = []  # 章节名
        self.url = []  # 章节链接
        self.num = 0  # 章节数

    def get_url(self):
        req = requests.get(url=self.target)
        html = req.content.decode('gbk')
        div_bf = BeautifulSoup(html, 'lxml')
        div = div_bf.find_all('div', class_='listmain')
        a_bf = BeautifulSoup(str(div[0]), 'lxml')
        a = a_bf.find_all('a')
        a = [_ for _ in a[12:] if re.search('[第|弟].*?[章|张]', str(_))]
        self.num = len(a)
        for each in a:
            self.chapter.append(each.string)
            self.url.append(self.server + each.get('href'))


def get_text(target):
    req = requests.get(url=target)
    html = req.content.decode('gbk')
    bf = BeautifulSoup(html, 'lxml')
    text = bf.find_all('div', class_='showtxt')
    text = text[0].text.replace('\xa0' * 8, '\n\n')
    return text


def write(path, chapter, text):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(chapter + '\n')
        f.writelines(text)
        f.write('\n\n')


if __name__ == "__main__":
    dl = Downloader()
    dl.get_url()
    print('《一念永恒》下载开始')
    for i in range(dl.num):
        write('yinianyongheng.txt', dl.chapter[i], get_text(dl.url[i]))
        sys.stdout.write("已下载：%.3f%%" % float((i / dl.num) * 100) + '\r')
        sys.stdout.flush()
    print('《一念永恒》下载完成')
