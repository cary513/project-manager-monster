import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from deep_translator import GoogleTranslator

# 1. 頁面配置
st.set_page_config(page_title="Solo Evolution Tracker Cloud", layout="wide")

# 2. 連接配置
conn = st.connection("gsheets", type=GSheetsConnection)

# 關鍵配置：網址與分頁名稱必須與截圖完全一致
SHEET_URL = "https://docs.google.com/spreadsheets/d/1JgBfeDw5aHkazCiR-kqFw7jJ8EC0DGGgnBm8kaJT7pk/edit#gid=0"
WORKSHEET_NAME = "Sheet1" # 根據截圖，這裡是關鍵修正點

def get_data():
    """封裝讀取邏輯"""
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
        # 當目前雲端沒資料或連線失敗時顯示
        st.error(f"連線失敗原因：{e}")
        st.session_state.projects = pd.DataFrame(columns=["專案名稱", "進度", "工具", "阻礙", "步驟", "排程"])

# --- 側邊欄控制台 ---
with st.sidebar:
    st.title("🛡️ 雲端控制台")
    mode = st.radio("功能切換", ["📊 檢視看板", "📝 編輯專案", "🍎 法文工具"])
    
    st.divider()
    if st.button("🔄 同步雲端資料"):
        try:
            st.session_state.projects = get_data()
            st.success("資料同步完成")
            st.rerun()
        except Exception as e:
            st.error(f"同步失敗：{e}")

# --- 主畫面標題 ---
st.title("🔭 內在座標 | Cloud Project Manager")

# --- 模式邏輯切換 ---
if mode == "📊 檢視看板":
    df = st.session_state.projects
    # 邏輯判斷：如果資料表只有標題而沒有內容，會顯示提示訊息
    if df is not None and len(df) > 0:
        required_cols = ['專案名稱', '進度', '排程', '阻礙', '步驟']
        if all(col in df.columns for col in required_cols):
            cols = st.columns(3)
            for i, row in df.iterrows():
                # 過濾掉全空的列
                if pd.isnull(row['專案名稱']) or row['專案名稱'] == "":
                    continue
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
            st.warning(f"目前欄位名稱不符，請檢查試算表首行。預期欄位：{required_cols}")
    else:
        st.info("目前雲端沒有資料，請切換至「📝 編輯專案」模式新增內容。")

elif mode == "📝 編輯專案":
    st.subheader("🛠️ 雲端編輯模式")
    
    # 資料編輯器
    edited_df = st.data_editor(
        st.session_state.projects, 
        num_rows="dynamic", 
        use_container_width=True,
        key="project_editor"
    )
    
    # 儲存按鈕：此處縮排已修正，確保屬於編輯模式
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
