import streamlit as st
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 한글 폰트 설정 (Windows 기본 폰트인 맑은 고딕)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 앱 전체 화면 넓게 쓰기
st.set_page_config(page_title="가족 바이오리듬 앱", layout="wide")

st.title("👨‍👩‍👦 우리 가족 바이오리듬 앱")
st.write("원하시는 조회 기간을 아래 달력에서 직접 선택해 보세요. (그래프가 자동으로 업데이트됩니다)")

# 💡 날짜 선택 달력 UI 추가
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("🗓️ 조회 시작일", datetime.date(2026, 9, 29))
with col2:
    end_date = st.date_input("🗓️ 조회 종료일", datetime.date(2026, 11, 29))

st.markdown("---")

# 종료일이 시작일보다 빠르면 안내 메시지 출력
if start_date >= end_date:
    st.error("종료일이 시작일보다 빠르거나 같습니다. 날짜를 다시 설정해 주세요.")
else:
    # 가족 생년월일 설정
    birthdays = {
        '본인 (아버님)': datetime.date(1971, 2, 21),
        '부인 (어머님)': datetime.date(1973, 12, 17),
        '자녀 (수험생)': datetime.date(2006, 8, 22)
    }

    days_diff = (end_date - start_date).days + 1
    dates = [start_date + datetime.timedelta(days=i) for i in range(days_diff)]

    cycles = {'신체': 23, '감성': 28, '지성': 33}
    colors = {'신체': '#d62728', '감성': '#2ca02c', '지성': '#1f77b4'}

    fig, axes = plt.subplots(3, 1, figsize=(12, 14), sharex=True)
    fig.suptitle(f'가족 바이오리듬 그래프\n({start_date} ~ {end_date})', fontsize=20, fontweight='bold', color='#2b4f81')

    for ax, (person, bday) in zip(axes, birthdays.items()):
        t = np.array([(d - bday).days for d in dates])
        
        physical = np.sin(2 * np.pi * t / cycles['신체']) * 100
        emotional = np.sin(2 * np.pi * t / cycles['감성']) * 100
        intellectual = np.sin(2 * np.pi * t / cycles['지성']) * 100
        
        ax.plot(dates, physical, color=colors['신체'], linewidth=2.5, label='신체 (23일 주기)')
        ax.plot(dates, emotional, color=colors['감성'], linewidth=2.5, label='감성 (28일 주기)')
        ax.plot(dates, intellectual, color=colors['지성'], linewidth=2.5, label='지성 (33일 주기)')
        
        ax.axhline(0, color='black', linewidth=1)
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        ax.set_ylim(-110, 110)
        ax.set_title(f'[{person}] ({bday.year}년 {bday.month}월 {bday.day}일생)', loc='left', pad=15, fontsize=14, fontweight='bold')
        
        # 수능일(11.19) 강조 수직선 (선택한 기간 안에 수능일이 있을 때만 표시되도록 수정)
        csat_date = datetime.date(2026, 11, 19)
        if start_date <= csat_date <= end_date:
            ax.axvline(csat_date, color='orange', linestyle=':', linewidth=2)
            ax.text(csat_date, 105, '수능일', color='orange', fontweight='bold', ha='center', va='bottom', bbox=dict(facecolor='white', edgecolor='none', alpha=0.8))

    # X축 간격 자동 조절 (몇 달 치를 한 번에 봐도 글자가 안 겹치도록 개선)
    interval = max(1, days_diff // 15)
    axes[-1].xaxis.set_major_locator(mdates.DayLocator(interval=interval))
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    axes[-1].set_xlabel('날짜', fontsize=12)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, 0.02), fontsize=12)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9, bottom=0.1)

    # 완성된 그래프를 웹 화면에 출력
    st.pyplot(fig)