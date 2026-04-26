import streamlit as st

# [설정] 페이지 레이아웃
st.set_page_config(page_title="25kg 감량 성공자의 AI 코칭 계산기", layout="centered")

def main():
    st.title("🏆 실패 없는 코칭형 영양 설계 시스템")
    st.write("단순한 계산기가 아닙니다. 당신의 목표를 현실로 만드는 **실전 가이드**입니다.")
    st.markdown("---")

    # 1. 사용자 신체 정보 입력 (사이드바)
    with st.sidebar:
        st.header("👤 신체 정보 입력")
        weight = st.number_input("현재 체중 (kg)", value=75.0, step=0.1)
        muscle = st.number_input("골격근량 (kg)", value=32.0, step=0.1)
        
        st.markdown("---")
        st.header("🥩 영양 전략 설정")
        
        # 단백질 설정 및 설명
        prot_ratio = st.slider("단백질 섭취 강도 (체중 1kg당 g)", 1.5, 2.5, 2.0, 0.1)
        with st.expander("❓ 단백질, 얼마나 먹어야 하나요?"):
            st.caption("""
            **목표별 추천 강도:**
            * **다이어트:** 2.0~2.4g (근손실 방지 최우선)
            * **린매스업:** 1.8~2.2g (근성장과 회복)
            * **벌크업:** 1.6~2.0g (탄수화물 비중 확보)
            
            단백질은 근육의 재료이며, 소화 시 열 발생이 높아 다이어트 자체에도 도움이 됩니다.
            """)

        # 지방 설정 및 설명
        fat_percent = st.slider("지방 섭취 비율 (%)", 20, 30, 25, 5) / 100
        with st.expander("❓ 지방은 왜 먹어야 하나요?"):
            st.caption("""
            지방은 **호르몬(남성호르몬 등) 생성**의 필수 원료입니다. 
            너무 적게 먹으면 무기력증이나 피부 건조가 올 수 있습니다. 
            * **20%:** 운동 에너지가 많이 필요한 경우
            * **30%:** 포만감과 호르몬 건강을 중시하는 경우
            """)

    # 2. 활동량 입력
    st.subheader("⏰ 오늘 나의 24시간 활동량")
    col1, col2 = st.columns(2)
    with col1:
        sleep = st.slider("💤 수면 (시간)", 0, 12, 7)
        office = st.slider("🪑 좌식 생활 (사무/운전/공부)", 0, 15, 8)
        walking = st.slider("🚶 가벼운 활동 (출퇴근/이동)", 0, 15, 4)
    with col2:
        labor = st.slider("🏗️ 고강도 활동 (현장/물류/진열)", 0, 15, 0)
        workout = st.slider("🏋️ 웨이트 트레이닝 (운동)", 0.0, 4.0, 1.0, 0.5)
        etc = st.slider("☕ 기타 (식사/휴식 등)", 0, 10, 4)

    total_h = sleep + office + walking + labor + workout + etc

    if total_h != 24:
        st.warning(f"⚠️ 현재 {total_h}시간입니다. 총 24시간을 맞춰주세요!")
    else:
        # --- 계산 로직 ---
        bmr = 370 + (21.6 * muscle)
        met_val = (sleep*1.0 + office*1.5 + walking*2.5 + labor*4.5 + workout*6.5 + etc*2.0)
        tdee = bmr * (met_val / 24)

        goals = {
            "📍 감량 (체지방 감소)": -500,
            "📍 유지 (리컴포지션)": 0,
            "📍 린벌크 (근성장 위주)": 200,
            "📍 벌크 (체중 및 근력 증대)": 500
        }
        
        st.markdown("---")
        st.subheader("📋 목표별 영양 설계 결과")
        
        for goal_name, offset in goals.items():
            target_kcal = tdee + offset
            p_g = weight * prot_ratio
            f_g = (target_kcal * fat_percent) / 9
            c_g = (target_kcal - (p_g * 4 + f_g * 9)) / 4
            
            with st.expander(f"{goal_name}", expanded=(offset == -500)):
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("총 칼로리", f"{int(target_kcal)} kcal")
                c2.metric("탄수화물", f"{int(c_g)}g", f"{int((c_g*4/target_kcal)*100)}%")
                c3.metric("단백질", f"{int(p_g)}g", f"{int((p_g*4/target_kcal)*100)}%")
                c4.metric("지방", f"{int(f_g)}g", f"{int((f_g*9/target_kcal)*100)}%")

        # --- 가이드 안내 ---
        st.markdown("---")
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.info("📈 **체중 변화 가이드**\n- 주당 0.25~0.5kg 변화: 정상\n- 변화 없음: 칼로리 부족/과다 체크")
        with col_g2:
            st.success("🍴 **식단 적용 팁**\n- 단백질은 하루 3~5회 분할 섭취\n- 탄수화물은 운동 전후 배치")

        st.caption("주의: 본 결과는 가이드라인이며, 2주 단위로 체중 변화를 보며 직접 조정하는 것이 가장 정확합니다.")

if __name__ == "__main__":
    main()