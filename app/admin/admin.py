from sqladmin import Admin, ModelView
<<<<<<< HEAD
from app.core.database import engine, SessionLocal
from app.forms import TagField
from wtforms import SelectField
from wtforms.validators import Optional
from sqlalchemy import text
=======
from app.core.database import engine
>>>>>>> 143acc3fd81c11943810fcb3a8f4ec99f21425af

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

<<<<<<< HEAD
=======
class StateAdmin(ModelView, model=State):
    column_list = [State.id, State.abbrev, State.name]


>>>>>>> 143acc3fd81c11943810fcb3a8f4ec99f21425af
class RichTextModelView(ModelView):
    create_template = "sqladmin/richtext_create.html"
    edit_template = "sqladmin/richtext_edit.html"


<<<<<<< HEAD
class StateAdmin(RichTextModelView, model=State):
    column_list = [State.id, State.abbrev, State.name]
    # Using native multi-select fields - will be transformed to tag UI by JavaScript
    # form_overrides = {'ahjs': TagField, 'utilities': TagField, 'clients': TagField}


=======
>>>>>>> 143acc3fd81c11943810fcb3a8f4ec99f21425af
class AHJAdmin(RichTextModelView, model=AHJ):
    column_list = [AHJ.id, AHJ.name, AHJ.state_id, AHJ.city, AHJ.county]


class UtilityAdmin(RichTextModelView, model=Utility):
    column_list = [Utility.id, Utility.name, Utility.state_id, Utility.ahj_id, Utility.utility_type]


class CodeAdmin(RichTextModelView, model=Code):
    column_list = [Code.id, Code.title, Code.edition, Code.code_type_id, Code.code_amendments]


class LabelAdmin(RichTextModelView, model=Label):
    column_list = [Label.id, Label.upc_code, Label.name, Label.is_active]
<<<<<<< HEAD
    
    # Define form widget arguments for color pickers
=======
>>>>>>> 143acc3fd81c11943810fcb3a8f4ec99f21425af
    form_widget_args = {
        "background_color": {
            "type": "color",
            "value": "#ffffff",
<<<<<<< HEAD
            "style": "width: 80px; height: 45px;",
=======
>>>>>>> 143acc3fd81c11943810fcb3a8f4ec99f21425af
        },
        "text_color": {
            "type": "color",
            "value": "#000000",
<<<<<<< HEAD
            "style": "width: 80px; height: 45px;",
        },
    }
    
    # Override form fields with SelectField
    form_overrides = {
        "upc_code": SelectField,
        "label_number": SelectField,
        "label_name": SelectField,
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Generate dynamic choices from database
        db_session = SessionLocal()
        
        try:
            # Get all unique UPC codes
            upc_codes_query = db_session.execute(
                text('SELECT DISTINCT upc_code FROM labels WHERE upc_code IS NOT NULL ORDER BY upc_code')
            ).fetchall()
            upc_code_choices = [("", "-- Select --")] + [(str(uc[0]), str(uc[0])) for uc in upc_codes_query]
            
            # Get all unique label_number values
            label_numbers_query = db_session.execute(
                text('SELECT DISTINCT label_number FROM labels WHERE label_number IS NOT NULL ORDER BY label_number')
            ).fetchall()
            label_number_choices = [("", "-- Select --")] + [(str(ln[0]), str(ln[0])) for ln in label_numbers_query]
            
            # Get all unique label_name values  
            label_names_query = db_session.execute(
                text('SELECT DISTINCT label_name FROM labels WHERE label_name IS NOT NULL ORDER BY label_name')
            ).fetchall()
            label_name_choices = [("", "-- Select --")] + [(str(ln[0][:100]), str(ln[0][:100])) for ln in label_names_query]
            
        except Exception as e:
            print(f"Warning: Could not load dynamic label choices: {e}")
            upc_code_choices = [("", "-- Select --")]
            label_number_choices = [("", "-- Select --")]
            label_name_choices = [("", "-- Select --")]
        finally:
            db_session.close()
        
        # Set form_args
        self.form_args = {
            "upc_code": {
                "choices": upc_code_choices,
                "validators": [Optional()],
            },
            "label_number": {
                "choices": label_number_choices,
                "validators": [Optional()],
            },
            "label_name": {
                "choices": label_name_choices,
                "validators": [Optional()],
            },
        }
    
    # Reorder fields - move color fields to the end
    form_columns = [
        "upc_code",
        "name",
        "label_number",
        "label_name",
        "description",
        "length",
        "width",
        "image_url",
        "is_active",
        "background_color",
        "text_color",
    ]


class CodeTypeAdmin(RichTextModelView, model=CodeType):
=======
        },
    }


class CodeTypeAdmin(ModelView, model=CodeType):
>>>>>>> 143acc3fd81c11943810fcb3a8f4ec99f21425af
    column_list = [
        CodeType.id,
        CodeType.title,
        CodeType.key,
        CodeType.description
    ]


<<<<<<< HEAD
class CombinationMapperAdmin(RichTextModelView, model=CombinationMapper):
=======
class CombinationMapperAdmin(ModelView, model=CombinationMapper):
>>>>>>> 143acc3fd81c11943810fcb3a8f4ec99f21425af
    column_list = [
        CombinationMapper.id,
        CombinationMapper.code_id,
        CombinationMapper.label_id
    ]


class NoteAdmin(RichTextModelView, model=Note):
    column_list = [Note.id, Note.code_id]


class FormulaAdmin(RichTextModelView, model=Formula):
    column_list = [Formula.id, Formula.code_id]


# -------------------------
# Register Admin
# -------------------------

def setup_admin(app):
    admin = Admin(
        app,
        engine,
        title="Admin",
        logo_url="https://res.cloudinary.com/dikq4mtrh/image/upload/v1762442702/illumine_logo_lmi7yw.png",
    )

    admin.add_view(StateAdmin)
    admin.add_view(AHJAdmin)
    admin.add_view(UtilityAdmin)
    admin.add_view(CodeAdmin)
    admin.add_view(LabelAdmin)
    admin.add_view(CodeTypeAdmin)
    admin.add_view(CombinationMapperAdmin)

    admin.add_view(NoteAdmin)
    admin.add_view(FormulaAdmin)