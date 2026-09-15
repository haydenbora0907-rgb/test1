import streamlit as st
from openai import OpenAI

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="AI Chat",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# 모바일 UI 스타일
# -----------------------------
st.markdown("""
<style>
    .block-container {
        max-width: 800px;
        padding: 1rem 1rem 5rem 1rem;
    }

    .stChatInput {
        padding-bottom: 10px;
    }

    [data-testid="stChatMessage"] {
        padding: 0.5rem 0;
    }

    h1 {
        font-size: 1.8rem;
    }

    @media (max-width: 600px) {
        .block-container {
            padding: 0.8rem 0.7rem 5rem 0.7rem;
        }

        h1 {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# API 연결
# -----------------------------
try:
    api_key = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
except Exception:
    st.error("OPENAI_API_KEY가 설정되지 않았습니다.")
    st.info("Streamlit Cloud → Settings → Secrets에 API 키를 입력하세요.")
    st.stop()

MODEL = "gpt-5.4-nano"

# -----------------------------
# 세션 상태
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# 상단 UI
# -----------------------------
col1, col2 = st.columns([4, 1])

with col1:
    st.title("🤖 AI Chat")

with col2:
    if st.button("새 대화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.caption("GPT-5.4-nano 기반 대화형 AI")

st.divider()

# -----------------------------
# 기존 대화 표시
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# 사용자 입력
# -----------------------------
if prompt := st.chat_input("메시지를 입력하세요..."):

    # 사용자 메시지 저장
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            stream = client.chat.completions.create(
                model=MODEL,
                messages=st.session_state.messages,
                stream=True
            )

            for chunk in stream:
                content = chunk.choices[0].delta.content

                if content:
                    full_response += content
                    response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)

            # AI 메시지 저장
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response
            })

        except Exception as e:
            st.error(f"API 오류가 발생했습니다: {str(e)}")
