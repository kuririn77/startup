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
# 2️⃣ 실시간 센서 데이터 분석
# -----------------------------
elif menu == "2️⃣ 실시간 센서 데이터 분석":
    st.header("🧪 변기 내 센서 데이터 수집 및 AI 분석")

    st.write("센서 데이터 예시 (pH, 단백질, 당, 색상, 온도 등):")

    # 센서 데이터 시뮬레이션
    sensor_data = {
        "pH": round(random.uniform(5.0, 8.0), 2),
        "단백질": round(random.uniform(0, 3), 2),
        "당": round(random.uniform(0, 2), 2),
        "색상": random.choice(["밝은 노랑", "진한 갈색", "붉은빛", "투명"]),
        "온도(°C)": round(random.uniform(30, 38), 1),
    }

    df = pd.DataFrame([sensor_data])
    st.dataframe(df)

    # -------------------------
    # AI 분석 로직 (예시)
    # -------------------------
    def analyze_sensor_data(data):
        score = {}
        advice = []

        # 장 건강 점수
        if 6.5 <= data["pH"] <= 7.5:
            score["장 건강"] = 90
        else:
            score["장 건강"] = 60
            advice.append("⚠️ 장내 환경이 불균형할 수 있습니다. 식이섬유를 늘려보세요.")

        # 수분 상태
        if data["색상"] in ["밝은 노랑", "투명"]:
            score["수분 상태"] = 95
        else:
            score["수분 상태"] = 70
            advice.append("💧 수분 섭취를 늘리세요. 물을 자주 마시세요.")

        # 영양 상태
        if data["단백질"] < 1.5 and data["당"] < 1.0:
            score["영양 상태"] = 90
        else:
            score["영양 상태"] = 65
            advice.append("🍗 단백질이나 당 섭취량이 높습니다. 식단 조절을 권장합니다.")

        overall = np.mean(list(score.values()))
        return score, overall, advice

    scores, total, advices = analyze_sensor_data(sensor_data)

    st.subheader("AI 분석 결과")
    st.metric("💩 종합 건강 지수", f"{total:.1f}/100")

    col1, col2, col3 = st.columns(3)
    col1.metric("장 건강", scores["장 건강"])
    col2.metric("수분 상태", scores["수분 상태"])
    col3.metric("영양 상태", scores["영양 상태"])

    st.subheader("🔍 맞춤형 건강 리포트")
    if advices:
        for tip in advices:
            st.write(tip)
    else:
        st.success("✅ 전반적으로 건강한 상태입니다!")

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
