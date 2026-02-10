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
