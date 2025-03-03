# rest-file-transfer-py

## ファイル転送RESTサーバー

このRESTサーバーは、株式会社MetaMoJi（[https://metamoji.com/](https://metamoji.com/)）の [eYACHO](https://product.metamoji.com/gemba/eyacho/) あるいは [GEMBA Note](https://product.metamoji.com/gemba/gembanote/)から送信されてきたJSONデータ、画像データ、PDFデータをファイルとして保存するAPIを提供する。また保存したJSONデータの内容を再びeYACHO/GEMBA Noteから取得する。

### Pythonをインストールする

[https://www.python.org/downloads/](https://www.python.org/downloads/)からPythonをインストールする。

**動作確認：** Python 3.12.xと3.13.xで動作を確認。

### 必要なパッケージのインストール

コマンドプロンプト上で、次のコマンドを実行し、必要なPythonのパッケージをインストールする。

```bash
pip install -r requirements.txt
```

### 環境変数を設定する

本アプリを起動するには環境変数の設定が必要である。以下の環境変数が.envファイルに定義されている。

|  変数名  |  説明  |
| ---- | ---- |
|  LOCAL_FOLDER  | アップロードしたファイルを保存するローカルフォルダの名前 |

### サーバーを起動する

コマンドプロンプトから次のコマンドを実行し、サーバーを起動する。

開発・デバッグ環境：

ソースコード編集内容が自動的に反映される。また、処理途中のログをコンソールに出力する。

```bash
uvicorn main:app --reload
```

本番環境：

```bash
uvicorn main:app
```

コマンドの説明:

| コマンドの要素 |  説明  |
| ---- | ---- |
|  uvicorn  | FastAPIベースの非同期Python Webアプリケーションを実行する |
|  main:app  | Pythonファイルmain.pyの中で、FastAPIが生成する変数がapp |
|  --reload  | 実行中にソースコードが変更されたとき、サーバーが自動的にリロードされる |

デフォルトのポート番号は**8000**。  
ポート番号を指定するときは --port [ポート番号] を後ろに付与する。

### サーバーへのアクセスを確認する

確認のため、Webブラウザを開き、次のURLへアクセスする（ポート番号が8000の場合）。

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

メッセージを表示するだけのトップページが現れる。

### REST APIs

#### /get/json (GETメソッド)

環境変数LOCAL_FOLDERに保存された物件情報JSONデータを読み込み、その内容をeYACHO/GEMBA Noteが受けることができるJSON形式にする。

リクエストの仕様：

|  メソッド |  リクエスト |
| ---- | ---- |
|  GET | なし |

レスポンスの仕様:

|  キー  | 説明  |
| ---- | ---- |
| keys | recordsキーの値に含まれるキー一覧 |
| records | 物件名称、種別、価格、住所、画像、PDF、位置から構成されるJSONデータのリスト |
| message | メッセージテキスト |

レスポンス例:

```bash
{
  "keys": ["Name", "Type", "Price", "Address", "photo", "pdf", "x", "y"],
  "records": [
    {
      'Name':'ABCアパート', 
      'Type':'アパート', 
      'Price':123456, 
      'Address': '東京都港区六本木9-8-1',
      'photo': 'data:image/jpeg;base64,/9j/...',
      'pdf': 'data:application/pdf;base64,...',
      'x': 35.738609, 
      'y': 139.828122
    }, 
    ...
  ],
  "message": None
}
```

#### /upload/binary (POSTメソッド)

eYACHO/GEMBA Noteアプリから送信されてきた画像とPDFをそれぞれファイルとして保存する。

リクエストボディ(JSON)の構造：

| キー | 説明 |
| ---- | ---- |
| name | 物件の名称 |
| photo | 物件画像のBase64文字列 |
| pdf | PDFのBase64文字列 |

全てのキーの値が設定されていないとファイルに保存されない。

レスポンスの仕様:

|  キー  | 説明  |
| ---- | ---- |
| message | 表示するメッセージ |

レスポンス例:

```bash
{
  'message': 'アップロードが完了しました'
}
```

#### /upload/json (POSTメソッド)

eYACHO/GEMBA Noteアプリから送信されてきた物件情報をJSONファイルとして保存する。

リクエストボディ(JSON)の構造：

| キー | 説明 |
| ---- | ---- |
| Name | 物件の名称 |
| Type | 物件の種別 |
| Price | 物件の価格 |
| Address | 物件の住所 |
| photo | 物件写真のBase64文字列 |
| pdf | 物件PDFファイルのBase64文字列 |
| x | 物件のX軸（緯度） |
| y | 物件のY軸（経度） |

上記のキーの他、eYACHO/GEMBA Noteが与えるシステムタグプロパティ（例えば、_userName）も含まれる。

Nameキーの値が設定されていないとファイルに保存されない。

レスポンスの仕様:

|  キー  | 説明  |
| ---- | ---- |
| message | 表示するメッセージ |

レスポンス例:

```bash
{
  'message': 'アップロードが完了しました'
}
```

### eYACHO/GEMBA Noteとのデータ連携テスト

- 「[eYACHO/GEMBA Noteでアプリケーションを作る～ 実践的なアプリ開発 ～](https://product.metamoji.com/manual/gemba_apps/gemba_dev_advanced/jp/)」（GEMBAアプリ開発実践本）のバックアップファイルをダウンロードして、eYACHO/GEMBA Note製品に復元する。
  - 開発オプションが必要
  - こちらからダウンロードする → [PracticalAppDev__<バージョン>__backup.gncproj](https://product.metamoji.com/manual/gemba_apps/gemba_dev_advanced/jp/contents/backup/PracticalAppDev__0.2.0__backup.gncproj)
- サーバーが起動していることを確認する。
  - Windowsアプリからローカルサーバーにアクセスする場合は、管理者モードで利用対象アプリのループバックを有効にする → [Windowsで開発する際の注意点](./NoticesForWindows.md)
- 上記「GEMBAアプリ開発実践本」の第6章の動作確認6-4に従い、REST連携動作を確認する。

### 更新履歴

- 2025-03-03 画像、PDF、位置をJSONに追加
- 2025-02-20 初版
