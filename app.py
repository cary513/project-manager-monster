import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from deep_translator import GoogleTranslator

# 1. 頁面配置
st.set_page_config(page_title="Solo Evolution Tracker Cloud", layout="wide")

# 2. 連接 Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    # 這裡會讀取你在 Secrets 中設定的試算表
    return conn.read(ttl="1m") 

# 3. 初始化或讀取資料
if 'projects' not in st.session_state:
    try:
        st.session_state.projects = get_data()
    except Exception as e:
        # 如果讀取失敗，顯示錯誤原因方便 Debug
        st.warning(f"目前無法從雲端讀取資料，請檢查 Secrets 設定。")
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
    # 確保資料是 DataFrame 格式
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
    # 這裡顯示編輯器
    edited_df = st.data_editor(st.session_state.projects, num_rows="dynamic", use_container_width=True)
    
    # 【關鍵修正】儲存按鈕必須放在編輯模式的縮排內，或是獨立判斷
    if st.button("💾 儲存並同步至 Google Sheets"):
        try:
            # 自動更新第一個分頁 (工作表1)
            conn.update(data=edited_df)
            st.session_state.projects = edited_df
            st.success("✅ 同步成功！資料已寫入雲端 Google Sheets。")
            st.balloons() # 成功的小驚喜
        except Exception as e:
            st.error(f"同步失敗！")
            st.info(f"技術錯誤訊息: {e}")

elif mode == "🍎 法文工具":
    st.subheader("🍎 法文自動化學習")
    user_input = st.text_input("輸入中文單字")
    if user_input:
        res = GoogleTranslator(source='zh-TW', target='fr').translate(user_input)
        st.success(f"✨ 法文翻譯：{res}")
