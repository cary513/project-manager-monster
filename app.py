import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from deep_translator import GoogleTranslator

# 1. 頁面配置
st.set_page_config(page_title="Solo Evolution Tracker Cloud", layout="wide")

# 2. 連接 Google Sheets
# 注意：正式部署時需在 Streamlit Cloud 的 Secrets 設定網址
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    return conn.read(ttl="5m") # 每 5 分鐘快取一次

# 3. 初始化或讀取資料
if 'projects' not in st.session_state:
    try:
        st.session_state.projects = get_data()
    except:
        # 如果連接失敗，先用範例數據
        st.session_state.projects = pd.DataFrame([
            {"專案名稱": "醫療輔助 App", "進度": 65, "工具": "Python", "阻礙": "無", "步驟": "流程分析", "排程": "2026-03-01"}
        ])

# --- 側邊欄與模式切換 ---
with st.sidebar:
    st.title("🛡️ 雲端控制台")
    mode = st.radio("功能切換", ["📊 檢視看板", "📝 編輯專案", "🍎 法文工具"])
    
    if st.button("🔄 同步雲端資料"):
        st.session_state.projects = get_data()
        st.rerun()

# --- 主介面 ---
st.title("🔭 內在座標 | Cloud Project Manager")

if mode == "📊 檢視看板":
    df = st.session_state.projects
    cols = st.columns(3)
    for i, row in df.iterrows():
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"### {row['專案名稱']}")
                st.progress(int(row['進度']))
                st.write(f"📅 **排程**: {row['排程']}")
                st.write(f"🛑 **阻礙**: {row['阻礙']}")
                with st.expander("查看行動細節"):
                    st.write(row['步驟'])

elif mode == "📝 編輯專案":
    st.subheader("🛠️ 雲端編輯模式")
    # 使用 Streamlit 內建的編輯器，直接修改表格
    edited_df = st.data_editor(st.session_state.projects, num_rows="dynamic", use_container_width=True)

if st.button("💾 儲存並同步至 Google Sheets"):
    try:
        # 使用服務帳號認證進行更新
        # 讓程式自動尋找第一個工作表，最不容易出錯
conn.update(data=edited_df),
            worksheet="工作表1" # 請確認你的 Google Sheets 標籤名稱，通常是 工作表1 或 Sheet1
        )
        st.session_state.projects = edited_df
        st.success("✅ 同步成功！資料已寫入雲端。")
    except Exception as e:
        st.error(f"同步失敗！請確認 Secrets 格式與 Google Sheets 編輯權限。")
        st.info(f"錯誤訊息: {e}")

elif mode == "🍎 法文工具":
    # (保留你原本的翻譯邏輯代碼...)
    pass
