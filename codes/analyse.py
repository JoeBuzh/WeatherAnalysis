# -*- encoding: utf-8 -*-
'''
@Filename    : analyse.py
@Datetime    : 2020/04/15 16:48:46
@Author      : Joe-Bu
@version     : 1.0
'''

import os
import sys
from datetime import datetime, timedelta

import pandas as pd
import matplotlib.pyplot as plt


def load(filename):
    assert os.path.exists(filename)

    df = pd.read_csv(filename, sep=',', encoding='utf-8', engine='python')
    return df


def analyse(data):
    print(data.info())


def main():
    df_PRCP = load('../results/PRCP.csv')
    # print(df_PRCP)
    analyse(df_PRCP)


if __name__ == "__main__":
    main()