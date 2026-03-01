# Tag Input UI Implementation for SQLAdmin

This document describes the complete implementation of a custom tag/chip-based multi-select UI for SQLAdmin in FastAPI.

## Overview

The implementation replaces default multi-select dropdowns with a modern, clean tag-based interface. Selected items appear as removable chips/tags inside a textbox, with a searchable dropdown for selection.

## Architecture

### 1. **Custom WTForms Widget & Field** (`app/forms/custom_fields.py`)

#### `TagWidget`
- Renders the hidden `<select multiple>` element
- Creates the tag container UI with HTML structure
- Provides JavaScript data attributes for targeting

#### `TagField(SelectMultipleField)`
- Extends WTForms' SelectMultipleField
- Properly coerces between model instances and IDs
- Handles SQLAdmin relationship data conversion
- Supports data binding and form submission

**Key Features:**
- Handles both SQLAlchemy model instances and raw IDs
- Automatic conversion from model objects to IDs
- Proper form data processing for submission

### 2. **Styling** (`app/static/sqladmin_custom.css`)

Comprehensive CSS for:
- Tag container and individual tags
- Dropdown styling with smooth animations
- Search input styling
- Responsive design
- Color picker minimization (80px width)
- Clean form aesthetics

### 3. **JavaScript** (`app/static/tag_input.js`)

#### `TagInputManager` Class
Manages tag input lifecycle:

**Methods:**
- `init()` - Initialize the tag input system
- `renderTags()` - Render selected items as tags
- `renderOptions()` - Render dropdown options with search
- `toggleOption()` - Add/remove selections
- `removeTag()` - Remove a specific tag
- `updateSelectElement()` - Sync hidden select for form submission
- `attachEventListeners()` - Bind all interactions

**Features:**
- Click to expand dropdown
- Type to search/filter options
- Click outside to close dropdown
- Keyboard navigation (ESC to close)
- Checkmark indicator for selected items
- Smooth animations

### 4. **Admin Configuration** (`app/admin/admin.py`)

```python
class StateAdmin(ModelView, model=State):
    column_list = [State.id, State.abbrev, State.name]
    
    form_overrides = {
        'ahjs': TagField,
        'utilities': TagField,
        'clients': TagField,
    }
    
    form_args = {
        'ahjs': {'label': 'AHJs (Authority Having Jurisdictions)', 'coerce': int},
        'utilities': {'label': 'Utilities', 'coerce': int},
        'clients': {'label': 'Clients', 'coerce': int},
    }
```

## Usage

### For Existing Fields

To apply tag UI to any relationship field in SQLAdmin:

1. **Import TagField:**
   ```python
   from app.forms import TagField
   ```

2. **Add to form_overrides:**
   ```python
   class YourAdmin(ModelView, model=YourModel):
       form_overrides = {
           'your_relationship_field': TagField,
       }
       
       form_args = {
           'your_relationship_field': {
               'label': 'Display Label',
               'coerce': int,
           }
       }
   ```

### For New Fields

When creating new relationship fields that need tag UI, use the same pattern.

## How It Works

### Data Flow

1. **On Load:**
   - SQLAdmin generates form with hidden select element + tag UI
   - JavaScript detects `data-tag-select` attribute
   - `TagInputManager` initializes
   - Existing selections render as tags

2. **On Selection:**
   - User clicks tag container → dropdown opens
   - User types to filter options
   - User clicks option → tag added
   - Hidden select element updated
   - Dropdown re-renders

3. **On Removal:**
   - User clicks × on tag
   - Tag removed from state
   - Hidden select updated
   - Re-renders

4. **On Submission:**
   - Form submits
   - Hidden select values sent to server
   - SQLAdmin saves relationships normally

## UI Component Breakdown

### Tag Container
```
┌─────────────────────────────────────────┐
│ [Tag 1] [Tag 2] [Tag 3]        ▼       │
│ (click to open dropdown)                 │
└─────────────────────────────────────────┘
```

### Dropdown (when open)
```
┌─────────────────────────────────────────┐
│ [Search box                           ] │
├─────────────────────────────────────────┤
│ ✓ Selected Item 1                       │
│   Unselected Item 2                     │
│   Unselected Item 3                     │
│   Item Matching Search                  │
└─────────────────────────────────────────┘
```

## CSS Classes

### Component Classes
- `.tag-input-wrapper` - Outer container
- `.tag-input-container` - Tag display box
- `.tag-dropdown-list` - Dropdown container
- `.tag` - Individual tag
- `.tag-remove` - Remove button on tag
- `.tag-dropdown-item` - Dropdown option
- `.tag-search-input` - Search field

### State Classes
- `.active` - Dropdown visible
- `.selected` - Option is selected
- `.highlighted` - Option hovered

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile responsive design
- Touch-friendly interactions

## Customization

### Colors
Edit `/app/static/sqladmin_custom.css`:
- Tag background: `.tag { background: #4f46e5; }`
- Highlight color: `.tag-input-container:focus-within { border-color: #4f46e5; }`

### Animation Speed
- Fade in/out: `animation: slideIn 0.2s ease;`
- Dropdown: `animation: dropdownOpen 0.15s ease;`

### Max Dropdown Height
- Default: `max-height: 300px;`
- Edit in CSS: `.tag-dropdown-list { max-height: 400px; }`

## Performance Considerations

- No DOM recreation for existing tag elements
- Efficient filtering using native Set/Array operations
- Event delegation for dropdown items
- Minimal re-renders
- No external dependencies (pure JavaScript)

## Troubleshooting

### Tags Not Showing
1. Verify CSS is loaded: Check network tab for `sqladmin_custom.css`
2. Verify JavaScript is loaded: Check for `tag_input.js`
3. Check browser console for errors
4. Verify `data-tag-select` attribute on hidden select

### Selection Not Persisting
1. Verify hidden select element is being updated
2. Check form submission in browser network tab
3. Verify SQLAdmin form values are being sent

### Dropdown Not Opening
1. Verify JavaScript is running (check console)
2. Check if CSS `display: flex` is applied on `.active`
3. Inspect element to verify HTML structure

## Files Modified/Created

```
app/forms/
├── __init__.py (created)
└── custom_fields.py (created)

app/admin/
└── admin.py (modified - added StateAdmin config)

app/static/
├── sqladmin_custom.css (modified)
└── tag_input.js (modified)

templates/sqladmin/
├── richtext_create.html (includes CSS/JS)
└── richtext_edit.html (includes CSS/JS)
```

## Integration Notes

- Works with FastAPI + SQLAdmin backend
- No server-side changes required beyond admin config
- Fully backward compatible
- Can be applied incrementally to different models
- Form data uses standard HTML form submission

---

**Version:** 1.0
**Last Updated:** March 1, 2026
