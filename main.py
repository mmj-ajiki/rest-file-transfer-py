#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
[FILE] main.py
[DESCRIPTION] eYACHO/GEMBA NoteとのREST API通信エンドポイントを定義する。

[HISTORY]
2026-01-07: Followed PEP 8
2025-03-03: Added photo, pdf, x and y support.
2025-02-20: Initial version.
"""

import sys
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import util.util as util

app = FastAPI()
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def is_reload_enabled():
    """
    実行コマンドに --reload が含まれるか（デバッグモードか）を判定する。

    Returns:
        bool: 含まれる場合は True。
    """
    return "--reload" in sys.argv


@app.get("/", response_class=HTMLResponse)
async def top_page(request: Request):
    """トップ画面（動作確認用）を表示する。"""
    return templates.TemplateResponse(
        "top.html", 
        {"request": request, "title": "GEMBA File Transfer REST Server"}
    )


@app.get("/get/json")
def get_json_file():
    """保存済みのJSONデータを取得して返す。"""
    results = {
        'keys': ['Name', 'Type', 'Price', 'Address', 'photo', 'pdf', 'x', 'y'],
        'records': util.get_json_data(),
        'message': None
    }

    if is_reload_enabled():
        util.print_list(results['records'])
       
    return results


@app.post("/upload/binary")
def upload_binary_file(json_data: dict):
    """画像およびPDFバイナリをBase64データからアップロード・保存する。"""
    results = {'message': "アップロードが完了しました"}

    # 必須キーの検証
    for key, label in [('name', "物件名称"), ('photo', "物件画像"), ('pdf', "PDF")]:
        if key not in json_data:
            results['message'] = f"{label}が設定されていません"
            return results
    
    # 画像とPDFの保存実行
    for b_type in ['photo', 'pdf']:
        file_path = util.store_binary_file(json_data, b_type)
        if file_path is None:
            results['message'] = f"{b_type}ファイルが保存できませんでした"
            return results
        
        if is_reload_enabled():
            print(f"[{b_type.upper()} SAVED]", file_path)
        
    return results


@app.post("/upload/json")
def upload_json_file(json_data: dict):
    """物件情報のJSONデータをファイルとして保存する。"""
    results = {'message': "アップロードが完了しました"}

    if is_reload_enabled():
        util.print_json(json_data)
        
    if 'Name' not in json_data:
        results['message'] = "物件名称が設定されていません"
        return results
       
    file_path = util.store_json_file(json_data)
    if file_path is None:
        results['message'] = "JSONファイルが保存できませんでした"
        return results

    if is_reload_enabled():
        print("[JSON SAVED]", file_path)
        
    return results