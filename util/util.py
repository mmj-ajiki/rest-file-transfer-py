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
#  物件名称、種別、価格、住所、画像、PDF、位置から構成されるJSONデータのリスト
#  [{
#    'Name': <物件名>,
#    'Type': <物件タイプ>, 
#    'Price': <物件価格>, 
#    'Address': <物件の住所>,
#    'photo': <物件写真のBase64文字列: data:image/jpeg;base64,/9j/...>,
#    'pdf': <物件PDFファイルのBase64文字列: data:application/pdf;base64,...>,
#    'x': <物件のX座業>, 
#    'y': <物件のY座業>
#   }, ...],
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
                property['photo'] = jsonLoad['photo']
                property['pdf'] = jsonLoad['pdf']
                property['x'] = jsonLoad['x']
                property['y'] = jsonLoad['y']
                records.append(property)
        except Exception as e:
            print("[FILE]", file)
            print(e)
            continue

    return records
#
# HISTORY
# [2] 2025-03-03 - Added photo, pdf, x and y
# [1] 2025-02-20 - Initial version
#

#
# [FUNCTION] printJson()
#
# [DESCRIPTION]
#  JSONデータをコンソールに表示するデバッグ向け関数。Base64文字の先頭部分だけ表示する。
#
# [INPUTS]
#  jsonData - 表示するJSONデータ
#
# [OUTPUTS] なし
#
# [NOTES]
#  JSONデータは複製し、データ内にキーphotoおよびpdfが存在すれば、50文字までで切り取る。
#
def printJson(jsonData):

    # 複製を作成
    copiedJson = jsonData.copy() 

    if 'photo' in copiedJson.keys(): # photoキーが存在するか確認
        copiedJson['photo'] = copiedJson['photo'][0:50]

    if 'pdf' in copiedJson.keys(): # pdfキーが存在するか確認
        copiedJson['pdf'] = copiedJson['pdf'][0:50]
    
    print("[JSON]", copiedJson)

# HISTORY
# [1] 2025-03-03 - Initial version
#

#
# [FUNCTION] printListList()
#
# [DESCRIPTION]
#  JSONデータのリストをコンソールに表示するデバッグ向け関数。Base64文字の先頭部分だけ表示する。
#
# [INPUTS]
#  list - 表示するJSONデータのリスト
#
# [OUTPUTS] なし
#
# [NOTES]
#
def printList(list):

    for element in list:
        printJson(element)

# HISTORY
# [1] 2025-03-03 - Initial version
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
#    "photo": <物件写真のBase64文字列: data:image/jpeg;base64,/9j/...>,
#    "pdf": <物件PDFファイルのBase64文字列: data:application/pdf;base64,...>
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
#    "photo": <物件写真のBase64文字列: data:image/jpeg;base64,/9j/...>,
#    "pdf": <物件PDFファイルのBase64文字列: data:application/pdf;base64,...>,
#    "x": <X座標>,
#    "y": <Y座標>,
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