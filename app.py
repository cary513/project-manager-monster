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

st.sidebar.header("📆 日期選擇")
selected_date = st.sidebar.date_input("查看日期", date.today())

# 今日重點
st.header(f"📍 {selected_date} 今日重點")

# 今日進度
st.subheader("📊 今日進度")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("完成率", "65%", "↑12%")
with col2:
    st.metric("語言學習", "210 分", "目標 300")
with col3:
    st.metric("文章/作品", "4 篇", "目標 5")

# 行程顯示
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

# 快速記錄 + 儲存到 Supabase
st.subheader("💪 快速記錄")
col_a, col_b = st.columns(2)
with col_a:
    weight = st.number_input("體重 (kg)", value=65.0, step=0.1)
with col_b:
    notes = st.text_area("今日心得・明天3件事", height=100)

if st.button("💾 儲存今日記錄", type="primary"):
    try:
        data = {
            "log_date": selected_date.isoformat(),
            "weight": weight,
            "notes": notes,
            "diet_168_completed": True
        }
        supabase.table("daily_logs").upsert(data).execute()
        st.success("✅ 記錄已永久儲存到 Supabase！")
    except Exception as e:
        st.error(f"儲存失敗: {e}")

st.success("🍽️ 16:8 飲食窗：12:00 – 20:20")

