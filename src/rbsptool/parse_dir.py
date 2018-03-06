import os
import pandas as pd
import numpy as np
import re


##################################
# mag.pku-space.cn path config

RBSP_PATH = '/data/ECT/rbsp-ect.lanl.gov/data_pub/'
RBSP_B_COMPONENT_PATH = '/data/EMFISIS/emfisis.physics.uiowa.edu/Flight/'
RBSP_WAVE_BACKGROUND_PATH = '/data/EMFISIS/emfisis.physics.uiowa.edu/Flight/'
RBSP_WAVE_MATRIX_PATH = '/data/EMFISIS/emfisis.physics.uiowa.edu/Flight/'

##################################
# parse dir
# 遍历某数据所有版本号，输出匹配的第一个


def parse_mageis_dir(date, parrent_dir=RBSP_PATH, level=3, twin='a'):
    assert level in (2, 3)
    assert twin in ('a', 'b')
    # 如果查询单个时间，则在内部将其补为tuple
    if isinstance(date, str):
        date = (date, date)
    begin = pd.to_datetime(date[0]).date()
    end = pd.to_datetime(date[1]).date()
    date = begin
    # 设置各个变量名
    if level == 3:
        mageis_dir_suffix = 'rbsp{}/mageis/level3/pitchangle'.format(twin)
    elif level == 2:
        mageis_dir_suffix = 'rbsp{}/mageis/level2/sectors'.format(twin)
    mageis_prefix = 'rbsp{}_rel03_ect-mageis-L{}_'.format(twin, level)
    # 通过循环获得所有文件名
    dir_list = []
    time_offset = pd.Timedelta(days=1)
    while date <= end:
        time_dir = date.strftime('%Y')
        time_file_name = date.strftime('%Y%m%d')
        file_dir = os.path.join(parrent_dir, mageis_dir_suffix, time_dir)
        file_name = mageis_prefix + time_file_name
        if os.path.exists(file_dir):
            all_file_list = os.listdir(file_dir)
            for temp_file_name in all_file_list:
                if re.match('^' + file_name + '.', temp_file_name):
                    dir_list.append(os.path.join(file_dir, temp_file_name))
                    break
        date += time_offset
    return dir_list


def parse_rept_dir(date, parrent_dir=RBSP_PATH, level=3, twin='a'):
    assert level in (2, 3)
    assert twin in ('a', 'b')
    # 如果查询单个时间，则在内部将其补为tuple
    if isinstance(date, str):
        date = (date, date)
    begin = pd.to_datetime(date[0]).date()
    end = pd.to_datetime(date[1]).date()
    date = begin
    # 设置各个变量名
    if level == 3:
        rept_dir_suffix = 'rbsp{}/rept/level3/pitchangle'.format(twin)
    elif level == 2:
        rept_dir_suffix = 'rbsp{}/rept/level2/sectors'.format(twin)
    rept_prefix = 'rbsp{}_rel03_ect-rept-sci-L{}_'.format(twin, level)
    # 通过循环获得所有文件名
    dir_list = []
    time_offset = pd.Timedelta(days=1)
    while date <= end:
        time_dir = date.strftime('%Y')
        time_file_name = date.strftime('%Y%m%d')
        file_dir = os.path.join(parrent_dir, rept_dir_suffix, time_dir)
        file_name = rept_prefix + time_file_name
        if os.path.exists(file_dir):
            all_file_list = os.listdir(file_dir)
            for temp_file_name in all_file_list:
                if re.match('^' + file_name + '.', temp_file_name):
                    dir_list.append(os.path.join(file_dir, temp_file_name))
                    break
        date += time_offset
    return dir_list


def parse_rbsp_B_component_dir(date, parrent_dir=RBSP_B_COMPONENT_PATH, twin='a'):
    assert twin in ('a', 'b')
    # 如果查询单个时间，则在内部将其补为tuple
    if isinstance(date, str):
        date = (date, date)
    begin = pd.to_datetime(date[0]).date()
    end = pd.to_datetime(date[1]).date()
    date = begin
    # 设置各个变量名
    parrent_dir += 'RBSP-{}/L3'.format(twin.upper())
    B_component_prefix = 'rbsp-{}_magnetometer_4sec-sm_emfisis-L3_'.format(
        twin)
    # 通过循环获得所有文件名
    dir_list = []
    time_offset = pd.Timedelta(days=1)
    while date <= end:
        time_dir = date.strftime('%Y/%m/%d')
        file_dir = os.path.join(parrent_dir, time_dir)
        time_file_name = date.strftime('%Y%m%d')
        file_name = B_component_prefix + time_file_name
        if os.path.exists(file_dir):
            all_file_list = os.listdir(file_dir)
            for temp_file_name in all_file_list:
                if re.match('^' + file_name + '.', temp_file_name):
                    dir_list.append(os.path.join(file_dir, temp_file_name))
                    break
        date += time_offset
    return dir_list


def parse_rbsp_wave_background_dir(date, parrent_dir=RBSP_WAVE_BACKGROUND_PATH, twin='a'):
    assert twin in ('a', 'b')
    # 如果查询单个时间，则在内部将其补为tuple
    if isinstance(date, str):
        date = (date, date)
    begin = pd.to_datetime(date[0]).date()
    end = pd.to_datetime(date[1]).date()
    date = begin
    # 设置各个变量名
    parrent_dir += 'RBSP-{}/L2'.format(twin.upper())
    B_component_prefix = 'rbsp-{}_magnetometer_uvw_emfisis-L2_'.format(twin)
    # 通过循环获得所有文件名
    dir_list = []
    time_offset = pd.Timedelta(days=1)
    while date <= end:
        time_dir = date.strftime('%Y/%m/%d')
        file_dir = os.path.join(parrent_dir, time_dir)
        time_file_name = date.strftime('%Y%m%d')
        file_name = B_component_prefix + time_file_name
        if os.path.exists(file_dir):
            all_file_list = os.listdir(file_dir)
            for temp_file_name in all_file_list:
                if re.match('^' + file_name + '.', temp_file_name):
                    dir_list.append(os.path.join(file_dir, temp_file_name))
                    break
        date += time_offset
    return dir_list


def parse_rbsp_wave_matrix_dir(date, parrent_dir=RBSP_WAVE_MATRIX_PATH, twin='a'):
    assert twin in ('a', 'b')
    # 如果查询单个时间，则在内部将其补为tuple
    if isinstance(date, str):
        date = (date, date)
    begin = pd.to_datetime(date[0]).date()
    end = pd.to_datetime(date[1]).date()
    date = begin
    # 设置各个变量名
    parrent_dir += 'RBSP-{}/L2'.format(twin.upper())
    B_component_prefix = 'rbsp-{}_WFR-spectral-matrix_emfisis-L2_'.format(twin)
    # 通过循环获得所有文件名
    dir_list = []
    time_offset = pd.Timedelta(days=1)
    while date <= end:
        time_dir = date.strftime('%Y/%m/%d')
        file_dir = os.path.join(parrent_dir, time_dir)
        time_file_name = date.strftime('%Y%m%d')
        file_name = B_component_prefix + time_file_name
        if os.path.exists(file_dir):
            all_file_list = os.listdir(file_dir)
            for temp_file_name in all_file_list:
                if re.match('^' + file_name + '.', temp_file_name):
                    dir_list.append(os.path.join(file_dir, temp_file_name))
                    break
        date += time_offset
    return dir_list
