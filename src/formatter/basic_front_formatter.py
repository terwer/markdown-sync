# Copyright (c) 2022 Landray Authors. All Rights Reserved.
# @author terwer on 2023/4/12
# ========================================================
import abc

import yaml

from src.utils import strutils


class BasicFrontFormatter(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def to_dict(self):
        pass

    @abc.abstractmethod
    def from_dict(self, data):
        pass

    def from_md(self, md_text):
        """
        根据 Markdown 文本内容提取 Vuepress2FrontMatter 对象中的属性
        :param md_text: Markdown 文本内容
        """
        # 实现从 Markdown 中提取 Vuepress2FrontMatter 对象中的属性逻辑
        data, content = strutils.extract_frontmatter(md_text)
        self.from_dict(data)

    def to_md(self):
        """
        将 Vuepress2FrontMatter 对象转换为 Markdown 格式的字符串
        :return: Markdown 格式字符串结果
        """
        result = ["---\n", self.to_yaml(), "---\n"]
        return "".join(result)

    def from_yaml(self, yaml_text, reverse=False):
        """
        加载或反向加载 Vuepress2FrontMatter 对象的属性，支持 YAML 格式的数据
        :param yaml_text: YAML 格式的字符串
        :param reverse: 是否为反向操作，True 表示反向操作，False 表示正常加载
        """
        if not reverse:
            data = yaml.load(yaml_text, Loader=yaml.FullLoader) or {}
            self.from_dict(data)
        else:
            data = self.to_dict()
            result = yaml.dump(data)
            return result

    @abc.abstractmethod
    def to_yaml(self):
        pass
