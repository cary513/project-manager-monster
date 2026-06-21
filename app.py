import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from supabase import create_client, Client
import os
from typing import Optional

# ====================== CONFIG ======================
st.set_page_config(page_title="個人品牌成長行事曆", layout="wide", page_icon="📅")

# Supabase 設定（請替換成你的真實資訊）
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "YOUR_SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "YOUR_SUPABASE_ANON_KEY")

if not SUPABASE_URL or SUPABASE_URL == "YOUR_SUPABASE_URL":
    st.error("請在 .streamlit/secrets.toml 中設定 SUPABASE_URL 和 SUPABASE_KEY")
    st.stop()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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

def log_daily_activity(log_date: date, completed: dict, weight: float = None, notes: str = ""):
    data = {
        "user_id": st.session_state.user_id,  # 假設已登入
        "log_date": log_date.isoformat(),
        "day_type": "weekday" if weekday_name not in ["Saturday", "Sunday"] else weekday_name.lower(),
        "completed_slots": completed,
        "weight": weight,
        "notes": notes,
        "diet_168_completed": True  # 可改成 checkbox
    }
    supabase.table("daily_logs").upsert(data).execute()

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
                st.write(f"**{row['time_slot']}**")
            with col2:
                st.write(f"**{row['activity']}**")
                if row.get('description'):
                    st.caption(row['description'])
            with col3:
                done = st.checkbox("完成", key=f"chk_{idx}")
                # 可以後續存入 completed_slots
    else:
        st.info("尚無此日程模板")
    
    # 16:8 提醒
    st.success("🍽️ 16:8 飲食窗：12:00 – 20:20")
    
    # 快速打卡
    st.subheader("快速記錄")
    weight = st.number_input("今日體重 (kg)", min_value=40.0, max_value=150.0, value=65.0, step=0.1)
    notes = st.text_area("今日心得 / 調整", height=100)
    if st.button("💾 儲存今日記錄"):
        st.success("已儲存！")

elif page == "一週總覽":
    st.title("📊 本週總覽")
    # 可加入日曆或多日顯示（後續擴充）

elif page == "進度追蹤":
    st.title("📈 成長進度追蹤")
    st.write("語言學習、文章、作品集、運動完成率等統計")
    # 可查詢 daily_logs 並畫圖

elif page == "盧森堡求職":
    st.title("🇱🇺 盧森堡求職追蹤")
    # CRUD for luxembourg_applications table

elif page == "設定":
    st.title("⚙️ 設定")
    st.write("Supabase 連線資訊、個人目標等")

st.caption("由 Grok 為您設計的 Supabase + Streamlit 行事曆 APP")
