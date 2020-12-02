#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from picamera import PiCamera

import tempfile
from pygame import mixer
import pyttsx3
import json

from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus

from paddleocr import PaddleOCR


# 替换你的 API_KEY
API_KEY = 'UejcHl2ZBMfuIgbmiarN1ekb'
SECRET_KEY = 'h5nkEM4IbV0zMqH72ThaHRoh9H199EmA'
TTS_URL = 'http://tsn.baidu.com/text2audio'
TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'

global offlineEngine
global onlineToken


def initOfflinePlayer():
    global offlineEngine
    offlineEngine = pyttsx3.init()
    offlineEngine.setProperty('voice', 'zh')


def initOnlinePlayer():
    global onlineToken

    #  配置百度TTS
    onlineToken = fetch_token()


def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()

    result_str = result_str.decode()

    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'audio_tts_post' in result['scope'].split(' '):
            print('please ensure has check the tts ability')
            exit()
        return result['access_token']
    else:
        print('please overwrite the correct API_KEY and SECRET_KEY')
        exit()


def speak(onlineFlag, speakText):
    if onlineFlag:
        with tempfile.NamedTemporaryFile(delete=True) as tf:

            tex = quote_plus(speakText)  # 此处TEXT需要两次urlencode
            params = {'tok': onlineToken, 'tex': tex, 'cuid': "quickstart",
                      'lan': 'zh', 'ctp': 1}  # lan ctp 固定参数
            data = urlencode(params)
            req = Request(TTS_URL, data.encode('utf-8'))
            has_error = False
            # Processing data

            try:
                f = urlopen(req)
                result_str = f.read()

                headers = dict((name.lower(), value) for name, value in f.headers.items())

                has_error = ('content-type' not in headers.keys() or headers['content-type'].find('audio/') < 0)
            except  URLError as err:
                print('http response http code : ' + str(err.code))
                result_str = err.read()
                has_error = True

            save_file = "error.txt" if has_error else "{}.mp3".format(tf.name)

            with open(save_file, 'wb') as of:
                of.write(result_str)

            if has_error:
                result_str = str(result_str, 'utf-8')
                print("tts api  error:" + result_str)
                play_voice_file("好像出错了呀.mp3")
            print("file saved as : " + save_file)

            play_voice_file("{}.mp3".format(tf.name))

    else:
        offlineEngine.say(speakText)
        offlineEngine.runAndWait()


def play_voice_file(fileName):
    #  配置播放速率
    mixer.pre_init(16000, -16, 2, 2048)
    mixer.init()
    mixer.music.load(fileName)
    if not mixer.music.get_busy():
        mixer.music.play()
        while mixer.music.get_busy():
            continue


if __name__ == '__main__':

    camera = PiCamera()
    # need to run only once to download and load model into memory
    ocr = PaddleOCR(use_gpu=False)

    with tempfile.NamedTemporaryFile(delete=True) as tf:
        save_file = "{}.jpg".format(tf.name)
        camera.start_preview()
        # camera.capture('/home/pi/TTS/image.jpg')
        camera.capture(save_file)
        camera.stop_preview()

        # img_path = 'timg.jpg'
        img_path = save_file
        result = ocr.ocr(img_path, det=True)
    # 联网标志位
    # isOnline = False
    isOnline = True
    try:
        initOfflinePlayer()
        initOnlinePlayer()

        imgText = ''
        # for line in result:
        for i in range(0, len(result)):
            # for line1 in line:
            line = result[i]
            tempText = line[1][0]
            print(line[1][0])
            if i == 1:
                imgText = tempText
            else:
                imgText = imgText + ',' + tempText
        print(imgText)

        speak(isOnline, imgText)

    except:
        play_voice_file("好像出错了呀.mp3")
    finally:
        pass


