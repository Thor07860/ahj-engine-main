from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserOut

class AuthAPI:
    def __init__(self):
        self.router = APIRouter()
        self.service = UserService()

        self.router.post("/register", response_model=UserOut)(self.register)
        self.router.post("/login")(self.login)

    def register(self, data: UserCreate, db: Session = Depends(get_db)):
        user = self.service.create_user(db, data.username, data.password)
        return user

    def login(self, data: UserCreate, db: Session = Depends(get_db)):
        user = self.service.authenticate(db, data.username, data.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        token = create_access_token({"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}