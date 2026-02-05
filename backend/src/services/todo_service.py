from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from backend.src.models.todo import Todo, TodoCreate, TodoUpdate
from backend.src.models.user import User
from datetime import datetime

class TodoService:
    def __init__(self, session: Session):
        self.session = session

    def create_todo(self, todo_create: TodoCreate, user_id: UUID) -> Todo:
        """Create a new todo for a user"""
        db_todo = Todo(
            title=todo_create.title,
            description=todo_create.description,
            status=todo_create.status,
            user_id=user_id
        )
        
        self.session.add(db_todo)
        self.session.commit()
        self.session.refresh(db_todo)
        
        return db_todo

    def get_todos(
        self,
        user: User,
        status_filter: Optional[str] = None,
        sort: str = "created_at",
        order: str = "desc",
        limit: int = 20,
        offset: int = 0
    ) -> tuple[List[Todo], int]:
        """Get todos for a user with optional filtering and sorting"""
        # Build the query
        query = select(Todo).where(Todo.user_id == user.id)
        
        # Apply status filter if provided
        if status_filter:
            if status_filter in ["active", "completed"]:
                query = query.where(Todo.status == status_filter)
        
        # Apply sorting
        if sort == "created_at":
            if order == "asc":
                query = query.order_by(Todo.created_at.asc())
            else:
                query = query.order_by(Todo.created_at.desc())
        elif sort == "updated_at":
            if order == "asc":
                query = query.order_by(Todo.updated_at.asc())
            else:
                query = query.order_by(Todo.updated_at.desc())
        elif sort == "title":
            if order == "asc":
                query = query.order_by(Todo.title.asc())
            else:
                query = query.order_by(Todo.title.desc())
        
        # Count total for pagination
        total_query = select(Todo).where(Todo.user_id == user.id)
        if status_filter:
            if status_filter in ["active", "completed"]:
                total_query = total_query.where(Todo.status == status_filter)
        
        total = len(self.session.exec(total_query).all())
        
        # Apply pagination
        query = query.offset(offset).limit(limit)
        todos = self.session.exec(query).all()
        
        return list(todos), total

    def get_todo(self, todo_id: UUID, user: User) -> Optional[Todo]:
        """Get a specific todo by ID for a user"""
        todo = self.session.get(Todo, todo_id)
        if todo and todo.user_id == user.id:
            return todo
        return None

    def update_todo(self, todo_id: UUID, todo_update: TodoUpdate, user: User) -> Optional[Todo]:
        """Update a todo if it belongs to the user"""
        db_todo = self.session.get(Todo, todo_id)
        if not db_todo or db_todo.user_id != user.id:
            return None
        
        # Update fields if provided
        if todo_update.title is not None:
            db_todo.title = todo_update.title
        if todo_update.description is not None:
            db_todo.description = todo_update.description
        if todo_update.status is not None:
            if todo_update.status in ["active", "completed"]:
                db_todo.status = todo_update.status
        
        # Update timestamp
        db_todo.updated_at = datetime.utcnow()
        
        self.session.add(db_todo)
        self.session.commit()
        self.session.refresh(db_todo)
        
        return db_todo

    def delete_todo(self, todo_id: UUID, user: User) -> bool:
        """Delete a todo if it belongs to the user"""
        db_todo = self.session.get(Todo, todo_id)
        if not db_todo or db_todo.user_id != user.id:
            return False
        
        self.session.delete(db_todo)
        self.session.commit()
        
        return True