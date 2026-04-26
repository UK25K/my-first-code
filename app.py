import streamlit as st

# [설정] 페이지 레이아웃 및 디자인
st.set_page_config(page_title="25kg 감량 성공자의 AI 코칭 계산기", layout="centered")

def main():
    st.title("🏆 실패 없는 코칭형 영양 설계 시스템")
    st.write("25kg 감량 성공자의 데이터와 전문 영양학 로직이 결합된 맞춤형 솔루션입니다.")
    st.markdown("---")

    # 1. 사용자 신체 정보 입력
    with st.sidebar:
        st.header("👤 신체 정보 입력")
        weight = st.number_input("현재 체중 (kg)", value=75.0, step=0.1)
        muscle = st.number_input("골격근량 (kg)", value=32.0, step=0.1)
        
        st.markdown("---")
        st.header("🥩 영양 전략 설정")
        prot_ratio = st.slider("단백질 섭취 강도 (체중 1kg당 g)", 1.6, 2.5, 2.0, 0.1)
        fat_percent = st.slider("지방 섭취 비율 (%)", 20, 30, 25, 5) / 100
        
        st.markdown("---")
        is_cheating = st.checkbox("🔥 오늘은 치팅데이인가요?")

    # 2. 활동량 입력 (설명 텍스트 추가)
    st.subheader("⏰ 오늘 나의 24시간 활동량")
    st.caption("비어있는 시간 없이 총 24시간을 채워주세요.")
    
    col1, col2 = st.columns(2)
    with col1:
        sleep = st.slider("💤 수면 (시간)", 0, 12, 7)
        office = st.slider("🪑 좌식 생활 (사무/운전/공부)", 0, 15, 8)
        walking = st.slider("🚶 가벼운 활동 (출퇴근/이동/집안일)", 0, 15, 4)
    with col2:
        labor = st.slider("🏗️ 고강도 활동 (현장작업/상하차/크로스핏)", 0, 15, 0)
        workout = st.slider("🏋️ 웨이트 트레이닝 (운동)", 0.0, 4.0, 1.0, 0.5)
        etc = st.slider("☕ 기타 (식사/휴식 등)", 0, 10, 4)

    total_h = sleep + office + walking + labor + workout + etc

    if total_h != 24:
        st.warning(f"⚠️ 현재 {total_h}시간입니다. 24시간을 맞춰주세요!")
    else:
        # --- 계산 로직 ---
        bmr = 370 + (21.6 * muscle)
        met_val = (sleep*1.0 + office*1.5 + walking*2.5 + labor*4.5 + workout*6.5 + etc*2.0)
        tdee = bmr * (met_val / 24)

        # 목표별 설정
        goals = {
            "감량 (체지방 감소 중심)": -500,
            "유지 (체중 유지 및 리컴포지션)": 0,
            "린벌크 (지방 최소화, 근육 증가)": 200,
            "벌크 (빠른 체중 및 근력 증가)": 500
        }
        
        st.markdown("---")
        st.subheader("📋 목표별 맞춤 영양 설계표")
        
        for goal_name, offset in goals.items():
            target_kcal = tdee + offset
            if is_cheating: target_kcal += 300
            
            p_g = weight * prot_ratio
            f_g = (target_kcal * fat_percent) / 9
            c_g = (target_kcal - (p_g * 4 + f_g * 9)) / 4
            
            # 비율 계산
            p_p = (p_g * 4 / target_kcal) * 100
            f_p = (f_g * 9 / target_kcal) * 100
            c_p = (c_g * 4 / target_kcal) * 100

            with st.expander(f"📍 {goal_name}", expanded=(offset == -500)):
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("칼로리", f"{int(target_kcal)} kcal")
                c2.metric("탄수화물", f"{int(c_g)}g", f"{int(c_p)}%")
                c3.metric("단백질", f"{int(p_g)}g", f"{int(p_p)}%")
                c4.metric("지방", f"{int(f_g)}g", f"{int(f_p)}%")

        # --- 현재 상태 기반 추천 문장 ---
        st.markdown("---")
        st.subheader("💡 AI 맞춤 코칭 메시지")
        bmi_simple = weight / ((1.75)**2) # 평균 키 가정 예시
        if muscle / weight < 0.4:
            st.info("📢 현재 근육량 대비 체중이 높습니다. **'감량'**을 통해 체지방을 먼저 걷어내는 것을 추천합니다.")
        else:
            st.success("📢 근육량이 훌륭합니다! **'린벌크'**를 통해 근성장을 노려보기에 아주 좋은 상태입니다.")

        # --- 가이드 섹션 (카드 형태) ---
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("""
            <div style="background-color:#f0f2f6; padding:15px; border-radius:10px;">
            <h4>📈 체중 변화 가이드</h4>
            <ul>
                <li>주당 0.25~0.5kg 증가: <b>정상</b></li>
                <li>1kg 이상 급격한 증가: <b>칼로리 과다</b></li>
                <li>변화 없음: <b>칼로리 부족</b></li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col_g2:
            st.markdown("""
            <div style="background-color:#e8f4ea; padding:15px; border-radius:10px;">
            <h4>🍴 식단 적용 팁</h4>
            <ul>
                <li>단백질은 하루 <b>3~5끼</b>로 나누어 섭취</li>
                <li>탄수화물은 <b>운동 전후</b>에 집중 배치</li>
                <li>지방은 견과류, 오일 등 양질의 급원 선택</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

        st.warning("⚠️ **주의:** 본 계산은 평균값이며 개인의 소화 흡수율과 활동 강도에 따라 차이가 발생할 수 있습니다. 2주간 체중 변화를 모니터링하며 조정하세요.")

if __name__ == "__main__":
    main()