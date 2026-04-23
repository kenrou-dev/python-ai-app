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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* ── 背景 ── */
.stApp {
    background: #f0f2f6;
}

[data-testid="block-container"] {
    padding: 1.5rem 2.5rem 3rem !important;
}

/* ── サイドバー ── */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0f0c29, #302b63, #24243e) !important;
}

[data-testid="stSidebar"] label {
    color: #a0aec0 !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: white !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li {
    color: #cbd5e0 !important;
}

[data-testid="stSidebar"] .stTextInput input {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    color: white !important;
    border-radius: 8px !important;
}

[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    color: white !important;
    border-radius: 8px !important;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.15) !important;
}

/* ── タイトル ── */
h1 {
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
}

h2 {
    color: #2d3748 !important;
    font-weight: 600 !important;
    font-size: 1.35rem !important;
}

h3 {
    color: #4a5568 !important;
    font-weight: 600 !important;
}

/* ── タブ ── */
.stTabs [data-baseweb="tab-list"] {
    background: white !important;
    border-radius: 14px !important;
    padding: 5px !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08) !important;
    gap: 4px !important;
    border-bottom: none !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    padding: 8px 18px !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    color: #718096 !important;
    border: none !important;
    transition: all 0.2s ease !important;
    background: transparent !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
}

.stTabs [data-baseweb="tab-panel"] {
    background: white !important;
    border-radius: 16px !important;
    padding: 2rem !important;
    box-shadow: 0 2px 16px rgba(0,0,0,0.07) !important;
    margin-top: 0.75rem !important;
}

/* ── ボタン（生成） ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.55rem 2rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    box-shadow: 0 4px 15px rgba(102,126,234,0.4) !important;
    transition: all 0.25s ease !important;
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(102,126,234,0.55) !important;
}

.stButton > button[kind="primary"]:active {
    transform: translateY(0px) !important;
}

/* ── ダウンロードボタン ── */
.stDownloadButton > button {
    background: white !important;
    color: #667eea !important;
    border: 2px solid #667eea !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.25s ease !important;
}

.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border-color: transparent !important;
}

/* ── 入力フィールド ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border: 2px solid #e2e8f0 !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    background: #fafafa !important;
    color: #1a202c !important;
    caret-color: #667eea !important;
    transition: all 0.2s ease !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102,126,234,0.15) !important;
    background: white !important;
}

/* ── セレクトボックス ── */
.stSelectbox > div > div {
    border: 2px solid #e2e8f0 !important;
    border-radius: 8px !important;
    background: #fafafa !important;
    transition: all 0.2s ease !important;
}

/* ── ラベル ── */
label {
    font-weight: 500 !important;
    color: #4a5568 !important;
    font-size: 0.88rem !important;
}

/* ── キャプション ── */
.stCaption, [data-testid="stCaptionContainer"] {
    color: #718096 !important;
    font-size: 0.84rem !important;
}

/* ── 区切り線 ── */
hr {
    border: none !important;
    height: 2px !important;
    background: linear-gradient(90deg, transparent, #667eea 30%, #764ba2 70%, transparent) !important;
    margin: 1.5rem 0 !important;
    opacity: 0.4 !important;
}

/* ── アラート ── */
.stAlert {
    border-radius: 10px !important;
    border: none !important;
}

/* ── スライダー ── */
[data-testid="stSlider"] [role="slider"] {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
}
</style>
""", unsafe_allow_html=True)

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
st.markdown(
    "<p style='color:#718096; margin-top:-0.8rem; margin-bottom:1.5rem; font-size:1rem;'>"
    "Gemini AI を使ったライティングアシスタント</p>",
    unsafe_allow_html=True,
)

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
