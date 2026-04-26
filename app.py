import streamlit as st

# [설정] 페이지 제목 및 레이아웃
st.set_page_config(page_title="25kg 감량 성공자의 실전 계산기", layout="centered")

def main():
    st.title("🏆 전 직종 맞춤형 영양 설계 시스템")
    st.write("25kg 감량 성공자가 직접 설계한 **실전용 탄/단/지 계산기**입니다.")
    st.markdown("---")

    # 1. 사용자 신체 정보 (사이드바)
    with st.sidebar:
        st.header("👤 나의 신체 정보")
        weight = st.number_input("현재 체중 (kg)", value=80.0, step=0.1)
        muscle = st.number_input("골격근량 (kg)", value=37.0, step=0.1)
        st.markdown("---")
        is_cheating = st.checkbox("🔥 오늘은 '치팅데이'인가요? (2주 1회)")

    # 2. 24시간 활동량 정밀 입력 (모든 항목 0.5시간 단위로 수정)
    st.subheader("⏰ 오늘 나의 24시간 (라이프스타일)")
    st.caption("모든 활동은 0.5(30분) 단위로 입력 가능합니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        sleep = st.slider("수면 (시간)", 0.0, 15.0, 7.0, 0.5)
        office = st.slider("좌식 생활 (사무/운전/공부)", 0.0, 15.0, 8.0, 0.5)
        walking = st.slider("가벼운 활동 (출퇴근/이동/집안일)", 0.0, 15.0, 4.0, 0.5)
    with col2:
        manual_labor = st.slider("고강도 활동 (현장작업/기계수리/상하차)", 0.0, 15.0, 0.0, 0.5)
        workout = st.slider("고강도 웨이트 트레이닝 (운동)", 0.0, 4.0, 1.0, 0.5)
        etc = st.slider("기타 (식사/샤워/휴식)", 0.0, 15.0, 4.0, 0.5)

    total_h = sleep + office + walking + manual_labor + workout + etc

    if total_h != 24:
        st.warning(f"⚠️ 현재 시간 합계가 {total_h}시간입니다. 24시간을 맞춰주세요!")
    else:
        bmr = 370 + (21.6 * muscle)
        met_total = (sleep*1.0 + office*1.5 + walking*2.5 + manual_labor*4.5 + workout*6.5 + etc*2.0)
        tdee = bmr * (met_total / 24)

        if is_cheating:
            target_kcal = tdee + 300
            msg = "🎊 오늘은 즐거운 치팅데이! 점심 한 끼는 원하는 메뉴를 즐기세요."
        else:
            target_kcal = tdee - 500
            msg = "🎯 확실한 감량을 위해 아래 영양 성분을 꼭 지켜주세요!"

        protein_g = weight * 2.0
        fat_g = (target_kcal * 0.2) / 9
        carb_g = (target_kcal - (protein_g * 4 + fat_g * 9)) / 4

        st.markdown("---")
        st.success(msg)
        
        res1, res2, res3 = st.columns(3)
        res1.metric("단백질 (Protein)", f"{int(protein_g)}g")
        res2.metric("탄수화물 (Carbs)", f"{int(carb_g)}g")
        res3.metric("지방 (Fat)", f"{int(fat_g)}g")
        
        st.info(f"💡 오늘 나의 총 섭취 권장량: **{int(target_kcal)} kcal**")

if __name__ == "__main__":
    main()