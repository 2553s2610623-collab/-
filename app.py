import streamlit as st
from google import genai
from google.genai import types

# 페이지 설정
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💕",
    layout="centered"
)

st.title("💕 AI 연애상담 챗봇")
st.caption("연애 고민을 편하게 이야기해보세요.")

# API Key 확인
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# Gemini Client 생성
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 초기화 오류: {e}")
    st.stop()

# 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요 😊\n\n"
                "저는 연애상담 AI입니다.\n"
                "썸, 연애, 이별, 재회, 인간관계 고민 등을 편하게 이야기해주세요."
            )
        }
    ]

# 기존 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
prompt = st.chat_input("연애 고민을 입력하세요...")

if prompt:

    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Gemini용 대화 기록 변환
        contents = []

        system_prompt = """
        당신은 따뜻하고 공감 능력이 높은 연애상담 전문가입니다.

        원칙:
        - 사용자의 감정을 존중한다.
        - 비난하지 않는다.
        - 현실적이고 구체적인 조언을 제공한다.
        - 지나친 단정은 피한다.
        - 답변은 자연스러운 한국어로 작성한다.
        - 필요하면 추가 질문을 한다.
        """

        contents.append(
            types.Content(
                role="user",
                parts=[types.Part(text=system_prompt)]
            )
        )

        for msg in st.session_state.messages:
            role = "model" if msg["role"] == "assistant" else "user"

            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part(text=msg["content"])]
                )
            )

        with st.chat_message("assistant"):
            with st.spinner("생각 중..."):

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=contents
                )

                answer = response.text

                st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    except Exception as e:

        error_msg = (
            "죄송합니다. 응답 생성 중 오류가 발생했습니다.\n\n"
            f"오류 내용: {str(e)}"
        )

        with st.chat_message("assistant"):
            st.error(error_msg)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": error_msg
            }
        )
