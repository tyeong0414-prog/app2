import streamlit as st
import datetime

# Page Configuration
st.set_page_config(page_title="우리 둘만의 다이어리", page_icon="❤️", layout="centered")

# Custom CSS for compact layout & modern styling
st.markdown("""
    <style>
        /* Hide standard padding & header */
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 1rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 480px;
        }
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Compact typography */
        h3 {
            font-size: 1.3rem !important;
            margin-bottom: 0.2rem !important;
            text-align: center;
        }
        .caption-text {
            font-size: 0.8rem;
            color: #888;
            text-align: center;
            margin-bottom: 0.8rem;
        }
        
        /* Diary card styling */
        .diary-card {
            background-color: #FFF5F5;
            border-radius: 12px;
            padding: 12px;
            margin-bottom: 8rem;
            border: 1px solid #FFE3E3;
        }
        .diary-header {
            display: flex;
            justify-content: space-between;
            font-weight: bold;
            font-size: 0.95rem;
            margin-bottom: 4rem;
            color: #D9480E;
        }
        .diary-body {
            font-size: 0.9rem;
            line-height: 1.4;
            color: #333;
            white-space: pre-wrap;
        }
        .empty-card {
            background-color: #F8F9FA;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            color: #ADB5BD;
            font-size: 0.85rem;
            border: 1px dashed #DEE2E6;
        }
        
        /* Streamlit UI tweaks */
        .stSelectbox label, .stTextArea label, .stTextInput label {
            font-size: 0.85rem !important;
            font-weight: 600;
        }
        div[data-baseweb="select"] > div {
            min-height: 38px;
        }
        .stButton button {
            width: 100%;
            border-radius: 8px;
            height: 40px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "diaries" not in st.session_state:
    st.session_state.diaries = {
        "User1": {"mood": "🥰 설렘", "text": "오늘 같이 카페 가서 공부하니까 너무 좋았어! 내일도 같이 맛있는 거 먹자 ❤️", "date": "2026-11-01", "read": False},
        "User2": {"mood": "😴 피곤", "text": "과제가 많아서 조금 힘들었지만 그래도 얼굴 봐서 힘났어 푹 자!", "date": "2026-11-01", "read": True}
    }

# Title & User Switcher
st.markdown("### ❤️ 커플 모바일 다이어리")
st.markdown("<div class='caption-text'>스마트폰 한 화면에서 서로의 일기를 나눠보세요</div>", unsafe_allow_html=True)

user_col1, user_col2 = st.columns([1, 1])
with user_col1:
    current_user = st.radio("👤 작성자 선택", ["나 (User1)", "상대방 (User2)"], horizontal=True, label_visibility="collapsed")

user_key = "User1" if "User1" in current_user else "User2"
partner_key = "User2" if user_key == "User1" else "User1"

# Main 2-Column Compact Layout
col_write, col_read = st.columns(2)

# Left Column: Write Diary
with col_write:
    st.markdown("**✍️ 오늘 내 일기 작성**")
    mood = st.selectbox(
        "오늘의 기분",
        ["🥰 설렘", "😊 행복", "🥹 감동", "😴 피곤", "🥺 속상"],
        label_visibility="collapsed"
    )
    diary_text = st.text_area(
        "일기 내용",
        placeholder="오늘 하루는 어땠나요?",
        height=100,
        label_visibility="collapsed"
    )
    
    if st.button("💌 저장하기", type="primary"):
        if diary_text.strip():
            st.session_state.diaries[user_key] = {
                "mood": mood,
                "text": diary_text,
                "date": datetime.date.today().strftime("%m/%d"),
                "read": False
            }
            st.toast("일기가 등록되었습니다!", icon="🎉")
            st.rerun()
        else:
            st.toast("내용을 입력해 주세요!", icon="⚠️")

# Right Column: Read Partner's Diary
with col_read:
    st.markdown("**💌 상대방 일기 확인**")
    partner_diary = st.session_state.diaries.get(partner_key)
    
    if partner_diary and partner_diary["text"]:
        st.markdown(f"""
            <div class="diary-card">
                <div class="diary-header">
                    <span>{partner_diary['mood']}</span>
                    <span>{partner_diary['date']}</span>
                </div>
                <div class="diary-body">{partner_diary['text']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Read Confirmation Checkbox
        is_read = st.checkbox("👀 읽음 확인하기", value=partner_diary["read"], key=f"read_{partner_key}")
        if is_read != partner_diary["read"]:
            st.session_state.diaries[partner_key]["read"] = is_read
            st.rerun()
            
        if partner_diary["read"]:
            st.caption("✅ 상대방이 확인을 마쳤습니다.")
        else:
            st.caption("⏳ 아직 확인 전입니다.")
    else:
        st.markdown("""
            <div class="empty-card">
                아직 상대방이<br>일기를 작성하지 않았어요 🐾
            </div>
        """, unsafe_allow_html=True)
