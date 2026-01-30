import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 데이터 파일 경로 설정
CSV_FILE = 'books.csv'

# 1. 데이터 불러오기 함수
def load_data():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        # 기존 파일에 '별점' 컬럼이 없다면(옛날 데이터라면) 추가해줌 (에러 방지)
        if '별점' not in df.columns:
            df['별점'] = 3 # 기본값 3점 부여
        return df
    else:
        # 파일이 없으면 3개 컬럼으로 생성
        return pd.DataFrame(columns=['날짜', '책 제목', '별점'])

# 2. 데이터 저장하기 함수 (별점 인자 추가)
def save_data(date, title, rating):
    df = load_data()
    # 새로운 데이터 생성
    new_data = pd.DataFrame({
        '날짜': [str(date)], 
        '책 제목': [title],
        '별점': [rating]
    })
    # 기존 데이터에 합치기
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    return df

# --- 웹앱 화면 구성 (UI) ---

st.title("📚 나의 독서 기록장")
st.write("읽은 책을 날짜, 별점과 함께 기록해보세요.")

# 사이드바: 입력 공간
st.sidebar.header("새로운 책 기록하기")

# 1. 날짜 선택
read_date = st.sidebar.date_input("읽은 날짜", datetime.now())

# 2. 책 제목 입력
book_title = st.sidebar.text_input("책 제목")

# 3. [추가됨] 별점 슬라이더 (1점 ~ 5점)
rating = st.sidebar.slider("별점", min_value=1, max_value=5, value=5)

# 4. 저장 버튼
add_button = st.sidebar.button("기록 추가")

# 버튼 동작
if add_button:
    if book_title:
        save_data(read_date, book_title, rating)
        # 별 개수만큼 이모지 생성 (예: 5 -> ⭐⭐⭐⭐⭐)
        star_display = "⭐" * rating
        st.sidebar.success(f"'{book_title}' ({star_display}) 저장 완료!")
    else:
        st.sidebar.warning("책 제목을 입력해주세요!")

# --- 메인 화면: 리스트 출력 ---

st.subheader("📖 내가 읽은 책 목록")

df = load_data()

if not df.empty:
    # 날짜 기준 내림차순 정렬 (최신순)
    df = df.sort_values(by='날짜', ascending=False)

    # [시각화] 숫자로 저장된 별점을 이모지로 변환해서 보여주기 위한 복사본 생성
    display_df = df.copy()
    display_df['별점'] = display_df['별점'].apply(lambda x: "⭐" * int(x))

    # 표 출력
    st.dataframe(
        display_df,
        column_config={
            "날짜": "읽은 날짜",
            "책 제목": "도서명",
            "별점": "평점"
        },
        use_container_width=True,
        hide_index=True
    )
    
    # 통계 (총 읽은 권수)
    st.metric(label="총 읽은 책 권수", value=f"{len(df)}권")
else:
    st.info("아직 기록된 책이 없습니다. 왼쪽 사이드바에서 책을 추가해주세요!")
