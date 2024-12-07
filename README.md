# WebSeekly


## 概要

WebSeekly は、特定のトピックに関連する情報を効率的に探索し、整理するためのツールです。  
インターネット上の膨大な情報の中から、指定されたトピックに基づいて関連するデータを検索し、必要な情報だけをリスト形式で取得できます。

例えば、「無料イベント」や「最新の技術トレンド」を探す場合、以下のような流れで情報を取得します：
1. **検索リクエストの送信**  
   ユーザーが「無料イベント」と検索します。
   
2. **関連データの探索**  
   WebSeekly はインターネット上の関連ページを検索し、リンクを収集します。

3. **情報の抽出と整理**  
   収集したページから、特定の条件（例えば「無料イベント」）に合致する情報だけを解析し、抽出します。

4. **結果の提示**  
   必要な情報をシンプルなリスト形式で提供します：


- 〇〇駅前 無料の夕涼みコンサート 19:00～ （from 公式サイトA） 
- 〇〇.com 無料ウェビナー 15:00～ （from 公式サイトB）


## 主な特徴
- トピックに基づいたキーワード生成
- Google Custom Search API を活用したリンク収集
- クローリングとスクレイピングによるイベント情報の抽出
- 情報の自動検証と保存機能
- 利用規約遵守と法的リスクの軽減

---

## ディレクトリ構造

```python
webseekly/
├── pyproject.toml              # プロジェクト設定
├── README.md                   # 本ファイル
├── requirements.txt            # 依存パッケージリスト
├── src/                        # ソースコード
│   ├── app.py                  # エントリーポイント
│   └── webseekly/              # メインモジュール
│       ├── core/               # コアモジュール
│       │   ├── factory.py
│       │   ├── node.py
│       ├── nodes/              # 各種ノード
│       │   ├── crawl_node.py
│       │   ├── keyword_node.py
│       │   ├── save_node.py
│       │   ├── scrape_node.py
│       │   ├── search_node.py
│       │   └── verification_node.py
│       └── workflow.py         # ワークフローの定義
├── test/                       # テストコード
│   ├── test_crawl_node.py
│   ├── test_keyword_node.py
│   ├── test_save_node.py
│   ├── test_scrape_node.py
│   ├── test_search_node.py
│   └── test_verification_node.py
└── uv.lock                     # Python仮想環境用のロックファイル
```


## セットアップ

## 必要要件
- Python 3.10以上
- Google Custom Search API のキー（設定方法は後述）

## インストール手順

1. リポジトリをクローンします。
```python
   $ git clone https://github.com/username/webseekly.git
   $ cd webseekly
```
2. 仮想環境を作成してアクティベートします。
```python
   $ python -m venv venv
   $ source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
```
3. 必要な依存パッケージをインストールします。
```python
   $ pip install -r requirements.txt
```
4. `.env` ファイルを作成し、APIキーなどの環境変数を設定します。
```python
   GOOGLE_CUSTOM_SEARCH_API_KEY=your_api_key_here
   GOOGLE_CUSTOM_SEARCH_ENGINE_ID=your_search_engine_id_here
```
5. アプリケーションを起動します。
```python
   $ python src/app.py
```
---

## 使用方法

1. トピック（例: "無料イベント", "オンライン"）を入力します。
2. WebSeekly が以下のプロセスを自動で実行します：
   - キーワード生成
   - リンク検索と収集
   - 必要な情報のスクレイピングと検証
3. 必要なイベント情報をリスト形式で取得できます。

---

## テスト

テストスイートを実行して、各ノードが正しく動作することを確認できます。
```python
$ pytest test/
```
---

# APIキーの取得と設定

## Google Custom Search API の設定

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス。
2. プロジェクトを作成し、Custom Search JSON API を有効化します。
3. APIキーを取得し、`.env` に設定します。

---

# ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。

MIT License
Copyright (c) 2024 Your Name

---

# 注意点
- APIキー はプロジェクトに必須です。`.env` ファイルに設定してください。
- 利用規約やrobots.txt を遵守し、不正なスクレイピングを避けるよう設計されています。