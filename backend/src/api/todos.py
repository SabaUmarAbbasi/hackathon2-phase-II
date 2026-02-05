from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import Optional
from backend.src.models.todo import TodoCreate, TodoRead, TodoUpdate, TodoList
from backend.src.database.database import get_session
from backend.src.auth.auth import get_current_user
from backend.src.models.user import User
from backend.src.services.todo_service import TodoService

router = APIRouter()

@router.get("/", response_model=TodoList)
def get_todos(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    status_filter: Optional[str] = Query(None, description="Filter by status (active, completed)"),
    sort: Optional[str] = Query("created_at", description="Sort by field"),
    order: Optional[str] = Query("desc", description="Sort order (asc, desc)"),
    limit: int = Query(20, ge=1, le=100, description="Number of results to return"),
    offset: int = Query(0, ge=0, description="Number of results to skip")
):
    """Get all todos for the authenticated user"""
    service = TodoService(session)
    todos, total = service.get_todos(
        user=current_user,
        status_filter=status_filter,
        sort=sort,
        order=order,
        limit=limit,
        offset=offset
    )
    
    return TodoList(
        todos=todos,
        total=total,
        limit=limit,
        offset=offset
    )


@router.post("/", response_model=TodoRead)
def create_todo(
    todo: TodoCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new todo for the authenticated user"""
    # Validate status
    if todo.status not in ["active", "completed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status. Use 'active' or 'completed'"
        )
    
    service = TodoService(session)
    db_todo = service.create_todo(todo, current_user.id)
    
    return db_todo


@router.get("/{id}", response_model=TodoRead)
def get_todo(
    id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific todo by ID"""
    # Convert string ID to UUID
    import uuid
    try:
        todo_id = uuid.UUID(id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid todo ID format"
        )
    
    service = TodoService(session)
    todo = service.get_todo(todo_id, current_user)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    return todo


@router.put("/{id}", response_model=TodoRead)
def update_todo(
    id: str,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update an existing todo"""
    # Convert string ID to UUID
    import uuid
    try:
        todo_id = uuid.UUID(id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid todo ID format"
        )
    
    service = TodoService(session)
    updated_todo = service.update_todo(todo_id, todo_update, current_user)
    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    return updated_todo


@router.delete("/{id}")
def delete_todo(
    id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a specific todo"""
    # Convert string ID to UUID
    import uuid
    try:
        todo_id = uuid.UUID(id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid todo ID format"
        )
    
    service = TodoService(session)
    deleted = service.delete_todo(todo_id, current_user)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    return {"message": "Todo deleted successfully"}