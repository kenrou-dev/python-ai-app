from .gemini import generate


def generate_titles(api_key: str, content: str, count: int, style: str, model: str) -> str:
    prompt = f"""以下のコンテンツに合うタイトル・見出しを{count}案考えてください。

## コンテンツ（記事の内容・テーマ・概要）
{content}

## スタイル
{style}

## 出力形式
- 番号付きリストで{count}案出力
- 各案に一言コメント（なぜこのタイトルが良いか）を添える
- 日本語で出力

タイトル案:"""

    return generate(api_key, prompt, model)


STYLES = [
    "クリックされやすい・興味を引く",
    "SEO重視・検索されやすい",
    "シンプル・わかりやすい",
    "疑問形・問いかけ型",
    "数字を使ったリスト型（例: 5つの方法）",
]
