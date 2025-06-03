# Simple authentication and user roles for demonstration
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from pydantic import BaseModel

# In-memory user store for demo
users_db = {
    "student@mergington.edu": {"username": "student@mergington.edu", "password": "studentpass", "role": "student"},
    "admin@mergington.edu": {"username": "admin@mergington.edu", "password": "adminpass", "role": "admin"},
    "faculty@mergington.edu": {"username": "faculty@mergington.edu", "password": "facultypass", "role": "faculty"}
}

class User(BaseModel):
    username: str
    role: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def fake_decode_token(token: str) -> Optional[User]:
    user = users_db.get(token)
    if user:
        return User(username=user["username"], role=user["role"])
    return None

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def require_role(role: str):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_checker
