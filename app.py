import streamlit as st
import pandas as pd

# [설정] 페이지 제목 및 레이아웃
st.set_page_config(page_title="25kg 감량 성공자의 실전 계산기", layout="centered")

def main():
    st.title("🏆 목표별 통합 영양 설계 시스템")
    st.info("💡 **시간 입력 팁:** 1.0 = 1시간 / 0.5 = 30분입니다.") 
    st.markdown("---")

    # 1. 사용자 신체 정보 (사이드바)
    with st.sidebar:
        st.header("👤 나의 신체 정보")
        weight = st.number_input("현재 체중 (kg)", value=87.8, step=0.1)
        muscle = st.number_input("골격근량 (kg)", value=37.0, step=0.1)
        
        st.markdown("---")
        st.header("🥩 영양 전략 설정")
        protein_factor = st.select_slider(
            "단백질 섭취 강도 (체중 1kg당)",
            options=[1.6, 1.8, 2.0, 2.2, 2.5],
            value=2.0,
            help="린매스업이나 벌크업 시에는 2.0 이상을 권장합니다."
        )
        
        is_cheating = st.checkbox("🔥 오늘은 '치팅데이'인가요?")

    # 2. 24시간 활동량 입력
    st.subheader("⏰ 오늘 나의 24시간 활동량")
    col1, col2 = st.columns(2)
    with col1:
        sleep = st.slider("수면 (시간)", 0.0, 15.0, 7.0, 0.5)
        office = st.slider("좌식 생활 (사무/운전/공부)", 0.0, 15.0, 0.0, 0.5)
        walking = st.slider("가벼운 활동 (출퇴근/이동/집안일)", 0.0, 15.0, 3.5, 0.5)
    with col2:
        manual_labor = st.slider("고강도 활동 (현장작업/상하차)", 0.0, 15.0, 8.0, 0.5)
        workout = st.slider("고강도 웨이트 트레이닝 (운동)", 0.0, 4.0, 1.5, 0.5)
        etc = st.slider("기타 (식사/샤워/휴식)", 0.0, 15.0, 4.0, 0.5)

    total_h = sleep + office + walking + manual_labor + workout + etc

    if total_h != 24:
        st.warning(f"⚠️ 현재 시간 합계가 {total_h}시간입니다. 24시간을 맞춰주세요!")
    else:
        bmr = 370 + (21.6 * muscle)
        met_total = (sleep*1.0 + office*1.5 + walking*2.5 + manual_labor*4.5 + workout*6.5 + etc*2.0)
        tdee = bmr * (met_total / 24)

        def calc_macros(target_kcal, w, p_factor):
            p = w * p_factor
            f = (target_kcal * 0.25) / 9
            c = (target_kcal - (p * 4 + f * 9)) / 4
            return int(target_kcal), int(c), int(p), int(f)

        results = []
        if is_cheating:
            results.append(["🔥 치팅데이 (대사 회복)", *calc_macros(tdee, weight, protein_factor)])
        else:
            results.append(["🎯 지방 컷팅 (-500kcal)", *calc_macros(tdee - 500, weight, protein_factor)])
            results.append(["⚖️ 현재 유지 (건강 관리)", *calc_macros(tdee, weight, protein_factor)])
            results.append(["🥗 린매스업 (+200kcal)", *calc_macros(tdee + 200, weight, protein_factor)]) # 린매스업 추가
            results.append(["💪 근성장 벌크업 (+500kcal)", *calc_macros(tdee + 500, weight, protein_factor)]) # 벌크업 칼로리 상향

        df = pd.DataFrame(results, columns=["목표 구분", "총 칼로리(kcal)", "탄수화물(g)", "단백질(g)", "지방(g)"])

        st.markdown("---")
        st.subheader("📋 목표별 통합 영양 설계표")
        st.table(df)

        st.success(f"✅ 설정된 단백질 강도: **체중 당 {protein_factor}g**")
        st.info(f"💡 린매스업은 깨끗한 탄수화물을 정해진 양만큼만 드시는 게 핵심입니다!")

if __name__ == "__main__":
    main()