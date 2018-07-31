#!/usr/bin/python
# -*- coding:utf-8 -*

import time
import pygame

"""用于实现坦克的各种音效"""
class Music():
    #1、发动机启动
    def start(self):
        file = r'C:\Users\chan\Desktop\Adele - All I Ask.mp3'
        pygame.mixer.init()
        print("播放发动机启动音效！")
        track = pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        time.sleep(10)
        pygame.mixer.music.stop()
    #2、发动机怠速
    def idling(self):
        pass
    #3、行进
    def move(self):
        pass
    #4、刹车急停
    def stop(self):
        pass
    #5、主炮开火声音
    def BigGunFire_Sound(self):
        pass
    #6、机枪开火声音
    def GunFire(self):
        pass
    #7、退弹装填
    def reload(self):
        pass
    #8、熄火
    def stalled(self):
        pass