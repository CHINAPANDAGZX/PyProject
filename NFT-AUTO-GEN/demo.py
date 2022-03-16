import os
import random
from PIL import Image

# 全局变量
base_path = "E:\\Work\\SuperMetaverse\\NFT头像批量生成\\NFT头像测试"
base_body_path = base_path + "\\本体"
background_path = base_path + "\\背景"
mouth_path = base_path + "\\口饰品"
hand_path = base_path + "\\手饰品"
head_path = base_path + "\\头饰品"
glasses_path = base_path + "\\眼镜"
clothes_path = base_path + "\\衣服"

# 叠加顺序：背景——本体

"""
获取文件夹中所有元素文件名称
"""


def file_name(file_dir):
    file_list = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            # if os.path.splitext(file)[1] == '.png':
            # L.append(os.path.join(root, file))
            file_list.append(file)
    return file_list


# """
# 一个递归函数，用于生成独特的图片组合
# """
# def create_new_image():
#     new_image = {}
#     # 对每一个特征组，根据权重选择一个随机的特征
#     new_image["Face"] = random.choices(face, face_weights)[0]
#     new_image["Ears"] = random.choices(ears, ears_weights)[0]
#     new_image["Eyes"] = random.choices(eyes, eyes_weights)[0]
#     new_image["Hair"] = random.choices(hair, hair_weights)[0]
#     new_image["Mouth"] = random.choices(mouth, mouth_weights)[0]
#     new_image["Nose"] = random.choices(nose, nose_weights)[0]
#
#     if new_image in all_images:
#         return create_new_image()
#     else:
#         return new_image

class NewImage:
    def __init__(self, background, mouth, hand, head, glasses, clothes):
        self.background = background
        self.mouth = mouth
        self.hand = hand
        self.head = head
        self.glasses = glasses
        self.clothes = clothes


if __name__ == '__main__':
    background_list = file_name(background_path)
    mouth_list = file_name(mouth_path)
    hand_list = file_name(hand_path)
    head_list = file_name(head_path)
    glasses_list = file_name(glasses_path)
    clothes_list = file_name(clothes_path)


    im1 = Image.open(background_path + "/" + random.choices(background_list)[0]).convert('RGBA')
    im2 = Image.open(base_body_path + ".png").convert('RGBA')
    im3 = Image.open(mouth_path + "/" + random.choices(mouth_list)[0]).convert('RGBA')
    im4 = Image.open(hand_path + "/" + random.choices(hand_list)[0]).convert('RGBA')
    im5 = Image.open(head_path + "/" + random.choices(head_list)[0]).convert('RGBA')
    im6 = Image.open(glasses_path + "/" + random.choices(glasses_list)[0]).convert('RGBA')
    im7 = Image.open(clothes_path + "/" + random.choices(clothes_list)[0]).convert('RGBA')
    #
    # # 创建每一个 composite
    # final = Image.new("RGBA", im1.size)
    com1 = Image.alpha_composite(im1, im2)
    com2 = Image.alpha_composite(com1, im3)
    com3 = Image.alpha_composite(com2, im4)
    com4 = Image.alpha_composite(com3, im5)
    # com5 = Image.alpha_composite(com4, im6)
    # com6 = Image.alpha_composite(com5, im7)
    # com3 = Image.alpha_composite(im1, im4)
    # img = Image.open(background_path + "/" + random.choices(background_list)[0])
    com4.show()


    # newImage = NewImage(random.choices(background_list),
    #                     random.choices(mouth_list),
    #                     random.choices(hand_list),
    #                     random.choices(head_list),
    #                     random.choices(glasses_list),
    #                     random.choices(clothes_list))
