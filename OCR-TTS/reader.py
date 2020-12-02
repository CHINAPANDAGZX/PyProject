#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from paddleocr import PaddleOCR


def init_reader():
    return PaddleOCR(use_gpu=False)


def read_text(ocr, img_path):
    return ocr.ocr(img_path, det=True)


if __name__ == '__main__':
    orc = init_reader()
    result = read_text(orc, 'image.jpg')
    imgText = ''
    try:
        for i in range(0, len(result)):
            line = result[i]
            tempText = line[1][0]
            print(line[1][0])
            if i == 1:
                imgText = tempText
            else:
                imgText = imgText + ',' + tempText
        print(imgText)
    except:
        print("好像出错了")
    finally:
        pass

