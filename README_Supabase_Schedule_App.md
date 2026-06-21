# 個人行事曆 APP - Supabase 版本

## 如何使用

1. 在 Supabase 建立新 Project
2. 在 SQL Editor 執行 `supabase_schedule_schema.sql`
3. 設定 Row Level Security (RLS)：
   - 所有 table 啟用 RLS
   - Policies: user can only access their own data (using auth.uid())

4. 前端開發建議（React / Next.js / Flutter）

## 推薦前端 Tech Stack
- Next.js 14 + TypeScript
- Supabase JS Client
- Tailwind CSS + shadcn/ui (美觀行事曆)
- React Calendar 或 FullCalendar

## 主要功能已涵蓋
- 每日/每週自動載入模板
- 打卡完成度
- 16:8 飲食提醒
- 語言 & 作品追蹤
- 盧森堡求職管理
- 每週回顧
