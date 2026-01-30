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
        # 파일이 없으면 빈 데이터프레임 생성
        return pd.DataFrame(columns=['날짜', '책 제목'])

# 2. 데이터 저장하기 함수
def save_data(date, title):
    df = load_data()
    new_data = pd.DataFrame({'날짜': [date], '책 제목': [title]})
    # 기존 데이터에 새로운 데이터 합치기
    df = pd.concat([df, new_data], ignore_index=True)
    # 파일로 저장
    df.to_csv(CSV_FILE, index=False)
    return df

# --- 웹앱 화면 구성 (UI) ---

st.title("📚 나의 독서 기록장")
st.write("읽은 책을 기록하고 날짜별로 정리해보세요.")

# 사이드바: 책 입력 공간
st.sidebar.header("새로운 책 기록하기")
book_title = st.sidebar.text_input("책 제목을 입력하세요")
add_button = st.sidebar.button("기록 추가")

# 버튼이 눌렸을 때의 동작
if add_button and book_title:
    today = datetime.now().strftime("%Y-%m-%d") # 오늘 날짜 (년-월-일)
    save_data(today, book_title)
    st.sidebar.success(f"'{book_title}'이(가) {today} 날짜로 저장되었습니다!")

# --- 메인 화면: 리스트 출력 ---

st.subheader("📖 내가 읽은 책 목록")

# 최신 데이터를 불러와서 보여주기
df = load_data()

if not df.empty:
    # 날짜 기준 내림차순 정렬 (최신순)
    df = df.sort_values(by='날짜', ascending=False)
    
    # 깔끔하게 표로 보여주기 (인덱스는 숨김)
    st.dataframe(
        df,
        column_config={
            "날짜": "읽은 날짜",
            "책 제목": "도서명"
        },
        use_container_width=True,

        hide_index=True
    # (선택사항) 통계 보여주기
    st.metric(label="총 읽은 책 권수", value=f"{len(df)}권")
else:
    st.info("아직 기록된 책이 없습니다. 왼쪽 사이드바에서 책을 추가해주세요!")
