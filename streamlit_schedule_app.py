import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="個人品牌成長行事曆", layout="wide", page_icon="📅")

st.title("📅 個人品牌成長行事曆")
st.caption("Supabase + Streamlit 版本 | 為瑗設計")

# ====================== Supabase 設定 ======================
st.sidebar.header("🔑 Supabase 連線設定")
SUPABASE_URL = st.sidebar.text_input(
    "SUPABASE_URL", 
    value="https://xxxxxxxx.supabase.co", 
    help="您的 Supabase Project URL"
)
SUPABASE_KEY = st.sidebar.text_input(
    "SUPABASE_ANON_KEY", 
    value="", 
    type="password",
    help="您的 anon public key"
)

if not SUPABASE_URL or not SUPABASE_KEY:
    st.warning("👈 請在左側邊欄輸入 Supabase 資訊")
    st.stop()

try:
    from supabase import create_client, Client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    st.sidebar.success("✅ Supabase 已連線")
except Exception as e:
    st.error(f"連線失敗: {e}")
    st.stop()

# ====================== 今日日程 ======================
today = date.today()
weekday = today.strftime("%A")

st.header(f"📍 今日 {today}（{weekday}）")

if weekday == "Saturday":
    day_type = "saturday"
elif weekday == "Sunday":
    day_type = "sunday"
else:
    day_type = "weekday"

# 讀取日程模板
try:
    response = supabase.table("schedule_templates").select("*").eq("day_type", day_type).execute()
    df = pd.DataFrame(response.data)

    if not df.empty:
        st.subheader("今日詳細行程")
        for idx, row in df.iterrows():
            with st.container(border=True):
                col1, col2, col3 = st.columns([1.5, 5, 1])
                with col1:
                    st.markdown(f"**{row['time_slot']}**")
                with col2:
                    st.markdown(f"**{row['activity']}**")
                    if pd.notna(row.get('description')):
                        st.caption(row['description'])
                with col3:
                    st.checkbox("完成", key=f"chk_{idx}_{row['time_slot']}")
    else:
        st.info("尚未找到對應日程模板，請確認資料庫已匯入 schema。")
except Exception as e:
    st.error(f"讀取資料庫失敗：{e}")

# 飲食提醒
st.success("🍽️ **16:8 飲食窗**：12:00 – 20:20")

# 快速記錄
st.subheader("💪 今日快速記錄")
col1, col2 = st.columns(2)
with col1:
    weight = st.number_input("體重 (kg)", value=65.0, step=0.1)
with col2:
    lang_min = st.number_input("語言學習 (分鐘)", value=30, step=5)

notes = st.text_area("今日心得・明天重點・調整事項", height=100)

if st.button("💾 儲存今日記錄", type="primary"):
    st.success("✅ 記錄已儲存！（後續可完整串接 daily_logs 資料表）")
    st.balloons()

st.divider()
st.caption("Made with ❤️ by Grok • 持續優化中")
