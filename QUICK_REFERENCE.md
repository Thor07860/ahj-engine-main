# Quick Reference: Regulatory Data & Model Relationships

## TL;DR - What Was Done

✅ **Countries** - Added relationships between countries and states  
✅ **States** - Added relationships to AHJs, Utilities, and Clients  
✅ **AHJs** - Imported 10,521+ authorities having jurisdiction  
✅ **Utilities** - Imported 990 utility providers  
✅ **Junction Tables** - Created StateCode and AHJCode many-to-many tables  
✅ **Import Script** - Automated import from Excel with validation  

---

## Model Hierarchy

```
Country (249 total)
  ↓
State (50 total - USA only)
  ├─ AHJ (10,521 total)
  │  └─ Utility (990 total via AHJ relationship)
  └─ Client (via state_id foreign key)
```

---

## Key Changes

### 1. **Country Model**
```python
from app.models import Country

# New fields:
.states = relationship("State")      # One-to-many
.clients = relationship("Client")     # One-to-many
```

### 2. **State Model**
```python
from app.models import State

# New fields:
.country_id = ForeignKey("countries.id")
.country = relationship("Country")    # Many-to-one
.ahjs = relationship("AHJ")          # One-to-many
.utilities = relationship("Utility")  # One-to-many
.clients = relationship("Client")     # One-to-many
```

### 3. **AHJ Model**
Fixed relationships to use `back_populates`:
```python
from app.models import AHJ

.state = relationship("State", back_populates="ahjs")
# Can access: ahj.state, ahj.state.country, ahj.state.abbrev
```

### 4. **Utility Model**
Fixed relationships to use `back_populates`:
```python
from app.models import Utility

.state = relationship("State", back_populates="utilities")
.ahj = relationship("AHJ")
# Can access: utility.state, utility.ahj
```

### 5. **Client Model**
Added bidirectional relationships:
```python
from app.models import Client

.state = relationship("State", back_populates="clients")
.country = relationship("Country", back_populates="clients")
.preferences = relationship("Preference", back_populates="client", uselist=False)
```

### 6. **Preference Model**
Added client relationship:
```python
from app.models import Preference

.client = relationship("Client", back_populates="preferences")
```

### 7. **StateCode Junction Table**
```python
from app.models import StateCode

class StateCode(Base):
    state_id = ForeignKey("states.id")
    code_id = ForeignKey("codes.id")
```

### 8. **AHJCode Junction Table**
```python
from app.models import AHJCode

class AHJCode(Base):
    ahj_id = ForeignKey("ahjs.id")
    code_id = ForeignKey("codes.id")
```

---

## Quick Queries

### List all AHJs in California
```python
from app.core.database import SessionLocal
from app.models import State

db = SessionLocal()
ca = db.query(State).filter_by(abbrev="CA").first()
for ahj in ca.ahjs:
    print(ahj.name)
```

### Get country for an AHJ
```python
ahj = db.query(AHJ).first()
print(ahj.state.country.name)  # "United States"
```

### Get utilities for a state
```python
state = db.query(State).filter_by(abbrev="TX").first()
for utility in state.utilities:
    print(utility.name, utility.utility_type)
```

### Get all utilities in an AHJ's service area
```python
ahj = db.query(AHJ).filter_by(name="CA - City of San Francisco").first()
utilities = db.query(Utility).filter_by(ahj_id=ahj.id).all()
for u in utilities:
    print(u.name)
```

---

## Files Updated/Created

### Models Updated
- `app/models/country.py` - Added relationships
- `app/models/state.py` - Added relationships + country_id FK
- `app/models/ahj.py` - Fixed relationships to use back_populates
- `app/models/utility.py` - Fixed relationships to use back_populates
- `app/models/client.py` - Added state + country relationships
- `app/models/preference.py` - Added client relationship
- `app/models/state_code.py` - Updated with timestamps + relationships
- `app/models/ahj_code.py` - Updated with timestamps + relationships
- `app/models/__init__.py` - Exported all models

### Scripts Created
- `scripts/import/import_regulatory_data.py` - Complete import system

### Documentation Created
- `REGULATORY_DATA_MAPPING.md` - Comprehensive guide
- `QUICK_REFERENCE.md` - This file!

---

## Import Script Usage

### Run Import
```bash
cd /path/to/ahj-engine
python scripts/import/import_regulatory_data.py
```

### Reset Database First
```bash
python reset_db.py
python scripts/import/import_regulatory_data.py
```

### Expected Results
- **Countries:** 249 ✓
- **States:** 50 ✓
- **AHJs:** 10,521 ✓
- **Utilities:** 990 ✓
- **Total:** 11,511 records

---

## Database Schema

### Countries Table
```sql
CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    iso2 VARCHAR(2) NOT NULL UNIQUE,
    iso3 VARCHAR(3) UNIQUE,
    calling_code VARCHAR(20),
    currency_code VARCHAR(3),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### States Table
```sql
CREATE TABLE states (
    id SERIAL PRIMARY KEY,
    country_id INTEGER FOREIGN KEY REFERENCES countries(id),
    name VARCHAR(100) NOT NULL,
    abbrev VARCHAR(2) NOT NULL UNIQUE,
    fips_code VARCHAR(2),
    region VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### AHJs Table
```sql
CREATE TABLE ahjs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    state_id INTEGER NOT NULL FOREIGN KEY REFERENCES states(id),
    county VARCHAR(255),
    city VARCHAR(255),
    guidelines TEXT,
    ...other fields...
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Utilities Table
```sql
CREATE TABLE utilities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    state_id INTEGER NOT NULL FOREIGN KEY REFERENCES states(id),
    ahj_id INTEGER FOREIGN KEY REFERENCES ahjs(id),
    utility_type VARCHAR(100),
    ...other fields...
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Next Steps

1. **Use the regulatory data** - Query AHJs and utilities via the API
2. **Link codes to jurisdictions** - Use StateCode and AHJCode tables
3. **Create API filters** - Filter AHJs by state, utilities by AHJ
4. **Add client preferences** - Use state/country info for client localization

---

## Testing

Verify the import:
```python
from app.core.database import SessionLocal
from app.models import Country, State, AHJ, Utility

db = SessionLocal()
print("Countries:", db.query(Country).count())  # Should be 249
print("States:", db.query(State).count())        # Should be 50
print("AHJs:", db.query(AHJ).count())           # Should be 10,521
print("Utilities:", db.query(Utility).count())  # Should be 990
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Foreign key constraint errors | Run `python reset_db.py` |
| Empty import results | Check Excel file location: `data/master/Regulatory data.xlsx` |
| "State not found" warnings | Expected - some references are incomplete in source data |
| Very slow import | Script commits per record for safety; normal behavior |

---

*✅ Regulatory data mapping complete!*
