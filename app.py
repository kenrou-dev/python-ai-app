import os
import streamlit as st
from dotenv import load_dotenv

from tools.blog import write_blog, TONES as BLOG_TONES, LENGTH_MAP
from tools.email_reply import write_email_reply, TONES as EMAIL_TONES
from tools.summarize import summarize_text, STYLES as SUMMARY_STYLES
from tools.rewrite import rewrite_text, STYLES as REWRITE_STYLES
from tools.titles import generate_titles, STYLES as TITLE_STYLES

load_dotenv()

MODELS = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]

st.set_page_config(
    page_title="AI ライティングツール",
    page_icon="✍️",
    layout="wide",
)

# --- サイドバー ---
with st.sidebar:
    st.title("⚙️ 設定")
    api_key = st.text_input(
        "Gemini API キー",
        value=os.getenv("GOOGLE_API_KEY", ""),
        type="password",
        help=".env に GOOGLE_API_KEY を設定するか、ここに直接入力してください",
    )
    model = st.selectbox("使用モデル", MODELS)
    st.divider()
    st.markdown("**ツール一覧**")
    st.markdown("- 📝 ブログ記事作成")
    st.markdown("- 📧 メール返信")
    st.markdown("- 📄 文章要約")
    st.markdown("- 🔄 文章リライト")
    st.markdown("- 💡 タイトル生成")


def check_api_key() -> bool:
    if not api_key or api_key == "your_api_key_here":
        st.warning("サイドバーで Gemini API キーを入力してください。")
        return False
    return True


# --- メインエリア ---
st.title("✍️ AI ライティングツール")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📝 ブログ記事", "📧 メール返信", "📄 文章要約", "🔄 リライト", "💡 タイトル生成"]
)

# =====================
# タブ1: ブログ記事
# =====================
with tab1:
    st.header("ブログ記事作成")
    st.caption("テーマや条件を指定するだけで、ブログ記事を自動生成します。")

    col1, col2 = st.columns([2, 1])
    with col1:
        topic = st.text_input("記事のテーマ・タイトル案 *", placeholder="例: 初心者でもできる家庭菜園の始め方")
        keywords = st.text_input("キーワード（任意）", placeholder="例: 節約, プランター, 初心者")
    with col2:
        tone = st.selectbox("文体・トーン", BLOG_TONES)
        length_label = st.selectbox("目標文字数", list(LENGTH_MAP.keys()))

    if st.button("記事を生成", type="primary", key="blog_btn"):
        if not check_api_key():
            pass
        elif not topic.strip():
            st.error("テーマを入力してください。")
        else:
            with st.spinner("記事を生成中..."):
                result = write_blog(api_key, topic, tone, length_label, keywords, model)
            st.divider()
            st.markdown(result)
            st.download_button("📥 テキストをダウンロード", result, file_name="blog.md", mime="text/markdown")

# =====================
# タブ2: メール返信
# =====================
with tab2:
    st.header("メール返信文の作成")
    st.caption("受け取ったメールを貼り付けると、返信文を自動で作成します。")

    received = st.text_area("受信メールの内容 *", height=200, placeholder="ここに受け取ったメールの本文を貼り付けてください...")

    col1, col2 = st.columns(2)
    with col1:
        email_tone = st.selectbox("返信のトーン", EMAIL_TONES)
        sender_name = st.text_input("自分の名前（署名用）", placeholder="例: 山田 太郎")
    with col2:
        points = st.text_area("必ず伝えたいこと（任意）", height=100, placeholder="例: 来週水曜日は参加できません。別日程を提案したい。")

    if st.button("返信文を生成", type="primary", key="email_btn"):
        if not check_api_key():
            pass
        elif not received.strip():
            st.error("受信メールの内容を入力してください。")
        else:
            with st.spinner("返信文を作成中..."):
                result = write_email_reply(api_key, received, email_tone, points, sender_name, model)
            st.divider()
            st.text_area("生成された返信文", value=result, height=300)
            st.download_button("📥 テキストをダウンロード", result, file_name="email_reply.txt", mime="text/plain")

# =====================
# タブ3: 文章要約
# =====================
with tab3:
    st.header("文章の要約")
    st.caption("長い文章を貼り付けると、指定したスタイルで要約します。")

    text_to_summarize = st.text_area("要約したい文章 *", height=250, placeholder="ここに要約したい文章を貼り付けてください...")

    col1, col2 = st.columns(2)
    with col1:
        summary_style = st.selectbox("要約スタイル", SUMMARY_STYLES)
    with col2:
        language = st.selectbox("出力言語", ["日本語", "英語"])

    if st.button("要約する", type="primary", key="summary_btn"):
        if not check_api_key():
            pass
        elif not text_to_summarize.strip():
            st.error("要約したい文章を入力してください。")
        else:
            with st.spinner("要約中..."):
                result = summarize_text(api_key, text_to_summarize, summary_style, language, model)
            st.divider()
            st.markdown(result)
            st.download_button("📥 テキストをダウンロード", result, file_name="summary.txt", mime="text/plain")

# =====================
# タブ4: リライト
# =====================
with tab4:
    st.header("文章のリライト・変換")
    st.caption("文体の変換・翻訳・簡略化など、文章を書き直します。")

    text_to_rewrite = st.text_area("書き直したい文章 *", height=200, placeholder="ここに変換したい文章を貼り付けてください...")

    col1, col2 = st.columns(2)
    with col1:
        rewrite_style = st.selectbox("変換スタイル", REWRITE_STYLES)
    with col2:
        extra_instruction = st.text_input("追加指示（任意）", placeholder="例: 200文字以内に収めて")

    if st.button("書き直す", type="primary", key="rewrite_btn"):
        if not check_api_key():
            pass
        elif not text_to_rewrite.strip():
            st.error("書き直したい文章を入力してください。")
        else:
            with st.spinner("リライト中..."):
                result = rewrite_text(api_key, text_to_rewrite, rewrite_style, extra_instruction, model)
            st.divider()
            col_orig, col_new = st.columns(2)
            with col_orig:
                st.subheader("元の文章")
                st.text_area("", value=text_to_rewrite, height=200, disabled=True, key="orig_display")
            with col_new:
                st.subheader("書き直した文章")
                st.text_area("", value=result, height=200, key="rewrite_display")
            st.download_button("📥 テキストをダウンロード", result, file_name="rewritten.txt", mime="text/plain")

# =====================
# タブ5: タイトル生成
# =====================
with tab5:
    st.header("タイトル・見出し生成")
    st.caption("記事の内容やテーマを入力すると、複数のタイトル案を提案します。")

    content_for_title = st.text_area(
        "記事の内容・テーマ・概要 *",
        height=150,
        placeholder="例: Pythonを使ってWebスクレイピングする方法について解説する記事。初心者向けで、BeautifulSoupの使い方を中心に説明する。",
    )

    col1, col2 = st.columns(2)
    with col1:
        title_style = st.selectbox("タイトルのスタイル", TITLE_STYLES)
    with col2:
        title_count = st.slider("生成する案の数", min_value=3, max_value=10, value=5)

    if st.button("タイトルを生成", type="primary", key="title_btn"):
        if not check_api_key():
            pass
        elif not content_for_title.strip():
            st.error("記事の内容・テーマを入力してください。")
        else:
            with st.spinner("タイトルを考え中..."):
                result = generate_titles(api_key, content_for_title, title_count, title_style, model)
            st.divider()
            st.markdown(result)
            st.download_button("📥 テキストをダウンロード", result, file_name="titles.txt", mime="text/plain")
