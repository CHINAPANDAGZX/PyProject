# -*- coding: UTF-8 -*-
# 用于存放需要的对象


class Instrument:
    """设备类"""

    def __init__(self, id, name):
        self.id = id  # 设备ID
        self.name = name  # 设备名称

class WorkPackageItem:
    """工作包关联工作项目中间表类"""

    def __init__(self, package_id, package_name, item_id, item_name):
        self.package_id = package_id  # 保养项目ID
        self.package_name = package_name  # 保养包名称
        self.item_id = item_id  # 保养项目ID
        self.item_name = item_name  # 保养项目名称
