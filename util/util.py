#!/usr/bin/env python
# coding: utf-8
#
# [FILE] util.py
#
# [DESCRIPTION]
#  RESTメソッドで利用するユーティリティ関数を定義する。
#
import json
import base64, os, sys
from dotenv import load_dotenv

# .envファイルの内容を読み込見込む
load_dotenv()

# ローカルフォルダを取得する
localFolder = os.environ.get("LOCAL_FOLDER")
if localFolder == None:
    print("環境変数LOCAL_FOLDERが設定されていません")
    sys.exit()

#
# [FUNCTION] getJsonData()
#
# [DESCRIPTION]
#  環境変数LOCAL_FOLDERに格納された物件情報JSONファイルの内容を取得する
#
# [INPUTS] None
#
# [OUTPUTS] 
#  物件名称、種別、価格、住所から構成されるJSONデータのリスト
#  [{'Name':'ABCアパート', 'Type':'アパート', 'Price':123456, 'Address': '東京都港区六本木9-8-1'}, ...],
#
# [NOTES]
#  JSONファイルを検索するフォルダには物件情報JSONデータしかないと仮定する。
#  JSONデータにNameキーがあるかどうかまではチェックする。
#
def getJsonData():
    records = []

    # JSONファイルを収集する
    fileNames = os.listdir(localFolder)

    # 各ファイルを開く
    for file in fileNames:
        try:
            fileOpen = open(localFolder+"/"+file, 'r')
            jsonLoad = json.load(fileOpen)
            if 'Name' in jsonLoad.keys(): # Nameキーが存在するか確認
                property = {}
                property['Name'] = jsonLoad['Name']
                property['Type'] = jsonLoad['Type']
                property['Price'] = jsonLoad['Price']
                property['Address'] = jsonLoad['Address']
                records.append(property)
        except Exception as e:
            print("[FILE]", file)
            print(e)
            continue

    return records
#
# HISTORY
# [1] 2025-02-20 - Initial version
#

#
# [FUNCTION] storeBinaryFile()
#
# [DESCRIPTION]
#  Base64文字列からバイナリファイルを保存する。
#
# [INPUTS]
#  jsonData - 次の構造をもつJSONデータ
#  {
#    "_userName": <ユーザー名>,
#    "_noteTitle": <ノートの見出し>,
#    "_noteLink": <ノートのURL>,
#    "_pageLink": <ページのURL>,
#    "_driveId": <ドライブID>,
#    "_documentId": <ドキュメントID>,
#    "_objectType": <オブジェクト種別>,
#    "_objectId": <オブジェクトID>,
#    "_pageId": <ページID>,
#    "_x": <X座標>,
#    "_y": <Y座標>,
#    "_width": <横幅>,
#    "_height": <高さ>,
#    "name": <物件名>,
#    "photo": <物件写真のBase64文字列: data:image/jpeg;base64,/9j/4AAQSkZJR...>,
#    "pdf": <物件PDFファイルのBase64文字列: data:application/pdf;base64,JVBERi0xLjQNCiXi4...>
#  }
#  bType - 'photo' あるいは 'pdf', jsonDataからBase64文字列を取得するため用いる
#
# [OUTPUTS] 
#  成功 - ファイル名を返却
#  失敗 - None
#
# [NOTES]
#  jsonDataにname, photo, pdfなどのキーが存在することを前提とする。
#
def storeBinaryFile(jsonData, bType):
    # 保存する内容を取得
    binString = jsonData[bType].split(',')
    binContent = base64.b64decode(binString[1])

    # ファイル拡張子を取得
    binString = binString[0].split('/')
    ext = binString[1].split(';')

    # 保存するファイル名を準備する
    # ファイル名は物件名から生成する
    binFile = localFolder + "/" + jsonData['name'] + "." + ext[0]

    # ファイルを保存
    try:
        with open(binFile, 'wb') as file:
            file.write(binContent)
    except Exception as e:
        print(e)
        binFile = None
    
    return binFile
#
# HISTORY
# [1] 2025-02-20 - Initial version
#

#
# [FUNCTION] storeJsonFile()
#
# [DESCRIPTION]
#  JSONデータをファイルに保存する。
#
# [INPUTS]
#  jsonData - 次の構造をもつJSONデータ
#  {
#    "_userName": <ユーザー名>,
#    "_noteTitle": <ノートの見出し>,
#    "_noteLink": <ノートのURL>,
#    "_pageLink": <ページのURL>,
#    "_driveId": <ドライブID>,
#    "_documentId": <ドキュメントID>,
#    "_objectType": <オブジェクト種別>,
#    "_objectId": <オブジェクトID>,
#    "_pageId": <ページID>,
#    "_x": <X座標>,
#    "_y": <Y座標>,
#    "_width": <横幅>,
#    "_height": <高さ>,
#    "Name": <物件名>,
#    "Type": <物件タイプ>,
#    "Price": <物件価格>,
#    "Address": <物件の住所>
#  }
#
# [OUTPUTS] 
#  成功 - ファイル名を返却
#  失敗 - None
#
# [NOTES]
#  jsonDataにNameなどのキーが存在することを前提とする。
#
def storeJsonFile(jsonData):

    # 保存するファイル名を準備する
    # ファイル名は物件名から生成する
    jsonFile = localFolder + "/" + jsonData['Name'] + ".json"
   
    # JSONファイルを保存
    try:
        with open(jsonFile, 'w', encoding='utf-8') as file:
            json.dump(jsonData, file, indent=4)
    except Exception as e:
        print(e)
        jsonFile = None
    
    return jsonFile
#
# HISTORY
# [1] 2025-02-20 - Initial version
#