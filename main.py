import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random
import matplotlib.pyplot as plt

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(page_title="💩 스마트 화장실 헬스케어", page_icon="🚽", layout="wide")
st.title("🚽 스마트 화장실 헬스케어 앱")
st.caption("당신의 💩은 건강의 거울입니다.")

# -----------------------------
# 메뉴 구성
# -----------------------------
menu = st.sidebar.radio(
    "메뉴를 선택하세요",
    ["1️⃣ 프로필 등록", "2️⃣ 화장실 방문 기록", "3️⃣ 💩 AI 건강 분석", "4️⃣ 건강 추이 리포트", "5️⃣ 뱃지 & 보상 시스템"]
)

# -----------------------------
# 1️⃣ 프로필 등록
# -----------------------------
if menu == "1️⃣ 프로필 등록":
    st.header("👤 사용자 프로필 등록")

    with st.form("profile_form"):
        nickname = st.text_input("닉네임", "")
        age = st.number_input("나이", 1, 120)
        health_info = st.text_area("건강 관련 특이사항 (예: 변비, 과민성대장증후군 등)")
        submitted = st.form_submit_button("저장하기")

    if submitted:
        st.success(f"✅ {nickname}님의 프로필이 저장되었습니다!")
        st.session_state["profile"] = {
            "nickname": nickname,
            "age": age,
            "health_info": health_info
        }

# -----------------------------
# 2️⃣ 화장실 방문 기록
# -----------------------------
elif menu == "2️⃣ 화장실 방문 기록":
    st.header("🚻 화장실 방문 기록")

    # 모의 데이터
    data = {
        "날짜": pd.date_range(datetime.date.today() - datetime.timedelta(days=7), periods=7),
        "입장시간": [f"{random.randint(7, 22)}:{random.randint(0,59):02d}" for _ in range(7)],
        "퇴장시간": [f"{random.randint(7, 22)}:{random.randint(0,59):02d}" for _ in range(7)],
        "변기물 내림 여부": [random.choice(["✅ O", "❌ X"]) for _ in range(7)]
    }
    df = pd.DataFrame(data)
    st.dataframe(df)

    flushed_rate = (df["변기물 내림 여부"] == "✅ O").mean() * 100
    st.metric("변기 물 내림 성공률", f"{flushed_rate:.1f}%")

# -----------------------------
# 3️⃣ 💩 AI 건강 분석
# -----------------------------
elif menu == "3️⃣ 💩 AI 건강 분석":
    st.header("🤖 AI가 분석하는 💩 건강 상태")

    st.write("오늘의 💩 사진을 업로드하세요 (샘플로 텍스트 입력 사용).")
    stool_description = st.text_area("💩 상태를 설명해주세요 (예: 딱딱함, 색깔, 냄새 등)")

    if st.button("AI 분석하기"):
        # 단순 규칙 기반 분석 (예시)
        if "딱딱" in stool_description:
            result = "💧 수분 섭취 부족, 섬유질 섭취를 늘리세요!"
        elif "묽" in stool_description:
            result = "🚨 설사 경향: 장염 가능성, 수분 보충과 휴식을 취하세요."
        elif "갈색" in stool_description:
            result = "✅ 정상적인 상태! 건강한 💩입니다."
        else:
            result = "🤔 분석이 어렵습니다. 좀 더 자세히 설명해주세요."

        st.success(f"AI 분석 결과: {result}")

# -----------------------------
# 4️⃣ 건강 추이 리포트
# -----------------------------
elif menu == "4️⃣ 건강 추이 리포트":
    st.header("📈 💩 건강 추이 리포트")

    start_date = st.date_input("시작일", datetime.date.today() - datetime.timedelta(days=14))
    end_date = st.date_input("종료일", datetime.date.today())

    if st.button("리포트 보기"):
        days = (end_date - start_date).days + 1
        dates = pd.date_range(start_date, end_date)
        health_scores = np.random.randint(50, 100, days)

        df = pd.DataFrame({"날짜": dates, "💩건강지수": health_scores})
        st.line_chart(df.set_index("날짜"))

        avg_score = np.mean(health_scores)
        st.metric("평균 💩건강지수", f"{avg_score:.1f}/100")

# -----------------------------
# 5️⃣ 뱃지 & 보상 시스템
# -----------------------------
elif menu == "5️⃣ 뱃지 & 보상 시스템":
    st.header("🏅 나의 💩 뱃지 현황")

    badges = [
        {"이름": "🚰 청결왕", "조건": "변기 물 내림 100% 달성"},
        {"이름": "💩 건강마스터", "조건": "건강지수 90점 이상 유지"},
        {"이름": "🧻 꾸준함의 신", "조건": "30일 연속 방문 기록"}
    ]

    for b in badges:
        st.subheader(b["이름"])
        st.caption(f"획득 조건: {b['조건']}")
        if random.random() > 0.5:
            st.success("획득 완료 🎉")
        else:
            st.warning("아직 획득하지 못했습니다.")

st.divider()
st.caption("© 2025 CleanToilet Corp. 모든 권리 보유.")
