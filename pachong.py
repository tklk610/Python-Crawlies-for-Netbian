import requests
import datetime
import time
import random
import os

from lxml import etree
from concurrent.futures import ThreadPoolExecutor

# 设置保存路径
path = r'xxx'

user_agent = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (WindowsNT 10.0; Win64; x64; rv:100.0) Gecko/20100101Firefox/100.0"
    ]

start = datetime.datetime.now()

def get_img(urls):
    headers = {
        "User-Agent": random.choice(user_agent),
        "Referer": "http://pic.netbian.com/4kdongman/index.html"
    }

    pic_num = 0
    for url_page in urls:
        response_page = requests.get(url_page, headers=headers)   # 发送请求,获取响应
        response_page.encoding = 'GBK'  # 重新设置编码解决编码问题
        print(response_page.text)
        html_page = etree.HTML(response_page.text)
        # xpath定位提取想要的数据  得到图片链接和名称
        # //从匹配选择的当前节点选择文档中的节点，而不考虑他们的位置
        # @选取属性
        # /是从根节点选取。
        page_src = html_page.xpath('//ul[@class="clearfix"]/li/a/@href')
        page_src = ['http://pic.netbian.com' + x for x in page_src]

        for url_img in page_src :
            response_img = requests.get(url_img, headers=headers)
            response_img.encoding = 'GBK'
            html_img = etree.HTML(response_img.text)
            print(html_img)

            img_src = html_img.xpath('//div[@class="wrap clearfix"]/div/div/div/div/a/img/@src')
            img_src = ['http://pic.netbian.com' + x for x in img_src]
            img_alt = html_img.xpath('//div[@class="wrap clearfix"]/div/div/div/div/a/img/@alt')

            if not os.path.exists(path):
                os.makedirs(path)

            for src, name in zip(img_src, img_alt):
                img_content = requests.get(src, headers=headers).content
                img_name = name + '.png'

                try :
                    with open(path + '/' + img_name, 'wb') as f:  # 图片保存到本地
                        print(f"正在为您下载第{urls.index(url_page)}页第{page_src.index(url_img)}张图片：{img_name}")
                        f.write(img_content)
                        pic_num += 1
                except :
                   # try模块出现了异常情况，则except语句会被执行。
                   print("图片下载出错")

                time.sleep(random.randint(5, 10))

            time.sleep(random.randint(5, 10))

    print("一共下载了{}张图片".format(pic_num))


def main():
    # 要请求的url列表
    url_list = ['https://pic.netbian.com/4kdongman/index.html'] + [f'https://pic.netbian.com/4kdongman/index_{i}.html' for i in range(2, 4)]
    # url_list = ['https://pic.netbian.com/4kyouxi/index.html'] + [f'https://pic.netbian.com/4kyouxi/index_{i}.html' for i in range(2, 4)]

    get_img(url_list)

    delta = (datetime.datetime.now() - start).total_seconds()
    print(f"抓取所有页图片用时：{delta}s")

if __name__ == '__main__':
    main()