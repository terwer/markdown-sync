# Copyright (c) 2022 Landray Authors. All Rights Reserved.
# @author terwer on 2023/7/13
# ========================================================
import unittest

from loguru import logger

from src.siyuan import siyuan_api


class MyTestCase(unittest.TestCase):
    def test_summarize(self):
        id = '20230220193510-i9c10up'
        md = siyuan_api.get_doc_content(id)

        # 调用 AI 的 API
        result = ""
        logger.info(f"result => {result}")
