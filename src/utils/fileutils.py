# Copyright (c) 2022 Terwer Authors. All Rights Reserved.
# @author terwer on 2023/4/12
# ========================================================
import json
import os

from loguru import logger


def read_json_file(filename):
    """
    读取json文件
    :param filename: 文件名
    """
    if not os.path.exists(filename):
        return {}
    with open(filename, encoding="utf-8") as json_file:
        resp = json.load(json_file)
    return resp


def save_data_to_txt(save_folder, filename, content):
    """
    保存数据到指定目录的指定文件
    :param save_folder: 保存目录
    :param filename: 文件名
    :param content: 数据列表
    """
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    fname = os.path.join(save_folder, filename)
    if os.path.isdir(fname):
        logger.warning(f"This is dir, ignore {fname}")
        return
    with open(fname, mode='w', encoding='utf-8') as f:
        f.write(content)
