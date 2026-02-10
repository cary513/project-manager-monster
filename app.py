import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

# 1. 頁面配置
st.set_page_config(page_title="Solo Evolution Tracker Pro", layout="wide")

# 2. 初始化資料庫 (Session State)
# 使用字典結構來支援「專案 > 步驟」的階層
if 'projects' not in st.session_state:
    st.session_state.projects = {
        "醫療輔助 App": {
            "進度": 65, "工具": "Python/Scraping", "阻礙點": "API 限流",
            "步驟": ["爬蟲腳本撰寫", "翻譯邏輯串接", "UI 原型設計"],
            "排程": "2026-03-01"
        },
        "心靈成長 App": {
            "進度": 42, "工具": "Rive/Figma", "阻礙點": "狀態機邏輯",
            "步驟": ["品牌核心定義", "Rive 動畫製作", "社交破冰邏輯"],
            "排程": "2026-04-15"
        },
        "法語學習": {
            "進度": 80, "工具": "DeepTranslator", "阻礙點": "語法複雜度",
            "步驟": ["B1 動詞變位", "盧森堡職場用語", "聽力模擬練習"],
            "排程": "2026-02-28"
        }
    }

# --- 側邊欄：法文與功能切換 ---
with st.sidebar:
    st.title("⚙️ 控制中心")
    mode = st.radio("功能切換", ["📋 檢視看板", "🛠️ 專案架構編輯", "🍎 法文工具"])
    st.markdown("---")
    if mode == "🍎 法文工具":
        user_input = st.text_input("輸入中文單字")
        if st.button("翻譯"):
            res = GoogleTranslator(source='zh-TW', target='fr').translate(user_input)
            st.success(f"✨ {res}")

# --- 主畫面邏輯 ---
st.title("🔭 內在座標 | Project Logic System")

# A. 檢視看板模式 (排程視角)
if mode == "📋 檢視看板":
    st.subheader("🗓️ 專案排程與進度綜覽")
    cols = st.columns(len(st.session_state.projects))
    for i, (p_name, p_data) in enumerate(st.session_state.projects.items()):
        with cols[i]:
            with st.container(border=True):
                st.markdown(f"### {p_name}")
                st.caption(f"📅 預計完成: {p_data['排程']}")
                st.progress(int(p_data['進度']))
                st.write(f"**下一階段步驟:**")
                for step in p_data['步驟'][:2]: # 只顯示前兩個步驟
                    st.write(f"- {step}")
                if st.button(f"進入 {p_name} 詳情", key=f"view_{p_name}"):
                    st.session_state.current_p = p_name

# B. 專案架構編輯 (自由增減欄位與層級)
elif mode == "🛠️ 專案架構編輯":
    st.subheader("📝 結構管理：編輯專案、步驟與自定義屬性")
    
    # 選項：新增專案
    with st.expander("➕ 新增全新專案"):
        new_p_name = st.text_input("專案名稱")
        if st.button("建立專案"):
            st.session_state.projects[new_p_name] = {"進度": 0, "工具": "", "阻礙點": "", "步驟": [], "排程": ""}
            st.rerun()

    st.markdown("---")
    
    # 編輯現有專案內容
    target_p = st.selectbox("選擇要編輯的專案", list(st.session_state.projects.keys()))
    p_content = st.session_state.projects[target_p]
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("#### 1. 核心屬性編輯")
        p_content["進度"] = st.slider("進度 %", 0, 100, int(p_content["進度"]))
        p_content["排程"] = st.text_input("排程 (YYYY-MM-DD)", p_content["排程"])
        p_content["工具"] = st.text_input("使用工具", p_content["工具"])
        p_content["阻礙點"] = st.text_area("阻礙點 (Blockers)", p_content["阻礙點"])
        
    with col2:
        st.write("#### 2. 下一層級：具體行動步驟")
        # 顯示並編輯步驟
        new_steps = st.text_area("編輯步驟 (每行一個步驟)", value="\n".join(p_content["步驟"]))
        p_content["步驟"] = new_steps.split("\n") if new_steps else []
        
    if st.button(f"💾 儲存 {target_p} 的變更"):
        st.session_state.projects[target_p] = p_content
        st.success("更新成功！")
        
    if st.button(f"🗑️ 刪除整個 {target_p} 專案"):
        del st.session_state.projects[target_p]
        st.rerun()
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
        # 建立連接並更新，自動尋找第一個工作表
        conn.update(
            spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"],
            data=edited_df
        )
        st.session_state.projects = edited_df
        st.success("✅ 雲端同步成功！你可以打開試算表查看即時更新。")
    except Exception as e:
        st.error(f"同步失敗！請確認 Google Sheets 是否已開啟『編輯者』權限。")
        st.info(f"技術錯誤訊息: {e}")


elif mode == "🍎 法文工具":
    # (保留你原本的翻譯邏輯代碼...)
    pass
