import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from deep_translator import GoogleTranslator

# 1. 頁面配置
st.set_page_config(page_title="Solo Evolution Tracker Cloud", layout="wide")

# 2. 連接配置與全域變數
conn = st.connection("gsheets", type=GSheetsConnection)

# 關鍵路徑設定：請確保 SHEET_URL 網址與 WORKSHEET_NAME 名稱完全正確
SHEET_URL = "https://docs.google.com/spreadsheets/d/1JgBfeDw5aHkazCiR-kqFw7jJ8EC0DGGgnBm8kaJT7pk/edit#gid=0"
WORKSHEET_NAME = "Sheet1" # 已根據您的指示修正為 Sheet1

def get_data():
    """封裝讀取邏輯，確保路徑一致性"""
    return conn.read(
        spreadsheet=SHEET_URL, 
        worksheet=WORKSHEET_NAME, 
        ttl="1m"
    )

# 3. 初始化 Session State
if 'projects' not in st.session_state:
    try:
        st.session_state.projects = get_data()
    except Exception as e:
        st.error(f"連線失敗原因：{e}")
        # 建立預設欄位，防止看板初始化報錯
        st.session_state.projects = pd.DataFrame(columns=["專案名稱", "進度", "工具", "阻礙", "步驟", "排程"])

# --- 側邊欄控制台 ---
with st.sidebar:
    st.title("🛡️ 雲端控制台")
    mode = st.radio("功能切換", ["📊 檢視看板", "📝 編輯專案", "🍎 法文工具"])
    
    st.divider()
    if st.button("🔄 同步雲端資料"):
        try:
            st.session_state.projects = get_data()
            st.success("資料已同步")
            st.rerun()
        except Exception as e:
            st.error(f"同步失敗：{e}")

# --- 主畫面標題 ---
st.title("🔭 內在座標 | Cloud Project Manager")

# --- 模式邏輯切換 ---
if mode == "📊 檢視看板":
    df = st.session_state.projects
    if df is not None and not df.empty:
        required_cols = ['專案名稱', '進度', '排程', '阻礙', '步驟']
        if all(col in df.columns for col in required_cols):
            cols = st.columns(3)
            for i, row in df.iterrows():
                with cols[i % 3]:
                    with st.container(border=True):
                        st.markdown(f"### {row['專案名稱']}")
                        try:
                            val = int(row['進度']) if pd.notnull(row['進度']) else 0
                            progress_val = min(max(val, 0), 100)
                        except:
                            progress_val = 0
                        st.progress(progress_val)
                        st.write(f"📅 **排程**: {row['排程']}")
                        st.write(f"🛑 **阻礙**: {row['阻礙']}")
                        with st.expander("查看行動細節"):
                            st.write(str(row['步驟']))
        else:
            st.warning("資料表格式不符，請至編輯模式檢查欄位名稱（專案名稱、進度、排程、阻礙、步驟）。")
    else:
        st.info("目前雲端沒有資料，請切換至編輯模式新增。")

elif mode == "📝 編輯專案":
    st.subheader("🛠️ 雲端編輯模式")
    
    # 資料編輯器
    edited_df = st.data_editor(
        st.session_state.projects, 
        num_rows="dynamic", 
        use_container_width=True,
        key="project_editor"
    )
    
    # 儲存邏輯：必須嚴格縮排在編輯模式區塊內
    if st.button("💾 儲存並同步至 Google Sheets"):
        try:
            conn.update(
                spreadsheet=SHEET_URL,
                worksheet=WORKSHEET_NAME,
                data=edited_df
            )
            st.session_state.projects = edited_df
            st.success("✅ 同步成功！雲端資料已更新。")
            st.balloons()
            st.rerun()
        except Exception as e:
            st.error(f"儲存失敗！技術訊息: {e}")

elif mode == "🍎 法文工具":
    st.subheader("🍎 法文自動化學習")
    word = st.text_input("輸入中文單字")
    if word:
        try:
            res = GoogleTranslator(source='zh-TW', target='fr').translate(word)
            st.success(f"✨ 法文翻譯：{res}")
        except Exception as e:
            st.error(f"翻譯服務異常：{e}")
