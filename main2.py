import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random

# -----------------------------
# 앱 기본 설정
# -----------------------------
st.set_page_config(page_title="💩 스마트 변기 AI 건강 분석", page_icon="🚽", layout="wide")
st.title("🚽 AI 기반 스마트 화장실 건강 분석 시스템")
st.caption("센서 데이터 기반 💩💧 건강 리포트")

# -----------------------------
# 메뉴
# -----------------------------
menu = st.sidebar.radio(
    "메뉴 선택",
    ["1️⃣ 프로필 등록", "2️⃣ 실시간 센서 데이터 분석", "3️⃣ 건강 리포트", "4️⃣ 장기 추세 리포트"]
)

# -----------------------------
# 1️⃣ 프로필 등록
# -----------------------------
if menu == "1️⃣ 프로필 등록":
    st.header("👤 사용자 프로필")
    with st.form("profile_form"):
        nickname = st.text_input("닉네임")
        age = st.number_input("나이", 1, 120)
        sex = st.selectbox("성별", ["남성", "여성", "기타"])
        health_notes = st.text_area("건강 특이사항")
        submitted = st.form_submit_button("저장")
    if submitted:
        st.session_state["profile"] = {
            "닉네임": nickname, "나이": age, "성별": sex, "건강정보": health_notes
        }
        st.success(f"{nickname}님의 프로필이 등록되었습니다!")

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
# 3️⃣ 건강 리포트 (최근 기록 요약)
# -----------------------------
elif menu == "3️⃣ 건강 리포트":
    st.header("📊 최근 건강 리포트 요약")

    # 최근 7일 데이터 시뮬레이션
    dates = pd.date_range(datetime.date.today() - datetime.timedelta(days=6), datetime.date.today())
    health_scores = np.random.randint(60, 100, size=7)
    df = pd.DataFrame({"날짜": dates, "건강지수": health_scores})

    st.line_chart(df.set_index("날짜"))
    avg_score = np.mean(health_scores)
    st.metric("최근 7일 평균 건강지수", f"{avg_score:.1f}/100")

# -----------------------------
# 4️⃣ 장기 추세 리포트
# -----------------------------
elif menu == "4️⃣ 장기 추세 리포트":
    st.header("📈 장기 건강 추세 리포트")
    st.write("날짜 범위를 선택하고 장기 변화를 확인하세요.")
    start = st.date_input("시작일", datetime.date.today() - datetime.timedelta(days=30))
    end = st.date_input("종료일", datetime.date.today())
    if st.button("리포트 보기"):
        days = (end - start).days + 1
        data = np.random.randint(55, 100, size=days)
        df = pd.DataFrame({
            "날짜": pd.date_range(start, end),
            "건강지수": data
        })
        st.line_chart(df.set_index("날짜"))
        st.metric("평균 건강지수", f"{np.mean(data):.1f}/100")

st.divider()
st.caption("© 2025 CleanToilet AI Healthcare System")
