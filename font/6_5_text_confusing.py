# coding: utf-8
# author: QCL
# software: PyCharm Professional Edition 2018.2.8

import json
import requests
import os
import base64
import pytesseract


def get_pic():
    """
    使用splash异步网络渲染服务获取目标数据截图
    :return:
    """
    render = "http://192.168.99.100:8050/execute"
    url = "http://www.porters.vip/confusion/movie.html"

    script = """
        function main(splash)
          assert(splash:go('%s'))
          assert(splash:wait(0.5))
          -- 截取票房
          -- total_png = splash:select('.movie-index-content.box .stonefont'):png()
          -- js = string.format("document.querySelector('.score-num .stonefont').attr('font-size', '30px;')")
          -- splash:evaljs(js)
          evaluate_png = splash:select('.score-num .stonefont'):png() 
          return {
           -- 将图片信息以键值对的方式返回
            -- total = total_png
            evaluate = evaluate_png
          }
        end
    """ % url

    # 构造请求头
    headers = {
        "Content-Type": "application/json"
    }

    # 按照splash规则提交命令
    data = json.dumps({"lua_source": script})

    # 向splash服务器接口发送请求，获取响应数据
    response = requests.post(url=render, data=data, headers=headers)

    # 将响应数据赋值给images变量
    images = response.json()
    # print(images)
    # print("---"*100)
    # print(images.items())
    save_pic(images)


def save_pic(images):
    """
    将图片保存到本地
    :param images: 图片源数据
    :return:
    """
    # 将图片保存到本地
    for key, value in images.items():
        # 获取图片二进制数据
        image_body = base64.b64decode(value)

        # 构造保存图片的名字
        filename = '{key}.png'.format(key=key)

        # 构建保存图片的绝对路径
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

        if not os.path.exists(path):
            # 将图标保存到本地
            with open(filename, "wb") as f:
                f.write(image_body)

        pic_2_text(filename)


def pic_2_text(filename):
    """
    将图片转化为文字
    :param filename: 图片名
    :return:
    """
    # 使用pytesseract库获取图片上面的文字信息
    pic_to_text = pytesseract.image_to_string(filename)

    print(pic_to_text)


def test_demo():
    """
    调试使用
    :return:
    """
    # pytesseract 识别中英文混淆的图片，效率不高
    print(pytesseract.image_to_string('test_demo.png'))  # 中文识别不了，英文字符字体偏小识别错误率高
    print("--"*100)
    print(pytesseract.image_to_string('test_demo.png', lang='chi_sim'))  # 能识别中文，但是英文识错误率也高


def use_txy_ocr():
    """
    使用第三方(腾讯云OCR)技术栈--->文字识别API url = "https://cloud.tencent.com/product/ocr-catalog"
    :return:
    """
    # 测试本地test_demo.png图片
    # cloud_tencent_url = "https://cloud.tencent.com/act/event/ocrdemo"

    # 识别结果
    Request = {
           "ImageUrl": "https://ocrdemo-temp-1254418846.cos.ap-guangzhou.myqcloud.com/1301162245-2.jpg"
    }

    Response = {
              "TextDetections": [
                {
                  "DetectedText": "战狼2",
                  "Confidence": 99,
                  "Polygon": [
                    {
                      "X": 58,
                      "Y": 9
                    },
                    {
                      "X": 140,
                      "Y": 9
                    },
                    {
                      "X": 140,
                      "Y": 43
                    },
                    {
                      "X": 58,
                      "Y": 43
                    }
                  ],
                  "AdvancedInfo": "{\"Parag\":{\"ParagNo\":1}}"
                },
                {
                  "DetectedText": "Wolf Warrior 2",
                  "Confidence": 85,
                  "Polygon": [
                    {
                      "X": 57,
                      "Y": 52
                    },
                    {
                      "X": 200,
                      "Y": 52
                    },
                    {
                      "X": 200,
                      "Y": 71
                    },
                    {
                      "X": 57,
                      "Y": 71
                    }
                  ],
                  "AdvancedInfo": "{\"Parag\":{\"ParagNo\":2}}"
                }
              ],
              "Language": "zh",
              "RequestId": "c29991c2-df39-427c-830e-258a2a164b0c"
            }


def main():
    # get_pic()
    test_demo()


if __name__ == '__main__':
    main()







