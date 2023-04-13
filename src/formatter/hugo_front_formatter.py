# Copyright (c) 2022 Terwer Authors. All Rights Reserved.
# @author terwer on 2023/4/13
# ========================================================
import yaml

from src.formatter.basic_front_formatter import BasicFrontFormatter
from src.utils.strutils import MyDumper


class HugoFrontFormatter(BasicFrontFormatter):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.slug = ""
        self.url = ""
        self.date = ""
        self.tags = ""
        self.categories = ""
        self.lastmod = ""
        self.toc = True
        self.keywords = ""
        self.description = ""
        self.isCJKLanguage = True

    def to_dict(self):
        return {"title": self.title,
                "slug": self.slug,
                "url": self.url,
                "date": self.date,
                "tags": self.tags,
                "categories": self.categories,
                "lastmod": self.lastmod,
                "toc": self.toc,
                "keywords": self.keywords,
                "description": self.description,
                "isCJKLanguage": self.isCJKLanguage}

    def from_dict(self, dict_):
        self.title = dict_.get("title", "")
        self.slug = dict_.get("slug", "")
        self.url = dict_.get("url", "")
        self.date = dict_.get("date", "")
        self.tags = dict_.get("tags", "")
        self.categories = dict_.get("categories", "")
        self.lastmod = dict_.get("lastmod", "")
        self.toc = dict_.get("toc", True)
        self.keywords = dict_.get("keywords", "")
        self.description = dict_.get("description", "")
        self.isCJKLanguage = dict_.get("isCJKLanguage", True)

    def to_yaml(self):
        """
        将 Vuepress2FrontMatter 对象的属性转为 YAML 格式的字符串
        :return: YAML 格式的字符串
        """
        data = self.to_dict()
        if self.description is None:
            data.pop("description")
        if not self.toc:
            data.pop("toc")
        if not self.isCJKLanguage:
            data.pop("isCJKLanguage")
        return yaml.dump(data, allow_unicode=True, Dumper=MyDumper, indent=2, sort_keys=False)