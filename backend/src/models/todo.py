from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid

class TodoBase(SQLModel):
    title: str
    description: Optional[str] = None
    status: str = Field(default="active")


class Todo(TodoBase, table=True):
    __tablename__ = "todos"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    description: Optional[str] = None
    status: str = Field(default="active")  # We'll validate this in the service layer
    user_id: uuid.UUID = Field(foreign_key="users.id")
    created_at: datetime = Field(default=datetime.utcnow())
    updated_at: datetime = Field(default=datetime.utcnow())


class TodoCreate(TodoBase):
    pass


class TodoRead(TodoBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class TodoUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None  # Will be validated in the service layer


class TodoList(SQLModel):
    todos: list[TodoRead]
    total: int
    limit: int
    offset: int