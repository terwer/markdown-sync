# Copyright (c) 2022 Terwer Authors. All Rights Reserved.
# @author terwer on 2023/4/12
# ========================================================
import yaml

from src.utils import strutils
from src.utils.strutils import MyDumper


class Vuepress2FrontFormatter:
    def __init__(self):
        """
        初始化函数，创建一个空的 Vuepress2FrontMatter 对象
        """
        self.title = ""  # 文章标题
        self.short_title = ""  # 文章短标题
        self.description = ""  # 文章描述
        self.icon = None  # 文章图标
        self.author = None  # 作者名称
        self.is_original = False  # 是否为原创文章
        self.date = ""  # 发布日期
        self.category = []  # 文章分类
        self.tag = []  # 文章标签
        self.sticky = False  # 是否置顶
        self.star = False  # 是否加星
        self.article = True  # 正文内容
        self.timeline = False  # 时间轴
        self.image = None  # 文章主图
        self.banner = None  # 文章横幅

    def to_dict(self):
        """
        将 Vuepress2FrontMatter 对象转换为字典类型
        :return: 字典类型结果
        """
        result = {
            "title": self.title,
            "short_title": self.short_title,
            "description": self.description,
            "icons": self.icon,
            "author": self.author,
            "is_original": self.is_original,
            "date": self.date,
            "category": self.category,
            "tag": self.tag,
            "sticky": self.sticky,
            "star": self.star,
            "article": self.article,
            "timeline": self.timeline,
            "image": self.image,
            "banner": self.banner
        }
        return result

    def from_dict(self, data):
        """
        从字典类型的数据中加载 Vuepress2FrontMatter 对象
        :param data: 字典类型数据
        """
        self.title = data.get("title", "")
        self.short_title = data.get("short_title", "")
        self.description = data.get("description", "")
        self.icon = data.get("icon", "")
        self.author = data.get("author", "")
        self.is_original = data.get("is_original", False)
        self.date = data.get("date", "")
        self.category = data.get("category", "")
        self.tag = data.get("tag", [])
        self.sticky = data.get("sticky", False)
        self.star = data.get("star", False)
        self.article = data.get("article", "")
        self.timeline = data.get("timeline", "")
        self.image = data.get("image", "")
        self.banner = data.get("banner", "")

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

    def to_yaml(self):
        """
        将 Vuepress2FrontMatter 对象的属性转为 YAML 格式的字符串
        :return: YAML 格式的字符串
        """
        data = self.to_dict()
        if self.description is None:
            data.pop("description")
        if self.icon is None:
            data.pop("icons")
        if self.author is None:
            data.pop("author")
        if self.image is None:
            data.pop("image")
        if self.banner is None:
            data.pop("banner")
        if not self.is_original:
            data.pop("is_original")
        if not self.sticky:
            data.pop("sticky")
        if not self.star:
            data.pop("star")
        return yaml.dump(data, allow_unicode=True, Dumper=MyDumper, indent=2, sort_keys=False)
