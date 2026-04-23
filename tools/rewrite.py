from .gemini import generate

STYLES = [
    "丁寧語・ビジネス文体に",
    "カジュアル・話し言葉に",
    "簡潔・短くシンプルに",
    "わかりやすく・専門用語なしに",
    "英語に翻訳",
    "日本語に翻訳",
    "ポジティブ・前向きな表現に",
    "SNS投稿向けに（短く・キャッチーに）",
]


def rewrite_text(api_key: str, text: str, style: str, instruction: str, model: str) -> str:
    extra = f"\n- 追加指示: {instruction}" if instruction.strip() else ""

    prompt = f"""以下の文章を指定されたスタイルに書き直してください。

## 元の文章
{text}

## 変換スタイル
{style}{extra}

## 注意
- 意味・内容は変えない
- 自然な表現にする
- 変換後の文章のみ出力する（説明不要）

書き直した文章:"""

    return generate(api_key, prompt, model)
