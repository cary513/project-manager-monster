import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from deep_translator import GoogleTranslator

# 1. 頁面配置
st.set_page_config(page_title="Solo Evolution Tracker Cloud", layout="wide")

# 2. 連接 Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    # 統一指向 Google Sheet 底部的分頁名稱
    return conn.read(worksheet="工作表1", ttl="1m")

# 3. 初始化或讀取資料
if 'projects' not in st.session_state:
    try:
        st.session_state.projects = get_data()
    except Exception as e:
        st.error(f"連線失敗原因：{e}")
        st.session_state.projects = pd.DataFrame([
            {"專案名稱": "醫療輔助 App", "進度": 65, "工具": "Python", "阻礙": "無", "步驟": "流程分析", "排程": "2026-03-01"}
        ])

# --- 側邊欄與模式切換 ---
with st.sidebar:
    st.title("🛡️ 雲端控制台")
    mode = st.radio("功能切換", ["📊 檢視看板", "📝 編輯專案", "🍎 法文工具"])
    
    if st.button("🔄 同步雲端資料"):
        try:
            st.session_state.projects = get_data()
            st.rerun()
        except Exception as e:
            st.error(f"同步失敗：{e}")

# --- 主介面 ---
st.title("🔭 內在座標 | Cloud Project Manager")

if mode == "📊 檢視看板":
    df = st.session_state.projects
    if not df.empty:
        cols = st.columns(3)
        for i, row in df.iterrows():
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"### {row['專案名稱']}")
                    progress_val = int(row['進度']) if pd.notnull(row['進度']) else 0
                    st.progress(min(max(progress_val, 0), 100))
                    st.write(f"📅 **排程**: {row['排程']}")
                    st.write(f"🛑 **阻礙**: {row['阻礙']}")
                    with st.expander("查看行動細節"):
                        st.write(str(row['步驟']))

elif mode == "📝 編輯專案":
    st.subheader("🛠️ 雲端編輯模式")
    
    # 使用 data_editor 實現自由修改
    edited_df = st.data_editor(
        st.session_state.projects, 
        num_rows="dynamic", 
        use_container_width=True,
        key="project_editor"
    )
    
    if st.button("💾 儲存並同步至 Google Sheets"):
        try:
            conn.update(
                worksheet="工作表1",
                data=edited_df
            )
            st.session_state.projects = edited_df
            st.success("✅ 同步成功！雲端資料已更新。")
            st.balloons()
            st.rerun()
        except Exception as e:
            st.error(f"同步失敗！技術診斷訊息: {e}")

elif mode == "🍎 法文工具":
    st.subheader("🍎 法文自動化學習")
    word = st.text_input("輸入中文單字")
    if word:
        res = GoogleTranslator(source='zh-TW', target='fr').translate(word)
        st.success(f"✨ 法文翻譯：{res}")
