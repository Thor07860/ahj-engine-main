# AHJ Engine - Excel Import & Data Flow Guide

## Quick Start - Running the Import

```bash
# From project root directory
python scripts/import/import_labels.py
```

### What it does:
1. **Loads Labels** from `app/data/master/Illumine-i X LabelFriday master data.xlsx`
   - Creates Label records with UPC codes, label numbers, names
   - Validates duplicates by `label_number`

2. **Loads Categories & Equipment** from `app/data/master/Label filter data.xlsx`
   - Creates Category records (if new)
   - Creates Equipment records (if new)
   - Links them through CombinationMapper

3. **Reports Results** with detailed logging
   - Shows created vs skipped records
   - Lists any errors encountered
   - Provides next steps

---

## Expected Excel File Formats

### File 1: `Illumine-i X LabelFriday master data.xlsx`

| Column | Type | Required | Notes |
|--------|------|----------|-------|
| `upc_code` | String | No | Barcode identifier, must be unique |
| `label_number` | String | **YES** | Primary identifier, must be unique |
| `label_name` | String | **YES** | Display name for the label |
| `name` | String | No | Alternative name |
| `field_type` | String | No | Classification (e.g., "Certificate", "Mark") |
| `description` | String | No | Rich text details/specifications |

**Example:**
```
upc_code         | label_number | label_name              | name      | field_type     | description
123456789012     | LBL-SOLAR-01 | Solar Panel Certificate | SPC       | Certificate    | UL listed solar equipment
987654321098     | LBL-WIND-01  | Wind Gen License        | WGL       | License        | Wind turbine certification
```

### File 2: `Label filter data.xlsx`

| Column | Type | Required | Notes |
|--------|------|----------|-------|
| `category` | String | No | Equipment category (creates if not exists) |
| `equipment` | String | No | Equipment type (creates if not exists) |
| `label_number` | String | **YES** | Link to label from File 1 |
| `code_name` | String | No | Link to existing code (optional) |

**Example:**
```
category    | equipment      | label_number   | code_name
Residential | Solar Panel    | LBL-SOLAR-01   | 2020 IBC
Residential | Inverter       | LBL-SOLAR-01   | 2020 IBC
Commercial  | Grid Tie       | LBL-WIND-01    | 2020 IECC
```

---

## Data Model Relationships

```
STATES (1) ──────> (many) AHJS ──────> (many) UTILITIES
   ↓
(many) CODES
   ↓
COMBINATION_MAPPER (junction table)
   ├─→ CODE_ID (FK)
   ├─→ LABEL_ID (FK)
   ├─→ CATEGORY_ID (FK, optional)
   └─→ EQUIPMENT_ID (FK, optional)
   
LABELS ──────> COMBINATION_MAPPER ──────> CATEGORIES
                                      └──→ EQUIPMENT
                                      
CODES ──────> NOTES, FORMULAS
```

---

## API Data Flow

### 1. Main Endpoint: `/api/v1/ahj-engine/get-ahj-details`

**Request:**
```json
{
  "ahj_name": "City of Los Angeles",
  "electrical_code": "2020 IBC",
  "structural_code": "2020 IBC",
  "fire_code": "2020 IBC"
}
```

**Processing Flow:**
```
1. Look up AHJ by name
   └─> db.query(AHJ).filter(AHJ.ahj_name == "City of Los Angeles").first()

2. For each code (electrical, structural, fire):
   a. Look up Code by code_name
      └─> db.query(Code).filter(Code.code_name == "2020 IBC").first()
   
   b. Find all related data:
      ├─ Labels: Via CombinationMapper
      │  └─> db.query(CombinationMapper)
      │       .filter(CombinationMapper.code_id == code.id).all()
      │       └─> Get Label.id → query Labels
      │
      ├─ Notes: Direct relationship
      │  └─> db.query(Note)
      │       .filter(Note.code_id == code.id).all()
      │
      └─ Formulas: Direct relationship
         └─> db.query(Formula)
             .filter(Formula.code_id == code.id).all()

3. Format and return CodeDetail with all related data
```

**Response:**
```json
{
  "ahj_name": "City of Los Angeles",
  "electrical": {
    "code_name": "2020 IBC",
    "labels": [
      {
        "id": 1,
        "label_name": "Solar Panel Certificate",
        "field_type": "Certificate"
      },
      {
        "id": 2,
        "label_name": "Wind Gen License",
        "field_type": "License"
      }
    ],
    "notes": [
      "Important note about setback requirements...",
      "Solar equipment must be UL listed..."
    ],
    "formulas": [
      "Setback = Property Line - Building Envelope",
      "Max Height = 1.5x Lot Width"
    ]
  },
  "structural": { ... },
  "fire": { ... }
}
```

---

## SQL Query Examples - How Imported Data Powers the API

### Query 1: Get All Labels for a Code
```sql
SELECT l.* 
FROM labels l
JOIN combination_mapper cm ON l.id = cm.label_id
WHERE cm.code_id = ?
```

**Mapped from:**
```python
mappings = db.query(CombinationMapper).filter(
    CombinationMapper.code_id == code_obj.id
).all()

label_ids = [m.label_id for m in mappings]
labels = db.query(Label).filter(Label.id.in_(label_ids)).all()
```

### Query 2: Get Categories & Equipment for a Label
```sql
SELECT c.name as category, e.name as equipment
FROM combination_mapper cm
LEFT JOIN categories c ON cm.category_id = c.id
LEFT JOIN equipment e ON cm.equipment_id = e.id
WHERE cm.label_id = ?
```

**Mapped from:**
```python
# From AHJ Engine Service
mappings = db.query(CombinationMapper).filter(
    CombinationMapper.label_id == label.id
).all()

for mapping in mappings:
    category = mapping.category  # SQLAlchemy auto-loads via relationship
    equipment = mapping.equipment  # SQLAlchemy auto-loads via relationship
```

### Query 3: Get All Codes with Their Labels for a State
```sql
SELECT c.*, array_agg(l.id) as label_ids
FROM codes c
LEFT JOIN combination_mapper cm ON c.id = cm.code_id
LEFT JOIN labels l ON cm.label_id = l.id
WHERE c.state_id = ?
GROUP BY c.id
```

**Example ORM equivalent:**
```python
codes = db.query(Code).filter(Code.state_id == state_id).all()
for code in codes:
    for mapper in code.combination_mappers:
        label = mapper.label
        category = mapper.category
        equipment = mapper.equipment
        # Now you have all related data
```

---

## Import Script - Detailed Execution Flow

### Step 1: Load Excel File
```python
filepath = get_excel_path("Illumine-i X LabelFriday master data.xlsx")
wb = openpyxl.load_workbook(filepath, data_only=True)
ws = wb.active
```

### Step 2: Parse Headers
```python
headers = [cell.value for cell in ws[1]]
# Find column indices dynamically
upc_idx = headers.index("upc_code") if "upc_code" in headers else 0
label_number_idx = headers.index("label_number") if "label_number" in headers else 1
# etc...
```

### Step 3: Process Each Row
```python
for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
    # Extract values
    upc_code = str(row[upc_idx]).strip() if row[upc_idx] else None
    label_number = str(row[label_number_idx]).strip() if row[label_number_idx] else None
    # ...
    
    # Check for duplicates
    existing = db.query(Label).filter(Label.label_number == label_number).first()
    if existing:
        stats["labels_skipped"] += 1
        continue
    
    # Create and save
    label = Label(upc_code=upc_code, label_number=label_number, ...)
    db.add(label)
    db.commit()
    stats["labels_created"] += 1
```

### Step 4: Link Category/Equipment/Code
```python
# Get or create category
category = db.query(Category).filter(Category.name == category_name).first()
if not category:
    category = Category(name=category_name)
    db.add(category)
    db.commit()

# Get or create equipment
equipment = db.query(Equipment).filter(Equipment.name == equipment_name).first()
if not equipment:
    equipment = Equipment(name=equipment_name)
    db.add(equipment)
    db.commit()

# Get label
label = db.query(Label).filter(Label.label_number == label_number).first()

# Get code (optional)
code = db.query(Code).filter(Code.code_name == code_name).first()

# Create combination
mapper = CombinationMapper(
    category_id=category.id,
    equipment_id=equipment.id,
    code_id=code.id,  # Can be None
    label_id=label.id
)
db.add(mapper)
db.commit()
```

---

## Common Queries for Future Rule Engine

### Get All Equipment for a Specific Code
```python
query = db.query(Equipment).distinct().join(
    CombinationMapper,
    Equipment.id == CombinationMapper.equipment_id
).filter(
    CombinationMapper.code_id == code_id
).all()
```

### Get All Codes That Apply to Specific Equipment and Category
```python
query = db.query(Code).distinct().join(
    CombinationMapper,
    Code.id == CombinationMapper.code_id
).filter(
    CombinationMapper.equipment_id == equipment_id,
    CombinationMapper.category_id == category_id
).all()
```

### Check if a Label is Active and Licensed for a Code
```python
label = db.query(Label).filter(
    Label.id == label_id,
    Label.is_active == True
).first()

mapper = db.query(CombinationMapper).filter(
    CombinationMapper.label_id == label_id,
    CombinationMapper.code_id == code_id
).first()

is_compatible = label is not None and mapper is not None
```

---

## Database Schema Verification

After running `python scripts/import/import_labels.py`, verify:

```bash
# All tables exist
psql -U postgres -d ahj_db -c "\dt"

# Check labels created
psql -U postgres -d ahj_db -c "SELECT COUNT(*) FROM labels;"

# Check categories created
psql -U postgres -d ahj_db -c "SELECT COUNT(*) FROM categories;"

# Check equipment created
psql -U postgres -d ahj_db -c "SELECT COUNT(*) FROM equipment;"

# Check combinations created
psql -U postgres -d ahj_db -c "SELECT COUNT(*) FROM combination_mapper;"

# See sample label
psql -U postgres -d ahj_db -c "SELECT * FROM labels LIMIT 1;"

# See combination mapping
psql -U postgres -d ahj_db -c "SELECT cm.*, c.name as category, e.name as equipment FROM combination_mapper cm LEFT JOIN categories c ON cm.category_id = c.id LEFT JOIN equipment e ON cm.equipment_id = e.id LIMIT 5;"
```

---

## Troubleshooting Import Issues

### Issue 1: "Excel file not found"
**Cause:** Wrong file path or Excel files in wrong directory
**Solution:** 
- Ensure Excel files are in: `app/data/master/`
- Check exact file names match (case-sensitive on Linux)
- Run from project root: `cd /path/to/ahj-engine && python scripts/import/import_labels.py`

### Issue 2: "Label already exists"
**Cause:** Duplicate label_number in Excel or already imported
**Solution:**
- Check Excel file for duplicate label_number values
- Delete records from DB and re-import: `DELETE FROM labels; DELETE FROM categories; DELETE FROM equipment; DELETE FROM combination_mapper;`

### Issue 3: "Label not found" for combination mapping
**Cause:** Label defined in File 2 but not in File 1
**Solution:**
- Ensure all label_numbers in File 2 exist in File 1
- Run File 1 import first
- Add missing labels to File 1

### Issue 4: "Code not found" for combination mapping
**Cause:** Code referenced in File 2 doesn't exist in codes table
**Solution:**
- Populate codes table first via API or directly
- Or set code_name to empty/null in File 2 (optional field)

### Issue 5: "openpyxl not installed"
**Solution:**
```bash
pip install openpyxl==3.1.5
# or from requirements.txt
pip install -r requirements.txt
```

---

## Performance Notes

- **First Import:** ~30 seconds for 1000 labels + 500 combinations
- **Schema Queries:** All queries indexed on ForeignKey columns
- **Memory:** Lazy-loaded relationships prevent memory bloat
- **Concurrent Imports:** Pool size=20, safe for 5-10 concurrent processes

---

## Extension Points for Future Development

### Add More Excel Sheets
1. Extend `import_labels.py` with new methods:
   ```python
   def import_additional_data(self):
       # Load from new Excel sheet
       pass
   ```

2. Add to import workflow in `run()`:
   ```python
   self.import_labels()
   self.import_category_equipment_mapping()
   self.import_additional_data()  # <-- New
   ```

### Auto-Generate Reports
```python
# Add to import script
def generate_import_report(self):
    report = {
        "timestamp": datetime.now(),
        "total_labels": self.db.query(Label).count(),
        "total_categories": self.db.query(Category).count(),
        "total_equipment": self.db.query(Equipment).count(),
        "total_mappings": self.db.query(CombinationMapper).count(),
    }
    return report
```

### Setup Cron Job (Linux)
```bash
# Run import daily at 2 AM
0 2 * * * cd /path/to/ahj-engine && python scripts/import/import_labels.py >> /var/log/ahj-import.log 2>&1
```

### Setup Windows Task Scheduler
```batch
REM Create scheduled task
schtasks /create /tn "AHJ Excel Import" /tr "C:\path\to\.venv\Scripts\python.exe C:\path\to\scripts\import\import_labels.py" /sc daily /st 02:00
```

---

## Next Steps

1. **Prepare Excel Files**: Update your Excel files with data
2. **Run Import**: `python scripts/import/import_labels.py`
3. **Verify Data**: Check admin panel at `/admin`
4. **Test API**: Call `/api/v1/ahj-engine/get-ahj-details` with sample data
5. **Populate Codes**: Create codes via API or direct SQL
6. **Test End-to-End**: Create AHJs→ Get details → See labels/notes/formulas

