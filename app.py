import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

# 1. 頁面極簡風配置
st.set_page_config(page_title="Solo Evolution Tracker", layout="wide")

# 2. 核心邏輯：道地法文庫
NATIVE_PHRASES = {
    "肚子": "J'ai du ventre. (我有小腹 / 最常用)",
    "贅肉": "J'ai un peu de brioche. (法式幽默用法)",
    "麵包店": "la boulangerie",
    "咖啡廳": "le café",
    "減肥": "Je fais attention à ma ligne. (我在注意身材/減肥中)"
}

def translate_logic(text):
    if text in NATIVE_PHRASES:
        return NATIVE_PHRASES[text]
    try:
        return GoogleTranslator(source='zh-TW', target='fr').translate(text).lower()
    except:
        return "翻譯服務暫時離線"

# 3. 初始化資料暫存
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 側邊欄：法文 App 功能區 ---
with st.sidebar:
    st.title("🍎 法文自動化學習")
    st.write("輸入中文聯想詞，自動產出法文並記錄")
    
    with st.form("translation_form", clear_on_submit=True):
        user_input = st.text_input("請輸入中文單字")
        submitted = st.form_submit_button("執行翻譯並存檔")
        
        if submitted and user_input:
            result = translate_logic(user_input)
            st.session_state.history.append({"中文": user_input, "法文": result})
            st.success(f"✨ {result}")

    if st.session_state.history:
        st.write("---")
        st.subheader("📚 本次練習清單")
        st.table(pd.DataFrame(st.session_state.history))

# --- 主畫面：專案看板 (資料夾形式) ---
st.title("🔭 內在座標 | Project Manager")
st.markdown("---")

# 這裡是你關注的三大核心專案
projects = [
    {"name": "醫療輔助 App", "pct": 65, "tool": "Python/Scraping", "blocker": "API 限流", "diff": "跨境醫療預填"},
    {"name": "心靈成長 App", "pct": 42, "tool": "Rive/Figma", "blocker": "互動狀態機邏輯", "diff": "沉浸式互動"},
    {"name": "法語學習專案", "pct": 80, "tool": "DeepTranslator", "blocker": "語態變化", "diff": "盧森堡語境特化"}
]

st.subheader("📁 專案執行資料夾 (Folders)")
cols = st.columns(3)
for i, p in enumerate(projects):
    with cols[i]:
        with st.expander(f"**{p['name']}**", expanded=True):
            st.write(f"🛠️ 工具: {p['tool']}")
            st.write(f"🛑 阻礙: {p['blocker']}")
            st.progress(p['pct'])
            st.caption(f"進度: {p['pct']}%")

# 下載練習紀錄
if st.session_state.history:
    csv = pd.DataFrame(st.session_state.history).to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 導出今日練習紀錄 (.csv)", data=csv, file_name="french_practice.csv")
