from .gemini import generate

STYLES = ["箇条書き（要点3〜5点）", "1段落にまとめる", "見出し付きで整理", "Q&A形式", "TL;DR（超短くひとこと）"]


def summarize_text(api_key: str, text: str, style: str, language: str, model: str) -> str:
    lang_line = "日本語で出力" if language == "日本語" else "英語で出力 (Output in English)"

    prompt = f"""以下の文章を要約してください。

## 元の文章
{text}

## 条件
- 要約スタイル: {style}
- 言語: {lang_line}
- 重要な情報は落とさないようにする

要約を出力してください。"""

    return generate(api_key, prompt, model)
