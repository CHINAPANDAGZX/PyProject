#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus
import json
import tempfile
from pygame import mixer

# 替换你的 API_KEY
API_KEY = 'UejcHl2ZBMfuIgbmiarN1ekb'
SECRET_KEY = 'h5nkEM4IbV0zMqH72ThaHRoh9H199EmA'
TTS_URL = 'http://tsn.baidu.com/text2audio'
TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'


def init_online_player():
    return fetch_token()


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


def online_speak(onlineToken, speakText):
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
        except URLError as err:
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
    onlineToken = init_online_player()
    online_speak(onlineToken, "现在使用的是联网模式")
