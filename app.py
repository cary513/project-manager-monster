import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from deep_translator import GoogleTranslator

# 1. 頁面配置
st.set_page_config(page_title="Solo Evolution Tracker Cloud", layout="wide")

# 2. 連接 Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    # 這裡會自動讀取 Secrets 中的設定
    return conn.read(ttl="1m") 

# 3. 初始化或讀取資料
if 'projects' not in st.session_state:
    try:
        st.session_state.projects = get_data()
    except Exception as e:
        # 顯示警示，讓你知道雲端讀取狀態
        st.warning("目前無法從雲端讀取資料，請檢查 Secrets 設定。")
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

# --- 這裡放在主程式區塊，確保 get_data 是全域可用的 ---
def get_data():
    # 明確指定工作表名稱為「工作表1」
    # 使用 worksheet 參數確保精準讀取
    return conn.read(worksheet="01", ttl="Project_DB")

# --- 模式切換邏輯 ---
if mode == "📊 檢視看板":
    # 檢視邏輯...
    pass

elif mode == "📝 編輯專案":
    st.subheader("🛠️ 雲端編輯模式")
    
    # 確保 session_state 裡有資料，否則先抓取
    if st.session_state.projects is None or st.session_state.projects.empty:
        st.session_state.projects = get_data()

    # 1. 顯示編輯表格：使用 data_editor 允許動態增減列
    edited_df = st.data_editor(
        st.session_state.projects, 
        num_rows="dynamic", 
        use_container_width=True,
        key="project_editor"
    )
    
    # 2. 儲存按鈕邏輯：必須與 edited_df 在同一層級
    if st.button("💾 儲存並同步至 Google Sheets"):
        try:
            # 產品邏輯：明確指定寫入到「工作表1」
            conn.update(
                worksheet="工作表1",
                data=edited_df
            )
            # 更新記憶體中的狀態，確保 UI 即時反應
            st.session_state.projects = edited_df
            st.success("✅ 同步成功！資料已寫入雲端。")
            st.balloons() 
            
        except Exception as e:
            st.error("同步失敗！請檢查權限設定。")
            st.info(f"技術診斷訊息: {e}")
            
elif mode == "🍎 法文工具":
    st.subheader("🍎 法文自動化學習")
    word = st.text_input("輸入中文單字")
    if word:
        res = GoogleTranslator(source='zh-TW', target='fr').translate(word)
        st.success(f"✨ 法文翻譯：{res}")
