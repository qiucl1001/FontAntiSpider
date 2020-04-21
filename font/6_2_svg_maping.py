# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import re
import requests
from parsel import Selector
from lxml import etree


def parsel_for_parse_page(response):
    """
    使用parsel模块解析网页数据
    :param response: 响应数据
    :return:
    """
    selector = Selector(response.text)

    # 定义映射关系
    mappings = {'vhk08k': 0, 'vhk6zl': 1, 'vhk9or': 2,
                'vhkfln': 3, 'vhkbvu': 4, 'vhk84t': 5,
                'vhkvxd': 6, 'vhkqsc': 7, 'vhkjj4': 8,
                'vhk0f1': 9}

    phone_element = selector.css('div.col.more > d').getall()
    tel_vhk_list = []
    for d_em in phone_element:
        d = Selector(d_em)
        x = d.css('d::attr("class")').get()
        tel_vhk_list.append(x)
    # print(tel_vhk_list)

    # 获取VSG的映射值
    tel_num_list = [mappings.get(i) for i in tel_vhk_list]
    tel_num_list = list(map(lambda x_: (str(x_) if x_ is not None else "-"), tel_num_list))

    phone = "".join(tel_num_list)
    print(phone)


def lxml_for_parse_page(response):
    """
    使用lxml库解析网页数据
    :param response: 响应数据
    :return:
    """
    html = etree.HTML(response.text)

    # 定义映射关系
    mappings = {'vhk08k': 0, 'vhk6zl': 1, 'vhk9or': 2,
                'vhkfln': 3, 'vhkbvu': 4, 'vhk84t': 5,
                'vhkvxd': 6, 'vhkqsc': 7, 'vhkjj4': 8,
                'vhk0f1': 9}

    # 获取商家联系电话的class属性值
    tel_vhk_list = html.xpath('//div[@class="col more"]/d/@class')

    # 获取SVG映射数值
    tel_num_list = [mappings.get(i) for i in tel_vhk_list]
    tel_num_list = list(map(lambda x: (str(x) if x is not None else "-"), tel_num_list))
    phone = "".join(tel_num_list)
    print(phone)


def svg_map():
    """基于svg-->css映射原理"""
    url_css = 'http://www.porters.vip/confusion/css/food.css'
    url_svg = 'http://www.porters.vip/confusion/font/food.svg'

    css_response = requests.get(url_css).text
    svg_response = requests.get(url_svg).text

    # 映射的 HTML 标签的 class 属性值
    css_class_name = 'vhkbvu'

    # 提取 CSS 样式文件中标签属性对应的坐标值，这里使用正则进行匹配即可
    css = css_response.replace('\n', '').replace(' ', '')
    pattern = re.compile(r'\.%s\{background:-(\d+)px-(\d+)px;\}' % css_class_name, re.S)
    res = re.findall(pattern, css)
    x, y = None, None
    if res:
        x, y = res[0]
        x, y = int(x), int(y)

    svg_data = Selector(svg_response)
    texts = svg_data.xpath('//text')
    axis_y = [int(i.attrib.get("y")) for i in texts if y <= int(i.attrib.get("y"))][0]

    # 得到 y 值后就可以确定具体是哪个 text 标签
    svg_text = svg_data.xpath('//text[@y="%d"]/text()' % axis_y).get()

    # svg中文字大小
    font_size = re.search(r'font-size:(\d+)px', svg_response).group(1)

    position = x // int(font_size)  # 结果为 27

    number = svg_text[position]
    print(number)


if __name__ == '__main__':
    # url = "http://www.porters.vip/confusion/food.html"
    # response_ = requests.get(url)

    # parsel_for_parse_page(response_)
    # lxml_for_parse_page(response_)

    svg_map()




