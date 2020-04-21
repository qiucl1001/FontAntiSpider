# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import re
import requests
from lxml import etree
from parsel import Selector


def parsel_for_parse_page(response):
    """
    使用parsel模块解析网页内容
    :param response: 响应数据
    :return:
    """
    sel = Selector(response.text)
    em = sel.css("em.rel").getall()

    for element in em:
        element = Selector(element)

        # 获取每个em标签中的所有b标签，返回的是一个列表
        element_b = element.css("b").getall()
        # 取每个em标签中的第一个b标签
        b1 = Selector(element_b.pop(0))
        # 获取b1标签的style
        b1_style = b1.css('b::attr("style")').get()
        # 获取b1标签的具体位置
        b1_width = "".join(re.findall(r'width:(.*)px;', b1_style))
        number = int(int(b1_width) / 16)
        # 获取第 1 对<b>标签中的值(列表)
        base_price = b1.css("i::text").getall()[:number]
        # print(base_price)

        alternative_price = []
        for eb in element_b:
            eb = Selector(eb)

            # 提取<b>标签的 style 属性值
            style = eb.css('b::attr("style")').get()
            # 获得具体的位置
            position = "".join(re.findall(r'left:(.*)px', style))
            # 获得该标签下的数字
            value = eb.css("b::text").get()
            # print({"position": position, "value": value})
            alternative_price.append({"position": position, "value": value})

        for item in alternative_price:
            position = int(item.get("position"))
            # 计算下标，以 16px 为基准
            index = int(position / 16)
            value = item.get("value")
            # 替换第一对<b>标签值列表中的元素，也就是完成值覆盖操作
            base_price[index] = value

        print(base_price)
        # break


def lxml_for_parse_page(response):
    """
    使用lxml库解析网页内容
    :param response: 响应数据
    :return:
    """
    html = etree.HTML(response.text)
    em_list = html.xpath('//em[@class="rel"]')

    for em in em_list:
        b_list = em.xpath('./b')
        b1 = b_list.pop(0)
        b1_style = "".join(b1.xpath('@style'))
        b1_text = b1.xpath('./i/text()')
        b1_width = int("".join(re.findall(r'width:(.*)px;', b1_style)))
        number = int(b1_width / 16)
        base_price = b1_text[:number]
        print("css偏移前价格列表情况：", base_price)

        alternative_price = []
        for b in b_list:
            b_style = "".join(b.xpath('@style'))
            position = "".join(re.findall(r'left:(.*)px', b_style))
            value = "".join(b.xpath("text()"))
            # print({"position": position, "value": value})
            alternative_price.append({"position": position, "value": value})
        # print(alternative_price)

        for item in alternative_price:
            position = int(item.get("position"))
            value = item.get("value")
            index = int(position / 16)
            base_price[index] = value
        print("绕过css偏移前价格列表情况处理后：", base_price)
        # break


if __name__ == '__main__':
    url = "http://www.porters.vip/confusion/flight.html"
    response_ = requests.get(url)

    # parsel_for_parse_page(response_)
    lxml_for_parse_page(response_)




