import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from deep_translator import GoogleTranslator

# 1. 頁面配置
st.set_page_config(page_title="Solo Evolution Tracker Cloud", layout="wide")

# 2. 連接配置
conn = st.connection("gsheets", type=GSheetsConnection)

# 關鍵配置：請確保這裡與你的試算表網址完全一致
SHEET_URL = "https://docs.google.com/spreadsheets/d/1JgBfeDw5aHkazCiR-kqFw7jJ8EC0DGGgnBm8kaJT7pk/edit#gid=0"
WORKSHEET_NAME = "Sheet1" 

def get_data():
    """封裝讀取邏輯，增加錯誤攔截"""
    # 使用最基礎的讀取方式，減少 API 參數衝突
    return conn.read(spreadsheet=SHEET_URL, worksheet=WORKSHEET_NAME, ttl=0)

# 3. 初始化 Session State
if 'projects' not in st.session_state:
    try:
        data = get_data()
        # 邏輯清洗：將空值填補為預設值，避免 int() 轉換失敗
        st.session_state.projects = data.fillna({
            "進度": 0, "工具": "", "阻礙": "無", "步驟": "", "排程": ""
        })
    except Exception as e:
        st.error(f"連線失敗原因：{e}")
        st.session_state.projects = pd.DataFrame(columns=["專案名稱", "進度", "工具", "阻礙", "步驟", "排程"])

# --- 側邊欄控制台 ---
with st.sidebar:
    st.title("🛡️ 雲端控制台")
    mode = st.radio("功能切換", ["📊 檢視看板", "📝 編輯專案", "🍎 法文工具"])
    
    if st.button("🔄 同步雲端資料"):
        st.cache_data.clear() # 強制清除快取
        st.rerun()

# --- 主畫面 ---
st.title("🔭 內在座標 | Cloud Project Manager")

if mode == "📊 檢視看板":
    df = st.session_state.projects
    if not df.empty:
        cols = st.columns(3)
        for i, row in df.iterrows():
            # 跳過沒有名稱的無效列
            if pd.isna(row['專案名稱']) or row['專案名稱'] == "":
                continue
                
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"### {row['專案名稱']}")
                    
                    # 強制數值轉換邏輯
                    try:
                        p_val = float(row['進度']) if pd.notnull(row['進度']) else 0.0
                        progress_val = int(min(max(p_val, 0), 100))
                    except:
                        progress_val = 0
                        
                    st.progress(progress_val)
                    st.write(f"📅 **排程**: {row.get('排程', '未定')}")
                    st.write(f"🛑 **阻礙**: {row.get('阻礙', '無')}")
                    with st.expander("查看行動細節"):
                        st.write(str(row.get('步驟', '暫無細節')))
    else:
        st.info("目前雲端沒有資料，請切換至編輯模式。")

elif mode == "📝 編輯專案":
    st.subheader("🛠️ 雲端編輯模式")
    edited_df = st.data_editor(
        st.session_state.projects, 
        num_rows="dynamic", 
        use_container_width=True
    )
    
    if st.button("💾 儲存並同步至 Google Sheets"):
        try:
            # 儲存時再次確保分頁名稱正確
            conn.update(
                spreadsheet=SHEET_URL,
                worksheet=WORKSHEET_NAME,
                data=edited_df
            )
            st.session_state.projects = edited_df
            st.success("✅ 同步成功！")
            st.balloons()
        except Exception as e:
            st.error(f"儲存失敗：{e}")

elif mode == "🍎 法文工具":
    st.subheader("🍎 法文自動化學習")
    word = st.text_input("輸入中文單字")
    if word:
        res = GoogleTranslator(source='zh-TW', target='fr').translate(word)
        st.success(f"✨ 法文翻譯：{res}")
