# Copyright (c) 2022 Terwer Authors. All Rights Reserved.
# @author terwer on 2023/4/12
# ========================================================
from loguru import logger

from src.converter.base_converter import BaseConverter


class siyuanToVuepress(BaseConverter):
    def __init__(self):
        pass

    def convert(self):
        logger.info("Convert is starting...")
