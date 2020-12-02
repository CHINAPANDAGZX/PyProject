#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import tempfile
from picamera import PiCamera
import offlinePlayer
import onlinePlayer
# import reader
from PIL import Image
from model import OcrHandle


def take_photo(camera, filePath):
    camera.start_preview()
    # camera.rotation = 180
    camera.capture(filePath)
    camera.stop_preview()

if __name__ == '__main__':
    camera = PiCamera()
    my_ocrhandle = OcrHandle()
    offlineEngine = offlinePlayer.init_offline_player()
    onlineToken = onlinePlayer.init_online_player()

    with tempfile.NamedTemporaryFile(delete=True) as tf:
        save_file = "{}.jpg".format(tf.name)
        take_photo(camera, save_file)
        img = Image.open(save_file)
        img = img.convert("RGB")
        res = my_ocrhandle.text_predict(img, 960)
    imgText = ''
    for i, r in enumerate(res):
        rect, txt, confidence = r
        if i == 0:
            imgText = txt
        else:
            imgText = imgText + ',' + txt
    print(imgText)
    # offlinePlayer.offline_speak(offlineEngine, imgText)
    onlinePlayer.online_speak(onlineToken, imgText)
