#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import pyttsx3


def init_offline_player():
    offline_engine = pyttsx3.init()
    offline_engine.setProperty('voice', 'zh')
    offline_engine.setProperty('rate', 140)
    return offline_engine


def offline_speak(offlineEngine, speakText):
    offlineEngine.say(speakText)
    offlineEngine.runAndWait()


if __name__ == '__main__':
    offlineEngine = init_offline_player()
    offline_speak(offlineEngine, "现在使用的是离线模式")
