# Copyright (c) 2022 Landray Authors. All Rights Reserved.
# @author terwer on 2023/7/13
# ========================================================

import requests


def get_doc_content(id):
    data = _siyuanRequest("/api/export/exportMdContent", {"id": id})
    return data["content"]


def ai_get_desc():
    # 构建请求数据
    request_data = {"ids": ["20220905122249-9atjoje"], "action": "提取摘要"}
    # 调用封装的函数进行请求
    response_data = _siyuanRequest("/api/ai/chatGPTWithAction", request_data)
    print(response_data)


#################################
# private function
#################################
def _siyuanRequest(url, data, method="POST"):
    siyuanConfig = {
        "apiUrl": "http://127.0.0.1:6806",
    }
    reqUrl = f"{siyuanConfig['apiUrl']}{url}"
    with open("data/cookie.txt", "r") as file:
        cookie = file.read().strip()
    headers = {"Cookie": cookie}
    if method == "GET":
        response = requests.get(reqUrl, headers=headers)
    else:
        response = requests.post(reqUrl, json=data, headers=headers)
    resJson = response.json()

    if resJson["code"] == -1:
        raise Exception(resJson["msg"])
    return resJson["data"] if resJson["code"] == 0 else None
