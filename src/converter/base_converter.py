# Copyright (c) 2022 Terwer Authors. All Rights Reserved.
# @author terwer on 2023/4/12
# ========================================================
import abc


class BaseConverter(metaclass=abc.ABCMeta):
    """
    通用转换器
    """

    @abc.abstractmethod
    def convert(self):
        """
        抽象的方法，需要转换器自己去实现
        """
        pass
