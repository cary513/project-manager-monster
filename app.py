import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from deep_translator import GoogleTranslator

# 1. 頁面配置
st.set_page_config(page_title="Solo Evolution Tracker Cloud", layout="wide")

# 2. 建立連線 (不使用快取，確保資料即時性)
conn = st.connection("gsheets", type=GSheetsConnection)

# 關鍵路徑設定：請確保這裡與你的試算表網址與標籤名完全一致
SHEET_URL = "https://docs.google.com/spreadsheets/d/1JgBfeDw5aHkazCiR-kqFw7jJ8EC0DGGgnBm8kaJT7pk/edit#gid=0"
WORKSHEET_NAME = "Sheet1" 

def get_data():
    """封裝讀取邏輯：強制不使用快取以避開 400 錯誤"""
    # 這裡移除 ttl 參數，改用最原始的 read 方法
    return conn.read(spreadsheet=SHEET_URL, worksheet=WORKSHEET_NAME)

# 3. 初始化或刷新資料
if 'projects' not in st.session_state or st.sidebar.button("🔄 強制刷新雲端連線"):
    try:
        # 強制清除 Streamlit 的所有快取記憶
        st.cache_data.clear()
        raw_data = get_data()
        
        # 資料清洗：處理可能導致看板崩潰的空值
        st.session_state.projects = raw_data.fillna({
            "進度": 0, "工具": "", "阻礙": "無", "步驟": "", "排程": ""
        })
        if 'projects' in st.session_state:
            st.toast("✅ 雲端資料同步成功！")
    except Exception as e:
        st.error(f"連線失敗原因：{e}")
        # 提供初始結構，防止程式完全無法啟動
        st.session_state.projects = pd.DataFrame(columns=["專案名稱", "進度", "工具", "阻礙", "步驟", "排程"])

# --- 側邊欄 ---
with st.sidebar:
    st.title("🛡️ 雲端控制台")
    mode = st.radio("功能切換", ["📊 檢視看板", "📝 編輯專案", "🍎 法文工具"])

# --- 主畫面 ---
st.title("🔭 內在座標 | Cloud Project Manager")

if mode == "📊 檢視看板":
    df = st.session_state.projects
    if not df.empty:
        # 確保看板需要的欄位都存在
        required_cols = ['專案名稱', '進度', '排程', '阻礙', '步驟']
        if all(col in df.columns for col in required_cols):
            cols = st.columns(3)
            for i, row in df.iterrows():
                # 過濾掉空行
                if pd.isna(row['專案名稱']) or str(row['專案名稱']).strip() == "":
                    continue
                
                with cols[i % 3]:
                    with st.container(border=True):
                        st.markdown(f"### {row['專案名稱']}")
                        
                        # 數值安全性轉換
                        try:
                            val = float(row['進度']) if pd.notnull(row['進度']) else 0.0
                            progress_val = int(min(max(val, 0), 100))
                        except:
                            progress_val = 0
                            
                        st.progress(progress_val)
                        st.write(f"📅 **排程**: {row['排程']}")
                        st.write(f"🛑 **阻礙**: {row['阻礙']}")
                        with st.expander("查看行動細節"):
                            st.write(f"🛠️ **工具**: {row['工具']}")
                            st.write(f"📝 **步驟**: {row['步驟']}")
        else:
            st.warning("⚠️ 試算表欄位名稱不符，請至編輯模式確認。")
    else:
        st.info("目前雲端沒有資料，請切換至編輯模式。")

elif mode == "📝 編輯專案":
    st.subheader("🛠️ 雲端編輯模式")
    # 使用資料編輯器
    edited_df = st.data_editor(
        st.session_state.projects, 
        num_rows="dynamic", 
        use_container_width=True
    )
    
    # 修正後的儲存按鈕位置
    if st.button("💾 儲存並同步至 Google Sheets"):
        try:
            conn.update(
                spreadsheet=SHEET_URL,
                worksheet=WORKSHEET_NAME,
                data=edited_df
            )
            st.session_state.projects = edited_df
            st.success("✅ 資料更新成功！")
            st.balloons()
        except Exception as e:
            st.error(f"儲存失敗：{e}")

elif mode == "🍎 法文工具":
    st.subheader("🍎 法文自動化學習")
    word = st.text_input("輸入中文單字")
    if word:
        try:
            res = GoogleTranslator(source='zh-TW', target='fr').translate(word)
            st.success(f"✨ 法文翻譯：{res}")
        except Exception as e:
            st.error(f"翻譯服務目前不可用：{e}")
