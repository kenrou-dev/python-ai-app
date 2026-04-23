# CLAUDE.md

このファイルは、リポジトリ内のコードを扱う際に Claude Code (claude.ai/code) へ提供するガイダンスです。

## コマンド

```bash
# アプリを起動する
streamlit run app.py

# 依存パッケージをインストールする
pip install -r requirements.txt
```

テストやリントのスクリプトは設定されていません。

## 環境設定

`.env` ファイルを作成して以下を記述してください：

```
GOOGLE_API_KEY=your_api_key_here
```

- `.env` は `.gitignore` で除外されているため、**絶対に git にコミットしないでください**。
- APIキーはサイドバーから実行時に直接入力することもできます。`.env` とサイドバーの両方に設定されている場合、サイドバー入力が優先されます。
- `check_api_key()` は空文字列だけでなく、`"your_api_key_here"` という文字列もキーが未設定とみなして警告を出します。

## アーキテクチャ

### 全体構成

`app.py` が唯一のUIエントリーポイントです。Streamlit のレイアウト（サイドバー・タブ・カラム）をすべて担い、AI生成処理は `tools/` フォルダに委譲しています。サイドバーで設定した `api_key` と `model` は全5タブで共有されます。

### tools/ フォルダ

ライティング機能ごとに1ファイルずつ配置されています：

| ファイル | エクスポート関数 | 定数 |
|---|---|---|
| `gemini.py` | `generate(api_key, prompt, model)` | — |
| `blog.py` | `write_blog(...)` | `TONES`, `LENGTH_MAP` |
| `email_reply.py` | `write_email_reply(...)` | `TONES` |
| `summarize.py` | `summarize_text(...)` | `STYLES` |
| `rewrite.py` | `rewrite_text(...)` | `STYLES` |
| `titles.py` | `generate_titles(...)` | `STYLES` |

### tools/gemini.py の注意点

- 全ツールファイルの共通 Gemini API ラッパーです。
- モジュールレベルに `_model` というグローバル変数がありますが、Streamlit はボタン操作のたびにスクリプトを先頭から再実行するため、実質的に毎回モデルが再生成されます。
- `api_key` と `model_name` は呼び出しのたびにUIから渡されます。サーバー側に認証情報は保持しません。

### 各タブの共通パターン

5タブはすべて同じ構造で実装されています：

```
入力ウィジェット（text_input / text_area / selectbox）
  ↓
ボタン（st.button）
  ↓
check_api_key() → 入力値バリデーション
  ↓
st.spinner でローディング表示しながら tools/ の関数を呼び出す
  ↓
結果を st.markdown / st.text_area で表示 + ダウンロードボタン
```

### 新しいツールを追加する場合

1. `tools/new_tool.py` に `generate_*` 関数とオプション定数（`TONES` / `STYLES` など）を実装する。
2. `app.py` の `st.tabs()` にタブ名を追加し、上記パターンに沿ってUIを実装する。

## 対応 Gemini モデル

以下の4種類からサイドバーで選択できます：

- `gemini-2.5-flash`（デフォルト）
- `gemini-2.0-flash`
- `gemini-1.5-flash`
- `gemini-1.5-pro`
