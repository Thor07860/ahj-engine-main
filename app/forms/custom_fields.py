"""
Custom WTForms widget and field for tag-based multi-select in SQLAdmin
Handles relationship fields properly for FastAPI + SQLAdmin
"""
from wtforms.widgets import Select
from wtforms import SelectMultipleField
from wtforms.validators import DataRequired
from markupsafe import Markup, escape


class TagWidget(Select):
    """
    Custom widget that renders a tag/chip-based multi-select UI
    while maintaining a hidden select element for form submission
    """
    
    def __call__(self, field, **kwargs):
        """Render the tag input widget"""
        
        try:
            field_id = kwargs.get('id', field.id)
            tag_container_id = f"{field_id}_tag_container"
            
            # Build the hidden select element
            html_parts = []
            html_parts.append(f'<select id="{field_id}" name="{field.name}" multiple style="display: none;" data-tag-select="true">')
            
            # Safely iterate over choices
            try:
                for value, label, selected in field.iter_choices():
                    selected_attr = ' selected' if selected else ''
                    html_parts.append(f'<option value="{value}"{selected_attr}>{escape(label)}</option>')
            except Exception as e:
                # If choice iteration fails, continue without options
                # They will be populated by SQLAdmin later
                pass
            
            html_parts.append('</select>')
            
            # Build the tag container UI
            html_parts.append(f'''<div class="tag-input-wrapper" id="{tag_container_id}_wrapper">
                <div class="tag-input-container" id="{tag_container_id}" data-tag-container="{field_id}">
                </div>
                <div class="tag-dropdown-list" id="{tag_container_id}_dropdown" data-tag-dropdown="{field_id}">
                    <input type="text" class="tag-search-input" data-tag-search="{field_id}" placeholder="Search and click to add...">
                    <div class="tag-dropdown-items" data-tag-items="{field_id}">
                    </div>
                </div>
            </div>''')
            
            return Markup(''.join(html_parts))
        except Exception as e:
            # Fallback to default Select widget rendering
            return super().__call__(field, **kwargs)


class TagField(SelectMultipleField):
    """
    Minimal extension of SelectMultipleField that uses TagWidget
    """
    widget = TagWidget()
    
    def __init__(self, *args, **kwargs):
        """Initialize the tag field"""
        super().__init__(*args, **kwargs)





