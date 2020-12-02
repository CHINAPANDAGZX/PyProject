#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from picamera import PiCamera


def printA():
    print("GzxA")


def take_photo(filePath):
    camera = PiCamera()
    camera.start_preview()
    # camera.rotation = 180
    camera.capture(filePath)
    camera.stop_preview()




