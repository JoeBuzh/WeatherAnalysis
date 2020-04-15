# -*- encoding: utf-8 -*-
'''
@Filename    : extract.py
@Datetime    : 2020/04/15 10:53:00
@Author      : Joe-Bu
@version     : 1.0
@Function    : Extract data from *.dly file and format save to *.csv file.
'''

import os
import re
import sys
import math
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FuncFormatter

ISTEST = False
STATIONID = 'CHM00057679'


def hsv2rgb(h, s, v):
    '''
        hsv mode -> rgb mode.
    '''
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0 ,0
    if hi == 0:
        r, g, b = v, t, p
    elif hi == 1:
        r, g, b = q, v, p
    elif hi == 2:
        r, g, b = p, v, t
    elif hi == 3:
        r, g, b = p, q, v
    elif hi == 4:
        r, g, b = t, p, v
    elif hi == 5:
        r, g, b = v, p, q
    r, g, b = int(r*255), int(g*255), int(b*255)

    return r, g, b


def color(value):
    '''
        rgb -> 16
    '''
    digit = list(map(str, range(10))) + list('ABCDEF')
    if isinstance(value, tuple):
        string = '#'
        for i in value:
            a1 = i // 16
            a2 = i % 16
            string += digit[a1] + digit[a2]

        return string

def getAllData(filename: str) -> list:
    '''
        Open file and get all records.
    '''
    assert os.path.exists(filename)

    with open(filename, 'r') as f:
        data = f.readlines()
        filtered_data = list(filter(lambda x: x != '', data))

    return filtered_data


def parseAll(lines: list, ):
    '''
        Parse all lines.
    '''
    # 准备DataFramer容器
    template = pd.DataFrame(columns=['datetime', 'year', 'month', 'day', 'value', 'color', 'type']) 
    df_PRCP = template # 降雨
    df_TAVG = df_PRCP  # 平均温度
    df_TMIN = df_PRCP  # 最小温度
    df_TMAX = df_PRCP  # 最大温度

    l1, l2, l3, l4 = [], [], [], []

    # print(lines)
    for _line in lines:
        _res = re.split(r'\s+|s|S', _line)
        # print(_res)
        res = list(filter(lambda x: x !='', _res))
        # print(' '.join(res))
        _type, dfs = parseRow(res)
        if _type == 'PRCP':
            # pd.concat([df_PRCP, dfs])
            l1.append(dfs)
        elif _type == 'TAVG':
            # pd.concat([df_TAVG, dfs])
            l2.append(dfs)
        elif _type == 'TMIN':
            # pd.concat([df_TMIN, dfs])
            l3.append(dfs)
        elif _type == 'TMAX':
            # pd.concat([df_TMAX, dfs])
            l4.append(dfs)

    print('-'*100)
    # print(l1)

    return pd.concat(l1), pd.concat(l2), pd.concat(l3), pd.concat(l4) 


def parseRow(row: list):
    '''
        Parse single row(line).
    '''
    _date = row[0].replace(STATIONID, '')[:-4]
    _type = row[0].replace(STATIONID, '')[-4:]

    temp = []

    for day, value in enumerate(row[1:]):
        if day < 9:
            dateStr = _date + '0{}'.format(str(day+1))
        elif day == 9:
            dateStr = _date + '{}'.format(str(day+1))
        elif day < 30:
            dateStr = _date + '{}'.format(str(day+1))
        else:
            continue
        dateTime = datetime.strptime(dateStr, "%Y%m%d")

        _df = singleDf(value, _type, dateTime)
        temp.append(_df)

    # print(pd.concat(temp))

    return _type, pd.concat(temp)


def singleDf(value, _type, dateTime):
    _value = float(value) * 0.1       # 值：温度(0.1摄氏度) 降水量(0.1mm)
    _year = dateTime.strftime("%Y")   # 年
    _month = dateTime.strftime("%m")  # 月
    _day = dateTime.strftime("%d")    # 日
    _color = None

    if _type == 'PCRC':
        _color = '#FFFFFF'
        if _value > 0:
            _color = color(tuple(hsv2rgb(int(_value*0.75)+180, 1, 1)))
        elif _value != -999.9:
            _color = '#FFFFFF'

    elif _type == 'TAVG':
        _color = '#FFFFFF'
        if _value != -999.9:
            _color = color(tuple(hsv2rgb(int(-7 * _value) + 240, 1, 1)))

    df = pd.DataFrame({'datetime': [dateTime], 'year': [_year], 'month': [_month],
        'day': [_day], 'value': [_value], 'color': [_color], 'type': [_type]})

    return df


def main():
    filepath = '../datas/{}.dly'.format(STATIONID)
    data = getAllData(filepath)
    # print(data[-1])
    df_PRCP, df_TAVG, df_TMAX, df_TMIN = parseAll(data[-36:])

    df_PRCP.to_csv('../results/PRCP.csv', encoding='utf-8')
    df_TAVG.to_csv('../results/TAVG.csv', encoding='utf-8')
    df_TMIN.to_csv('../results/TMIN.csv', encoding='utf-8')
    df_TMAX.to_csv('../results/TMAX.csv', encoding='utf-8')


if __name__ == "__main__":
    main()