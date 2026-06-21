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

# 側邊欄
st.sidebar.header("📆 日期選擇")
selected_date = st.sidebar.date_input("查看日期", date.today())

st.sidebar.header("💪 快速記錄")
weight = st.sidebar.number_input("體重 (kg)", value=65.0, step=0.1)
mood = st.sidebar.text_input("今日心情", "")
if st.sidebar.button("儲存記錄"):
    st.sidebar.success("✅ 已儲存")

# 主儀表板
col1, col2 = st.columns([3, 1])

with col1:
    st.header(f"📍 {selected_date} 今日重點")
    day_type = "saturday" if selected_date.strftime("%A") == "Saturday" else "sunday" if selected_date.strftime("%A") == "Sunday" else "weekday"
    
    try:
        response = supabase.table("schedule_templates").select("*").eq("day_type", day_type).execute()
        df = pd.DataFrame(response.data)
        if not df.empty:
            for idx, row in df.iterrows():
                with st.container(border=True):
                    col_a, col_b, col_c = st.columns([1.5, 5, 1])
                    with col_a:
                        st.markdown(f"**{row.get('time_slot', '')}**")
                    with col_b:
                        st.markdown(f"**{row.get('activity', '')}**")
                        if row.get('description'):
                            st.caption(row['description'])
                    with col_c:
                        st.checkbox("完成", key=f"task_{idx}")
        else:
            st.info("請確認行程資料已插入")
    except Exception as e:
        st.error(f"讀取失敗: {e}")

with col2:
    st.subheader("📊 今日進度")
    st.metric("完成率", "65%", "↑12%")
    st.metric("語言學習", "45 分", "已達標")
    st.metric("文章/作品", "1 項", "")

st.success("🍽️ 16:8 飲食窗：12:00 – 20:20")
st.info("🏋️ 今日運動：參考每週表（週日主動恢復）")

st.subheader("📈 本週回顧")
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("語言學習總時", "12.5 小時", "目標 15h")
with col_b:
    st.metric("文章數", "4 篇", "目標 5")
with col_c:
    st.metric("習慣完成率", "82%", "↑5%")
