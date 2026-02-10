import streamlit as st
import pandas as pd
from datetime import datetime

# 頁面配置 (極簡風設定)
st.set_page_config(page_title="Project Logic Tracker", layout="wide")

# 初始化資料庫 (若無則建立範例)
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=[
        "類別", "行動項目", "優先級", "狀態", "進度%", "阻礙點", "工時(h)", "掌握度"
    ])

# --- 側邊欄：輸入區 ---
with st.sidebar:
    st.title("📂 專案控制台")
    st.subheader("錄入新行動")
    with st.form("input_form", clear_on_submit=True):
        category = st.selectbox("專案類別", ["醫療 App", "心靈成長 App", "法語學習"])
        action = st.text_input("具體行動內容")
        priority = st.select_slider("優先級", options=["P3", "P2", "P1", "P0"])
        status = st.selectbox("時程狀態", ["🟢 正常", "🟡 延遲", "🔴 嚴重阻塞"])
        progress = st.slider("完成進度 %", 0, 100, 0)
        blocker = st.text_input("阻礙點 (Blockers)")
        hours = st.number_input("投入時數", min_value=0.0, step=0.5)
        mastery = st.select_slider("知識掌握度", options=["L1", "L2", "L3"])
        
        submit = st.form_submit_button("新增至追蹤表")
        if submit and action:
            new_data = {
                "類別": category, "行動項目": action, "優先級": priority,
                "狀態": status, "進度%": progress, "阻礙點": blocker or "None",
                "工時(h)": hours, "掌握度": mastery
            }
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_data])], ignore_index=True)
            st.success("數據已同步")

# --- 主介面：視覺化儀表板 ---
st.title("🔭 內在座標 | 專案進度儀表板")
st.markdown("---")

# 數據摘要 (Top Metrics)
col1, col2, col3 = st.columns(3)
with col1:
    total_hours = st.session_state.db["工時(h)"].sum()
    st.metric("累計投入總時數", f"{total_hours} Hours")
with col2:
    avg_progress = st.session_state.db["進度%"].mean() if not st.session_state.db.empty else 0
    st.metric("平均執行進度", f"{avg_progress:.1f}%")
with col3:
    blockers_count = len(st.session_state.db[st.session_state.db["阻礙點"] != "None"])
    st.metric("待處理阻礙點", f"{blockers_count} Items")

# 區塊化呈現 (資料夾邏輯)
st.subheader("📁 項目明細")
for cat in ["醫療 App", "心靈成長 App", "法語學習"]:
    with st.expander(f"{cat} (查看詳情)", expanded=True):
        filtered_df = st.session_state.db[st.session_state.db["類別"] == cat]
        if not filtered_df.empty:
            # 增加進度條視覺化
            st.dataframe(filtered_df, use_container_width=True)
            # 簡易進度可視化
            current_pct = filtered_df["進度%"].mean()
            st.progress(int(current_pct))
        else:
            st.write("尚無行動數據")

# 差異化分析與反思 (Markdown)
st.markdown("---")
st.subheader("💡 產品分析與差異化維度")
st.info("目前的開發重點應聚焦於 **醫療 App 的翻譯邏輯** 與 **心靈成長 App 的 Rive 互動設計**。")
