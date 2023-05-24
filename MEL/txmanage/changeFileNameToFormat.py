# -*- coding:utf-8 -*-

import os
import re

# RE_FILE_NAME_FORMAT = "(\d{2,3})-尚硅谷-Java语言高级-(.*)\.avi"


pathList = ["C:\\Users\\admin\\Desktop\\体系开发相关\\ITG体系8.0版 PDF\\须知下 SMI II"]

class BatchRename:
    def __init__(self):
        self.path = []
        for path in pathList:
            path = os.path.abspath(path)
            if (os.path.exists(path)):
                self.path.append(path)
        print({"当前修改的文件目录列表": self.path})

    def getFileNames(self, path):
        return os.listdir(path)

    def renameOnefile(self, src_name, dst_name):
        os.rename(src_name, dst_name)

    def batchRename(self, path):
        fileNames = self.getFileNames(path)

        # rule = re.compile(RE_FILE_NAME_FORMAT)
        for fileName in fileNames:
            fileNewName = fileName.replace(" ", "_", 1)
            srcName = os.path.join(os.path.abspath(path), fileName)
            dstName = os.path.join(os.path.abspath(path), fileNewName)
            self.renameOnefile(srcName, dstName)
            print("修改前：{}-{}".format(path, fileName))
            print("修改后：{}-{}".format(path, fileNewName))
            # if fileName.endswith('.pdf'):
                # subNames = rule.findall(fileName)
                # if (len(subNames) > 0):
                #     sn, name = subNames[0]
                #     newFileName = "{}-{}.avi".format(sn, name)
                #     srcName = os.path.join(os.path.abspath(path), fileName)
                #     dstName = os.path.join(os.path.abspath(path), newFileName)
                #     self.renameOnefile(srcName, dstName)
                # 将文件名中的前两个空格替换为下划线


    def runBatchProc(self):
        for path in self.path:
            self.batchRename(path)


if __name__ == '__main__':
    """
        用于对国贸体系文件导入文件进行格式化处理
    匹配方式：
        修改RE_FILE_NAME_FORMAT正则表达式
    使用方法:
        1,在pathString添加需要修改文件名的路径在
        2,打开cmd终端
        3,执行：python batchRename.py
    """
    batch = BatchRename()
    batch.runBatchProc()