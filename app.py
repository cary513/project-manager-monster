import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. 頁面配置
st.set_page_config(page_title="Solo Evolution Tracker Cloud", layout="wide")

# 2. 建立連線
conn = st.connection("gsheets", type=GSheetsConnection)

# 關鍵變數：確保這裡與你的試算表網址與名稱完全對齊
SHEET_URL = "https://docs.google.com/spreadsheets/d/1JgBfeDw5aHkazCiR-kqFw7jJ8EC0DGGgnBm8kaJT7pk/edit#gid=0"
WORKSHEET_NAME = "Sheet1" 

def get_data():
    # 邏輯修正：移除所有複雜參數，僅傳入最基本路徑
    return conn.read(spreadsheet=SHEET_URL, worksheet=WORKSHEET_NAME)

# 3. 強制重置機制（解決 400 錯誤的關鍵）
if st.sidebar.button("♻️ 徹底重置連線 (修復 400 錯誤)"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()

# 4. 初始化資料
if 'projects' not in st.session_state:
    try:
        # 讀取資料並立即清洗空值
        df = get_data()
        st.session_state.projects = df.dropna(subset=['專案名稱'])
    except Exception as e:
        st.error(f"連線失敗原因：{e}")
        # 建立預設架構，避免 App 崩潰
        st.session_state.projects = pd.DataFrame(columns=["專案名稱", "進度", "工具", "阻礙", "步驟", "排程"])

# --- 看板邏輯 ---
st.title("🔭 內在座標 | Cloud Project Manager")

# 假設目前在檢視模式
df = st.session_state.projects
if not df.empty:
    cols = st.columns(3)
    for i, row in df.iterrows():
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"### {row['專案名稱']}")
                # 數值清洗邏輯
                try:
                    p_val = int(float(row['進度'])) if pd.notnull(row['進度']) else 0
                except:
                    p_val = 0
                st.progress(min(max(p_val, 0), 100))
                st.write(f"📅 排程: {row['排程']}")
else:
    st.info("目前雲端沒有資料，請切換至編輯模式新增，並確保試算表名稱為 Sheet1。")
