from sqlmodel import SQLModel, create_engine, Session, select
from models import Project, Task, Log  # 假設你已將模型放入 models.py

# 1. 建立資料庫引擎 (使用 SQLite 進行本地測試)
sqlite_file_name = "evolution.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def add_demo_data():
    with Session(engine) as session:
        # 建立專案
        my_project = Project(title="AI 學習專案", deadline="2026-12-31")
        session.add(my_project)
        session.commit()
        
        # 建立任務並關聯專案
        my_task = Task(title="Python 自動化設計", est_hours=20, project_id=my_project.id)
        session.add(my_task)
        session.commit()
        
        # 建立過程日誌
        log = Log(task_id=my_task.id, duration=2.5, progress_val=15, note="完成基礎開發環境配置")
        session.add(log)
        session.commit()
        print("Demo 資料已寫入！")

def get_project_progress():
    with Session(engine) as session:
        statement = select(Task).where(Task.project_id == 1)
        results = session.exec(statement).all()
        for task in results:
            print(f"任務: {task.title}, 進度: {task.status}")

if __name__ == "__main__":
    create_db_and_tables()
    add_demo_data()
    get_project_progress()
