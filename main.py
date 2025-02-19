#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# [FILE] main.py
#
# [DESCRIPTION]
#  eYACHO/GEMBA Noteからファイルをアップロード、そのファイルからeYACHO/GEMBA Noteへデータを取り込むRESTメソッドを定義する。
# 
# [NOTES]
#
import sys
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from util.util import getJsonData, storeBinaryFile, storeJsonFile

app = FastAPI()
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

#
# [FUNCTION] is_reload_enabled()
#
# [DESCRIPTION]
#  実行するコマンドに--reloadが含まれるか判定する。
#
# [INPUTS] None
#
# [OUTPUTS]
#  True: 含まれる False: 含まれない
#
# [NOTES]
#  Trueの場合はデバッグ実行とみなし、JSONデータをコンソール上に表示するために用いる。
#
def is_reload_enabled():
    return "--reload" in sys.argv
#
# HISTORY
# [1] 2025-02-20 - Initial version
#

#
# GET Method
# End Point: /
#
# [DESCRIPTION]
#  動作確認用のトップページを開く。
#
# [INPUTS]
#  request - リクエスト
# 
# [OUTPUTS]
# 
# [NOTES]
#  Web画面上に単に、"GEMBA File Transfer REST Server"と表示するのみ。
#
@app.get("/", response_class=HTMLResponse)
async def topPage(request: Request):
    
    return templates.TemplateResponse("top.html", {"request": request, "title": "GEMBA File Transfer REST Server"})
#
# HISTORY
# [1] 2025-02-20 - Initial version
#

#
# GET Method
# End Point: /get/json
#
# [DESCRIPTION]
#  ローカルフォルダに保存されているJSONファイルの内容を取得する。
#
# [INPUTS] None
# 
# [OUTPUTS]
#  物件名称、種別、価格、住所から構成されるJSONデータ
#  {
#    "keys": ["Name", "Type", "Price", "Address"],
#    "records": [
#        {'Name':'ABCアパート', 'Type':'アパート', 'Price':123456, 'Address': '東京都港区六本木9-8-1'}, ...
#    ],
#    "message": None
#  }
# 
# [NOTES]
#  関数getJsonData()は、エンドポイント/upload/jsonで保存したJSONファイルの内容を読み込みJSONデータとする。
#
@app.get("/get/json")
def getJsonFile():
    results = {}
    results['keys'] = ['Name', 'Type', 'Price', 'Address']
    results['records'] = getJsonData()
    results['message'] = None

    if is_reload_enabled():
        print("[JSON]", results)
       
    return results
#
# HISTORY
# [1] 2025-02-20 - Initial version
#

#
# POST Method
# End Point: /upload/binary
#
# [DESCRIPTION]
#  eYACHO/GEMBA Noteから送信されてきた画像データとPDFデータをファイルに保存する。
#
# [INPUTS] 
#  request - bodyにクライアント（eYACHO/GEMBA Note）からの情報が格納されている
#    {..., 
#      "_noteLink": <ノートリンク>, 
#      "_pageId": <ページID>, 
#      ...,
#      "name": "メタモジマンション",
#      "photo": "data:image/jpeg;base64,/9j/4AAQSkZJR...", 
#      "pdf": "data:application/pdf;base64,JVBERi0xLjQNCiXi4..."
#      ...}
# 
# [OUTPUTS]
#  次のJSONを返す
#    {'message': <メッセージ>}
# 
# [NOTES]
#  タグスキーマpropertyPhotoの以下のタグプロパティが設定されていることを前提とする
#    name: 物件名称
#    photo: 物件画像
#    pdf: PDFファイル
#
@app.post("/upload/binary")
def uploadBinaryFile(jsonData: dict):
    results = {}
    results['message'] = "アップロードが完了しました"

    if ('name' in jsonData) == False:
        results['message'] = "物件名称が設定されていません"
        return results
    
    if ('photo' in jsonData) == False:
        results['message'] = "物件画像が設定されていません"
        return results

    if ('pdf' in jsonData) == False:
        results['message'] = "PDFが設定されていません"
        return results
    
    fileName = storeBinaryFile(jsonData, 'photo')
    if fileName == None:
        results['message'] = "画像ファイルが保存できませんでした"
        return results

    if is_reload_enabled():
        print("[IMG SAVED]", fileName)

    fileName = storeBinaryFile(jsonData, 'pdf')
    if fileName == None:
        results['message'] = "PDFファイルが保存できませんでした"
        return results

    if is_reload_enabled():
        print("[PDF SAVED]", fileName)
        
    return results
#
# HISTORY
# [1] 2025-02-20 - Initial version
#

#
# POST Method
# End Point: /upload/json
#
# [DESCRIPTION]
#  eYACHO/GEMBA Noteから送信されてきた物件情報をJSONファイルに保存する。
#
# [INPUTS] 
#  request - bodyにクライアント（eYACHO/GEMBA Note）からの画像情報が格納されている
#    {..., 
#      "_noteLink": <ノートリンク>, 
#      "_pageId": <ページID>, 
#      ...,
#      "Name": "メタモジマンション",
#      "Type": "アパート", 
#      "Price": 78600000,
#      "Address": "東京都港区六本木...", 
#      ...}
# 
# [OUTPUTS]
#  次のJSONを返す
#    {'message': <メッセージ>}
# 
# [NOTES]
#  タグスキーマPropertyの以下のタグプロパティの値を含んだすべてのキーを保存する
#    Name - 物件の名称
#    Type - 物件の種別
#    Price - 物件の価格
#    Address - 物件の住所
#
@app.post("/upload/json")
def uploadJsonFile(jsonData: dict):
    results = {}
    results['message'] = "アップロードが完了しました"

    if is_reload_enabled():
        print("[JSON]", jsonData)
        
    if ('Name' in jsonData) == False:
        results['message'] = "物件名称が設定されていません"
        return results
       
    fileName = storeJsonFile(jsonData)
    if fileName == None:
        results['message'] = "JSONファイルが保存できませんでした"
        return results

    if is_reload_enabled():
        print("[JSON SAVED]", fileName)
        
    return results
#
# HISTORY
# [1] 2025-02-20 - Initial version
#
