import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

# 1. 頁面配置
st.set_page_config(page_title="Solo Evolution Tracker", layout="wide")

# 2. 初始化專案數據 (使用 Session State 保持編輯狀態)
if 'project_db' not in st.session_state:
    st.session_state.project_db = pd.DataFrame([
        {"專案名稱": "醫療輔助 App", "進度%": 65, "工具": "Python/Scraping", "阻礙點": "API 限流", "差異化維度": "跨境醫療預填"},
        {"專案名稱": "心靈成長 App", "進度%": 42, "工具": "Rive/Figma", "阻礙點": "互動狀態機邏輯", "差異化維度": "沉浸式互動"},
        {"專案名稱": "法語學習專案", "進度%": 80, "工具": "DeepTranslator", "阻礙點": "語態變化", "差異化維度": "盧森堡語境特化"}
    ])

if 'history' not in st.session_state:
    st.session_state.history = []

# --- 側邊欄：功能切換與法文學習 ---
with st.sidebar:
    st.title("⚙️ 管理面板")
    mode = st.radio("選擇模式", ["📊 檢視看板", "📝 編輯專案內容"])
    
    st.write("---")
    st.header("🍎 法文自動化學習")
    with st.form("translation_form", clear_on_submit=True):
        user_input = st.text_input("請輸入中文單字")
        if st.form_submit_button("執行翻譯"):
            if user_input:
                res = GoogleTranslator(source='zh-TW', target='fr').translate(user_input).lower()
                st.session_state.history.append({"中文": user_input, "法文": res})
                st.success(f"✨ {res}")

# --- 主畫面邏輯 ---
st.title("🔭 內在座標 | Project Manager")

if mode == "📝 編輯專案內容":
    st.subheader("編輯模式：直接修改下方表格內容")
    # 使用 data_editor 讓表格變為可編輯
    edited_df = st.data_editor(st.session_state.project_db, num_rows="dynamic", use_container_width=True)
    if st.button("💾 儲存所有變更"):
        st.session_state.project_db = edited_df
        st.success("變更已成功存儲！")

else:
    # 檢視模式：原本的卡片美化介面
    st.subheader("📁 專案執行資料夾 (Folders)")
    cols = st.columns(3)
    for i, row in st.session_state.project_db.iterrows():
        with cols[i % 3]:
            with st.expander(f"**{row['專案名稱']}**", expanded=True):
                st.write(f"🛠️ 工具: {row['工具']}")
                st.write(f"🛑 阻礙: {row['阻礙點']}")
                st.progress(int(row['進度%']))
                st.caption(f"進度: {row['進度%']}% | 核心: {row['差異化維度']}")

# 下載練習紀錄
if st.session_state.history:
    st.download_button("📥 導出法文紀錄", pd.DataFrame(st.session_state.history).to_csv(index=False).encode('utf-8-sig'), "french.csv")
