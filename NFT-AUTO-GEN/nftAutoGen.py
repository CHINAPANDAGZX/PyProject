#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from Pillow import Image
# from IPython.display import display
import random
import json
import os

def file_name(file_dir):
    L=[]
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.jpeg':
                L.append(os.path.join(root, file))
    return L

# 每个图像由一系列特征组成
# 每个特征的权重决定了其稀有性，加起来为 100%
face = ["White", "Black"]
face_weights = [60, 40]

ears = ["ears1", "ears2", "ears3", "ears4"]
ears_weights = [25, 30, 44, 1]

eyes = ["regular", "small", "rayban", "hipster", "focused"]
eyes_weights = [70, 10, 5, 1, 14]

hair = ['hair1', 'hair10', 'hair11', 'hair12', 'hair2', 'hair3', 'hair4', 'hair5', 'hair6', 'hair7', 'hair8', 'hair9']
hair_weights = [10, 10, 10, 10, 10, 10, 10, 10, 10, 7, 1, 2]

mouth = ['m1', 'm2', 'm3', 'm4', 'm5', 'm6']
mouth_weights = [10, 10, 50, 10, 15, 5]

nose = ['n1', 'n2']
nose_weights = [90, 10]


# 为每种特征创建一个字典类型的变量
# 每个特征对应的是其文件名
face_files = {
    "White": "face1",
    "Black": "face2"
}

ears_files = {
    "ears1": "ears1",
    "ears2": "ears2",
    "ears3": "ears3",
    "ears4": "ears4"
}

eyes_files = {
    "regular": "eyes1",
    "small": "eyes2",
    "rayban": "eyes3",
    "hipster": "eyes4",
    "focused": "eyes5"
}

hair_files = {
    "hair1": "hair1",
    "hair2": "hair2",
    "hair3": "hair3",
    "hair4": "hair4",
    "hair5": "hair5",
    "hair6": "hair6",
    "hair7": "hair7",
    "hair8": "hair8",
    "hair9": "hair9",
    "hair10": "hair10",
    "hair11": "hair11",
    "hair12": "hair12"
}

mouth_files = {
    "m1": "m1",
    "m2": "m2",
    "m3": "m3",
    "m4": "m4",
    "m5": "m5",
    "m6": "m6"
}

nose_files = {
    "n1": "n1",
    "n2": "n2"
}

# 生成特征
TOTAL_IMAGES = 100  # 生成的图片数量
all_images = []


# 一个递归函数，用于生成独特的图片组合
def create_new_image():
    new_image = {}
    # 对每一个特征组，根据权重选择一个随机的特征
    new_image["Face"] = random.choices(face, face_weights)[0]
    new_image["Ears"] = random.choices(ears, ears_weights)[0]
    new_image["Eyes"] = random.choices(eyes, eyes_weights)[0]
    new_image["Hair"] = random.choices(hair, hair_weights)[0]
    new_image["Mouth"] = random.choices(mouth, mouth_weights)[0]
    new_image["Nose"] = random.choices(nose, nose_weights)[0]

    if new_image in all_images:
        return create_new_image()
    else:
        return new_image


# 根据权重生成独一无二的图片组合
for i in range(TOTAL_IMAGES):
    new_trait_image = create_new_image()
    all_images.append(new_trait_image)

# 生成图像
for item in all_images:
    im1 = Image.open(f'./trait-layers/face/{face_files[item["Face"]]}.png').convert('RGBA')
    im2 = Image.open(f'./trait-layers/eyes/{eyes_files[item["Eyes"]]}.png').convert('RGBA')
    im3 = Image.open(f'./trait-layers/ears/{ears_files[item["Ears"]]}.png').convert('RGBA')
    im4 = Image.open(f'./trait-layers/hair/{hair_files[item["Hair"]]}.png').convert('RGBA')
    im5 = Image.open(f'./trait-layers/mouth/{mouth_files[item["Mouth"]]}.png').convert('RGBA')
    im6 = Image.open(f'./trait-layers/nose/{nose_files[item["Nose"]]}.png').convert('RGBA')

    # 创建每一个 composite
    com1 = Image.alpha_composite(im1, im2)
    com2 = Image.alpha_composite(com1, im3)
    com3 = Image.alpha_composite(com2, im4)
    com4 = Image.alpha_composite(com3, im5)
    com5 = Image.alpha_composite(com4, im6)

    # 转换为 RGB 模式
    rgb_im = com5.convert('RGB')
    file_name = str(item["tokenId"]) + ".png"
    rgb_im.save("./images/" + file_name)
