# AHJ Engine - Complete System Documentation

**Created:** March 1, 2026  
**Status:** Ready for Render Deployment  
**Database:** PostgreSQL  
**Framework:** FastAPI + SQLAdmin

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Database Structure](#database-structure)
3. [Data Imports Summary](#data-imports-summary)
4. [How Everything Connects](#how-everything-connects)
5. [Installation & Setup](#installation--setup)
6. [Deployment to Render](#deployment-to-render)
7. [Admin Panel Guide](#admin-panel-guide)
8. [API Endpoints](#api-endpoints)
9. [Troubleshooting](#troubleshooting)

---

## System Overview

### What is AHJ Engine?

**AHJ Engine** is a web application for managing Authority Having Jurisdiction (AHJ) data. It helps organize:
- **Electrical codes** (NEC, IEC, etc.)
- **Equipment** (Solar modules, inverters, optimizers)
- **Safety labels** (Arc flash warnings, electrical hazard labels)
- **Geographic data** (States, utilities, jurisdictions)

### Technology Stack

| Component | Purpose |
|-----------|---------|
| **FastAPI** | Web framework (backend API) |
| **SQLAdmin** | Admin dashboard with web UI |
| **PostgreSQL** | Database storage |
| **SQLAlchemy** | Database connection tool |
| **Gunicorn + Uvicorn** | Web server for production |

---

## Database Structure

### Core Tables (22 Total)

#### 1. **States & Geography**
```
states (50 records)
  ├─ State names (Texas, California, etc.)
  ├─ Abbreviations (TX, CA)
  └─ FIPS codes for federal identification

countries (249 records)
  ├─ Country names
  ├─ ISO codes (US, CA, MX)
  └─ Currency codes
```

**Example Data:**
- Texas: TX, FIPS: 48
- California: CA, FIPS: 06

#### 2. **Authorities & Utilities**
```
ahjs (10,521 records) - Authorities Having Jurisdiction
  ├─ City/county government offices
  ├─ Building permit departments
  ├─ Contact information
  └─ Jurisdiction type

utilities (990 records)
  ├─ Electric companies (PG&E, Texas Power, etc.)
  ├─ Service territory
  ├─ Utility type (Municipal, Investor-Owned, etc.)
  └─ Requirements for solar systems
```

**Why This Matters:** Different jurisdictions have different electrical code requirements. This maps which utility serves which area.

#### 3. **Electrical Codes**
```
code_types (10 records)
  ├─ NEC (National Electrical Code)
  ├─ IEC (International Electrical Code)
  ├─ NFPA
  └─ Others

applicable_code_categories (7 records)
  ├─ Building
  ├─ Electrical ✓ (398 codes imported)
  ├─ Fire
  ├─ Mechanical
  ├─ Plumbing
  ├─ Residential
  └─ Energy

code_amendments (4 records)
  ├─ LOCAL (city-specific changes)
  ├─ STATE (state-level amendments)
  ├─ STANDARD (national standard)
  └─ INTERNATIONAL (global standards)

codes (398 records) ✓ IMPORTED
  ├─ Code title: "2021 National Electrical Code"
  ├─ Edition: 2021
  ├─ Associated category
  ├─ Amendment level
  └─ Year adopted
```

**How It Works:**
1. You have a **Code** (e.g., "2021 NEC")
2. It has a **Type** (NEC)
3. It belongs to a **Category** (Electrical)
4. It may have **Amendments** (LOCAL changes)
5. Different **States** adopt different versions

**Data Imported:** ✓ 398 codes across 7 categories

#### 4. **Equipment & Categories**
```
equipment (26 records) ✓ IMPORTED
  ├─ DC Module
  ├─ AC Module
  ├─ Microinverter
  ├─ Inverter
  ├─ Optimizer
  ├─ Combiner
  ├─ Meter
  ├─ Battery
  ├─ And more...

categories (14 records) ✓ IMPORTED
  ├─ Module (for DC/AC modules)
  ├─ Inverter (for inverters/microinverters)
  ├─ Optimizer (for optimizers)
  ├─ Combiner (for combiners)
  ├─ MID (type of disconnect)
  ├─ Disconnect
  ├─ Panel
  ├─ Meter
  ├─ Battery
  ├─ EVCS (Electric Vehicle Charging Station)
  ├─ Generator
  ├─ Transfer switch
  ├─ Other
  └─ Junction box

combination_mapper (26 records) ✓ IMPORTED
  ├─ Links equipment → category
  └─ Will link to codes & labels
```

**What This Does:**
- Equipment = physical solar parts
- Categories = types/groups
- Mapper = says "DC Module is a type of Module"

#### 5. **Safety Labels** 
```
labels (410 records) ✓ IMPORTED
  ├─ UPC Code: LF-001 to LF-410 (unique ID)
  ├─ Name: WRITE IN LABEL, ARC FLASH LABEL, etc. (16 types)
  ├─ Label Number: LN-1000 to LN-1409 (system numbering)
  ├─ Label Name: Description of what label says
  ├─ Description: Full text of warning
  ├─ Length & Width: Physical dimensions in inches
  ├─ Colors:
  │  ├─ Red (#FF0000): 211 danger/arc flash labels
  │  ├─ Orange (#FFA500): 147 general/write-in labels
  │  ├─ Yellow (#FFFF00): 29 caution labels
  │  ├─ White (#FFFFFF): 13 minimal labels
  │  └─ Others: Small special labels
  └─ Image URL: Link to label image
```

**Color Distribution:**
- 🔴 **Red (211)** - Extreme danger: Arc flash hazard, shock risk
- 🟠 **Orange (147)** - General warnings: Write-in fields, basic info
- 🟡 **Yellow (29)** - Caution: Not immediate danger but requires care
- ⚪ **White (13)** - Information only
- **Custom (10)** - Black, blue, green for specific needs

**Data Imported:** ✓ 410 safety labels with full specifications

#### 6. **Notes & Formulas** (Not Yet Imported)
```
note_types (0 records) - Not imported
  ├─ General notes
  ├─ Electrical notes
  ├─ Attachments
  └─ Placard specifications

notes (0 records) - Not imported
  ├─ Code-specific notes
  ├─ Equipment-specific instructions
  ├─ Page numbers
  └─ Physical dimensions

formula_linker_types (0 records) - Not imported
  ├─ Wire size calculations
  ├─ Module counts
  ├─ Inverter sizing
  └─ Other calculations

formulas (0 records) - Not imported
  ├─ Actual calculation formulas
  ├─ Links to codes
  └─ Links to equipment
```

#### 7. **Clients & Preferences** (Optional)
```
clients (0 records)
  ├─ Company information
  ├─ Contact details
  └─ Location data

preferences (0 records)
  ├─ Language (English, Spanish, etc.)
  ├─ Timezone
  ├─ Date format
  └─ Theme (light/dark)
```

---

## Data Imports Summary

### What We Imported ✓

| Data Source | Records | Table | Status |
|---|---|---|---|
| States (built-in) | 50 | states | ✓ Complete |
| Countries (built-in) | 249 | countries | ✓ Complete |
| **code_mapping.xlsx** | 398 | codes | ✓ Complete |
| **Equipment Category and types.xlsx** | 26 equipment + 14 categories | equipment, categories | ✓ Complete |
| | 26 mappings | combination_mapper | ✓ Complete |
| **Illumine-i X LabelFriday master data.xlsx** | 410 | labels | ✓ Complete |
| Code Amendments (hardcoded) | 4 | code_amendments | ✓ Complete |
| Code Categories (hardcoded) | 7 | applicable_code_categories | ✓ Complete |
| Code Types (auto-created) | 10 | code_types | ✓ Complete |

### What We Have Separate Data For (Optional)

| Data | Table | Status | Notes |
|---|---|---|---|
| AHJs (10,521) | ahjs | Pre-populated | From initial database seed |
| Utilities (990) | utilities | Pre-populated | From initial database seed |

---

## How Everything Connects

### The Connection Flow (Simplified)

```
User → Label Selection → Auto-Fill Form Fields

Example Workflow:
1. Admin selects Label "LF-001" (UPC code)
2. System auto-fills:
   - Label Number: LN-1000
   - Label Name: "Write in DC label"
   - Length: 4 inches
   - Width: 1 inch
   - Description: Complete text
   - Background Color: Orange (#FFA500)
   - Text Color: Black (#000000)
```

### Database Relationships (How Tables Link)

```
🔗 STATES (Geographic Root)
   ├─→ UTILITIES (serve states)
   ├─→ AHJs (have jurisdiction in states)
   ├─→ CLIENTS (have state address)
   └─→ CODES (sometimes state-specific)

🔗 CODES (Rules/Standards)
   ├─→ CODE_TYPE (NEC, IEC, etc.)
   ├─→ APPLICABLE_CODE_CATEGORY (Electrical, Fire, etc.)
   ├─→ CODE_AMENDMENTS (Local, State, Standard, International)
   ├─→ NOTES (instructions per code)
   └─→ FORMULAS (calculations per code)

🔗 EQUIPMENT (Physical Solar Components)
   ├─→ CATEGORIES (groups equipment types)
   ├─→ COMBINATION_MAPPER (links to codes & labels)
   └─→ NOTES (equipment-specific notes)

🔗 LABELS (Safety Warnings)
   ├─→ COMBINATION_MAPPER (links to equipment)
   └─→ Gets displayed in admin as dropdowns
```

### Admin Panel Data Selection Flow

```
Step 1: Create New State
  Input: Alabama, AL (abbreviation), 01 (FIPS code)
  Stored in: states table

Step 2: Create New Code
  Input: 2021 National Electrical Code
  Selects: Type (NEC), Category (Electrical), Amendment (STANDARD)
  Links to: States (if state-specific)
  Stored in: codes table with foreign key to code_type, applicable_code_category

Step 3: Create New Equipment/Category
  Input: DC Module
  Selects: Category (Module)
  Stored in: equipment table
  Linked via: combination_mapper to category

Step 4: Create New Label
  Input: Select LF-001 from dropdown
  Auto-fills: Length, Width, Description, Colors
  Selects or creates: Label Name
  Stored in: labels table
  Links to: combination_mapper (optional, for equipment-specific labels)
```

---

## Installation & Setup

### For Local Development

#### 1. **Clone and Setup**
```bash
# Navigate to project
cd c:\Users\aadil\Videos\ahj-engine-main-main

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

#### 2. **Initialize Database**
```bash
# Create all tables and import data
python init_db_full.py

# Output shows:
# [1/4] Creating database tables... ✓
# [2/4] Importing reference data... ✓
# [3/4] Importing data from Excel files... ✓
# [4/4] Verifying database... ✓
```

#### 3. **Start Development Server**
```bash
python -m uvicorn app.main:app --reload

# Server runs at: http://localhost:8000
# Admin panel: http://localhost:8000/admin
```

### For Production (Render Deployment)

#### Step-by-Step

**1. Create Render Account**
- Go to https://render.com
- Sign up with GitHub

**2. Connect GitHub Repository**
- Go to Dashboard → New + → Web Service
- Select your GitHub repo with AHJ Engine code

**3. Configure Environment**
```
Environment Variables:
  DATABASE_URL = postgresql://username:password@host/dbname
  DEBUG = false
  SECRET_KEY = your-secret-key-here
```

**4. Build & Deploy**
```
Build Command: bash build.sh
Start Command: gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

**5. Database Setup**
- The `init_db_full.py` runs automatically in build phase
- Creates all tables
- Imports Excel data
- Ready to use!

---

## Admin Panel Guide

### How to Use the Web Interface

#### Access Admin
1. Go to `http://localhost:8000/admin`
2. Login (if authentication is configured)

#### Sections in Left Menu

**Data Management:**
- **States** - US states, abbreviations, FIPS codes
- **AHJs** - Authorities Having Jurisdiction (building departments)
- **Utilities** - Electric companies and service areas
- **Codes** - Electrical codes and requirements
- **Code Types** - NEC, IEC, etc.
- **Labels** - Safety warning labels
- **Equipment** - Solar components
- **Categories** - Equipment groupings
- **Combination Mappers** - Links between equipment and categories

**Advanced:**
- **Notes** - Code-specific instructions
- **Formulas** - Calculation formulas
- **Clients** - Company information

#### Creating a Code

1. Go to **Codes** → **New Code**
2. Fill fields:
   - **Title:** "2021 National Electrical Code"
   - **Edition:** 2021
   - **Code Type:** Select "NEC"
   - **Category:** Select "Electrical"
   - **Amendment:** Select "STANDARD"
3. Click **Save**

#### Creating a Label

1. Go to **Labels** → **New Label**
2. **Select UPC Code** from dropdown
3. Form auto-fills:
   - Label Number
   - Label Name (description)
   - Length & Width
4. Review all fields
5. Click **Save**

#### Editing Data

1. Find record in table
2. Click edit icon (pencil)
3. Modify fields
4. Click **Save**

#### Deleting Data

1. Find record in table
2. Click delete icon (trash)
3. Confirm deletion

---

## API Endpoints

### Base URL
```
http://localhost:8000/api/v1
```

### Labels API

**Get All Labels**
```
GET /api/v1/label/
Response: [{ id, upc_code, name, length, width, ... }]
```

**Get Label by ID**
```
GET /api/v1/label/{id}/details
Response: { id, upc_code, name, label_number, length, width, ... }
```

**Get Label by UPC**
```
GET /api/v1/label/by-upc/{upc_code}/details
Response: { id, upc_code, name, length, width, description, ... }
```

**Create Label**
```
POST /api/v1/label/create
Body: {
  upc_code: "LF-001",
  name: "WRITE IN LABEL",
  length: 4,
  width: 1,
  description: "Write in DC label",
  background_color: "#FFA500",
  text_color: "#000000"
}
```

### Codes API

**Get All Codes**
```
GET /api/v1/codes/
```

**Get Code by ID**
```
GET /api/v1/codes/{id}
```

---

## Troubleshooting

### Issue: "UniqueViolation: duplicate key value"

**Cause:** Trying to add duplicate data (e.g., TX state twice)

**Solution:** 
```python
# Check for duplicates
python -c "
from sqlalchemy import text
from app.core.database import engine

with engine.connect() as conn:
    result = conn.execute(text('SELECT COUNT(*) as cnt, abbrev FROM states GROUP BY abbrev HAVING COUNT(*) > 1'))
    print(result.fetchall())
"

# Delete duplicate if necessary
# DELETE FROM states WHERE id = XXX AND name = 'test data'
```

### Issue: Labels dropdown not showing values

**Solution:**
1. Ensure labels are imported: `python scripts/import/import_labels_new.py`
2. Refresh browser cache: Ctrl+Shift+Delete
3. Check server is running: `python -m uvicorn app.main:app --reload`
4. Check browser console for JavaScript errors

### Issue: Form fields not auto-filling

**Solution:**
1. Check JavaScript loaded: F12 → Console tab
2. Verify API endpoint working: `curl http://localhost:8000/api/v1/label/1/details`
3. Check label exists in database: `python audit_database.py`

### Issue: Cannot connect to database

**Cause:** PostgreSQL not running or wrong connection string

**Solution:**
```bash
# Check connection string in .env
echo $DATABASE_URL

# Test connection
python -c "from app.core.database import engine; print(engine.url)"

# Restart PostgreSQL service
# Windows: Services → PostgreSQL → Restart
# Mac: brew services restart postgresql
# Linux: sudo systemctl restart postgresql
```

---

## Summary Checklist

### ✓ Completed

- [x] 22 database tables created
- [x] 398 electrical codes imported
- [x] 410 safety labels imported
- [x] 26 equipment items configured
- [x] 14 equipment categories set up
- [x] Admin panel with auto-fill dropdowns
- [x] Color-coded labels (Red/Orange/Yellow/White)
- [x] Label dimensions accurate (4"x1", 2"x3", etc.)
- [x] SQLAdmin web interface working
- [x] API endpoints for label retrieval
- [x] Database audit script
- [x] Initialization script for Render

### ⏳ Ready for Future

- [ ] Notes/Placard imports (when Excel file provided)
- [ ] Formula calculations (when requirements defined)
- [ ] User authentication (when needed)
- [ ] Multi-language support

### 🚀 Ready to Deploy

1. Push code to GitHub
2. Connect to Render (https://render.com)
3. Set DATABASE_URL in environment
4. Deploy! (automatic init_db_full.py runs)
5. Access at your-app.onrender.com

---

## Questions?

For issues or questions:
1. Check the audit: `python audit_database.py`
2. Review server logs: Browser console (F12)
3. Check database: `psql -U username -d database_name`

Your system is production-ready! 🎉
