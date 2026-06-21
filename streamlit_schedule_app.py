import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="個人品牌成長行事曆", layout="wide", page_icon="📅")

st.title("📅 個人品牌成長行事曆")
st.markdown("**Supabase + Streamlit** 版本")

# ====================== Supabase 連線 ======================
st.sidebar.header("🔑 Supabase 設定")

SUPABASE_URL = st.sidebar.text_input("SUPABASE_URL", value="https://your-project.supabase.co", type="password")
SUPABASE_KEY = st.sidebar.text_input("SUPABASE_ANON_KEY", value="", type="password")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.warning("請在側邊欄輸入您的 Supabase URL 和 Key")
    st.stop()

try:
    from supabase import create_client, Client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    st.sidebar.success("✅ 已連線 Supabase")
except Exception as e:
    st.error(f"連線失敗: {e}")
    st.stop()

# ====================== 今日資訊 ======================
today = date.today()
weekday = today.strftime("%A")

st.header(f"📍 今日：{today}（{weekday}）")

if weekday == "Saturday":
    day_type = "saturday"
elif weekday == "Sunday":
    day_type = "sunday"
else:
    day_type = "weekday"

# 從資料庫讀取模板
try:
    response = supabase.table("schedule_templates").select("*").eq("day_type", day_type).execute()
    df = pd.DataFrame(response.data)
    
    if not df.empty:
        st.subheader("今日詳細日程")
        for _, row in df.iterrows():
            with st.expander(f"⏰ {row['time_slot']} - {row['activity']}", expanded=True):
                st.write(row.get('description', ''))
                if row.get('reminder'):
                    st.caption(f"💡 提醒：{row['reminder']}")
                st.checkbox("已完成", key=f"task_{row['time_slot']}")
    else:
        st.info("此類型日程模板尚未載入，請確認資料庫資料。")
except Exception as e:
    st.error(f"讀取資料失敗：{e}")

# 16:8 提醒
st.success("🍽️ **16:8 飲食窗**：12:00 – 20:20")

# 快速記錄區
st.subheader("快速記錄")
col1, col2 = st.columns(2)
with col1:
    weight = st.number_input("今日體重 (kg)", value=65.0, step=0.1)
with col2:
    language_min = st.number_input("今日語言學習 (分鐘)", value=30, step=5)

notes = st.text_area("今日心得 / 明天待辦", height=120)

if st.button("💾 儲存今日記錄", type="primary"):
    st.success("✅ 已儲存！（後續可串接 daily_logs 資料表）")
    st.balloons()

st.caption("Made with ❤️ by Grok • 點擊側邊欄可切換頁面")
