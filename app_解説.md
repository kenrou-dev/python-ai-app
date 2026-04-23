# app.py を読み解く — AIライティングツールの設計図

## はじめに：このファイルの役割

`app.py` はアプリの「顔」にあたるファイルです。ユーザーが見る画面（UI）の構築と、各AIツールへの橋渡しをすべてここで担っています。

---

## 1. 冒頭のインポート（1〜11行目）

```python
import os
import streamlit as st
from dotenv import load_dotenv

from tools.blog import write_blog, TONES as BLOG_TONES, LENGTH_MAP
from tools.email_reply import write_email_reply, TONES as EMAIL_TONES
...

load_dotenv()
```

まず必要な道具を「輸入」しています。

- **`streamlit`** — 画面を作るライブラリ。`st.button()` や `st.text_area()` と書くだけでボタンや入力欄が生まれます
- **`dotenv`** — `.env` ファイルを読み込むツール。`load_dotenv()` を呼ぶことで、`.env` に書いた `GOOGLE_API_KEY` が環境変数として使えるようになります
- **`tools.blog` など** — 実際にAI生成を行う処理は `tools/` フォルダの各ファイルに分離してあり、ここではその「関数」と「選択肢リスト」だけを借りてきています

---

## 2. ページ全体の設定（15〜19行目）

```python
st.set_page_config(
    page_title="AI ライティングツール",
    page_icon="✍️",
    layout="wide",
)
```

ブラウザのタブに表示されるタイトル・アイコンと、画面を横幅いっぱいに使う設定を一括で指定しています。アプリの起動直後、一番最初に実行される設定です。

---

## 3. サイドバー（22〜37行目）

```python
with st.sidebar:
    api_key = st.text_input("Gemini API キー", value=os.getenv("GOOGLE_API_KEY", ""), type="password")
    model = st.selectbox("使用モデル", MODELS)
```

`with st.sidebar:` のブロックに書いた内容は、画面左端のサイドバーに表示されます。ここで設定した `api_key` と `model` の2つの変数が、この後の全タブで共通して使われます。

`os.getenv("GOOGLE_API_KEY", "")` は「`.env` にキーが書いてあればそれを使い、なければ空欄にする」という意味です。

---

## 4. APIキーチェック関数（40〜44行目）

```python
def check_api_key() -> bool:
    if not api_key or api_key == "your_api_key_here":
        st.warning("サイドバーで Gemini API キーを入力してください。")
        return False
    return True
```

「ボタンを押したときにAPIキーが未入力だったら警告を出して止める」ための小さな関数です。全5つのタブで同じチェックが必要なので、共通関数として切り出すことで重複を避けています。

---

## 5. タブ構成（50〜52行目）

```python
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📝 ブログ記事", "📧 メール返信", "📄 文章要約", "🔄 リライト", "💡 タイトル生成"]
)
```

5つのタブを一行で作っています。以降は `with tab1:` のように書くだけで、そのブロックの内容が対応するタブに表示されます。

---

## 6. 各タブの共通パターン

5つのタブはすべて同じ構造で書かれています。

```
① 入力欄を並べる（st.text_input, st.text_area, st.selectbox など）
         ↓
② ボタンを置く（st.button）
         ↓
③ ボタンが押されたら：
   - APIキーチェック
   - 入力値チェック
   - AI生成を実行（with st.spinner でローディング表示）
         ↓
④ 結果を表示 ＋ ダウンロードボタン
```

例としてブログ記事タブを見てみましょう（57〜79行目）。

```python
with tab1:
    col1, col2 = st.columns([2, 1])   # 横2列に分割（左が2:右が1の比率）
    with col1:
        topic = st.text_input("記事のテーマ")
    with col2:
        tone = st.selectbox("文体・トーン", BLOG_TONES)

    if st.button("記事を生成"):
        if not check_api_key(): pass
        elif not topic.strip(): st.error("テーマを入力してください。")
        else:
            with st.spinner("生成中..."):
                result = write_blog(api_key, topic, tone, ...)  # tools/blog.py に投げる
            st.markdown(result)
            st.download_button("📥 ダウンロード", result, ...)
```

`st.columns([2, 1])` は入力欄を2列に並べるレイアウト指定です。`[2, 1]` は「左の列を右の2倍の幅にする」という比率です。

---

## 7. Streamlit の動作のしくみ

Streamlit の最大の特徴は、**ボタンを押すたびにファイルの先頭から末尾まで全部再実行される**という点です。

```
ユーザーがボタンを押す
    ↓
app.py を最初から最後まで全部実行
    ↓
その結果を画面に描画し直す
```

だからこそ `if st.button("..."):` というシンプルな `if` 文だけで「ボタンを押したときの処理」が書けます。従来のWeb開発のような複雑なイベント処理が不要なのが、Streamlitの強みです。

---

## まとめ

| 部分 | 役割 |
|---|---|
| インポート + `load_dotenv()` | 必要な道具を揃える |
| `st.set_page_config()` | ページ全体の見た目設定 |
| `with st.sidebar:` | 全タブ共通の設定UI |
| `check_api_key()` | バリデーションの共通化 |
| `st.tabs()` | 5機能をタブで切り替え |
| 各タブ内の `if st.button():` | 入力→生成→表示の一連の流れ |

`app.py` はUIの「組み立て図」に徹しており、AIへの実際の命令文（プロンプト）は `tools/` 以下の各ファイルに分離されています。この分離のおかげで、新しいツールを追加したいときは `tools/` に新ファイルを作ってタブを一つ増やすだけで済む構造になっています。
