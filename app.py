import streamlit as st
import datetime
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 앱 전체 화면 넓게 쓰기
st.set_page_config(page_title="가족 바이오리듬 앱", layout="wide")

st.title("👨‍👩‍👧‍👦 우리 가족 바이오리듬 앱")
st.write("원하시는 조회 기간을 아래 달력에서 직접 선택해 보세요.")
st.info("💡 **스마트폰 이용 팁**: 특정 날짜의 그래프 선을 가볍게 터치하면 정확한 수치를 볼 수 있습니다. (화면을 편하게 내리실 수 있도록 그래프 확대/축소 기능은 잠가두었습니다)")

# 접속한 '오늘' 날짜를 기준으로 앞뒤 한 달(30일) 자동 세팅
today = datetime.date.today()
default_start = today - datetime.timedelta(days=30)
default_end = today + datetime.timedelta(days=30)

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("🗓️ 조회 시작일", default_start)
with col2:
    end_date = st.date_input("🗓️ 조회 종료일", default_end)

st.markdown("---")

if start_date >= end_date:
    st.error("종료일이 시작일보다 빠르거나 같습니다. 날짜를 다시 설정해 주세요.")
else:
    # 가족 5명 생년월일 순서대로 설정
    birthdays = {
        '본인 (아버님)': datetime.date(1971, 2, 21),
        '부인 (어머님)': datetime.date(1973, 12, 17),
        '자녀H': datetime.date(2001, 6, 5),
        '자녀J': datetime.date(2003, 9, 4),
        '자녀S (수험생)': datetime.date(2006, 8, 22)
    }

    days_diff = (end_date - start_date).days + 1
    dates = [start_date + datetime.timedelta(days=i) for i in range(days_diff)]

    cycles = {'신체': 23, '감성': 28, '지성': 33}
    colors = {'신체': '#d62728', '감성': '#2ca02c', '지성': '#1f77b4'}

    titles = [f"[{person}] ({bday.year}년 {bday.month}월 {bday.day}일생)" for person, bday in birthdays.items()]
    fig = make_subplots(rows=len(birthdays), cols=1, subplot_titles=titles, vertical_spacing=0.04)

    for i, (person, bday) in enumerate(birthdays.items(), start=1):
        t = np.array([(d - bday).days for d in dates])
        
        physical = np.sin(2 * np.pi * t / cycles['신체']) * 100
        emotional = np.sin(2 * np.pi * t / cycles['감성']) * 100
        intellectual = np.sin(2 * np.pi * t / cycles['지성']) * 100
        
        fig.add_trace(go.Scatter(x=dates, y=physical, mode='lines', name='신체(23일)', line=dict(color=colors['신체'], width=2.5), hovertemplate="%{y:.0f}점", showlegend=(i==1)), row=i, col=1)
        fig.add_trace(go.Scatter(x=dates, y=emotional, mode='lines', name='감성(28일)', line=dict(color=colors['감성'], width=2.5), hovertemplate="%{y:.0f}점", showlegend=(i==1)), row=i, col=1)
        fig.add_trace(go.Scatter(x=dates, y=intellectual, mode='lines', name='지성(33일)', line=dict(color=colors['지성'], width=2.5), hovertemplate="%{y:.0f}점", showlegend=(i==1)), row=i, col=1)

        fig.add_hline(y=0, line_color='black', line_width=1, row=i, col=1)

        if start_date <= today <= end_date:
            fig.add_vline(x=today, line_width=1.5, line_dash='dash', line_color='gray', row=i, col=1)
            fig.add_annotation(x=today, y=-95, text="오늘", showarrow=False, font=dict(color="gray", size=12), bgcolor="rgba(255,255,255,0.8)", row=i, col=1)

        csat_date = datetime.date(2026, 11, 19)
        if start_date <= csat_date <= end_date:
            fig.add_vline(x=csat_date, line_width=2, line_dash='dot', line_color='orange', row=i, col=1)
            fig.add_annotation(x=csat_date, y=100, text="수능일", showarrow=False, font=dict(color="orange", size=13), bgcolor="rgba(255,255,255,0.8)", row=i, col=1)

        # 💡 핵심 해결책: 스크롤 시 그래프가 망가지지 않도록 위아래(Y축)와 좌우(X축)를 단단히 고정(Lock)
        fig.update_yaxes(range=[-110, 110], fixedrange=True, row=i, col=1)
        fig.update_xaxes(tickformat="%m/%d", fixedrange=True, row=i, col=1)

    # 💡 핵심 해결책 2: 차트의 드래그(이동/확대) 모드를 완전히 끄고 화면 스크롤에 양보
    fig.update_layout(
        height=1600,
        hovermode="x unified",
        dragmode=False, 
        legend=dict(orientation="h", yanchor="bottom", y=-0.04, xanchor="center", x=0.5),
        margin=dict(t=50, b=50, l=30, r=30)
    )

    # 완성된 차트를 웹 화면에 출력
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
