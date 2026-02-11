import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from deep_translator import GoogleTranslator

# 1. 頁面配置
st.set_page_config(page_title="Solo Evolution Tracker Cloud", layout="wide")

# 2. 連接 Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 全域函數：確保讀取邏輯一致 ---
def get_data():
    """
    邏輯解析：
    worksheet: 必須與 Google Sheets 底部標籤名稱完全一致（例如 "工作表1"）
    ttl: 緩存時間，建議設定為 "1m" 以兼顧效能與即時性
    """
    return conn.read(worksheet="工作表1", ttl="1m")

# 3. 初始化資料 (確保 session_state 運作正常)
if 'projects' not in st.session_state:
    try:
        st.session_state.projects = get_data()
    except Exception as e:
        st.warning("目前無法從雲端讀取資料，請檢查 Secrets 設定。")
        # 備用初始數據
        st.session_state.projects = pd.DataFrame([
            {"專案名稱": "醫療輔助 App", "進度": 65, "工具": "Python", "阻礙": "無", "步驟": "流程分析", "排程": "2026-03-01"}
        ])

# --- 側邊欄與模式切換 ---
with st.sidebar:
    st.title("🛡️ 雲端控制台")
    mode = st.radio("功能切換", ["📊 檢視看板", "📝 編輯專案", "🍎 法文工具"])
    
    if st.button("🔄 同步雲端資料"):
        # 強制從雲端重新抓取
        st.session_state.projects = get_data()
        st.rerun()

# --- 主介面 ---
st.title("🔭 內在座標 | Cloud Project Manager")

if mode == "📊 檢視看板":
    df = st.session_state.projects
    if df is not None and not df.empty:
        cols = st.columns(3)
        for i, row in df.iterrows():
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"### {row['專案名稱']}")
                    # 確保進度是整數，避免 progress bar 報錯
                    progress_val = int(row['進度']) if pd.notnull(row['進度']) else 0
                    st.progress(min(max(progress_val, 0), 100))
                    
                    st.write(f"📅 **排程**: {row['排程']}")
                    st.write(f"🛑 **阻礙**: {row['阻礙']}")
                    with st.expander("查看行動細節"):
                        st.write(row['步驟'])
    else:
        st.info("目前沒有進行中的專案。")

elif mode == "📝 編輯專案":
    st.subheader("🛠️ 雲端編輯模式")
    st.info("提示：您可以直接在表格內修改、新增或刪除列（點擊表格右側或下方）。")
    
    # 使用 data_editor 實現自由化修改
    edited_df = st.data_editor(
        st.session_state.projects, 
        num_rows="dynamic", 
        use_container_width=True,
        key="project_editor"
    )
    
   # 儲存按鈕邏輯
    if st.button("💾 儲存並同步至 Google Sheets"):
        try:
            # --- 以下兩行必須比 try 縮排更深（4 個空格） ---
            conn.update(
                worksheet="工作表1",
                data=edited_df
            )
            st.session_state.projects = edited_df
            st.success("✅ 同步成功！雲端資料已更新。")
            st.balloons()
            
        except Exception as e:
            st.error(f"同步失敗！")
            st.info(f"技術診斷訊息: {e}")
