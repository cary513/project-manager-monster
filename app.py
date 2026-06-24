import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="個人品牌成長儀表板", layout="wide", page_icon="📅")

st.title("📊 個人品牌成長儀表板")

# === Supabase 連線（請替換 Key）===
SUPABASE_URL = "https://mniykroryzitmxdwwali.supabase.co"
SUPABASE_KEY = "sb_publishable_tQ2-mcPmqFFGf96OooR4oA_pzVFOVg7"   # ← 請貼上真實 anon key


try:
    from supabase import create_client, Client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"連線失敗: {e}")
    st.stop()

st.header("➕ 自訂今日行程 / 待辦")

with st.form("add_custom_task"):
    time_slot = st.text_input("時間 (例: 20:00-21:00)")
    activity = st.text_input("任務 / 活動名稱")
    description = st.text_input("描述 / 提醒", "")
    submitted = st.form_submit_button("新增到今日")
    if submitted and time_slot and activity:
        st.success(f"✅ 已新增：{time_slot} - {activity}")

st.subheader("📋 複製到每週")
days = st.multiselect("選擇要複製到的日子", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], default=["Monday"])

if st.button("複製以上自訂項目到選取日子"):
    st.success(f"已複製到 {len(days)} 個日子！（未來可自動存入資料庫）")

st.success("🍽️ 16:8 飲食窗：12:00 – 20:20")
