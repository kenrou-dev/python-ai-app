from .gemini import generate

TONES = ["丁寧・フォーマル", "カジュアル・親しみやすい", "専門的・解説調", "熱量高め・エネルギッシュ"]

LENGTH_MAP = {
    "短め（〜500文字）": 500,
    "普通（〜1000文字）": 1000,
    "長め（〜2000文字）": 2000,
    "詳細（〜3000文字）": 3000,
}


def write_blog(api_key: str, topic: str, tone: str, length_label: str, keywords: str, model: str) -> str:
    target_len = LENGTH_MAP.get(length_label, 1000)
    keyword_line = f"- キーワード（自然に盛り込む）: {keywords}" if keywords.strip() else ""

    prompt = f"""あなたはプロのブログライターです。以下の条件でブログ記事を書いてください。

## 条件
- テーマ: {topic}
- 文体・トーン: {tone}
- 目標文字数: 約{target_len}文字
{keyword_line}

## 出力形式
- タイトルを1行目に書く（# タイトル）
- 導入→本文（見出し付き）→まとめ の構成
- Markdown形式で出力

それでは記事を書いてください。"""

    return generate(api_key, prompt, model)
