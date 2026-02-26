from sqlalchemy.orm import Session, joinedload
from app.models.state import State
from app.models.ahj import AHJ
from app.models.utility import Utility

class StateLookupService:

    def get_state_details(self, db: Session, abbrev: str):
        state = db.query(State).filter(State.abbrev == abbrev).first()
        if not state:
            return None

        # Fetch AHJs with utilities
        ahjs = db.query(AHJ).options(joinedload(AHJ.utilities)).filter(AHJ.state_id == state.id).all()

        ahj_list = []
        for ahj in ahjs:
            ahj_list.append({
                "id": ahj.id,
                "ahj_name": ahj.ahj_name,
                "utilities": [{"id": u.id, "utility_name": u.utility_name, "response_type": u.response_type} for u in ahj.utilities]
            })

        return {
            "abbrev": state.abbrev,
            "name": state.name,
            "ahjs": ahj_list
        }