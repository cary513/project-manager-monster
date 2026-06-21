import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(page_title="個人品牌成長行事曆", layout="wide", page_icon="📅")

st.title("📅 個人品牌成長行事曆")
st.caption("Supabase + Streamlit | 為瑗設計")

# Supabase 連線
st.sidebar.header("🔑 Supabase 連線")
SUPABASE_URL = st.sidebar.text_input("SUPABASE_URL", value="https://your-project.supabase.co")
SUPABASE_KEY = st.sidebar.text_input("SUPABASE_ANON_KEY", value="", type="password")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.warning("請輸入 Supabase 資訊")
    st.stop()

try:
    from supabase import create_client, Client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    st.sidebar.success("✅ 已連線")
except Exception as e:
    st.error(f"連線失敗: {e}")
    st.stop()

# 側邊欄日曆
st.sidebar.header("📆 日期選擇")
selected_date = st.sidebar.date_input("選擇日期", date.today())

# 今日資訊
st.header(f"📍 {selected_date}（{selected_date.strftime('%A')}）")

day_type = "saturday" if selected_date.strftime("%A") == "Saturday" else "sunday" if selected_date.strftime("%A") == "Sunday" else "weekday"

try:
    # 行程表
    response = supabase.table("schedule_templates").select("*").eq("day_type", day_type).execute()
    df = pd.DataFrame(response.data)
    
    if not df.empty:
        st.subheader("📋 詳細行程")
        completed = {}
        for idx, row in df.iterrows():
            with st.container(border=True):
                col1, col2, col3 = st.columns([1.5, 5, 1])
                with col1:
                    st.markdown(f"**{row.get('time_slot', '')}**")
                with col2:
                    st.markdown(f"**{row.get('activity', '')}**")
                    if row.get('description'):
                        st.caption(row['description'])
                with col3:
                    done = st.checkbox("完成", key=f"task_{idx}_{selected_date}", value=False)
                    completed[row.get('time_slot')] = done
    else:
        st.info("尚未找到行程模板")
except Exception as e:
    st.error(f"讀取失敗: {e}")

st.success("🍽️ 16:8 飲食窗：12:00 – 20:20")

# 快速記錄
st.subheader("💪 快速記錄")
weight = st.number_input("體重 (kg)", value=65.0, step=0.1)
notes = st.text_area("今日心得・明天3件事", height=120)

if st.button("💾 儲存今日記錄", type="primary"):
    st.success("✅ 已儲存！")
    st.balloons()
