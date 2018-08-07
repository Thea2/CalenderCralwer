# -*- coding: utf-8 -*-
# Author: zhou
# Time:  18-8-6 下午4:16
import csv


def format_data(year_dict):
    """
    将获取到的数据转为写入格式
    :param year_dict:
    :return:
    """
    col_name = ['日期', '今日是周几', '今日是本年的第几周', '今日是本年的第几天', '是否节假日', '本周的节假日有几天', '距离下一个工作日有几天']
    day_dict = {0: "星期天", 1: "星期一", 2: "星期二", 3: "星期三", 4: "星期四", 5: "星期五", 6: "星期六"}
    is_dict = {0: "否", 1: "是"}
    col_data = []
    for i in range(1, len(year_dict) + 1):
        day = year_dict[i]
        day_list = []
        day_list.append(day['date'])
        day_list.append(day_dict[day['day']])
        day_list.append(day['sum_week'])
        day_list.append(day['sum_day'])
        day_list.append(is_dict[day['is_holiday']])
        day_list.append(day['week_holiday'])
        day_list.append(day['next_workday'])
        col_data.append(day_list)
    return col_name, col_data


def write_calender(filename, col_name, col_data):
    """
    将数据写入csv文件
    :param filename: 文件名
    :param col_name: 列名列表
    :param col_data: 数据列表（可多行）
    :return:
    """
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        # 先写入列名
        writer.writerow(col_name)
        # 再写入数据
        writer.writerows(col_data)