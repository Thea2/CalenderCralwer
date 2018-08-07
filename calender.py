# -*- coding: utf-8 -*-
# Author: zhou
# Time:  18-8-6 下午1:59
import spider
import save
import re


def first_day(source):
    """
    获取该月的第一天是星期几
    :param source: 页面源代码
    :return: 0-6分别代表星期日到星期六
    """
    # 通过当月第一天前有几天空白天判断其为星期几
    pattern = re.compile('<div class="wnrl_xingqi">(.*?)<div class="wnrl_riqi">')
    content = re.findall(pattern, source)
    blank_pattern = re.compile('<div class="wnrl_kongbai">')
    blank = re.findall(blank_pattern, content[0])
    print 'blank', len(blank)
    return (len(blank) + 1) % 7


def get_month_dict(source, cur_days, cur_week, year, month, last_month_day=0, last_month_week = 0):
    """
    获取这个月的日历
    :param source: 源代码
    :param cur_days: 该月第一天为该年第几天
    :param cur_week: 该月第一天为该年第几个星期
    :param month: 该月是几月份
    :return:
    """
    cur_day = first_day(source)
    day_pattern = re.compile('<div class="wnrl_riqi">(.*?)</div>')
    days = re.findall(day_pattern, source)
    print "days: ", len(days)
    xiu_pattern = re.compile('wnrl_riqi_xiu')
    ban_pattern = re.compile('wnrl_riqi_ban')
    holiday_pattern_one = re.compile('<span class="wnrl_td_bzl wnrl_td_bzl_lv">(.*?)</span>')
    holiday_pattern_two = re.compile('<span class="wnrl_td_bzl wnrl_td_bzl_hong">(.*?)</span>')
    month_dict = {}

    day_num = 1
    for day in days:
        day_dict = {}
        # 是否是节日，如果是保存其节日名称，否则保存-1
        holiday = re.findall(holiday_pattern_one, day)
        if len(holiday) != 0:
            day_dict['traditional_holiday'] = holiday[0]
        else:
            holiday = re.findall(holiday_pattern_two, day)
            if len(holiday) != 0:
                day_dict['traditional_holiday'] = holiday[0]
            else:
                day_dict['traditional_holiday'] = -1
        # 是否是工作日
        ban = len(re.findall(ban_pattern, day))
        if ban != 0:
            day_dict['is_workday'] = 1
        else:
            if cur_day == 0:
                day_dict['is_workday'] = 0
            elif cur_day == 6:
                day_dict['is_workday'] = 0
            else:
                day_dict['is_workday'] = 1
        # 是否是节假日
        xiu = len(re.findall(xiu_pattern, day))
        if xiu != 0:
            day_dict['is_holiday'] = 1
            day_dict['is_workday'] = 0
        else:
            day_dict['is_holiday'] = 0
        # 周几
        day_dict['day'] = cur_day
        # 第几天
        day_dict['sum_day'] = cur_days - last_month_day + 1
        # 第几周
        day_dict['sum_week'] = cur_week - last_month_week + 1
        # 日期
        if day_num < 10:
            day_num = '0' + str(day_num)
        day_str = year + '-' + month + '-' + str(day_num)
        day_dict['date'] = day_str

        month_dict[cur_days] = day_dict

        if cur_day == 0:
            cur_week += 1
        day_num = int(day_num) + 1
        cur_day = (cur_day + 1) % 7
        cur_days += 1

    return month_dict, cur_days, cur_week


def count_week_holiday(year_dict):
    """
    计算本周的节假日有几天
    :param year_dict:
    :return:
    """
    holiday_num = 0
    for i in range(1, len(year_dict) + 1):
        day = year_dict[i]
        if day['is_holiday'] == 1:
            holiday_num += 1
        if day['day'] == 0:
            for j in range(i - 6, i + 1):
                if j > 0:
                    if j <= len(year_dict):
                        year_dict[j]['week_holiday'] = holiday_num
            holiday_num = 0
    # 若最后一天不是星期天，统计这个不完整的星期的数据
    if year_dict[len(year_dict)]['day'] != 0:
        day = year_dict[len(year_dict)]
        for i in range(len(year_dict) - day['day'] + 1, len(year_dict) + 1):
            year_dict[i]['week_holiday'] = holiday_num
    return year_dict


def count_next_workday(year_dict):
    """
    计算每一天的下一个工作日还有几天
    :param year_dict:
    :return:
    """
    for i in range(1, len(year_dict) + 1):
        if year_dict[i]['is_workday'] == 1:
            if i < len(year_dict):
                if year_dict[i + 1]['is_workday'] == 1:
                    # 若当天为工作日且下一天为工作日时赋值0
                    year_dict[i]['next_workday'] = 0
                else:
                    next_day = 1
                    for j in range(i + 1, len(year_dict) + 1):
                        if year_dict[j]['is_workday'] == 1:
                            break
                        else:
                            next_day += 1
                    year_dict[i]['next_workday'] = next_day
            else:
                year_dict[i]['next_workday'] = 1
        else:
            next_day = 1
            for j in range(i + 1, len(year_dict) + 1):
                if year_dict[j]['is_workday'] == 1:
                    break
                else:
                    next_day += 1
            day = year_dict[i]
            day['next_workday'] = next_day
            year_dict[i] = day
    return year_dict


def my_main(year_need):
    """
    需要爬取某一年的日历
    :param year_need: int类型,暂支持区间(1900,2100)
    :return:
    """
    sum_day = 1
    sum_week = 1
    year_dict = {}
    # 打开在线日历网页
    spider.get_page("https://wannianrili.51240.com/")

    # 跳转到需要获取那一年的前一年的12月，并获取数据
    spider.select_year_option(str(year_need - 1))
    spider.select_month_option("12")
    source = spider.get_source()
    month_dict, sum_day, sum_week = get_month_dict(source, sum_day, sum_week, str(year_need - 1), "12")
    year_dict = dict(year_dict.items() + month_dict.items())
    last_month_day = sum_day
    last_month_week = sum_week

    spider.select_year_option(str(year_need))
    for month in range(1, 13):
        # 月份格式化
        if month < 10:
            month = '0' + str(month)
        else:
            month = str(month)
        print 'month:', month

        spider.select_month_option(month)
        source = spider.get_source()
        month_dict, sum_day, sum_week = get_month_dict(source, sum_day, sum_week, str(year_need),
                                                       month, last_month_day, last_month_week)
        year_dict = dict(year_dict.items() + month_dict.items())
        # break  # 测试
    print year_dict

    # 跳转到需要获取那一年的后一年的1月，并获取数据
    spider.select_year_option(str(year_need + 1))
    spider.select_month_option("01")
    source = spider.get_source()
    month_dict, sum_day, sum_week = get_month_dict(source, sum_day, sum_week, str(year_need + 1), "01")
    year_dict = dict(year_dict.items() + month_dict.items())

    # 统计
    year_dict = count_next_workday(year_dict)
    year_dict = count_week_holiday(year_dict)
    print year_dict

    col_name, col_data = save.format_data(year_dict, year_need)
    save.write_calender(str(year_need) + '年日历.csv', col_name, col_data)


if __name__ == '__main__':
    year = 2017
    my_main(year)
