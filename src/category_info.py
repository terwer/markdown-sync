# Copyright (c) 2022 Terwer Authors. All Rights Reserved.
# @author terwer on 2023/4/12
# ========================================================
class CategoryInfo:
    """分类信息类"""

    def __init__(self):
        """初始化分类信息类"""
        self.category_id = None  # 分类ID
        self.parent_id = None  # 父分类ID
        self.description = None  # 分类名称
        self.category_name = None  # 分类英文名
        self.category_description = None  # 分类详情
        self.html_url = None  # 分类地址
        self.rss_url = None  # 分类订阅地址
