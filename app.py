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
        # 컬럼이 없는 경우 대비(에러 방지)
        if '별점' not in df.columns:
            df['별점'] = 3
        return df
    else:
        return pd.DataFrame(columns=['날짜', '책 제목', '별점'])

# 2. 데이터 파일 통째로 저장하기
def save_dataframe(df):
    df.to_csv(CSV_FILE, index=False)

# --- 웹앱 화면 구성 (UI) ---

st.title("📚 나의 독서 기록장")

# === 사이드바: 입력 공간 ===
st.sidebar.header("새로운 책 기록하기")

# 날짜, 제목, 별점 입력
read_date = st.sidebar.date_input("읽은 날짜", datetime.now())
book_title = st.sidebar.text_input("책 제목")
rating = st.sidebar.slider("별점", 1, 5, 5)

# 추가 버튼
if st.sidebar.button("기록 추가"):
    if book_title:
        # 기존 데이터 불러와서 한 줄 추가
        df = load_data()
        new_row = pd.DataFrame({
            '날짜': [str(read_date)], 
            '책 제목': [book_title], 
            '별점': [rating]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        save_dataframe(df) # 저장
        
        st.sidebar.success(f"'{book_title}' 저장 완료!")
        st.rerun() # 화면 새로고침 (즉시 반영)
    else:
        st.sidebar.warning("책 제목을 입력해주세요!")

# === 메인 화면: 리스트 및 삭제 ===

st.subheader("📖 내가 읽은 책 목록")
st.write("지우고 싶은 책을 체크(✅)하고 아래 삭제 버튼을 누르세요.")

df = load_data()

if not df.empty:
    # 날짜 기준 내림차순 정렬 (최신순)
    df = df.sort_values(by='날짜', ascending=False).reset_index(drop=True)

    # 삭제 선택을 위한 체크박스 컬럼 추가 (기본값 False)
    df.insert(0, "삭제", False)

    # 데이터 에디터로 출력 (체크박스 기능 활성화)
    edited_df = st.data_editor(
        df,
        column_config={
            "삭제": st.column_config.CheckboxColumn(
                "삭제 선택",
                help="삭제할 항목을 선택하세요",
                default=False,
                width="small"
            ),
            "날짜": st.column_config.TextColumn("읽은 날짜"),
            "책 제목": st.column_config.TextColumn("도서명"),
            "별점": st.column_config.NumberColumn(
                "평점",
                format="%d점" # 숫자 뒤에 '점' 표시
            )
        },
        disabled=["날짜", "책 제목", "별점"], # 다른 컬럼은 수정 못하게 막음
        hide_index=True,
        use_container_width=True
    )

    # 삭제 버튼
    if st.button("선택한 항목 삭제하기", type="primary"):
        # '삭제' 체크박스가 False인(체크 안 된) 데이터만 남기기
        rows_to_keep = edited_df[edited_df['삭제'] == False]
        
        # 실제로 삭제된 항목이 있는지 확인
        if len(rows_to_keep) < len(edited_df):
            # '삭제' 임시 컬럼은 저장하지 않으므로 제거
            rows_to_keep = rows_to_keep.drop(columns=['삭제'])
            
            # 파일에 저장
            save_dataframe(rows_to_keep)
            
            st.success("선택한 책이 삭제되었습니다.")
            st.rerun() # 화면 새로고침
        else:
            st.warning("삭제할 책을 먼저 선택해주세요.")

else:
    st.info("아직 기록된 책이 없습니다.")

