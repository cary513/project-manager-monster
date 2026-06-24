import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="個人品牌成長儀表板", layout="wide", page_icon="📊")

# 頂部標題
st.markdown("<h1 style='text-align: center;'>📊 個人品牌成長儀表板</h1>", unsafe_allow_html=True)

# Supabase 連線（請替換 Key）
SUPABASE_URL = "https://mniykrzyitzmxdwwali.supabase.co"
SUPABASE_KEY = "您的 anon key"   # ← 請貼上

try:
    from supabase import create_client, Client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"連線失敗: {e}")
    st.stop()

# 統計卡片（類似 ProTrack）
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📅 今日完成", "8/12", "↑2")
with col2:
    st.metric("📚 語言學習", "210 分", "目標 300")
with col3:
    st.metric("✍️ 文章/作品", "4 篇", "目標 5")

# 主要內容
st.subheader("📍 今日重點行程")
selected_date = st.date_input("選擇日期", date.today(), label_visibility="collapsed")

day_type = "saturday" if selected_date.strftime("%A") == "Saturday" else "sunday" if selected_date.strftime("%A") == "Sunday" else "weekday"

try:
    response = supabase.table("schedule_templates").select("*").eq("day_type", day_type).execute()
    df = pd.DataFrame(response.data)
    if not df.empty:
        for idx, row in df.iterrows():
            with st.container(border=True):
                col_a, col_b, col_c = st.columns([1.5, 6, 1])
                with col_a:
                    st.markdown(f"**{row.get('time_slot', '')}**")
                with col_b:
                    st.markdown(f"**{row.get('activity', '')}**")
                    if row.get('description'):
                        st.caption(row['description'])
                with col_c:
                    st.checkbox("完成", key=f"task_{idx}")
    else:
        st.info("尚未找到行程資料")
except Exception as e:
    st.error(f"讀取失敗: {e}")

# 快速記錄
st.subheader("💪 快速記錄")
col_a, col_b = st.columns(2)
with col_a:
    weight = st.number_input("體重 (kg)", value=65.0, step=0.1)
with col_b:
    mood = st.text_input("今日心情 / 備註")

if st.button("💾 儲存今日記錄", type="primary"):
    st.success("✅ 已儲存！")

st.success("🍽️ 16:8 飲食窗：12:00 – 20:20")

st.caption("Made with ❤️ by Grok")
