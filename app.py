import tempfile
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from main import run_pipeline
from core.rag_engine import ask_question


# ============================================================
# CONFIG
# ============================================================

load_dotenv()

st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background:
            radial-gradient(circle at 15% 10%, rgba(99, 102, 241, 0.14), transparent 30%),
            radial-gradient(circle at 85% 15%, rgba(14, 165, 233, 0.10), transparent 30%),
            #080b14;
        color: #f8fafc;
    }

    .main .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0d1220 0%,
                #090d17 100%
            );
        border-right: 1px solid rgba(255,255,255,0.07);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    .sidebar-brand {
        padding: 8px 4px 24px 4px;
    }

    .sidebar-logo {
        width: 48px;
        height: 48px;
        border-radius: 14px;
        background: linear-gradient(135deg, #6366f1, #06b6d4);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        box-shadow: 0 8px 25px rgba(99,102,241,0.28);
        margin-bottom: 14px;
    }

    .sidebar-title {
        font-size: 21px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.4px;
    }

    .sidebar-subtitle {
        color: #94a3b8;
        font-size: 13px;
        margin-top: 4px;
        line-height: 1.5;
    }

    .sidebar-section {
        color: #64748b;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.3px;
        margin: 24px 0 10px 2px;
    }

    .pipeline-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 9px 10px;
        margin-bottom: 5px;
        border-radius: 9px;
        color: #cbd5e1;
        font-size: 13px;
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.035);
    }

    .pipeline-icon {
        width: 27px;
        height: 27px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(99,102,241,0.12);
        font-size: 13px;
    }

    /* ---------- HERO ---------- */

    .hero {
        position: relative;
        overflow: hidden;
        padding: 48px 45px;
        margin-bottom: 30px;
        border-radius: 26px;
        border: 1px solid rgba(255,255,255,0.08);
        background:
            radial-gradient(circle at 85% 20%, rgba(99,102,241,0.23), transparent 32%),
            radial-gradient(circle at 70% 100%, rgba(6,182,212,0.14), transparent 30%),
            linear-gradient(135deg, #111827, #0c1120);
        box-shadow: 0 20px 60px rgba(0,0,0,0.28);
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 260px;
        height: 260px;
        border-radius: 50%;
        right: -90px;
        top: -110px;
        background: rgba(99,102,241,0.10);
        filter: blur(10px);
    }

    .hero-badge {
        display: inline-block;
        padding: 7px 13px;
        border-radius: 999px;
        background: rgba(99,102,241,0.12);
        border: 1px solid rgba(129,140,248,0.25);
        color: #a5b4fc;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.1px;
        margin-bottom: 17px;
    }

    .hero-title {
        font-size: 48px;
        line-height: 1.08;
        font-weight: 850;
        letter-spacing: -2px;
        margin: 0;
        color: #ffffff;
    }

    .hero-gradient {
        background: linear-gradient(90deg, #818cf8, #22d3ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-description {
        max-width: 720px;
        margin-top: 18px;
        color: #94a3b8;
        font-size: 16px;
        line-height: 1.7;
    }

    .hero-stack {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 25px;
    }

    .tech-pill {
        padding: 7px 11px;
        border-radius: 8px;
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.07);
        color: #cbd5e1;
        font-size: 11px;
        font-weight: 600;
    }

    /* ---------- SECTION ---------- */

    .section-header {
        margin: 28px 0 17px 0;
    }

    .section-title {
        font-size: 22px;
        font-weight: 800;
        color: #f8fafc;
        margin: 0;
    }

    .section-subtitle {
        margin-top: 5px;
        color: #64748b;
        font-size: 13px;
    }

    /* ---------- FEATURE CARDS ---------- */

    .feature-card {
        height: 100%;
        padding: 22px;
        border-radius: 17px;
        background: rgba(15,23,42,0.72);
        border: 1px solid rgba(255,255,255,0.07);
        transition: 0.2s ease;
    }

    .feature-number {
        color: #818cf8;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 15px;
    }

    .feature-icon {
        font-size: 25px;
        margin-bottom: 13px;
    }

    .feature-title {
        font-size: 16px;
        font-weight: 750;
        color: #f8fafc;
        margin-bottom: 7px;
    }

    .feature-description {
        color: #94a3b8;
        font-size: 12px;
        line-height: 1.6;
    }

    /* ---------- STATUS ---------- */

    .status-card {
        display: flex;
        align-items: center;
        gap: 11px;
        padding: 12px 15px;
        border-radius: 12px;
        background: rgba(34,197,94,0.07);
        border: 1px solid rgba(34,197,94,0.15);
        margin-bottom: 20px;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #22c55e;
        box-shadow: 0 0 12px rgba(34,197,94,0.7);
    }

    .status-text {
        color: #bbf7d0;
        font-size: 12px;
        font-weight: 600;
    }

    /* ---------- METRICS ---------- */

    div[data-testid="stMetric"] {
        background: rgba(15,23,42,0.65);
        border: 1px solid rgba(255,255,255,0.07);
        padding: 16px;
        border-radius: 14px;
    }

    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
    }

    /* ---------- BUTTONS ---------- */

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        border: 1px solid rgba(129,140,248,0.25);
        background: linear-gradient(
            135deg,
            rgba(99,102,241,0.95),
            rgba(79,70,229,0.95)
        );
        color: white;
        font-weight: 700;
        min-height: 42px;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        border-color: rgba(129,140,248,0.7);
        transform: translateY(-1px);
        box-shadow: 0 8px 25px rgba(79,70,229,0.25);
    }

    /* ---------- INPUTS ---------- */

    .stTextInput input,
    .stTextArea textarea {
        background: rgba(15,23,42,0.75) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255,255,255,0.09) !important;
        border-radius: 10px !important;
    }

    .stSelectbox div[data-baseweb="select"] > div {
        background: rgba(15,23,42,0.75);
        border-color: rgba(255,255,255,0.09);
        border-radius: 10px;
    }

    /* ---------- TABS ---------- */

    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        border-bottom: 1px solid rgba(255,255,255,0.07);
    }

    .stTabs [data-baseweb="tab"] {
        color: #64748b;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        color: #a5b4fc !important;
    }

    /* ---------- CHAT ---------- */

    [data-testid="stChatMessage"] {
        background: rgba(15,23,42,0.55);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
    }

    /* ---------- EMPTY STATE ---------- */

    .empty-state {
        text-align: center;
        padding: 70px 30px;
        border-radius: 22px;
        border: 1px dashed rgba(255,255,255,0.10);
        background: rgba(15,23,42,0.30);
        margin-top: 10px;
    }

    .empty-icon {
        font-size: 45px;
        margin-bottom: 15px;
    }

    .empty-title {
        color: #f8fafc;
        font-size: 20px;
        font-weight: 750;
    }

    .empty-description {
        max-width: 520px;
        margin: 8px auto 0;
        color: #64748b;
        font-size: 13px;
        line-height: 1.6;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        margin-top: 60px;
        padding-top: 20px;
        border-top: 1px solid rgba(255,255,255,0.06);
        color: #475569;
        font-size: 11px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "processing" not in st.session_state:
    st.session_state.processing = False


# ============================================================
# HELPERS
# ============================================================

def save_uploaded_file(uploaded_file):
    temp_dir = Path(tempfile.gettempdir()) / "ai_video_assistant"
    temp_dir.mkdir(parents=True, exist_ok=True)

    file_path = temp_dir / uploaded_file.name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return str(file_path)


def reset_session():
    st.session_state.result = None
    st.session_state.chat_history = []
    st.session_state.processing = False


def run_with_progress(source, language):

    progress = st.progress(0)

    with st.status("Running AI Video Assistant...", expanded=True) as status:

        st.write("🎧 Processing audio...")
        progress.progress(15)

        st.write("📝 Transcribing with Whisper...")
        progress.progress(35)

        st.write("🧠 Generating AI insights...")
        progress.progress(55)

        st.write("📊 Extracting structured information...")
        progress.progress(75)

        st.write("🔎 Building conversational knowledge base...")
        progress.progress(90)

        result = run_pipeline(source, language)

        progress.progress(100)

        status.update(
            label="Analysis completed successfully",
            state="complete",
            expanded=False,
        )

    return result


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html(
        """
        <div class="sidebar-brand">
            <div class="sidebar-logo">🎙️</div>
            <div class="sidebar-title">AI Video Assistant</div>
            <div class="sidebar-subtitle">
                Transform long-form video into structured knowledge.
            </div>
        </div>
        """
    )

    st.markdown(
        '<div class="sidebar-section">Input Source</div>',
        unsafe_allow_html=True,
    )

    input_type = st.radio(
        "Choose source",
        ["YouTube URL", "Upload file"],
        label_visibility="collapsed",
    )

    source = None

    if input_type == "YouTube URL":

        source = st.text_input(
            "YouTube URL",
            placeholder="https://youtube.com/watch?v=...",
            label_visibility="collapsed",
        )

    else:

        uploaded_file = st.file_uploader(
            "Upload audio/video",
            type=[
                "mp3",
                "wav",
                "m4a",
                "mp4",
                "mov",
                "avi",
                "mkv",
                "webm",
            ],
            label_visibility="collapsed",
        )

        if uploaded_file:
            source = save_uploaded_file(uploaded_file)

    st.markdown(
        '<div class="sidebar-section">Language</div>',
        unsafe_allow_html=True,
    )

    language = st.selectbox(
        "Language",
        ["english", "hinglish"],
        label_visibility="collapsed",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    analyze_button = st.button(
        "⚡ Analyze Video",
        use_container_width=True,
        type="primary",
    )

    if st.session_state.result is not None:

        if st.button(
            "↻ New Analysis",
            use_container_width=True,
        ):
            reset_session()
            st.rerun()

    st.markdown(
        '<div class="sidebar-section">Pipeline</div>',
        unsafe_allow_html=True,
    )

    pipeline_items = [
        ("🎧", "Audio Processing"),
        ("📝", "Whisper Transcription"),
        ("🧠", "LLM Analysis"),
        ("📌", "Insight Extraction"),
        ("🔎", "RAG Knowledge Base"),
    ]

    for icon, label in pipeline_items:
        st.html(
            f"""
            <div class="pipeline-item">
                <div class="pipeline-icon">{icon}</div>
                <span>{label}</span>
            </div>
            """
        )

    st.markdown(
        """
        <div style="
            margin-top:30px;
            color:#475569;
            font-size:11px;
            line-height:1.6;
        ">
            Built with Streamlit · Whisper · LLM · RAG
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# HERO
# ============================================================

st.html(
    """
    <div class="hero">

        <div class="hero-badge">
            ✦ GENAI · RAG · SPEECH AI
        </div>

        <h1 class="hero-title">
            Turn videos into<br>
            <span class="hero-gradient">
                actionable intelligence.
            </span>
        </h1>

        <div class="hero-description">
            Upload a meeting, lecture or YouTube video and let AI
            transform it into a structured knowledge base with
            summaries, decisions, action items and conversational Q&A.
        </div>

        <div class="hero-stack">
            <div class="tech-pill">🎙️ Speech-to-Text</div>
            <div class="tech-pill">🧠 LLM Analysis</div>
            <div class="tech-pill">🔎 RAG</div>
            <div class="tech-pill">📊 Structured Insights</div>
            <div class="tech-pill">💬 AI Q&A</div>
        </div>

    </div>
    """
)


# ============================================================
# FEATURE SECTION
# ============================================================

if st.session_state.result is None:

    st.html(
        """
        <div class="section-header">
            <div class="section-title">What your video becomes</div>
            <div class="section-subtitle">
                One pipeline. Multiple layers of useful intelligence.
            </div>
        </div>
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.html(
            """
            <div class="feature-card">
                <div class="feature-number">01</div>
                <div class="feature-icon">📝</div>
                <div class="feature-title">
                    Accurate Transcription
                </div>
                <div class="feature-description">
                    Convert spoken content into searchable text
                    using AI-powered speech recognition.
                </div>
            </div>
            """
        )

    with col2:
        st.html(
            """
            <div class="feature-card">
                <div class="feature-number">02</div>
                <div class="feature-icon">🧠</div>
                <div class="feature-title">
                    Smart Insights
                </div>
                <div class="feature-description">
                    Automatically identify summaries, decisions,
                    action items and unanswered questions.
                </div>
            </div>
            """
        )

    with col3:
        st.html(
            """
            <div class="feature-card">
                <div class="feature-number">03</div>
                <div class="feature-icon">💬</div>
                <div class="feature-title">
                    Ask Your Video
                </div>
                <div class="feature-description">
                    Chat with the video's knowledge base and get
                    context-aware answers using RAG.
                </div>
            </div>
            """
        )

    st.html(
        """
        <div class="empty-state">
            <div class="empty-icon">🎬</div>
            <div class="empty-title">
                Your video intelligence workspace is ready
            </div>
            <div class="empty-description">
                Add a YouTube URL or upload a local audio/video file
                from the sidebar, then click
                <b>Analyze Video</b> to begin.
            </div>
        </div>
        """
    )


# ============================================================
# START ANALYSIS
# ============================================================

if analyze_button:

    if not source:
        st.error(
            "Please provide a YouTube URL or upload a file first."
        )

    else:

        try:

            with st.spinner("Preparing AI pipeline..."):
                result = run_with_progress(
                    source,
                    language,
                )

            st.session_state.result = result
            st.session_state.chat_history = []

            st.rerun()

        except Exception as e:

            st.error("Something went wrong while processing the video.")

            with st.expander("View technical error"):
                st.exception(e)


# ============================================================
# RESULTS
# ============================================================

if st.session_state.result is not None:

    result = st.session_state.result

    title = result.get("title", "Untitled Video")
    transcript = result.get("transcript", "")
    summary = result.get("summary", "")
    action_items = result.get("action_items", "")
    decisions = result.get("key_decisions", "")
    questions = result.get("open_questions", "")
    rag_chain = result.get("rag_chain")

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    st.html(
        """
        <div class="status-card">
            <div class="status-dot"></div>
            <div class="status-text">
                Analysis completed successfully
            </div>
        </div>
        """
    )

    # --------------------------------------------------------
    # RESULT HEADER
    # --------------------------------------------------------

    st.html(
        f"""
        <div style="margin-bottom:25px;">

            <div style="
                color:#818cf8;
                font-size:11px;
                font-weight:800;
                letter-spacing:1.2px;
                text-transform:uppercase;
                margin-bottom:8px;
            ">
                VIDEO INTELLIGENCE REPORT
            </div>

            <div style="
                color:#f8fafc;
                font-size:32px;
                font-weight:850;
                letter-spacing:-1px;
                line-height:1.2;
            ">
                {title}
            </div>

        </div>
        """
    )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    word_count = len(transcript.split()) if transcript else 0

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric(
            "Transcript Words",
            f"{word_count:,}",
        )

    with m2:
        st.metric(
            "AI Sections",
            "4",
        )

    with m3:
        st.metric(
            "Knowledge Base",
            "Ready",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # TABS
    # --------------------------------------------------------

    (
        summary_tab,
        actions_tab,
        decisions_tab,
        questions_tab,
        transcript_tab,
        chat_tab,
    ) = st.tabs(
        [
            "📋 Summary",
            "✅ Action Items",
            "🎯 Decisions",
            "❓ Open Questions",
            "📄 Transcript",
            "💬 Ask Your Video",
        ]
    )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    with summary_tab:

        st.html(
            """
            <div class="section-header">
                <div class="section-title">
                    Executive Summary
                </div>
                <div class="section-subtitle">
                    The most important information extracted from the video.
                </div>
            </div>
            """
        )

        if summary:
            st.markdown(summary)
        else:
            st.info("No summary was generated.")

    # --------------------------------------------------------
    # ACTION ITEMS
    # --------------------------------------------------------

    with actions_tab:

        st.html(
            """
            <div class="section-header">
                <div class="section-title">
                    Action Items
                </div>
                <div class="section-subtitle">
                    Tasks and follow-ups identified from the conversation.
                </div>
            </div>
            """
        )

        if action_items:
            st.markdown(action_items)
        else:
            st.info("No action items were identified.")

    # --------------------------------------------------------
    # DECISIONS
    # --------------------------------------------------------

    with decisions_tab:

        st.html(
            """
            <div class="section-header">
                <div class="section-title">
                    Key Decisions
                </div>
                <div class="section-subtitle">
                    Important decisions and conclusions extracted by AI.
                </div>
            </div>
            """
        )

        if decisions:
            st.markdown(decisions)
        else:
            st.info("No major decisions were identified.")

    # --------------------------------------------------------
    # QUESTIONS
    # --------------------------------------------------------

    with questions_tab:

        st.html(
            """
            <div class="section-header">
                <div class="section-title">
                    Open Questions
                </div>
                <div class="section-subtitle">
                    Questions or unresolved points found in the video.
                </div>
            </div>
            """
        )

        if questions:
            st.markdown(questions)
        else:
            st.info("No open questions were identified.")

    # --------------------------------------------------------
    # TRANSCRIPT
    # --------------------------------------------------------

    with transcript_tab:

        st.html(
            """
            <div class="section-header">
                <div class="section-title">
                    Full Transcript
                </div>
                <div class="section-subtitle">
                    Complete searchable transcription generated from the video.
                </div>
            </div>
            """
        )

        st.text_area(
            "Transcript",
            transcript,
            height=550,
            label_visibility="collapsed",
        )

    # --------------------------------------------------------
    # RAG CHAT
    # --------------------------------------------------------

    with chat_tab:

        st.html(
            """
            <div class="section-header">
                <div class="section-title">
                    Ask Your Video
                </div>
                <div class="section-subtitle">
                    Ask questions and retrieve answers from your video's
                    knowledge base.
                </div>
            </div>
            """
        )

        # Suggested questions
        st.markdown("**Try asking:**")

        q1, q2, q3 = st.columns(3)

        suggested_question = None

        with q1:
            if st.button(
                "📌 What are the main points?",
                key="suggested_1",
            ):
                suggested_question = (
                    "What are the main points discussed in the video?"
                )

        with q2:
            if st.button(
                "✅ What are the action items?",
                key="suggested_2",
            ):
                suggested_question = (
                    "What are the action items mentioned in the video?"
                )

        with q3:
            if st.button(
                "🎯 What decisions were made?",
                key="suggested_3",
            ):
                suggested_question = (
                    "What important decisions were made?"
                )

        question = st.chat_input(
            "Ask anything about the video..."
        )

        if suggested_question:
            question = suggested_question

        # ----------------------------------------------------
        # ASK QUESTION
        # ----------------------------------------------------

        if question:

            st.session_state.chat_history.append(
                {
                    "role": "user",
                    "content": question,
                }
            )

            try:

                with st.spinner("Searching the video knowledge base..."):

                    answer = ask_question(
                        rag_chain,
                        question,
                    )

                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

            except Exception as e:

                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": (
                            "Sorry, I couldn't process that question."
                        ),
                    }
                )

                with st.expander("View technical error"):
                    st.exception(e)

        # ----------------------------------------------------
        # CHAT HISTORY
        # ----------------------------------------------------

        for message in st.session_state.chat_history:

            with st.chat_message(message["role"]):
                st.markdown(message["content"])


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div class="footer">
        AI Video Assistant · GenAI + Speech AI + RAG
    </div>
    """
)