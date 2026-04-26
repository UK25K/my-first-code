import streamlit as st

# [설정] 페이지 제목 및 레이아웃
st.set_page_config(page_title="25kg 감량 성공자의 실전 계산기", layout="centered")

def main():
    # --- 메인 프로그램 시작 ---
    st.title("🏆 전 직종 맞춤형 영양 설계 시스템")
    st.write("25kg 감량 성공자가 직접 설계한 **실전용 탄/단/지 계산기**입니다.")
    st.markdown("---")

    # 1. 사용자 신체 정보 (사이드바)
    with st.sidebar:
        st.header("👤 나의 신체 정보")
        weight = st.number_input("현재 체중 (kg)", value=70.0, step=0.1)
        muscle = st.number_input("골격근량 (kg)", value=30.0, step=0.1)
        st.info("💡 골격근량을 모르면 인바디 결과를 참고하세요.")
        
        st.markdown("---")
        # 선생님의 '2주 1회 점심 치팅' 노하우 반영
        is_cheating = st.checkbox("🔥 오늘은 '치팅데이'인가요? (2주 1회)")

    # 2. 24시간 활동량 정밀 입력
    st.subheader("⏰ 오늘 나의 24시간 (라이프스타일)")
    st.caption("사무직부터 현장직까지, 본인의 하루 일과에 맞춰 시간을 배분하세요.")
    
    col1, col2 = st.columns(2)
    with col1:
        sleep = st.slider("수면 (시간)", 0, 12, 7)
        office = st.slider("좌식 생활 (사무/운전/공부)", 0, 15, 8)
        walking = st.slider("가벼운 활동 (출퇴근/이동/집안일)", 0, 15, 4)
    with col2:
        manual_labor = st.slider("고강도 활동 (현장작업/기계수리/상하차)", 0, 15, 0)
        workout = st.slider("고강도 웨이트 트레이닝 (운동)", 0.0, 4.0, 1.0, 0.5)
        etc = st.slider("기타 (식사/샤워/휴식)", 0, 10, 4)

    total_h = sleep + office + walking + manual_labor + workout + etc

    # 24시간 합계 체크
    if total_h != 24:
        st.warning(f"⚠️ 현재 시간 합계가 {total_h}시간입니다. 24시간을 맞춰주셔야 정확한 계산이 가능합니다.")
    else:
        # --- 영양학 로직 (Katch-McArdle 공식) ---
        # 1. 기초대사량(BMR) 계산
        bmr = 370 + (21.6 * muscle)
        
        # 2. 활동소모량(MET 지수 적용)
        # 사무(1.5), 가벼운활동(2.5), 현장작업(4.5), 웨이트(6.5)
        met_total = (sleep*1.0 + office*1.5 + walking*2.5 + manual_labor*4.5 + workout*6.5 + etc*2.0)
        tdee = bmr * (met_total / 24)

        # 3. 목표 칼로리 설정
        if is_cheating:
            target_kcal = tdee + 300  # 치팅 시 대사 회복을 위해 약간의 잉여분
            msg = "🎊 오늘은 즐거운 치팅데이! 점심 한 끼는 원하는 메뉴를 즐기세요."
        else:
            target_kcal = tdee - 500  # 표준 감량 수치 (하루 -500kcal)
            msg = "🎯 확실한 감량을 위해 아래 영양 성분을 꼭 지켜주세요!"

        # 4. 탄/단/지 배분 (선생님의 실전 공식)
        protein_g = weight * 2.0  # 단백질: 체중 2배
        fat_g = (target_kcal * 0.2) / 9 # 지방: 총 칼로리의 20%
        carb_g = (target_kcal - (protein_g * 4 + fat_g * 9)) / 4 # 탄수화물: 잔여량 전체

        # 결과 발표
        st.markdown("---")
        st.success(msg)
        
        res1, res2, res3 = st.columns(3)
        res1.metric("단백질 (Protein)", f"{int(protein_g)}g")
        res2.metric("탄수화물 (Carbs)", f"{int(carb_g)}g")
        res3.metric("지방 (Fat)", f"{int(fat_g)}g")
        
        st.info(f"💡 오늘 나의 총 섭취 권장량: **{int(target_kcal)} kcal**")

        # 📢 실전 가이드 섹션
        st.markdown("---")
        st.subheader("💡 25kg 감량 성공자의 실전 코칭")
        st.write(f"✅ 오늘 단백질 **{int(protein_g)}g**은 닭가슴살 약 **{round(protein_g/23, 1)}팩** 분량입니다. (나눠서 섭취 권장)")
        st.write("✅ **닭가슴살 팁:** 제가 공유해드린 합리적 구매처와 비법 레시피를 활용해 지치지 않게 드세요.")
        
        if is_cheating:
            st.warning("⚠️ **주의:** 치팅은 반드시 **'점심 한 끼'**로 마무리하세요. 저녁까지 이어지면 안 됩니다!")
        else:
            st.write("✅ **활동량 팁:** 현장 작업이나 운동량이 많았던 날은 탄수화물을 조금 더 늘려도 괜찮습니다.")

if __name__ == "__main__":
    main()
