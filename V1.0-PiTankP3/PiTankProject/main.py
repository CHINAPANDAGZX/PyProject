#!/usr/bin/python
# -*- coding:utf-8 -*-

from .tankBody import Tank


print("坦克上电云台启动函数")
tank = Tank()
print("俯仰云台展开！")
tank.pwm.setPWM(tank.servoPitchNum, 0, tank.servoMid_pitch)
print("偏航云台展开！")
tank.pwm.setPWM(tank.servoYawNum, 0, tank.servoMid_yaw)
print("前大灯开启！")
tank.Forward_light("on")
print("尾灯灯开启！")
tank.Backward_light("on")

