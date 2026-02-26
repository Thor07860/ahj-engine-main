from sqladmin import Admin, ModelView
from app.core.database import engine

from app.models.state import State
from app.models.ahj import AHJ
from app.models.utility import Utility
from app.models.code import Code
from app.models.note import Note
from app.models.formula import Formula
from app.models.label import Label
from app.models.code_type import CodeType
from app.models.combination_mapper import CombinationMapper


# -------------------------
# SQLAdmin Model Views
# -------------------------

class StateAdmin(ModelView, model=State):
    column_list = [State.id, State.name]


class AHJAdmin(ModelView, model=AHJ):
    column_list = [AHJ.id, AHJ.ahj_name]


class UtilityAdmin(ModelView, model=Utility):
    column_list = [Utility.id, Utility.utility_name]


class CodeAdmin(ModelView, model=Code):
    column_list = [Code.id, Code.code_name]


class LabelAdmin(ModelView, model=Label):
    column_list = [Label.id, Label.label_name]


class CodeTypeAdmin(ModelView, model=CodeType):
    # IMPORTANT: Your table field is 'name', not 'title'
    column_list = [
        CodeType.id,
        CodeType.key,
        CodeType.description
    ]


class CombinationMapperAdmin(ModelView, model=CombinationMapper):
    column_list = [
        CombinationMapper.id,
        CombinationMapper.code_id,
        CombinationMapper.label_id
    ]


class NoteAdmin(ModelView, model=Note):
    column_list = [Note.id, Note.code_id]
    form_widget_overrides = {
        "note_description": "textarea"
    }


class FormulaAdmin(ModelView, model=Formula):
    column_list = [Formula.id, Formula.code_id]
    form_widget_overrides = {
        "description": "textarea"
    }


# -------------------------
# Register Admin
# -------------------------

def setup_admin(app):
    admin = Admin(app, engine)

    admin.add_view(StateAdmin)
    admin.add_view(AHJAdmin)
    admin.add_view(UtilityAdmin)
    admin.add_view(CodeAdmin)
    admin.add_view(LabelAdmin)
    admin.add_view(CodeTypeAdmin)
    admin.add_view(CombinationMapperAdmin)

    admin.add_view(NoteAdmin)
    admin.add_view(FormulaAdmin)