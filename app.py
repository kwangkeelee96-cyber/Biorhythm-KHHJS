import streamlit as st
import datetime
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 앱 전체 화면 넓게 쓰기
st.set_page_config(page_title="가족 바이오리듬 앱", layout="wide")

st.title("👨‍👩‍👧‍👦 우리 가족 바이오리듬 앱")
st.write("원하시는 조회 기간을 아래 달력에서 직접 선택해 보세요.")
st.info("💡 **스마트폰 이용 팁**: 그래프 안에서 두 손가락으로 확대/축소(핀치줌) 하거나, 옆으로 밀어서 이동해 보세요! 특정 날짜를 터치하면 정확한 수치도 볼 수 있습니다.")

# 날짜 선택 달력 UI
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("🗓️ 조회 시작일", datetime.date(2026, 10, 01))
with col2:
    end_date = st.date_input("🗓️ 조회 종료일", datetime.date(2026, 11, 30))

st.markdown("---")

if start_date >= end_date:
    st.error("종료일이 시작일보다 빠르거나 같습니다. 날짜를 다시 설정해 주세요.")
else:
    # 1. 가족 5명 생년월일 순서대로 설정
    birthdays = {
        '본인 (아버님)': datetime.date(1971, 2, 21),
        '부인 (어머님)': datetime.date(1973, 12, 17),
        '자녀H': datetime.date(2001, 6, 5),
        '자녀J': datetime.date(2003, 9, 4),
        '자녀S': datetime.date(2006, 8, 22)
    }

    days_diff = (end_date - start_date).days + 1
    dates = [start_date + datetime.timedelta(days=i) for i in range(days_diff)]

    cycles = {'신체': 23, '감성': 28, '지성': 33}
    colors = {'신체': '#d62728', '감성': '#2ca02c', '지성': '#1f77b4'}

    # 2. 프리미엄 반응형 차트(Plotly) 서브플롯 생성
    titles = [f"[{person}] ({bday.year}년 {bday.month}월 {bday.day}일생)" for person, bday in birthdays.items()]
    fig = make_subplots(rows=len(birthdays), cols=1, subplot_titles=titles, vertical_spacing=0.04)

    for i, (person, bday) in enumerate(birthdays.items(), start=1):
        t = np.array([(d - bday).days for d in dates])
        
        physical = np.sin(2 * np.pi * t / cycles['신체']) * 100
        emotional = np.sin(2 * np.pi * t / cycles['감성']) * 100
        intellectual = np.sin(2 * np.pi * t / cycles['지성']) * 100
        
        # 선 그리기 및 터치 시 점수(%) 팝업 설정
        fig.add_trace(go.Scatter(x=dates, y=physical, mode='lines', name='신체(23일)', line=dict(color=colors['신체'], width=2.5), hovertemplate="%{y:.0f}점", showlegend=(i==1)), row=i, col=1)
        fig.add_trace(go.Scatter(x=dates, y=emotional, mode='lines', name='감성(28일)', line=dict(color=colors['감성'], width=2.5), hovertemplate="%{y:.0f}점", showlegend=(i==1)), row=i, col=1)
        fig.add_trace(go.Scatter(x=dates, y=intellectual, mode='lines', name='지성(33일)', line=dict(color=colors['지성'], width=2.5), hovertemplate="%{y:.0f}점", showlegend=(i==1)), row=i, col=1)

        # 기준선 (0)
        fig.add_hline(y=0, line_color='black', line_width=1, row=i, col=1)

        # 수능일(11.19) 수직선
        csat_date = datetime.date(2026, 11, 19)
        if start_date <= csat_date <= end_date:
            fig.add_vline(x=csat_date, line_width=2, line_dash='dot', line_color='orange', row=i, col=1)
            fig.add_annotation(x=csat_date, y=100, text="수능일", showarrow=False, font=dict(color="orange", size=13), bgcolor="rgba(255,255,255,0.8)", row=i, col=1)

        # Y축 범위 및 모든 차트 하단에 날짜 형식 표시
        fig.update_yaxes(range=[-110, 110], row=i, col=1)
        fig.update_xaxes(tickformat="%m/%d", row=i, col=1)

    # 3. 전체 레이아웃 설정
    fig.update_layout(
        height=1600, # 5명 가족이 넉넉하게 보이도록 전체 높이 조정
        hovermode="x unified", # 날짜 터치 시 3가지 바이오리듬 점수 한 번에 표시
        legend=dict(orientation="h", yanchor="bottom", y=-0.04, xanchor="center", x=0.5),
        margin=dict(t=50, b=50, l=30, r=30)
    )

    # 완성된 반응형 차트를 웹 화면에 출력 (가로 크기 자동 맞춤)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
