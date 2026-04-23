from .gemini import generate

TONES = ["丁寧・ビジネス", "フレンドリー", "簡潔・要点のみ", "謝罪・お詫び", "断り・辞退"]


def write_email_reply(api_key: str, received: str, tone: str, points: str, sender_name: str, model: str) -> str:
    points_line = f"- 必ず伝えたいこと: {points}" if points.strip() else ""
    sender_line = f"- 送信者名（差出人）: {sender_name}" if sender_name.strip() else ""

    prompt = f"""あなたはビジネスメールの専門家です。受信したメールへの返信文を書いてください。

## 受信メール
{received}

## 条件
- 文体・トーン: {tone}
{points_line}
{sender_line}

## 出力形式
- 件名（件名: ○○）を1行目に書く
- 本文のみ出力（宛名〜署名まで）
- 自然な日本語で

返信文を書いてください。"""

    return generate(api_key, prompt, model)
