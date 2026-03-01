# AHJ Engine - API Usage & Data Flow Guide

## Quick Start - Testing the API

### 1. Swagger Documentation
- Visit: http://127.0.0.1:8000/docs
- All endpoints documented with request/response schemas
- Try-it-out functionality available

### 2. Admin Panel
- Visit: http://127.0.0.1:8000/admin
- Browse/manage all data visually
- Create, edit, delete records
- No code required

---

## Example API Workflows

### Workflow 1: Create AHJ for a State

**Step 1: Get or Create a State**
```
POST /api/v1/states/create
{
  "name": "California",
  "abbrev": "CA",
  "fips_code": "06",
  "region": "West"
}
Response: { "id": 1, "name": "California", "abbrev": "CA", ... }
```

**Step 2: Create AHJ in that State**
```
POST /api/v1/ahj/create
{
  "name": "City of Los Angeles",
  "ahj_name": "Los Angeles AHJ",
  "state_id": 1,
  "county": "Los Angeles",
  "city": "Los Angeles",
  "guidelines": "<p>AHJ Guidelines for LA...</p>",
  "jurisdiction_type": "City",
  "phone": "555-0123",
  "email": "info@la.gov",
  "website": "https://la.gov"
}
Response: { "id": 1, "name": "City of Los Angeles", "state_id": 1, ... }
```

**Step 3: Get All AHJs**
```
GET /api/v1/ahj/
Response: [
  { "id": 1, "name": "City of Los Angeles", "state_id": 1, ... },
  ...
]
```

**Step 4: Update AHJ**
```
PUT /api/v1/ahj/1
{
  "email": "newemail@la.gov",
  "phone": "555-9999"
}
Response: { "id": 1, "name": "City of Los Angeles", "email": "newemail@la.gov", ... }
```

**Step 5: Delete AHJ**
```
DELETE /api/v1/ahj/1
Response: OK
```

---

### Workflow 2: Create Utility and Link to AHJ

**Step 1: Create Utility**
```
POST /api/v1/utility/create
{
  "name": "LA Water Department",
  "utility_name": "LAWD",
  "state_id": 1,
  "ahj_id": 1,
  "requirements": "<p>Utility requirements...</p>",
  "utility_type": "Water",
  "eia_id": "12345",
  "service_territory": "Los Angeles County",
  "phone": "555-WATER",
  "website": "https://lawater.gov"
}
Response: { "id": 1, "name": "LA Water Department", "ahj_id": 1, ... }
```

**Step 2: Link multiple utilities to same AHJ**
```
Create another utility with ahj_id: 1
Result: AHJ now has multiple utilities (one-to-many relationship)
```

**Step 3: Get all utilities in a state**
```
GET /api/v1/utility/
Response: [
  { "id": 1, "name": "LA Water Department", "state_id": 1, "ahj_id": 1, ... },
  ...
]
```

---

### Workflow 3: Create Building Code with Notes and Formulas

**Step 1: Create Code Type (reference data)**
```
POST /api/v1/code-type/create
{
  "title": "Building Code",
  "key": "BUILDING_CODE",
  "description": "International Building Code"
}
Response: { "id": 1, "title": "Building Code", "key": "BUILDING_CODE", ... }
```

**Step 2: Create Applicable Category (reference data)**
```
POST /api/v1/applicable-code-category/create
{
  "name": "Solar Installation"
}
Response: { "id": 1, "name": "Solar Installation" }
```

**Step 3: Create Code**
```
POST /api/v1/code/create
{
  "code_name": "2020 IBC",
  "title": "2020 International Building Code",
  "code_type_id": 1,
  "applicable_code_category_id": 1,
  "state_id": 1,
  "description": "<p>The 2020 International Building Code establishes...</p>",
  "edition": "2020",
  "issuing_body": "ICC",
  "adopted_at": "2022-01-01"
}
Response: { "id": 1, "code_name": "2020 IBC", "title": "2020 International Building Code", ... }
```

**Step 4: Add Notes to Code**
```
POST /api/v1/note/create
{
  "code_id": 1,
  "note_description": "<p>Important note about setback requirements...</p>",
  "page_no": 45,
  "section_no": 6,
  "length": 10.5,
  "width": 8.2
}
Response: { "id": 1, "code_id": 1, "note_description": "...", ... }
```

**Step 5: Add Formula to Code**
```
POST /api/v1/formula/create
{
  "code_id": 1,
  "title": "Setback Calculation",
  "description": "<p>Setback = Property Line - Building Envelope</p>"
}
Response: { "id": 1, "code_id": 1, "title": "Setback Calculation", ... }
```

---

### Workflow 4: Create Labels and Link to Codes

**Step 1: Create Label**
```
POST /api/v1/label/create
{
  "upc_code": "123456789012",
  "label_number": "LBL-001",
  "name": "Solar Panel Certificate",
  "label_name": "Solar Certification Label",
  "field_type": "Certificate",
  "description": "<p>Label for certified solar equipment...</p>",
  "image_url": "https://example.com/label.png",
  "background_color": "#FFFFFF",
  "text_color": "#000000",
  "is_active": true
}
Response: { "id": 1, "label_number": "LBL-001", "name": "Solar Panel Certificate", ... }
```

**Step 2: Link Code to Label via Combination Mapper**
```
POST /api/v1/combination-mapper/create
{
  "code_id": 1,
  "label_id": 1,
  "category_id": null,
  "equipment_id": null
}
Response: { "id": 1, "code_id": 1, "label_id": 1, ... }

Result: Code 1 now associated with Label 1
```

**Step 3: Add Equipment to Combination**
```
POST /api/v1/combination-mapper/create
{
  "code_id": 1,
  "label_id": 1,
  "category_id": null,
  "equipment_id": 1  (Solar Panel Equipment)
}
Response: { "id": 2, "code_id": 1, "label_id": 1, "equipment_id": 1, ... }

Result: Code 1 now applies to Label 1 specifically for Equipment 1
```

---

## Data Flow Diagram

```
Frontend/Client
    ↓
FastAPI Router (/api/v1/*)
    ↓
Schema Validation (Pydantic)
    ↓
Service Layer (Business Logic)
    ↓
ORM Models (SQLAlchemy)
    ↓
PostgreSQL Database
    ↓
Response back to Client
```

---

## Key Service Methods

### AHJ Service
```python
AHJService.create(db, AHJCreate)      # Create new AHJ
AHJService.get(db, ahj_id)            # Get single AHJ
AHJService.get_all(db)                # Get all AHJs
AHJService.update(db, ahj_id, data)   # Update AHJ
AHJService.delete(db, ahj_id)         # Delete AHJ
```

### State Service
```python
StateService.create(db, StateCreate)
StateService.get(db, state_id)
StateService.get_all(db)
StateService.update(db, state_id, data)
StateService.delete(db, state_id)
```

### Code Service
```python
CodeService.create(db, CodeCreate)
CodeService.get(db, code_id)
CodeService.get_all(db)
CodeService.update(db, code_id, data)
CodeService.delete(db, code_id)
```

*(Pattern repeated for Label, Note, Formula, Utility services)*

---

## Request/Response Schema Examples

### AHJ Schema
**Request (AHJCreate):**
```json
{
  "name": "string",
  "ahj_name": "string (optional)",
  "state_id": 1,
  "county": "string (optional)",
  "city": "string (optional)",
  "guidelines": "string (optional)",
  "fireset_back": 0.0,
  "jurisdiction_type": "string (optional)",
  "phone": "string (optional)",
  "email": "string (optional)",
  "website": "string (optional)"
}
```

**Response (AHJOut):**
```json
{
  "id": 1,
  "name": "string",
  "ahj_name": "string",
  "state_id": 1,
  "county": "string",
  "city": "string",
  "guidelines": "string",
  "fireset_back": 0.0,
  "jurisdiction_type": "string",
  "phone": "string",
  "email": "string",
  "website": "string",
  "created_at": "2026-02-28T00:00:00"
}
```

### Code Schema
**Request (CodeCreate):**
```json
{
  "code_name": "string",
  "title": "string",
  "code_type_id": 1,
  "code_amendments": 1,
  "description": "string (optional)",
  "edition": "string (optional)",
  "applicable_code_category_id": 1,
  "issuing_body": "string (optional)",
  "state_id": 1,
  "adopted_at": "2022-01-01"
}
```

### Label Schema
**Request (LabelCreate):**
```json
{
  "upc_code": "string (optional)",
  "name": "string (optional)",
  "label_number": "string",
  "label_name": "string",
  "field_type": "string (optional)",
  "description": "string (optional)",
  "length": 0,
  "width": 0,
  "image_url": "string (optional)",
  "background_color": "string (optional)",
  "text_color": "string (optional)",
  "is_active": true
}
```

---

## Database State After Example Workflows

If you execute all workflows above, you'd have:

**States:** 1 record (California)
**AHJs:** 1 record (Los Angeles)
**Utilities:** 1 record (LA Water Department)
**Code Types:** 1 record (Building Code)
**Codes:** 1 record (2020 IBC)
**Labels:** 1 record (Solar Panel Certificate)
**Notes:** 1 record (Setback requirements)
**Formulas:** 1 record (Setback Calculation)
**Combination Mapper:** 2 records (code-label, code-label-equipment)

---

## Admin Panel Features

### Available Admin Views
- States
- AHJs
- Utilities
- Codes
- Code Types
- Labels
- Notes
- Formulas
- Combination Mapper
- Clients
- Preferences

### Rich Text Editing
Labels with "is_active" field use toggle.
Text fields support CKEditor/TinyMCE for formatted content.
Custom templates: `sqladmin/richtext_edit.html` and `richtext_create.html`

### Bulk Operations
- View all records in paginated table
- Sort by any column
- Search/filter capabilities
- Edit multiple records
- Delete with confirmation

---

## Error Handling

Common HTTP responses:

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | GET, POST, PUT return data |
| 201 | Created | POST creates new resource |
| 204 | No Content | DELETE successful |
| 400 | Bad Request | Invalid schema |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Database issue |

Exception handler in `/app/core/error_handler.py` converts exceptions to HTTP responses.

---

## Authentication (Future Implementation)

**Location:** `/app/api/v1/auth_api.py`
**Security Module:** `/app/core/security.py`

Currently available but not enforced on endpoints.
JWT-based authentication ready for implementation.

---

## Performance Considerations

1. **Connection Pooling:** Pool size 20 for concurrent requests
2. **Session Management:** Auto-commit disabled, explicit transactions
3. **Relationships:** Lazy-loaded by default (optimize with joinedload if needed)
4. **Indexes:** Primary keys and unique constraints indexed automatically
5. **Query Building:** ORM builds efficient SQL statements

---

## Data Import Strategy

For production data population:

1. **Import States** - One-time setup
2. **Import AHJs** - Link to states
3. **Import Code Types** - Reference data
4. **Import Codes** - Link to code types, states
5. **Import Labels** - Independent setup
6. **Import Utilities** - Link to AHJs, states
7. **Import Notes** - Link to codes
8. **Import Formulas** - Link to codes
9. **Build Combinations** - Link codes, labels, equipment via mapper

---

## Testing Example Requests with cURL

```bash
# Create State
curl -X POST "http://127.0.0.1:8000/api/v1/states/" \
  -H "Content-Type: application/json" \
  -d '{"name":"California","abbrev":"CA","fips_code":"06","region":"West"}'

# Create AHJ
curl -X POST "http://127.0.0.1:8000/api/v1/ahj/create" \
  -H "Content-Type: application/json" \
  -d '{"name":"City of LA","state_id":1,"city":"Los Angeles"}'

# Get all AHJs
curl -X GET "http://127.0.0.1:8000/api/v1/ahj/"

# Update AHJ
curl -X PUT "http://127.0.0.1:8000/api/v1/ahj/1" \
  -H "Content-Type: application/json" \
  -d '{"email":"new@la.gov"}'

# Delete AHJ
curl -X DELETE "http://127.0.0.1:8000/api/v1/ahj/1"
```

