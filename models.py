from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

# 1. 專案層級模型
class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    deadline: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    tasks: List["Task"] = Relationship(back_populates="project")

# 2. 任務層級模型
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    title: str
    status: str = "todo"
    est_hours: float
    project: Project = Relationship(back_populates="tasks")
    logs: List["Log"] = Relationship(back_populates="task")

# 3. 歷程日誌模型
class Log(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")
    duration: float
    progress_val: int
    note: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    task: Task = Relationship(back_populates="logs")
