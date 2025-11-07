# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="Smart Toilet Health App", layout="wide")
st.title("🚻 스마트 화장실 건강 관리 앱 (Streamlit 프로토타입)")

# sidebar: user selection / create
st.sidebar.header("사용자 관리")
users_df = get_users()

selected_user_id = st.sidebar.selectbox("사용자 선택", options=["--새 사용자 생성--"] + list(users_df["user_id"]) if not users_df.empty else ["--새 사용자 생성--"], format_func=lambda x: "--- 새 사용자 생성 ---" if x == "--새 사용자 생성--" else users_df[users_df["user_id"]==x]["nickname"].values[0])

if selected_user_id == "--새 사용자 생성--":
    st.sidebar.markdown("### 새 사용자 등록")
    nickname = st.sidebar.text_input("닉네임")
    age = st.sidebar.number_input("나이", min_value=1, max_value=120, value=25)
    gender = st.sidebar.selectbox("성별", options=["선택안함","남성","여성","기타"])
    health_flags = st.sidebar.multiselect("건강 특이사항 (선택)", options=["알레르기", "만성질환", "임신", "기저질환(간/신장 등)", "특이사항 없음"])
    if st.sidebar.button("등록"):
        if not nickname.strip():
            st.sidebar.error("닉네임을 입력하세요.")
        else:
            user_id = create_user(nickname.strip(), int(age), gender, health_flags or ["특이사항 없음"])
            st.sidebar.success("사용자 등록 완료.")
            st.experimental_rerun()
else:
    user = get_user(selected_user_id)
    if user:
        st.sidebar.markdown(f"**선택된 사용자:** {user['nickname']}  (나이: {user['age']}, 성별: {user['gender']})")
        if st.sidebar.button("프로필 편집"):
            # Quick edit modal area in main
            st.session_state["edit_user"] = selected_user_id

# Main tabs
tabs = st.tabs(["대시보드","방문 기록(지문 시뮬레이션)","건강 리포트(분석)","기간별 그래프","뱃지/성과"])

# ---------------------------
# Tab: Dashboard (summary)
# ---------------------------
with tabs[0]:
    st.header("대시보드")
    if selected_user_id == "--새 사용자 생성--":
        st.info("왼쪽에서 사용자를 생성하거나 선택하세요.")
    else:
        u = get_user(selected_user_id)
        st.subheader(f"안녕하세요, {u['nickname']}님 👋")
        visits = get_visits_for_user(selected_user_id)
        total = len(visits)
        st.metric("총 방문 수", total)
        if total > 0:
            last = visits.iloc[-1]
            st.metric("마지막 검사 점수", f"{last['stool_score']}/100")
            st.write("최근 리포트 요약:")
            st.write(last["report_text"])
        st.markdown("---")
        st.write("프로필 정보:")
        st.write({
            "닉네임": u["nickname"],
            "나이": u["age"],
            "성별": u["gender"],
            "건강 특이사항": u["health_flags"]
        })

# ---------------------------
# Tab: Visit / Fingerprint (simulate)
# ---------------------------
with tabs[1]:
    st.header("🚪 지문 스캔 & 화장실 방문 기록 (시뮬레이션)")
    if selected_user_id == "--새 사용자 생성--":
        st.info("사용자를 선택/생성하세요.")
    else:
        st.write("지문 인식을 시뮬레이션하려면 버튼을 눌러주세요.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("지문 인식 (입장)"):
                st.success("지문 인식 성공 — 입장 허용")
                st.session_state["in_restroom"] = True
                st.session_state["enter_time"] = datetime.utcnow()
        with col2:
            if st.button("물 내리기 (퇴실 시)"):
                if not st.session_state.get("in_restroom", False):
                    st.warning("먼저 지문 인식을 통해 입장해야 합니다.")
                else:
                    # simulate sensor reading on flush/exit
                    reading = simulate_sensor_reading()
                    reading["report"] = generate_report(reading)
                    visit_id = log_visit(selected_user_id, reading)
                    st.success(f"방문 기록 저장: {visit_id}")
                    st.write("센서 요약:")
                    st.json(reading)
                    # award badges if eligible
                    award_badge_if_eligible(selected_user_id)
                    # exit
                    st.session_state["in_restroom"] = False
                    st.session_state["enter_time"] = None

        # show recent visits preview
        st.markdown("### 최근 방문 기록 (최대 10개)")
        visits = get_visits_for_user(selected_user_id)
        if visits.empty:
            st.write("방문 기록이 없습니다.")
        else:
            preview = visits[['visit_id','timestamp','stool_score','hydrated_score','nutrition_score','report_text']].sort_values('timestamp', ascending=False).head(10)
            st.dataframe(preview)

# ---------------------------
# Tab: Health Report (analysis)
# ---------------------------
with tabs[2]:
    st.header("🩺 건강 리포트")
    if selected_user_id == "--새 사용자 생성--":
        st.info("사용자를 선택/생성하세요.")
    else:
        st.markdown("최근 방문 데이터로부터 분석된 리포트를 확인할 수 있습니다.")
        visits = get_visits_for_user(selected_user_id)
        if visits.empty:
            st.write("방문 기록이 없습니다. (지문 인식 -> 물 내리기 시 센서값이 수집됩니다.)")
        else:
            latest = visits.iloc[-1]
            st.subheader("최신 리포트")
            st.write(f"검사 시간: {latest['timestamp']}")
            st.metric("장 건강 점수", f"{latest['stool_score']}/100")
            st.metric("수분 점수", f"{latest['hydrated_score']:.1f}/100")
            st.metric("영양 점수", f"{latest['nutrition_score']:.1f}/100")
            st.markdown("**상세 센서 데이터**")
            st.write({
                "pH": latest["ph"],
                "단백질": latest["protein"],
                "당(Glucose)": latest["glucose"],
                "색상 이상도": latest["color_score"],
                "온도(°C)": latest["temp"]
            })
            st.markdown("**맞춤 권고 안내**")
            st.write(latest["report_text"])

            # allow user to request "심층분석" (simulated AI)
            if st.button("심층 AI 분석(시뮬레이션)"):
                st.info("심층 분석 중... (시뮬레이션)")
                # simple simulated message
                deeper = []
                if latest['protein'] > 0.6:
                    deeper.append("고단백 식단이 장기간 지속되면 신장 부담 가능 — 단백질 섭취량을 1주간 조정해 보세요.")
                if latest['glucose'] > 0.4:
                    deeper.append("소변 당 상승 소견: 혈당 체크 권장.")
                if latest['stool_score'] < 50:
                    deeper.append("장내 미생물 다양성 개선을 위한 프로바이오틱스/식이섬유 권장(의사 상담 권고).")
                if not deeper:
                    deeper.append("심층 이상 없음 — 현재 상태 유지 권고.")
                for p in deeper:
                    st.write("- " + p)

# ---------------------------
# Tab: Time-range Graphs
# ---------------------------
with tabs[3]:
    st.header("📈 기간별 건강 변화 보기")
    if selected_user_id == "--새 사용자 생성--":
        st.info("사용자를 선택/생성하세요.")
    else:
        visits_all = get_visits_for_user(selected_user_id)
        if visits_all.empty:
            st.write("방문 기록이 없습니다.")
        else:
            # date pickers
            min_date = pd.to_datetime(visits_all['timestamp']).dt.date.min()
            max_date = pd.to_datetime(visits_all['timestamp']).dt.date.max()
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("시작일", value=min_date, min_value=min_date, max_value=max_date)
            with col2:
                end_date = st.date_input("종료일", value=max_date, min_value=min_date, max_value=max_date)
            if start_date > end_date:
                st.error("시작일은 종료일보다 이전이어야 합니다.")
            else:
                start_dt = datetime.combine(start_date, datetime.min.time())
                end_dt = datetime.combine(end_date, datetime.max.time())
                sel = get_visits_for_user(selected_user_id, start=start_dt, end=end_dt)
                if sel.empty:
                    st.write("해당 기간의 데이터가 없습니다.")
                else:
                    df = sel.copy()
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    df = df.sort_values('timestamp')
                    # melt for charting
                    plot_df = df[['timestamp','stool_score','hydrated_score','nutrition_score']].melt('timestamp', var_name='metric', value_name='value')
                    chart = alt.Chart(plot_df).mark_line(point=True).encode(
                        x='timestamp:T',
                        y='value:Q',
                        color='metric:N',
                        tooltip=['timestamp:T','metric:N','value:Q']
                    ).interactive()
                    st.altair_chart(chart, use_container_width=True)
                    st.markdown("원시 표")
                    st.dataframe(df[['timestamp','stool_score','hydrated_score','nutrition_score','report_text']])

# ---------------------------
# Tab: Badges / Gamification
# ---------------------------
with tabs[4]:
    st.header("🏅 뱃지 및 성취")
    if selected_user_id == "--새 사용자 생성--":
        st.info("사용자를 선택/생성하세요.")
    else:
        badges_df = get_badges(selected_user_id)
        if badges_df.empty:
            st.write("아직 획득한 뱃지가 없습니다. 규칙적으로 사용해보세요!")
        else:
            st.write("획득한 뱃지:")
            st.dataframe(badges_df)
        st.markdown("획득 가능한 뱃지 예시:")
        st.write("- Hydrated Streak: 연속 3회 수분 상태 양호")
        st.write("- Nutrition Improved: 최근 영양 점수 향상")
        st.write("- Clean Flusher: 규칙적으로 물 내림을 준수")

# ---------------------------
# Inline: Profile edit modal (simple)
# ---------------------------
if st.session_state.get("edit_user"):
    edit_id = st.session_state["edit_user"]
    u = get_user(edit_id)
    if u:
        st.markdown("---")
        st.subheader("프로필 편집")
        col1, col2, col3 = st.columns(3)
        with col1:
            new_nick = st.text_input("닉네임", value=u["nickname"])
        with col2:
            new_age = st.number_input("나이", min_value=1, max_value=120, value=int(u["age"]))
        with col3:
            new_gender = st.selectbox("성별", options=["선택안함","남성","여성","기타"], index=["선택안함","남성","여성","기타"].index(u["gender"]) if u["gender"] in ["선택안함","남성","여성","기타"] else 0)
            new_flags = st.multiselect("건강 특이사항", options=["알레르기", "만성질환", "임신", "기저질환(간/신장 등)", "특이사항 없음"], default=u["health_flags"].split(","))
        if st.button("저장"):
            c = conn.cursor()
            c.execute('UPDATE users SET nickname=?, age=?, gender=?, health_flags=? WHERE user_id=?', (new_nick, int(new_age), new_gender, ",".join(new_flags), edit_id))
            conn.commit()
            st.success("프로필이 업데이트되었습니다.")
            st.session_state["edit_user"] = None
            st.experimental_rerun()
        if st.button("취소"):
            st.session_state["edit_user"] = None
            st.experimental_rerun()
