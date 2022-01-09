# -*- coding: utf-8 -*-
import logging
import numpy as np
from PIL import Image
from cnocr import CnOcr

logging.basicConfig(format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
                    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


def img_2_cn(img_path, threshold=10, result='text'):
    """
    小说图片转文字
    :param img_path:
    :param threshold:自定义灰度界限，大于这个值为黑色，小于这个值为白色，默认为 10
    :param result:返回结果类型，must be list or text
    :return:
    """
    img = Image.open(img_path)

    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    # 图片二值化
    photo = img.point(table, '1').convert('L')

    # 去除黑色横线，但是去除过后效果发现文字识别也不是很好
    # width, height = photo.size
    #
    # for h in range(height):
    #     # 统计连续多少个黑色像素
    #     serial_count = 0
    #     for w in range(width):
    #         pixel = photo.getpixel((w, h))
    #         if pixel == 0:
    #             # 黑色
    #             serial_count += 1
    #         else:
    #             # 白色
    #             serial_count = 0
    #         if serial_count >= 20:
    #             # 连续 20 个黑色像素即认为其为直线
    #             for i in range(width):
    #                 photo.putpixel((i, h), 255)
    #             serial_count = 0
    #             break
    # photo.save('1.png')

    # 转换为 np array
    img_array = np.expand_dims(np.array(photo), -1)
    # 识别图片中文字
    ocr = CnOcr()
    res = ocr.ocr(img_array)
    if result == 'text':
        text = ''
        for i in res:
            text += ''.join(i[0]) + '\n\n'

        # print(text)
        return text
    elif result == 'list':
        return res
    else:
        raise ValueError(f'[result] must be "text" or "list"')


if __name__ == '__main__':
    import os

    img_2_cn(os.path.join(os.path.dirname(__file__), '../../test_files/test_img_2_cn.gif'))
    img_2_cn(r'D:\lzc\maida\test_files\test_img_2_cn.gif')
