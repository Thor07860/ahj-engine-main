from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.auth_utils import hash_password, verify_password

class UserService:

    def create_user(self, db: Session, username: str, password: str):
        hashed = hash_password(password)
        user = User(username=username, password_hash=hashed)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def authenticate(self, db: Session, username: str, password: str):
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    def get_user(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()