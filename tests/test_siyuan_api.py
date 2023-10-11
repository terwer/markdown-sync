# Copyright (c) 2022 Landray Authors. All Rights Reserved.
# @author terwer on 2023/7/13
# ========================================================
import unittest

from loguru import logger

from src.siyuan import siyuan_api


class MyTestCase(unittest.TestCase):
    def test_get_doc_content(self):
        id = "20230220193510-i9c10up"
        md = siyuan_api.get_doc_content(id)
        logger.info(f"md => {md}")

    def test_ai_get_desc(self):
        siyuan_api.ai_get_desc()
