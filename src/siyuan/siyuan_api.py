# Copyright (c) 2022 Landray Authors. All Rights Reserved.
# @author terwer on 2023/7/13
# ========================================================
import json

import requests
from loguru import logger


def get_doc_content(id):
    data = _siyuanRequest("/api/export/exportMdContent", {"id": id})
    return data["content"]


def _siyuanRequest(url, data):
    siyuanConfig = {
        "apiUrl": "http://127.0.0.1:6806",
    }
    reqUrl = f"{siyuanConfig['apiUrl']}{url}"
    headers = {
        "Cookie": "_ga=GA1.1.1895521166.1687438205; siyuan=MTY4OTIyMDYxMHxEdi1CQkFFQ180SUFBUkFCRUFBQV81Yl9nZ0FCQm5OMGNtbHVad3dHQUFSa1lYUmhCbk4wY21sdVp3eDZBSGg3SWxkdmNtdHpjR0ZqWlhNaU9uc2lMMVZ6WlhKekwzUmxjbmRsY2k5RWIyTjFiV1Z1ZEhNdmJYbGtiMk56TDFOcFdYVmhibGR2Y210emNHRmpaUzl3ZFdKc2FXTWlPbnNpUVdOalpYTnpRWFYwYUVOdlpHVWlPaUl4TURVd016WWlMQ0pEWVhCMFkyaGhJam9pYldWMmQzQXhjaUo5ZlgwPXyWi5GF_y6v6hjZH8rnGnJ2LG-sSuDkOnSJKj9RH5i0Sg==; _ga_L7WEXVQCR9=GS1.1.1689220611.80.1.1689221271.0.0.0"
    }
    logger.info(f"body => {data}")
    response = requests.post(reqUrl, json=data, headers=headers)
    resJson = response.json()

    if resJson["code"] == -1:
        raise Exception(resJson["msg"])
    return resJson["data"] if resJson["code"] == 0 else None
