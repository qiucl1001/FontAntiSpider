# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import io
import tesserocr
import pytesseract
import requests
from urllib.parse import urljoin
from urllib.request import urlretrieve
from lxml import etree
from PIL import Image


def lxml_for_get_page():
    """
    使用lxml库解析网页内容
    :return:
    """
    url = "http://www.porters.vip/confusion/recruit.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/79.0.3945.117 Safari/537.36"
    }

    response = requests.get(url=url, headers=headers)
    html = etree.HTML(response.text)
    try:
        image_url = html.xpath('//img[@class="pn"]/@src')[0]
    except Exception as e:
        print(e.args)
        image_url = None
    if image_url:
        image_full_url = urljoin(url, image_url)

        # 下载图片到本地文件
        urlretrieve(image_full_url, "tel.png")

        # 请求图片资源，拿到图片的字节流
        image_content = requests.get(url=image_full_url, headers=headers).content

        # 使用Image.open方法打开图片字节流，获取图片对象
        image_stream = Image.open(io.BytesIO(image_content))

        # 使用光学识别技术库pytesseract将图片内容转化为文字
        image_2_word = pytesseract.image_to_string(image_stream)

        print(image_2_word)


def pic_word():
    """
    将图片转化为文字
    :return:
    """
    image = Image.open('tel.png')
    result = tesserocr.image_to_text(image)
    print(result)


def gxrc_lxml_for_get_page():
    """
    使用lxml库解析广西人才招聘网站的联系电话
    :return:
    """
    # 广西人才招聘网站某公司详情页地址
    url = "https://www.gxrc.com/company/1345732"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/79.0.3945.130 Safari/537.36"
    }
    response = requests.get(url=url, headers=headers)
    html = etree.HTML(response.text)
    try:
        tel_base_url = html.xpath('//div[contains(@class, "contact-info-con")]/p[2]//img/@src')[0]
    except Exception as e:
        print(e.args)
        tel_base_url = None
    if tel_base_url:
        tel_full_url = urljoin(url, tel_base_url)

        # 下载图片到本地文件
        urlretrieve(tel_full_url, "gxrc.png")

        # # 请求图片资源，拿到图片的字节流
        image_content = requests.get(url=tel_full_url, headers=headers).content

        # 使用Image.open方法打开图片字节流，获取图片对象
        image_stream = Image.open(io.BytesIO(image_content))

        # 使用光学识别技术库pytesseract将图片内容转化为文字
        image_2_word = pytesseract.image_to_string(image_stream)  # 会把数字8错误识别为数字3

        print(image_2_word)  # 13074313240 真正的电话号码：18074813240

        # real_tel_list = "".join(list(map(lambda x: (x if x != '3' else '8'), image_2_word)))
        real_tel_list = []
        for index, value in enumerate(image_2_word):
            if index <= 5 and value == '3':
                real_tel_list.append('8')
            else:
                real_tel_list.append(value)

        real_tel_number = "".join(real_tel_list)
        print(real_tel_number)


if __name__ == '__main__':
    # lxml_for_get_page()
    # pic_word()
    gxrc_lxml_for_get_page()
