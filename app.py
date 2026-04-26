import streamlit as st
import pandas as pd

# [설정] 페이지 제목 및 레이아웃
st.set_page_config(page_title="25kg 감량 성공자의 실전 계산기", layout="centered")

def main():
    st.title("🏆 목표별 통합 영양 설계 시스템")
    st.write("25kg 감량 성공자의 실전 노하우: **단 한 번의 입력으로 모든 목표치를 확인하세요.**")
    st.markdown("---")

    # 1. 사용자 신체 정보 (사이드바)
    with st.sidebar:
        st.header("👤 나의 신체 정보")
        weight = st.number_input("현재 체중 (kg)", value=66.0, step=0.1)
        muscle = st.number_input("골격근량 (kg)", value=30.0, step=0.1)
        st.markdown("---")
        is_cheating = st.checkbox("🔥 오늘은 '치팅데이'인가요?")
        if is_cheating:
            st.error("⚠️ 치팅은 '유지 칼로리' 내에서 점심 한 끼만 권장합니다!")

    # 2. 24시간 활동량 입력
    st.subheader("⏰ 오늘 나의 24시간 활동량")
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

        # 데이터 계산 함수
        def calc_macros(target_kcal, w):
            p = w * 2.0
            f = (target_kcal * 0.2) / 9
            c = (target_kcal - (p * 4 + f * 9)) / 4
            return int(target_kcal), int(c), int(p), int(f)

        # 결과 데이터 생성
        results = []
        if is_cheating:
            results.append(["🔥 치팅데이 (대사 회복)", *calc_macros(tdee, weight)])
        else:
            results.append(["🎯 지방 컷팅 (-500kcal)", *calc_macros(tdee - 500, weight)])
            results.append(["⚖️ 현재 유지 (건강 관리)", *calc_macros(tdee, weight)])
            results.append(["💪 근성장 벌크업 (+300kcal)", *calc_macros(tdee + 300, weight)])

        # 표(DataFrame) 생성
        df = pd.DataFrame(results, columns=["목표 구분", "총 칼로리(kcal)", "탄수화물(g)", "단백질(g)", "지방(g)"])

        st.markdown("---")
        st.subheader("📋 목표별 영양 섭취 가이드라인")
        st.table(df) # 표 형태로 깔끔하게 출력

        # 실전 팁
        st.info(f"💡 오늘 단백질 목표는 **{int(weight * 2.0)}g**입니다. (닭가슴살 약 {round((weight*2.0)/23, 1)}팩 분량)")
        if not is_cheating:
            st.success("위 표에서 본인의 현재 목표에 맞는 행을 확인하여 식단에 적용하세요!")

if __name__ == "__main__":
    main()