# Copyright (c) 2022 Terwer Authors. All Rights Reserved.
# @author terwer on 2023/4/12
# ========================================================
import os
import re

import yaml
from loguru import logger

from src.category_info import CategoryInfo
from src.converter.base_converter import BaseConverter
from src.formatter.vuepress2_front_formatter import Vuepress2FrontFormatter
from src.post import Post
from src.utils import strutils, dictutils, fileutils
from src.utils.strutils import MyDumper


class vuepress1ToVuepress2(BaseConverter):
    def __init__(self):
        self.IGNORED_PATHS = ["node_modules", ".vuepress"]
        self.IGNORED_FILES = [".DS_Store"]
        self.EXCLUDE_CATS = ["更多", "默认分类", "temp", "博文", "心情随笔", "_posts"]
        self.VUEPRESS1_FOLDER = (
            "/Users/terwer/Documents/mydocs/gitlab-repos/terwer.github.io/docs"
        )
        self.CATS_MAP_DIR = (
            "/Users/terwer/Documents/mydocs/zhi-markdown-sync/src/dir_cats_map.json"
        )
        self.VUEPRESS2_DOCS_PATH = (
            "/Users/terwer/Documents/mydocs/github-repos/vuepress2-blog/src/post"
        )
        self.LIMIT_COUNT = -1
        # 是否使用分类作为保存路径
        self.use_category_as_dir = False

    def convert(self):
        logger.info("Convert is starting...")
        self._do_parse_file_info(self.VUEPRESS1_FOLDER)

    def _do_parse_file_info(self, base_dir):
        """
        解析目录获取文件和文件名
        :param base_dir: 目录
        """
        logger.info(f"Start reading paths at {base_dir}")
        # 遍历指定目录及子目录
        files_count = 0
        dir_cats = []
        for dirpath, dirnames, filenames in os.walk(base_dir):
            if strutils.is_contain_any_char(dirpath, self.IGNORED_PATHS):
                # logger.warning(f"Ignored folder {dirpath}")
                continue
            if 0 < self.LIMIT_COUNT <= files_count:
                logger.warning(f"Limited size {self.LIMIT_COUNT}, end")
                break

            for each_file in filenames:
                if strutils.is_contain_any_char(each_file, self.IGNORED_FILES):
                    # logger.warning(f"Ignored file {each_file}")
                    continue
                cat_save_path = ""
                title_save_path = ""

                post = Post()
                post.title = strutils.remove_title_number(each_file)
                cates = self._parse_cat_arr(dirpath)
                post.categories = cates

                full_path = str(os.path.join(dirpath, each_file))
                # 读取文件属性等操作
                data, content = strutils.extract_frontmatter_from_file(full_path)
                post.description = content

                # 解析 front formatter
                if data is not None:
                    # 标题
                    post.title = dictutils.get_dict_str_value(data, "title")
                    # permalink
                    permalink = dictutils.get_dict_str_value(data, "permalink")
                    # 分类
                    f_cats = dictutils.get_dict_value(data, "categories")
                    if f_cats is not None:
                        cate_names = [c.description for c in post.categories]
                        f_cats = [s.replace("《", "").replace("》", "") for s in f_cats]
                        dir_cats = dir_cats + f_cats
                        # 保存路径
                        dir_cates_map = fileutils.read_json_file(self.CATS_MAP_DIR)
                        cat_path_list = []
                        for cate_name in cate_names:
                            cate_name_en = dir_cates_map.get(cate_name)
                            cate_slug = strutils.slug(cate_name_en)
                            cat_path_list.append(cate_slug)
                            # 保存目录说明
                            cur_cat_save_path = os.sep.join(cat_path_list)
                            # 是否保存目录
                            if self.use_category_as_dir:
                                self._make_vuepress2_dir_category(
                                    cur_cat_save_path, cate_name
                                )
                        cat_save_path = os.sep.join(cat_path_list)
                        title_save_path = permalink.replace(".html", ".md")
                        title_save_path = title_save_path.replace("/post/", "")
                        title_save_path = title_save_path.replace("/pages/", "")
                        if title_save_path.endswith("/"):
                            title_save_path = (
                                title_save_path[:-1] + ".md"
                            )  # 去掉末尾的斜杠，然后拼接扩展名
                        title_save_path = os.sep + title_save_path

                        post_cats = cate_names + f_cats
                        # 去重
                        post_cats = list(set(post_cats))
                        # 去除分类
                        post_cats = [i for i in post_cats if i not in self.EXCLUDE_CATS]
                        post_cats = ["timeline" if i == "随笔" else i for i in post_cats]
                        cts = []
                        for pc in post_cats:
                            ct = CategoryInfo()
                            ct.description = pc
                            cts.append(ct)
                        post.categories = cts
                    # date
                    post.date_created = dictutils.get_dict_str_value(data, "date")
                    # short_desc
                    meta = dictutils.get_dict_value(data, "meta")
                    if meta is not None:
                        for meta_item in meta:
                            if meta_item["name"] == "description":
                                post.short_desc = meta_item["content"]
                                break
                    tags = dictutils.get_dict_value(data, "tags")
                    if tags is not None:
                        tags = list(filter(lambda x: x is not None, tags))
                        post.mt_keywords = tags
                    else:
                        post.mt_keywords = []

                # 生成vuepress2支持的formatter
                v2f = self._make_vuepress2_formatter(post)
                # 附加formatter到正文
                post.description = v2f + post.description

                # 生成分类目录
                md_save_full_path = self.VUEPRESS2_DOCS_PATH
                if self.use_category_as_dir:
                    md_save_full_path = os.path.join(
                        self.VUEPRESS2_DOCS_PATH, cat_save_path
                    )
                if cat_save_path == "":
                    logger.warning("Cate path is empty, ignore")
                    continue

                if title_save_path == "":
                    logger.warning("File name is empty, ignore")
                    continue

                # logger.debug(f"title_save_path=>{title_save_path}")
                md_file_full_path = md_save_full_path + title_save_path
                p = os.path.dirname(md_file_full_path)
                f = os.path.basename(md_file_full_path)
                # logger.debug(f"p=>{p}")
                # logger.debug(f"f=>{f}")
                fileutils.save_data_to_txt(p, f, post.description)

                files_count = files_count + 1

        # dir_cats = list(set(dir_cats))
        # print(json.dumps(dir_cats,ensure_ascii=False))
        logger.info(f"all posts converts finished.handed {files_count} file (s)")

    def _parse_cat_arr(self, path):
        cats: list[CategoryInfo] = []

        # 对每一个文件进行操作
        prefix = "terwer.github.io/docs/"
        find_index = path.find(prefix)

        # 去掉前缀
        cate_path = ""
        if path.find(prefix) != -1:
            cate_path = path[find_index + len(prefix) : len(path)]
        ori_cates = cate_path.split(os.sep)

        for ori_cate in ori_cates:
            cate_name = strutils.remove_title_number(ori_cate)
            # 去掉尖括号
            cate_name = re.sub(r"[《》]", "", cate_name).strip()
            cate_name = cate_name.replace("_posts", "")
            if cate_name != "":
                cate = CategoryInfo()
                cate.description = cate_name
                # 会卡死，后面单独处理
                # cate.category_name = strutils.slug(cate_name)
                cats.append(cate)
        return cats

    def _make_vuepress2_formatter(self, post: Post):
        """
        生成vuepress2支持的formatter
        :param post:
        :return:
        """
        v2f = Vuepress2FrontFormatter()
        v2f.title = post.title
        # v2f.short_title = post.title
        v2f.description = post.short_desc
        v2f.date = post.date_created
        v2f.category = [c.description for c in post.categories]
        str_tags = []
        for t in post.mt_keywords:
            str_tags.append(str(t))
        v2f.tag = str_tags

        if "timeline" in v2f.category:
            v2f.timeline = True
            v2f.article = True
        return v2f.to_md()

    def _make_vuepress2_dir_category(self, cate_save_path, cate_name):
        cate_readme_full_path = os.path.join(
            self.VUEPRESS2_DOCS_PATH, cate_save_path, "README.md"
        )
        # print(cate_readme_full_path)
        md_formatter = {"article": False, "timeline": False}
        title_text = f"# {cate_name}"
        md_text = yaml.dump(
            md_formatter, allow_unicode=True, Dumper=MyDumper, indent=2, sort_keys=False
        )
        result = ["---\n", md_text, "---\n", title_text]
        md_content = "".join(result)
        p = os.path.dirname(cate_readme_full_path)
        f = os.path.basename(cate_readme_full_path)
        # 不存在才写
        if not os.path.exists(cate_readme_full_path):
            logger.info(
                f"Creating dir category README.md in {cate_save_path}=>{cate_name} ..."
            )
            fileutils.save_data_to_txt(p, f, md_content)
