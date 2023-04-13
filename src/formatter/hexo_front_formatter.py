# Copyright (c) 2022 Terwer Authors. All Rights Reserved.
# @author terwer on 2023/4/12
# ========================================================
import yaml

from src.formatter.basic_front_formatter import BasicFrontFormatter
from src.utils.strutils import MyDumper


class HexoFrontFormatter(BasicFrontFormatter):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.date = None
        self.updated = ""
        self.excerpt = ""
        self.tags = ""
        self.categories = ""
        self.permalink = ""
        self.comments = True
        self.toc = True
        self.hidden = False

    def to_dict(self):
        return {
            "title": self.title,
            "date": self.date,
            "updated": self.updated,
            "excerpt": self.excerpt,
            "tags": self.tags,
            "categories": self.categories,
            "permalink": self.permalink,
            "comments": self.comments,
            "toc": self.toc,
            "hidden": self.hidden
        }

    def from_dict(self, data):
        self.title = data.get("title", "")
        self.date = data.get("date", "")
        self.updated = data.get("updated", "")
        self.excerpt = data.get("excerpt", "")
        self.tags = data.get("tags", "")
        self.categories = data.get("categories", "")
        self.permalink = data.get("permalink", "")
        self.comments = data.get("comments", True)
        self.toc = data.get("toc", True)
        self.hidden = data.get("hidden", False)

    def to_yaml(self):
        """
        将 Vuepress2FrontMatter 对象的属性转为 YAML 格式的字符串
        :return: YAML 格式的字符串
        """
        data = self.to_dict()
        if self.excerpt is None:
            data.pop("excerpt")
        if self.date is None:
            data.pop("date")
        if not self.hidden:
            data.pop("hidden")
        return yaml.dump(data, allow_unicode=True, Dumper=MyDumper, indent=2, sort_keys=False)

