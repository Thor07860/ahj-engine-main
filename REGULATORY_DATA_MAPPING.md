# Regulatory Data Mapping & Import Guide

## Overview

The AHJ Engine now has complete regulatory data support with proper relationships between Countries, States, AHJs (Authorities Having Jurisdiction), and Utilities. All data has been imported from the `Regulatory data.xlsx` Excel file.

---

## Data Model Relationships

### 1. **Country Model** (`app/models/country.py`)
**Purpose:** Store global country information

**Key Fields:**
- `id` - Primary key
- `name` - Full country name (e.g., "United States")
- `iso2` - ISO 3166-1 alpha-2 code (e.g., "US")
- `iso3` - ISO 3166-1 alpha-3 code (nullable)
- `calling_code` - International dialing code (e.g., "+1")
- `currency_code` - ISO 4217 currency code (e.g., "USD")
- `created_at` - Timestamp

**Relationships:**
```python
states = relationship("State", back_populates="country")
clients = relationship("Client", back_populates="country")
```

### 2. **State Model** (`app/models/state.py`)
**Purpose:** Store state/province information

**Key Fields:**
- `id` - Primary key
- `country_id` - Foreign key to Countries (defaults to USA)
- `name` - Full state name (e.g., "California")
- `abbrev` - 2-letter abbreviation (e.g., "CA") - unique
- `abbreviation` - Synonym for `abbrev`
- `fips_code` - Federal FIPS state code
- `region` - Geographic region (e.g., "West", "Midwest")
- `created_at` - Timestamp

**Relationships:**
```python
country = relationship("Country", back_populates="states")
ahjs = relationship("AHJ", back_populates="state")
utilities = relationship("Utility", back_populates="state")
clients = relationship("Client", back_populates="state")
```

### 3. **AHJ Model** (`app/models/ahj.py`)
**Purpose:** Store Authority Having Jurisdiction data

**Key Fields:**
- `id` - Primary key
- `name` - AHJ name (e.g., "CA - City of San Francisco")
- `ahj_name` - Alternative AHJ name field
- `state_id` - Foreign key to States
- `county` - County name (optional)
- `city` - City name (optional)
- `guidelines` - Guidelines text (rich text)
- `fireset_back` - Setback requirement (float)
- `jurisdiction_type` - Type of jurisdiction (e.g., "city", "county", "state")
- `phone` - Contact phone
- `email` - Contact email
- `website` - Website URL
- `created_at` - Timestamp

**Relationships:**
```python
state = relationship("State", back_populates="ahjs")
utilities = relationship("Utility", backref="ahjs")
```

### 4. **Utility Model** (`app/models/utility.py`)
**Purpose:** Store utility provider information

**Key Fields:**
- `id` - Primary key
- `name` - Utility name
- `utility_name` - Alternative name field
- `state_id` - Foreign key to States
- `ahj_id` - Foreign key to AHJs (optional, nullable)
- `eia_id` - EIA Utility ID (US Energy Information Administration)
- `utility_type` - Type of utility (e.g., "Investor-Owned", "Municipal", "Co-op", "Federal")
- `service_territory` - Service territory description
- `phone` - Contact phone
- `website` - Website URL
- `requirements` - Requirements text (rich text)
- `response_type` - Response type (enum, for future use)
- `created_at` - Timestamp

**Relationships:**
```python
ahj = relationship("AHJ", backref="utilities")
state = relationship("State", back_populates="utilities")
```

### 5. **Junction Tables**

#### StateCode (`app/models/state_code.py`)
**Purpose:** Many-to-Many relationship between States and Codes

**Fields:**
- `id` - Primary key
- `state_id` - Foreign key to States
- `code_id` - Foreign key to Codes
- `created_at` - Timestamp

#### AHJCode (`app/models/ahj_code.py`)
**Purpose:** Many-to-Many relationship between AHJs and Codes

**Fields:**
- `id` - Primary key
- `ahj_id` - Foreign key to AHJs
- `code_id` - Foreign key to Codes
- `created_at` - Timestamp

---

## Data Flow Diagram

```
Countries (249 records)
    ↓ (one-to-many)
States (50 records - USA)
    ├─→ AHJs (10,521 records)
    │   ├─→ Utilities (mapped 1-to-many)
    │   └─→ Codes (via AHJCode junction)
    ├─→ Utilities (990 records)
    └─→ Codes (via StateCode junction)

Clients ←─┬─→ State
          └─→ Country
```

---

## Import Process

### Overview
The `import_regulatory_data.py` script imports data from `data/master/Regulatory data.xlsx`:

**File Location:** `scripts/import/import_regulatory_data.py`

**Usage:**
```bash
python scripts/import/import_regulatory_data.py
```

### Sheets Imported

1. **Country List Sheet** (249 rows)
   - **Columns:** Country, Short Name (ISO2)
   - **Import Behavior:**
     - Creates Country records with ISO2 codes
     - Skips duplicates based on ISO2 uniqueness
     - Sets ISO3 to NULL (can be populated later)

2. **State List - USA Sheet** (52 rows, 50 imported)
   - **Columns:** State Name, Short Name
   - **Import Behavior:**
     - Creates State records tied to USA country
     - Extracts 2-letter abbreviation
     - Skips existing states

3. **AHJ - State List Sheet** (10,543 rows)
   - **Columns:** Name, State
   - **Import Behavior:**
     - Extracts state abbreviation from AHJ name (e.g., "CA - City Name" → "CA")
     - Looks up state by abbreviation, then by name
     - Creates 10,521 AHJ records
     - Skips duplicates and validates state existence

4. **AHJ - Utility Mapping Sheet** (7,790 rows)
   - **Columns:** Utility, AHJ
   - **Import Behavior:**
     - Looks up AHJ by name
     - Creates Utility records linked to AHJ and State
     - Creates 990 utility records
     - Skips utilities with non-existent AHJs

### Running the Import

#### Prerequisites
1. Ensure database is properly initialized:
   ```bash
   python reset_db.py
   ```

2. Ensure Excel file exists at:
   ```
   data/master/Regulatory data.xlsx
   ```

#### Execute Import
```bash
cd /path/to/ahj-engine
python scripts/import/import_regulatory_data.py
```

#### Sample Output
```
============================================================
REGULATORY DATA IMPORT
============================================================

Loading Excel file: C:\...\Regulatory data.xlsx

============================================================
IMPORTING COUNTRIES
============================================================
[OK] Created: United States (US)
[OK] Created: Canada (CA)
...
Countries Summary:
  Created: 249
  Skipped: 0
  Total rows processed: 249

============================================================
IMPORTING STATES
============================================================
[OK] Created: California (CA)
[OK] Created: Texas (TX)
...
States Summary:
  Created: 50
  Skipped: 0
  Total rows processed: 52

============================================================
IMPORTING AHJs (AUTHORITIES HAVING JURISDICTION)
============================================================
[OK] Created: CA - City of San Francisco (CA)
[OK] Created: CA - County of Los Angeles (CA)
...
AHJs Summary:
  Created: 10521
  Skipped: 22
  Total rows processed: 10543

============================================================
IMPORTING UTILITY-AHJ MAPPINGS
============================================================
[OK] Created: PG&E (linked to CA - State)
...
Utilities Summary:
  Created: 990
  Skipped: 6800
  Total rows processed: 7790

============================================================
IMPORT SUMMARY
============================================================
Countries Created: 249
States Created: 50
AHJs Created: 10521
Utilities Created: 990

Total Records Created: 11511
Total Records Skipped: 7121

============================================================
IMPORT COMPLETE!
============================================================
```

---

## API Endpoints

### Countries
- `POST /api/v1/countries/create` - Create country
- `GET /api/v1/countries/{country_id}` - Get country details
- `GET /api/v1/countries/` - List all countries
- `PUT /api/v1/countries/{country_id}` - Update country
- `DELETE /api/v1/countries/{country_id}` - Delete country

### States
- `POST /api/v1/states/create` - Create state
- `GET /api/v1/states/{state_id}` - Get state details
- `GET /api/v1/states/` - List all states
- `PUT /api/v1/states/{state_id}` - Update state
- `DELETE /api/v1/states/{state_id}` - Delete state

### AHJs
- `POST /api/v1/ahjs/create` - Create AHJ
- `GET /api/v1/ahjs/{ahj_id}` - Get AHJ details
- `GET /api/v1/ahjs/` - List all AHJs
- `PUT /api/v1/ahjs/{ahj_id}` - Update AHJ
- `DELETE /api/v1/ahjs/{ahj_id}` - Delete AHJ

### Utilities
- `POST /api/v1/utilities/create` - Create utility
- `GET /api/v1/utilities/{utility_id}` - Get utility details
- `GET /api/v1/utilities/` - List all utilities
- `PUT /api/v1/utilities/{utility_id}` - Update utility
- `DELETE /api/v1/utilities/{utility_id}` - Delete utility

---

## Database Queries

### Get all AHJs in a specific state
```python
from app.core.database import SessionLocal
from app.models import State, AHJ

db = SessionLocal()

# Get California AHJs
ca_state = db.query(State).filter_by(abbrev="CA").first()
ahjs = db.query(AHJ).filter_by(state_id=ca_state.id).all()

for ahj in ahjs:
    print(f"{ahj.name} - {ahj.state.name}")
```

### Get utilities for an AHJ
```python
# Get utilities for a specific AHJ
ahj = db.query(AHJ).filter_by(name="CA - City of San Francisco").first()
utilities = ahj.utilities

for utility in utilities:
    print(f"{utility.name} - {utility.utility_type}")
```

### Get all states in a country
```python
# Get all US states
usa = db.query(Country).filter_by(iso2="US").first()
states = usa.states

for state in states:
    print(f"{state.abbrev} - {state.name}")
```

### Get AHJ with its state and country
```python
ahj = db.query(AHJ).filter_by(id=1).first()
print(f"AHJ: {ahj.name}")
print(f"State: {ahj.state.name}")
print(f"Country: {ahj.state.country.name}")
```

---

## Troubleshooting

### Issue: "Column countries.created_at does not exist"
**Solution:** Run `python reset_db.py` to recreate all tables with the updated schema

### Issue: "AHJ not found" warnings during utility import
**Reason:** Some utilities are mapped to AHJs that don't exist in the AHJ sheet
**Solution:** This is expected; the script logs these as warnings and skips them

### Issue: Import script runs very slowly
**Solution:** The script commits per record for transaction safety. For bulk imports on fast connections, modify the script to batch commits in groups of 100-1000

### Issue: Duplicate key violations
**Solution:** Ensure you've reset the database before re-running import - use `python reset_db.py`

---

## Future Enhancements

1. **Batch Commits:** Modify import script to commit in batches for better performance
2. **ISO3 Codes:** Populate ISO3 codes for countries during import
3. **State Regions:** Auto-categorize states by geographic region
4. **Error Recovery:** Implement better error handling and data validation before insertion
5. **Incremental Updates:** Support updating existing records instead of always recreating
6. **Relationship Export:** Export full relationship data as CSV/JSON

---

## Model Exports

All models are exported from `app/models/__init__.py`:

```python
from app.models import (
    Country, State, AHJ, Utility,
    StateCode, AHJCode,
    Code, CodeType, CodeAmendment,
    ApplicableCodeCategory,
    Label, Category, Equipment, CombinationMapper,
    Note, NoteType,
    Formula, FormulaLinkerType,
    Client, Preference,
    User
)
```

Use these imports in your code:
```python
from app.models import Country, State, AHJ, Utility

# Now you can use them directly
country = Country(name="USA", iso2="US")
```

---

## Statistics

**Import Results:**
- **Countries:** 249 records
- **States:** 50 records (USA)
- **AHJs:** 10,521 records
- **Utilities:** 990 records
- **Total Records Created:** 11,511
- **Total Records Skipped:** 7,121 (duplicates and invalid references)

---

*Last Updated: March 1, 2026*
*Regulatory Data Import Complete*
