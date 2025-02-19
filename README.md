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
| records | 物件名称、種別、価格、住所から構成されるJSONデータのリスト |
| message | メッセージテキスト |

レスポンス例:

```bash
{
  "keys": ["Name", "Type", "Price", "Address"],
  "records": [
    {'Name':'ABCアパート', 'Type':'アパート', 'Price':123456, 'Address': '東京都港区六本木9-8-1'}, 
    ...
  ],
  "message": None
}
```

#### /upload/binary (POSTメソッド)

eYACHO/GEMBA Noteアプリから送信されてきた画像とPDFをファイルに保存する。

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

- 「[eYACHO/GEMBA Noteでアプリケーションを作る～ 実践的なアプリ開発 ～](https://product.metamoji.com/manual/gemba_apps/gemba_dev_advanced/jp/)」のバックアップファイルをダウンロードして、eYACHO/GEMBA Note製品に復元する。
  - 開発オプションが必要
  - こちらからダウンロードする → [PracticalAppDev__<バージョン>__backup.gncproj](https://product.metamoji.com/manual/gemba_apps/gemba_dev_advanced/jp/contents/backup/PracticalAppDev__0.2.0__backup.gncproj)
- サーバーが起動していることを確認する。
  - Windowsアプリからローカルサーバーにアクセスする場合は、管理者モードで利用対象アプリのループバックを有効にする → [Windowsで開発する際の注意点](./NoticesForWindows.md)

#### eYACHO/GEMBA Noteから送信テスト

開発パッケージフォルダ以下にあるサブフォルダ **データ連携** にあるノート「**RESTサーバーへ送信**」を開く。

**JSONファイルをアップロードする**  

- 物件情報フォームに物件名称が設定されていることを確認する。
  - タイプ、価格、住所も適当に入力する。なくてもよい。
- ページ上の **アップロード** ボタンをクリックする。
  - 「アップロードが完了しました」とダイアログが現れると成功。
  - 物件名称が設定されていないと、「物件名称が設定されていません」と表示される。
  - ファイル保存が失敗すると「JSONファイルが保存されませんでした」と表示される。
- 環境変数LOCAL_FOLDERに設定してあるフォルダにJSONファイルが格納されていることを確認する。
  - ファイルをテキストエディタで開き、内容を確認する。

**画像・PDFファイルをアップロードする**  

- 物件名称、物件画像、PDFファイルが設定されていることを確認する。
- ページ上の **アップロード** ボタンをクリックする。
  - 「アップロードが完了しました」とダイアログが現れると成功。
  - 物件名称、物件画像、PDFファイルが設定されていないと、「...が設定されていません」と表示される。
  - ファイル保存が失敗すると「...ファイルが保存されませんでした」と表示される。
- 環境変数LOCAL_FOLDERに設定してあるフォルダに画像とPDFファイルが格納されていることを確認する。
  - ファイルをクリックして画像やPDFの内容が表示されるか確かめる。

#### eYACHO/GEMBA Noteで受信テスト

開発パッケージフォルダにあるサブフォルダ **データ連携** にあるノート「**RESTサーバーから取得**」を開く。

**保存されたJSONファイルの内容を取得する**  

- 環境変数LOCAL_FOLDERに設定してあるフォルダにJSONファイルが保存されていることを確認する。
- ページ上の **最新に更新** ボタンをクリックする。
  - 各JSONファイルのName、Type、Price、Addressの値が表形式として出力される。

#### 注意事項

サーバーのポート番号を変更した場合やリモートサーバーで運用可能にした時は、関連するボタンコマンドやアグリゲーション検索条件（RESTコネクタ）の **URL** を変更する。  

### 更新履歴

- 2025-02-20 初版
