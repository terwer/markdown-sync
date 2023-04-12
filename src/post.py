# Copyright (c) 2022 Terwer Authors. All Rights Reserved.
# @author terwer on 2023/4/12
# ========================================================
from src.category_info import CategoryInfo


class Post:
    """文章模型类，用于表示一篇文章对象"""

    def __init__(self):
        """创建一个新的文章对象"""
        self.post_id = ""  # 文章ID
        self.title = ""  # 标题
        self.mt_keywords = ""  # 关键词，用逗号分隔
        self.link = None  # 文章链接（可选）
        self.permalink = ""  # 永久链接
        self.short_desc = None  # 摘要（可选）
        self.description = ""  # 描述
        self.mt_excerpt = None  # 短评（可选）
        self.wp_slug = ""  # 别名
        self.date_created = None  # 创建时间
        self.categories: list[CategoryInfo] = []  # 分类列表
        self.mt_text_more = None  # 更多内容（可选）
        self.post_status = None  # 发布状态（可选）
        self.is_published = False  # 是否发布
        self.wp_password = ""  # 发布密码
