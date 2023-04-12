# Copyright (c) 2022 Terwer Authors. All Rights Reserved.
# @author terwer on 2023/4/12
# ========================================================
from src.converter.vuepress1_to_vuepress2 import vuepress1ToVuepress2

if __name__ == "__main__":
    """
    vuepress1 转换 vuepress2
    :return:
    """
    app = vuepress1ToVuepress2()
    app.convert()
