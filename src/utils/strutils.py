# Copyright (c) 2022 Terwer Authors. All Rights Reserved.
# @author terwer on 2023/4/12
# ========================================================
import datetime
import json
import re

import requests
import yaml
from slugify import slugify


def is_contain_any_char(my_string, char_array):
    """
    哦安短字符串是否包含数组中的任何一个
    :param my_string: 字符串
    :param char_array: 待检测字符数组
    """
    for char in char_array:
        if char in my_string:
            return True
    return False


def remove_title_number(str):
    ret = re.sub(r"^\d+\.?", "", str).strip()
    ret = ret.replace(".md", "")
    return ret


def translate(q, to_lang="en", from_lang="zh"):
    """
    获取翻译结果
    :param q: 中文
    :param to_lang: 目标语言
    :param from_lang: 原始语言
    """
    # Define the endpoint and query parameters
    url = "https://api.terwer.space/api/translate"
    params = {"q": q, "to": to_lang}

    # Make a GET request to the API with the parameters
    response = requests.get(url, params=params)

    # Parse the JSON response to extract the translation text
    result = json.loads(response.text)
    translation = result[0][0]

    return translation


def slug(q):
    """
    根据中文获取别名
    :param q: 中文字符
    :return:
    """
    if not q:
        return ""
    slug_text = slugify(q)
    return slug_text


def slug_with_translate(q):
    """
    根据中文获取别名，自带翻译
    :param q: 中文字符
    :return:
    """
    translation = translate(q)
    # logger.debug(f"translation=>{translation}")
    slug_text = slugify(translation)
    return slug_text


def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} is not JSON serializable")


class MyDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)

    def represent_data(self, data):
        return super(MyDumper, self).represent_data(data)


def extract_frontmatter_from_file(file_path):
    """
    从 Markdown 文件中提取 front matter，并返回 front matter 和正文内容

    Args:
        file_path (str): Markdown 文件路径

    Returns:
        tuple: 包含两个元素的元组，第一个元素为 front matter 的字典格式，第二个元素为去除 front matter 后的 Markdown 正文内容
    """
    with open(file_path, "r") as f:
        content = f.read()
    return extract_frontmatter(content)


def extract_frontmatter(content):
    """
    从 Markdown 字符串中提取 front matter，并返回 front matter 和正文内容

    Args:
        content (str): 包含 front matter 的 Markdown 字符串

    Returns:
        tuple: 包含两个元素的元组，第一个元素为 front matter 的字典格式，第二个元素为去除 front matter 后的 Markdown 正文内容
    """
    # 使用正则表达式匹配 front matter
    match = re.search(r"^---\n(.|\n)*?---\n", content)
    # 如果找到了 front matter 则提取并删除
    if match:
        front_matter = match.group(0).strip()
        content = content.replace(front_matter, "").strip()
        # 从 front_matter 中加载 YAML 数据
        data = list(yaml.load_all(front_matter, Loader=yaml.FullLoader))[0]
        # 将 data 转换为 JSON 字符串
        # json_data = json.dumps(data, default=serialize_datetime, ensure_ascii=False)
        # print(json_data)
    else:
        data = None

    return data, content
