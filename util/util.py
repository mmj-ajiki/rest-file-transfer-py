#!/usr/bin/env python
# coding: utf-8
"""
[FILE] util.py
[DESCRIPTION] RESTメソッドで利用するユーティリティ関数を定義する。

[HISTORY]
2026-01-07: Followed PEP 8
2025-03-03: Added photo, pdf, x and y.
2025-02-20: Initial version.
"""

import json
import base64
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# .envファイルの内容を読み込む
load_dotenv()

# ローカルフォルダを取得
_folder_env = os.environ.get("LOCAL_FOLDER")
if _folder_env is None:
    print("環境変数LOCAL_FOLDERが設定されていません")
    sys.exit()

LOCAL_FOLDER = Path(_folder_env)


def get_json_data():
    """
    環境変数に指定されたフォルダから物件情報のJSONデータを一括取得する。

    Returns:
        list[dict]: 物件情報を含む辞書のリスト。
    """
    records = []
    if not LOCAL_FOLDER.exists():
        return records

    for file_path in LOCAL_FOLDER.glob("*.json"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Nameキーが存在するデータのみ抽出
            if 'Name' in data:
                # 必要なキーのみをフィルタリング
                record = {key: data.get(key) for key in [
                    'Name', 'Type', 'Price', 'Address', 'photo', 'pdf', 'x', 'y'
                ]}
                records.append(record)
        except (json.JSONDecodeError, IOError) as e:
            print(f"[FILE ERROR] {file_path.name}: {e}")
            continue

    return records


def print_json(json_data):
    """
    JSONデータをコンソールに表示する。Base64文字列は先頭のみ表示する。

    Args:
        json_data (dict): 表示対象のJSONデータ。
    """
    copied_json = json_data.copy()
    for key in ['photo', 'pdf']:
        if key in copied_json and isinstance(copied_json[key], str):
            copied_json[key] = copied_json[key][:50]
    
    print("[JSON]", copied_json)


def print_list(data_list):
    """
    JSONデータのリストを順にコンソールへ表示する。

    Args:
        data_list (list[dict]): 表示対象のリスト。
    """
    for element in data_list:
        print_json(element)


def store_binary_file(json_data, b_type):
    """
    Base64文字列からバイナリファイルをデコードして保存する。

    Args:
        json_data (dict): 'name' および b_type で指定されたキーを持つデータ。
        b_type (str): 'photo' または 'pdf'。

    Returns:
        str | None: 成功時は保存した絶対パス、失敗時は None。
    """
    try:
        # data:image/jpeg;base64,... の形式を分割
        header, encoded = json_data[b_type].split(',')
        bin_content = base64.b64decode(encoded)

        # 拡張子の抽出 (例: image/jpeg -> jpeg)
        ext = header.split('/')[1].split(';')[0]
        file_path = LOCAL_FOLDER / f"{json_data['name']}.{ext}"

        with open(file_path, 'wb') as f:
            f.write(bin_content)
        
        return str(file_path)
    except Exception as e:
        print(f"[BINARY SAVE ERROR] {e}")
        return None


def store_json_file(json_data):
    """
    JSONデータをファイルとして保存する。

    Args:
        json_data (dict): 保存対象のデータ。'Name'キーをファイル名に使用する。

    Returns:
        str | None: 成功時は保存した絶対パス、失敗時は None。
    """
    file_path = LOCAL_FOLDER / f"{json_data['Name']}.json"
   
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)
        return str(file_path)
    except Exception as e:
        print(f"[JSON SAVE ERROR] {e}")
        return None