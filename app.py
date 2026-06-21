import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="個人品牌成長儀表板", layout="wide", page_icon="📅")

st.title("📊 個人品牌成長儀表板")

# Supabase 連線（請替換 Key）
SUPABASE_URL = "https://mniykroryzitmxdwwali.supabase.co"
SUPABASE_KEY = "sb_publishable_tQ2-mcPmqFFGf96OooR4oA_pzVFOVg7"   # ← 請貼上

try:
    from supabase import create_client, Client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"連線失敗: {e}")
    st.stop()

st.sidebar.header("📆 日期選擇")
selected_date = st.sidebar.date_input("查看日期", date.today())

st.sidebar.header("💪 快速記錄")
weight = st.sidebar.number_input("體重 (kg)", value=65.0, step=0.1)
mood = st.sidebar.text_input("今日心情", "")
if st.sidebar.button("儲存記錄"):
    st.sidebar.success("✅ 已儲存")

# 主內容
st.header(f"📍 {selected_date} 今日重點")

# 今日進度（放在上方）
st.subheader("📊 今日進度")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("完成率", "65%", "↑12%")
with col2:
    st.metric("語言學習", "45 分", "已達標")
with col3:
    st.metric("文章/作品", "1 項", "↑1")

# 今日行程
day_type = "saturday" if selected_date.strftime("%A") == "Saturday" else "sunday" if selected_date.strftime("%A") == "Sunday" else "weekday"

try:
    response = supabase.table("schedule_templates").select("*").eq("day_type", day_type).execute()
    df = pd.DataFrame(response.data)
    
    if not df.empty:
        st.subheader("⏰ 今日詳細行程")
        for idx, row in df.iterrows():
            with st.container(border=True):
                col_a, col_b, col_c = st.columns([2, 6, 2])
                with col_a:
                    st.markdown(f"**{row.get('time_slot', '')}**")
                with col_b:
                    st.markdown(f"**{row.get('activity', '')}**")
                    if row.get('description'):
                        st.caption(row['description'])
                with col_c:
                    st.checkbox("完成", key=f"task_{idx}")
    else:
        st.info("尚未找到行程")
except Exception as e:
    st.error(f"讀取失敗: {e}")

# 手動新增
if st.button("➕ 新增自訂待辦事項"):
    st.session_state.show_form = True

if st.session_state.get("show_form", False):
    with st.form("add_task"):
        new_time = st.text_input("時間 (例: 20:00-21:00)")
        new_task = st.text_input("任務名稱")
        new_desc = st.text_input("描述")
        if st.form_submit_button("確認新增"):
            st.success(f"✅ 已新增：{new_time} - {new_task}")
            st.session_state.show_form = False

st.success("🍽️ 16:8 飲食窗：12:00 – 20:20")
st.info("🏋️ 今日運動：參考每週表（週日主動恢復）")
