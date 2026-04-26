import streamlit as st

# [설정] 페이지 제목 및 레이아웃
st.set_page_config(page_title="25kg 감량 성공자의 실전 계산기", layout="centered")

def main():
    st.title("🏆 전 직종 맞춤형 영양 설계 시스템")
    st.write("25kg 감량 성공자의 노하우가 담긴 **목표별 맞춤 식단 계산기**입니다.")
    st.markdown("---")

    # 1. 사용자 신체 정보 및 목표 (사이드바)
    with st.sidebar:
        st.header("👤 나의 정보 & 목표")
        weight = st.number_input("현재 체중 (kg)", value=66.0, step=0.1)
        muscle = st.number_input("골격근량 (kg)", value=30.0, step=0.1)
        
        st.markdown("---")
        # 🔥 목표 설정 추가
        goal = st.radio(
            "🎯 나의 현재 목표는?",
            ["체중 감량 (지방 컷팅)", "체중 유지 (건강 관리)", "벌크업 (근성장)"]
        )
        
        is_cheating = st.checkbox("🔥 오늘은 '치팅데이'인가요? (2주 1회)")

    # 2. 24시간 활동량 입력
    st.subheader("⏰ 오늘 나의 24시간")
    col1, col2 = st.columns(2)
    with col1:
        sleep = st.slider("수면 (시간)", 0.0, 15.0, 7.0, 0.5)
        office = st.slider("좌식 생활 (사무/운전/공부)", 0.0, 15.0, 8.0, 0.5)
        walking = st.slider("가벼운 활동 (출퇴근/이동/집안일)", 0.0, 15.0, 4.0, 0.5)
    with col2:
        manual_labor = st.slider("고강도 활동 (현장작업/상하차)", 0.0, 15.0, 0.0, 0.5)
        workout = st.slider("고강도 웨이트 트레이닝 (운동)", 0.0, 4.0, 1.0, 0.5)
        etc = st.slider("기타 (식사/샤워/휴식)", 0.0, 15.0, 4.0, 0.5)

    total_h = sleep + office + walking + manual_labor + workout + etc

    if total_h != 24:
        st.warning(f"⚠️ 현재 시간 합계가 {total_h}시간입니다. 24시간을 맞춰주세요!")
    else:
        # 기초대사량 및 활동대사량 계산
        bmr = 370 + (21.6 * muscle)
        met_total = (sleep*1.0 + office*1.5 + walking*2.5 + manual_labor*4.5 + workout*6.5 + etc*2.0)
        tdee = bmr * (met_total / 24)

        # 🎯 목표별 칼로리 조정 로직
        if is_cheating:
            target_kcal = tdee + 300
            msg = "🎊 오늘은 치팅데이! 점심은 자유롭게 드시고 대사를 끌어올리세요."
        elif goal == "체중 감량 (지방 컷팅)":
            target_kcal = tdee - 500
            msg = "🎯 지방을 태우는 중입니다! 단백질을 꼭 챙겨주세요."
        elif goal == "벌크업 (근성장)":
            target_kcal = tdee + 300
            msg = "💪 근성장을 위한 벌크업 모드! 충분한 에너지를 섭취하세요."
        else:
            target_kcal = tdee
            msg = "⚖️ 현재 상태를 유지하는 건강 식단 모드입니다."

        # 탄/단/지 배분 로직
        protein_g = weight * 2.0  # 단백질은 체중의 2배 고정
        fat_g = (target_kcal * 0.2) / 9 # 지방은 총 칼로리의 20%
        carb_g = (target_kcal - (protein_g * 4 + fat_g * 9)) / 4 # 나머지는 탄수화물

        st.markdown("---")
        st.success(msg)
        
        # 결과 표시
        res1, res2, res3 = st.columns(3)
        res1.metric("단백질 (Protein)", f"{int(protein_g)}g")
        res2.metric("탄수화물 (Carbs)", f"{int(carb_g)}g")
        res3.metric("지방 (Fat)", f"{int(fat_g)}g")
        
        st.info(f"💡 나의 목표별 총 섭취 권장량: **{int(target_kcal)} kcal** (평소보다 {'+300' if goal=='벌크업 (근성장)' else '-500' if goal=='체중 감량 (지방 컷팅)' else '0'} kcal)")

if __name__ == "__main__":
    main()