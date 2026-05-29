import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="연애 코칭 앱",
    page_icon="💖",
    layout="centered"
)

# 제목
st.title("💖 연애 코칭 앱")
st.write("연애 고민을 입력하면 간단한 조언을 해드립니다.")

# 사용자 입력
user_input = st.text_area(
    "연애 고민을 적어주세요",
    height=150
)

# 코칭 함수
def love_coach(text):
    text = text.lower()

    if "헤어" in text:
        return "지금은 감정적으로 힘들 수 있어요. 충분히 쉬고 자신을 먼저 돌보세요."

    elif "고백" in text:
        return "상대에게 솔직한 마음을 자연스럽게 표현해보세요."

    elif "짝사랑" in text:
        return "상대의 반응을 천천히 살피면서 다가가는 것이 좋아요."

    elif "싸웠" in text:
        return "감정을 바로 표현하기보다 차분하게 대화하는 것이 중요해요."

    elif text.strip() == "":
        return "고민을 입력해주세요."

    else:
        return "상대방의 입장을 이해하려는 태도가 가장 중요해요."

# 버튼
if st.button("코칭 받기 💌"):

    advice = love_coach(user_input)

    st.success("연애 코칭 결과")
    st.write(advice)

# 하단 문구
st.markdown("---")
st.caption("Made with Streamlit 💖")
