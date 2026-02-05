from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from datetime import timedelta
from backend.src.models.user import UserCreate, UserRead, User
from backend.src.database.database import get_session
from backend.src.auth.auth import authenticate_user, create_access_token, get_password_hash
from typing import Dict

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    """Register a new user"""
    # Check if user already exists
    existing_user = session.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    # Hash the password
    hashed_password = get_password_hash(user.password)
    
    # Create new user
    db_user = User(
        email=user.email,
        password_hash=hashed_password
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user


@router.post("/login")
def login_user(form_data: UserCreate, session: Session = Depends(get_session)):
    """Authenticate user and return JWT token"""
    user = authenticate_user(session, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 30 * 60  # 30 minutes in seconds
    }


@router.post("/logout")
def logout_user():
    """Logout user (client-side token removal is sufficient)"""
    # In a stateless JWT system, logout is typically handled client-side
    # by removing the token from storage. For enhanced security, you could
    # implement a token blacklist mechanism here.
    return {"message": "Logged out successfully"}