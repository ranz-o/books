import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 데이터 파일 경로 설정
CSV_FILE = 'books.csv'

# 1. 데이터 불러오기 함수
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=['날짜', '책 제목'])

# 2. 데이터 저장하기 함수
def save_data(date, title):
    df = load_data()
    # 날짜를 문자열로 변환하여 저장
    new_data = pd.DataFrame({'날짜': [str(date)], '책 제목': [title]})
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    return df

# --- 웹앱 화면 구성 (UI) ---

st.title("📚 나의 독서 기록장")
st.write("읽은 책을 기록하고 날짜별로 정리해보세요.")

# 사이드바: 입력 공간
st.sidebar.header("새로운 책 기록하기")

# [변경됨] 날짜 선택 기능 추가 (기본값은 오늘)
read_date = st.sidebar.date_input("읽은 날짜 선택", datetime.now())

# 책 제목 입력
book_title = st.sidebar.text_input("책 제목을 입력하세요")

# 버튼
add_button = st.sidebar.button("기록 추가")

# 버튼이 눌렸을 때의 동작
if add_button:
    if book_title:
        save_data(read_date, book_title)
        st.sidebar.success(f"'{book_title}'이(가) {read_date} 날짜로 저장되었습니다!")
    else:
        st.sidebar.warning("책 제목을 입력해주세요!")

# --- 메인 화면: 리스트 출력 ---

st.subheader("📖 내가 읽은 책 목록")

df = load_data()

if not df.empty:
    # 날짜 기준 내림차순 정렬 (최신순)
    df = df.sort_values(by='날짜', ascending=False)
    
    # 깔끔하게 표로 보여주기
    st.dataframe(
        df,
        column_config={
            "날짜": "읽은 날짜",
            "책 제목": "도서명"
        },
        use_container_width=True,
        hide_index=True
    )
    
    # 통계
    st.metric(label="총 읽은 책 권수", value=f"{len(df)}권")
else:
    st.info("아직 기록된 책이 없습니다. 왼쪽 사이드바에서 책을 추가해주세요!")
