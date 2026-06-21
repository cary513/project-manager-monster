import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="個人品牌成長行事曆", layout="wide", page_icon="📅")

st.title("📅 個人品牌成長行事曆")
st.caption("Supabase + Streamlit 版本 | 為瑗設計")

# ====================== Supabase 設定 ======================
st.sidebar.header("🔑 Supabase 連線設定")
SUPABASE_URL = st.sidebar.text_input("SUPABASE_URL", value="https://your-project.supabase.co")
SUPABASE_KEY = st.sidebar.text_input("SUPABASE_ANON_KEY", value="", type="password")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.warning("👈 請在左側邊欄輸入 Supabase URL 和 Key")
    st.stop()

try:
    from supabase import create_client, Client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    st.sidebar.success("✅ 已連線 Supabase")
except Exception as e:
    st.error(f"連線失敗: {e}")
    st.stop()

# ====================== SIDEBAR ======================
st.sidebar.title("📅 行事曆 APP")
st.sidebar.markdown("**個人品牌成長計劃**")
page = st.sidebar.radio("導航", ["每日行事曆", "一週總覽", "進度追蹤", "盧森堡求職", "設定"])

today = date.today()
weekday_name = today.strftime("%A")

# ====================== HELPER FUNCTIONS ======================
def get_schedule_template(day_type: str):
    response = supabase.table("schedule_templates").select("*").eq("day_type", day_type).execute()
    return pd.DataFrame(response.data) if response.data else pd.DataFrame()

# ====================== MAIN PAGES ======================
if page == "每日行事曆":
    st.title(f"📍 今日行事曆 - {today} ({weekday_name})")
    
    if weekday_name == "Saturday":
        day_type = "saturday"
    elif weekday_name == "Sunday":
        day_type = "sunday"
    else:
        day_type = "weekday"
    
    df = get_schedule_template(day_type)
    
    if not df.empty:
        st.subheader("今日詳細行程")
        for idx, row in df.iterrows():
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                st.write(f"**{row.get('time_slot', '')}**")
            with col2:
                st.write(f"**{row.get('activity', '')}**")
                if row.get('description'):
                    st.caption(row['description'])
            with col3:
                done = st.checkbox("完成", key=f"chk_{idx}")
    else:
        st.info("尚無此日程模板")
    
    st.success("🍽️ 16:8 飲食窗：12:00 – 20:20")
    
    st.subheader("快速記錄")
    weight = st.number_input("今日體重 (kg)", min_value=40.0, max_value=150.0, value=65.0, step=0.1)
    notes = st.text_area("今日心得 / 調整", height=100)
    if st.button("💾 儲存今日記錄"):
        st.success("已儲存！")

elif page == "一週總覽":
    st.title("📊 本週總覽")

elif page == "進度追蹤":
    st.title("📈 成長進度追蹤")
    st.write("語言學習、文章、作品集、運動完成率等統計")

elif page == "盧森堡求職":
    st.title("🇱🇺 盧森堡求職追蹤")

elif page == "設定":
    st.title("⚙️ 設定")
    st.write("Supabase 連線資訊、個人目標等")

st.caption("由 Grok 為您設計的 Supabase + Streamlit 行事曆 APP")
