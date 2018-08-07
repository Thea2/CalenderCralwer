# -*- coding: utf-8 -*-
# Author: zhou
# Time:  18-8-6 下午1:47
import random
import time

from selenium import webdriver
from selenium.webdriver.support.ui import Select


browser = webdriver.Firefox(executable_path='/home/zhou/PycharmProjects/CalenderCrawler/geckodriver')


def close_browser():
    # 关闭浏览器
    browser.close()


def get_source():
    # 返回当前页面源代码
    return browser.page_source


def get_page(url):
    """
    获取某个页面源代码
    :param url: 页面链接
    :return: 页面源代码
    """
    browser.get(url)
    minute = random.randint(4, 9)
    time.sleep(minute)
    return browser.page_source


def select_year_option(year):
    """
    选择页面为某一年的日历
    :param year: 字符串格式xxxx，如：2017
    :return:
    """
    select = Select(browser.find_element_by_id("wnrl_xuanze_nian"))
    select.select_by_value(year)
    minute = random.randint(4, 9)
    time.sleep(minute)


def select_month_option(month):
    """
    选择页面为某一个月的日历
    :param month: 字符串格式xx，如：01
    :return:
    """
    select = Select(browser.find_element_by_id("wnrl_xuanze_yue"))
    select.select_by_value(month)
    minute = random.randint(4, 9)
    time.sleep(minute)


def get_one_calender(url, year, month):
    """
    获取某年某月的日历页面源代码
    :param url:
    :param year:
    :param month:
    :return:
    """
    get_page(url)
    select_year_option(year)
    select_month_option(month)
    return browser.page_source
