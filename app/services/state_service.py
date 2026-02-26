from sqlalchemy.orm import Session
from app.models.state import State
from app.schemas.state import StateCreate, StateUpdate

class StateService:

    def create(self, db: Session, data: StateCreate):
        state = State(**data.dict())
        db.add(state)
        db.commit()
        db.refresh(state)
        return state

    def get(self, db: Session, state_id: int):
        return db.query(State).filter(State.id == state_id).first()

    def get_all(self, db: Session):
        return db.query(State).all()

    def update(self, db: Session, state_id: int, data: StateUpdate):
        state = self.get(db, state_id)
        if not state:
            return None
        for key, value in data.dict().items():
            setattr(state, key, value)
        db.commit()
        db.refresh(state)
        return state

    def delete(self, db: Session, state_id: int):
        state = self.get(db, state_id)
        if not state:
            return None
        db.delete(state)
        db.commit()
        return True