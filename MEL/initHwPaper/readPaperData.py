# -*- coding: UTF-8 -*-
# 读取CSV中的数据
# 时间：2023年3月17日10:32:15


import codecs
import csv
import uuid
import time

hw_paper_list = []  # 空列表


def readData():
    with codecs.open('./paper.csv', encoding='GBK') as f:
        # for row in csv.DictReader(f, skipinitialspace=True):
        sqlFile = open("insert.sql", "w", encoding='utf-8')
        count = 0
        for paper in csv.reader(f):
            id = str(uuid.uuid1())
            ship_id = "091"
            code = "PP" + ship_id + str(count).zfill(7)
            paper_code = ""
            name = paper[1]
            eng_name = ""
            paper_type = ""
            is_permanent = "1" if paper[4].replace(' ', '').lower() == "long" else "0"
            issue_date = "" if paper[3].replace(' ', '') == "" else paper[3].replace(' ', '').replace('.', '-')
            expiration_time = "" if paper[4].replace(' ', '').lower() == "long" else paper[4].replace(' ', '').replace('.', '-')
            inspection_cycle = "0"
            front_tolerance = "0"
            back_tolerance = "0"
            issue_authority = "" if paper[2].replace(' ', '') == "" else paper[2].replace(' ', '')
            property = "0" if paper[4].replace(' ', '').lower() == "long" else ""
            instrument_id = ""
            crew_id = ""
            responsible_role = ""
            remark = "" if paper[5].replace(' ', '') == "" else paper[5].replace(' ', '')
            create_by = "1"
            create_time = time.strftime("%F %T")
            update_by = "1"
            update_time = time.strftime("%F %T")
            del_flag = "0"
            is_sent = "0"
            sent_status = "0"
            sent_target = ""
            is_wfpass = ""
            sort_id = ""
            zfUserId = ""
            zfReason = ""
            zfTime = ""
            editeReason = ""
            status = "0"
            super_role = ""
            last_check_time = ""
            # 都是船舶证书
            paper_property = "0"
            paper_class = ""
            ship = ""
            #  处理周期
            sql = "INSERT INTO `hw_paper`" \
                  "(`id`, `code`, `paper_code`, `name`, `eng_name`," \
                  " `paper_type`, `is_permanent`, `issue_date`, `inspection_cycle`," \
                  " `expiration_time`, `front_tolerance`, `back_tolerance`, `issue_authority`," \
                  " `property`, `instrument_id`, `crew_id`, `responsible_role`, `remark`," \
                  " `create_by`, `create_time`, `update_by`, `update_time`, `del_flag`," \
                  " `is_sent`, `sent_status`, `sent_target`, `is_wfpass`, `ship_id`," \
                  " `sort_id`, `zfUserId`, `zfReason`, `zfTime`, `editeReason`, `status`," \
                  " `super_role`, `last_check_time`, `paper_property`, `paper_class`, `ship`) VALUES " \
                  "({}, {}, {}, {}, {}," \
                  " {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});\n" \
                .format("'" + id + "'", "'" + code + "'", "'" + paper_code + "'", "'" + name + "'",
                        "'" + eng_name + "'",
                        "'" + paper_type + "'", "'" + is_permanent + "'", "'" + issue_date + "'",
                        "'" + inspection_cycle + "'",
                        "'" + expiration_time + "'", "'" + front_tolerance + "'", "'" + back_tolerance + "'",
                        "'" + issue_authority + "'",
                        "'" + property + "'", "'" + instrument_id + "'", "'" + crew_id + "'",
                        "'" + responsible_role + "'", "'" + remark + "'",
                        "'" + create_by + "'", "'" + create_time + "'", "'" + update_by + "'", "'" + update_time + "'",
                        "'" + del_flag + "'",
                        "'" + is_sent + "'", "'" + sent_status + "'", "'" + sent_target + "'", "'" + is_wfpass + "'",
                        "'" + ship_id + "'",
                        "'" + sort_id + "'", "'" + zfUserId + "'", "'" + zfReason + "'", "'" + zfTime + "'",
                        "'" + editeReason + "'", "'" + status + "'",
                        "'" + super_role + "'", "'" + last_check_time + "'", "'" + paper_property + "'",
                        "'" + paper_class + "'",
                        "'" + ship + "'")

            print(paper)
            sqlFile.write(sql)
            count += 1
        sqlFile.close()
    f.close()
    return hw_paper_list


if __name__ == '__main__':
    hw_paper_list = readData()
