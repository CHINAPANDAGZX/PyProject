# -*- coding: UTF-8 -*-
# 用于将设备名称进行替换


def replaceDeviceName(device_name):
    """
    将设备名称进行替换
    """
    device_name = device_name.replace("瓶位、", "瓶位").replace("（", "(").replace("）", ")").replace(" ", "").replace("\n", "")
    device_name.replace("瓶位、", "瓶位")
    device_name_list = device_name.split("、")
    result_device_name_list = []
    for device_name_item in device_name_list:
        if device_name_item == "直读深海温盐深剖面仪及采水系统":
            result_device_name_list.append("SBE911 PLUS CTD  温盐深剖面仪（24瓶位/12升）、SBE911 PLUS CTD  温盐深剖面仪（36瓶位/10升）")
        elif device_name_item == "直读深海温盐深剖面仪及采水系统(24瓶位12L)":
            result_device_name_list.append("SBE911 PLUS CTD  温盐深剖面仪（24瓶位/12升）")
        elif device_name_item == "直读深海温盐深剖面仪及采水系统(36瓶位10L)":
            result_device_name_list.append("SBE911 PLUS CTD  温盐深剖面仪（36瓶位/10升）")
        elif device_name_item == "自容式深海投放式ADCP":
            result_device_name_list.append("挂载式多普勒声速剖面仪（LADCP）（24瓶位12L）、挂载式多普勒声速剖面仪（LADCP）（36瓶位10L）")
        elif device_name_item == "船舶自动气象站(AWS430)":
            result_device_name_list.append("船舶气象站")
        elif device_name_item == "船载相控阵宽带走航式声学多普勒海流剖面仪":
            result_device_name_list.append("OS38 走航声学多普勒流速剖面式、OS150 走航声学多普勒流速剖面式、Mariner300 走航声学多普勒流速剖面式")
        elif device_name_item == "走航海水多参数剖面观测仪(MVP300)":
            result_device_name_list.append("走航式多参数剖面仪")
        elif device_name_item == "走航表层海水多参数观测仪(SBE21)":
            result_device_name_list.append("SBE21 走航表层温盐仪")
        else:
            result_device_name_list.append(device_name_item)
    device_name = '、'.join(result_device_name_list)
    return device_name
