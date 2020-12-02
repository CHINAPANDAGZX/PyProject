#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import tempfile
import offlinePlayer
import onlinePlayer
# import reader
from PIL import Image
from model import OcrHandle
import subprocess
import os





if __name__ == '__main__':
    my_ocrhandle = OcrHandle()
    offlineEngine = offlinePlayer.init_offline_player()
    onlineToken = onlinePlayer.init_online_player()

    with tempfile.NamedTemporaryFile(delete=True) as tf:
        # save_file = "{}.jpg".format(tf.name)
        save_file = "/home/pi/OCR/image.jpg"
        cmd = ("fswebcam --no-banner --rotate 180 -r 1920x1080 " + save_file)
        # cmd = ("fswebcam /dev/video0  " + save_file)
        # fswebcam /dev/video0 /home/pi/1080p.jpg
        pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        pro.wait()
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
    offlinePlayer.offline_speak(offlineEngine, imgText)
    onlinePlayer.online_speak(onlineToken, imgText)
