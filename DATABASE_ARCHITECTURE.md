# AHJ Engine - Complete Database & Architecture Overview

## Project Overview
**AHJ Engine** is a FastAPI-based application for managing Authority Having Jurisdiction (AHJ) data, codes, utilities, formulas, labels, and related governmental/regulatory information.

**Version:** v1  
**Framework:** FastAPI + SQLAlchemy + PostgreSQL  
**Database:** PostgreSQL (psycopg2-binary)  
**Database URL:** `postgresql://postgres:SRM%401245@localhost:5432/ahj_db`

---

## Database Connection Architecture

### Connection Config
- **Engine Type:** SQLAlchemy async-supported connection pool
- **Pool Size:** 20 connections
- **Max Overflow:** 0 (no overflow pool)
- **Isolation:** Standard SQLAlchemy ORM handling
- **Loading:** Models loaded at startup via `init_db()` in `main.py`

### Database Initialization Flow
```
startup event → init_db() → Base.metadata.create_all() → Tables created/verified
```

---

## Complete Database Schema (22 Tables)

### Core Tables (Primary Domain)

#### 1. **states** (6 columns, 0 rows)
- **Primary Key:** id (Integer)
- **Columns:**
  - `name` - State name (String 100)
  - `abbrev` - State abbreviation (String 2, UNIQUE)
  - `fips_code` - Federal code (String 2)
  - `region` - Geographic region (String 50)
  - `created_at` - Timestamp
- **Purpose:** Master list of US states and regions
- **Relationships:** Referenced by AHJ, Code, Utility

---

#### 2. **ahjs** (13 columns, 0 rows)
- **Primary Key:** id (Integer)
- **Foreign Keys:**
  - `state_id` → states.id (NOT NULL)
- **Columns:**
  - `name` - Canonical AHJ name (String 255, NOT NULL)
  - `ahj_name` - Alternative AHJ name (String 255)
  - `county` - County name (String 255)
  - `city` - City name (String 255)
  - `guidelines` - Rich text guidance (Text)
  - `fireset_back` - Distance requirement (Float)
  - `jurisdiction_type` - Type of authority (String 100)
  - `phone` - Contact phone (String 50)
  - `email` - Contact email (String 255)
  - `website` - URL (String 500)
  - `created_at` - Timestamp
- **Purpose:** Authority Having Jurisdiction entities
- **Relationships:** 
  - One-to-Many: hasMany(utilities)
  - One-to-Many: hasMany(ahj_codes)

---

#### 3. **utilities** (13 columns, 0 rows)
- **Primary Key:** id (Integer)
- **Foreign Keys:**
  - `state_id` → states.id (NOT NULL)
  - `ahj_id` → ahjs.id (NULLABLE)
- **Columns:**
  - `name` - Utility name (String 255, NOT NULL)
  - `utility_name` - Alternative name (String 255, NOT NULL)
  - `requirements` - Rich text requirements (Text)
  - `eia_id` - Energy Information Admin ID (String 100)
  - `utility_type` - Type of utility (String 100)
  - `service_territory` - Service area (String 255)
  - `response_type` - Response classification (String 50)
  - `phone` - Contact number (String 50)
  - `website` - URL (String 500)
  - `created_at` - Timestamp
- **Purpose:** Utility companies and their requirements
- **Relationships:**
  - Many-to-One: belongsTo(states)
  - Many-to-One: belongsTo(ahjs)

---

#### 4. **codes** (12 columns, 0 rows)
- **Primary Key:** id (Integer)
- **Foreign Keys:**
  - `code_type_id` → code_types.id (NOT NULL)
  - `code_amendments` → code_amendments.id (NULLABLE)
  - `applicable_code_category_id` → applicable_code_categories.id (NULLABLE)
  - `state_id` → states.id (NULLABLE)
- **Columns:**
  - `code_name` - Code identifier (String 255, NOT NULL)
  - `title` - Display title (String 255, NOT NULL)
  - `description` - Rich text details (Text)
  - `edition` - Version/edition (String 100)
  - `issuing_body` - Authority that issued (String 255)
  - `adopted_at` - Adoption date (Date)
  - `created_at` - Timestamp
- **Purpose:** Building/safety codes and regulations
- **Relationships:**
  - Many-to-One: belongsTo(code_types)
  - Many-to-One: belongsTo(code_amendments)
  - Many-to-One: belongsTo(applicable_code_categories)
  - One-to-Many: hasMany(notes)
  - One-to-Many: hasMany(formulas)
  - Many-to-Many: hasMany(labels) via combination_mapper

---

#### 5. **code_types** (4 columns, 0 rows)
- **Primary Key:** id (Integer)
- **Columns:**
  - `title` - Type name (String 255)
  - `key` - Unique identifier (String 255)
  - `description` - Details (Text)
- **Purpose:** Classification of code types
- **Relationships:** One-to-Many: hasMany(codes)

---

#### 6. **labels** (14 columns, 0 rows)
- **Primary Key:** id (Integer)
- **Columns:**
  - `upc_code` - Barcode identifier (String 100, UNIQUE, NULLABLE)
  - `name` - Label name (String 255)
  - `label_number` - Unique label ID (String 100, UNIQUE, NOT NULL)
  - `label_name` - Display name (String 255, NOT NULL)
  - `field_type` - Type classification (String 100)
  - `description` - Rich text details (Text)
  - `length` - Dimension (Integer)
  - `width` - Dimension (Integer)
  - `image_url` - URL to label image (String 500)
  - `background_color` - Hex color (String 100)
  - `text_color` - Hex color (String 100)
  - `is_active` - Boolean flag (Boolean, default=1)
  - `created_at` - Timestamp
- **Purpose:** Product labels, certificates, markings
- **Relationships:** Many-to-Many: hasMany(codes) via combination_mapper

---

#### 7. **notes** (9 columns, 0 rows)
- **Primary Key:** id (Integer)
- **Foreign Keys:**
  - `note_type_id` → note_types.id (NULLABLE)
  - `code_id` → codes.id (NULLABLE)
  - `equipment_id` → equipment.id (NULLABLE)
- **Columns:**
  - `note_description` - Rich text note (Text, NOT NULL)
  - `page_no` - Reference page (Integer)
  - `length` - Measurement (Float)
  - `width` - Measurement (Float)
  - `section_no` - Reference section (Integer)
  - `created_at` - Timestamp
- **Purpose:** Detailed notes and annotations on codes/equipment
- **Relationships:**
  - Many-to-One: belongsTo(codes)
  - Many-to-One: belongsTo(note_types)
  - Many-to-One: belongsTo(equipment)

---

#### 8. **formulas** (5 columns, 0 rows)
- **Primary Key:** id (Integer)
- **Foreign Keys:**
  - `code_id` → codes.id (NOT NULL)
  - `formula_link_type_id` → formula_linker_types.id (NULLABLE)
- **Columns:**
  - `title` - Formula title (Text, NULLABLE)
  - `description` - Rich text formula details (Text, NOT NULL)
  - `created_at` - Timestamp
- **Purpose:** Formulas and calculations related to codes
- **Relationships:**
  - Many-to-One: belongsTo(codes)
  - Many-to-One: belongsTo(formula_linker_types)

---

#### 9. **combination_mapper** (5 columns, 0 rows)
- **Primary Key:** id (Integer)
- **Foreign Keys:**
  - `category_id` → categories.id (NULLABLE)
  - `equipment_id` → equipment.id (NULLABLE)
  - `code_id` → codes.id (NOT NULL)
  - `label_id` → labels.id (NOT NULL)
- **Purpose:** Many-to-Many junction table linking codes, labels, categories, and equipment
- **Relationships:** Junction point for code-label-equipment combinations

---

### Reference/Lookup Tables (No FK dependencies)

#### 10. **code_amendments** (2 columns, 0 rows)
- `id` - Primary Key
- `name` - Amendment description

#### 11. **applicable_code_categories** (2 columns, 0 rows)
- `id` - Primary Key
- `name` - Category name

#### 12. **categories** (2 columns, 0 rows)
- `id` - Primary Key
- `name` - Category name

#### 13. **equipment** (2 columns, 0 rows)
- `id` - Primary Key
- `name` - Equipment name

#### 14. **note_types** (3 columns, 0 rows)
- `id` - Primary Key
- `name` - Type name
- `variation_type` - Classification

#### 15. **formula_linker_types** (2 columns, 0 rows)
- `id` - Primary Key
- `name` - Type name

#### 16. **countries** (6 columns, 0 rows)
- `id` - Primary Key
- `name` - Country name
- `iso2`, `iso3`, `calling_code`, `created_at`

#### 17. **state_codes** (3 columns, 0 rows)
- `id` - Primary Key
- `state_id` → states.id
- `code_id` → codes.id

#### 18. **ahj_codes** (3 columns, 0 rows)
- `id` - Primary Key
- `ahj_id` → ahjs.id
- `code_id` → codes.id

---

### Administrative Tables

#### 19. **clients** (14 columns, 0 rows)
- Client management with: `spex_client_code`, `company_name`, `first_name`, `last_name`, contact info
- Relationships: One-to-Many: hasMany(preferences)

#### 20. **preferences** (9 columns, 0 rows)
- `client_id` → clients.id
- User settings: language, timezone, date_format, etc.

#### 21. **users** (3 columns, 0 rows)
- `id` - Primary Key
- `username` - Login (String)
- `password_hash` - Hashed password (String)

#### 22. **alembic_version** (auto-managed)
- Database migration tracking

---

## API Endpoints (FastAPI Routes)

### Registered API Routers
```
/api/v1/ahj              → AHJ CRUD operations
/api/v1/utility          → Utility CRUD operations
/api/v1/code-type        → Code Type CRUD
/api/v1/code             → Code CRUD
/api/v1/ahj-engine       → Complex AHJ Engine operations
/api/v1/state            → State Lookup operations
/api/v1/auth             → Authentication
/api/v1/states           → State management
/api/v1/label            → Label management
/api/v1/note             → Note management
/api/v1/formula          → Formula management
/api/v1/combination-mapper  → Mapper management
```

### Admin Panel
```
/admin          → SQLAdmin web interface
/docs           → Swagger API documentation
/redoc          → ReDoc API documentation
/static         → Static files (CKEditor, TinyMCE)
```

---

## Architecture Pattern

### Service Layer Architecture
```
API Router → Service → ORM Models → PostgreSQL DB
```

**Example Flow (AHJ Creation):**
1. POST `/api/v1/ahj/create` with AHJCreate schema
2. AHJAPI.create() validates via Pydantic schema
3. AHJService.create() processes business logic
4. AHJ model stored in DB via SQLAlchemy
5. AHJOut schema returned to client

### Key Files by Layer

**API Layer:**
- `/app/api/v1/*_api.py` - Route handlers and endpoint definitions

**Service Layer:**
- `/app/services/*_service.py` - Business logic (CRUD operations)

**Data Layer:**
- `/app/models/*.py` - SQLAlchemy ORM models
- `/app/schemas/*.py` - Pydantic request/response schemas

**Core:**
- `/app/core/database.py` - DB connection and session management
- `/app/core/security.py` - Authentication utilities
- `/app/core/error_handler.py` - Exception handling

**Admin:**
- `/app/admin/admin.py` - SQLAdmin configuration and model views

---

## Current Database State

**Total Records:** 0 (All tables empty - fresh schema)
**Last Action:** Database reset with schema resync
**Tables Created:** 22 (all verified)

### Schema Validation Status
All model columns match database columns:
- ✅ States table has all required columns
- ✅ AHJs table has `name` column (fixed)
- ✅ Utilities, Codes, Labels, Notes, Formulas all present
- ✅ Foreign key relationships validated
- ✅ All reference tables exist

---

## Key Design Patterns

### 1. **Canonical Name Pattern**
Entities like AHJ and Utility use dual-name strategy:
- `name` - Canonical/primary name
- `ahj_name`/`utility_name` - Alternative name
- Service logic ensures `name` is always set if either provided

### 2. **Rich Text Fields**
Following fields support HTML/formatted content:
- `guidelines` (ahjs)
- `requirements` (utilities)
- `description` (codes, labels, notes, formulas)

### 3. **Junction Tables**
- `combination_mapper` - Flexible linking of codes, labels, categories, equipment
- `state_codes`, `ahj_codes` - code associations
- `preferences` - client settings

### 4. **Timestamp Tracking**
- `created_at` - Auto-set on insert
- Most tables include this field

---

## TODO Items from Project

1. **Base Model Class** - Create inherited base class for common fields (id, created_at, updated_at, is_deleted, deleted_at)
2. **Rich Text Fields** - Ensure all designated fields support full rich text
3. **String Representations** - Add `__str__`, `__repr__` methods to all models
4. **Admin Interface** - Use custom templates for rich text fields (already implemented)

---

## Dependencies

**Key Python Packages:**
- `fastapi` (0.133.1) - Web framework
- `sqlalchemy` (2.0.47) - ORM
- `psycopg2-binary` (2.9.11) - PostgreSQL adapter
- `sqladmin` (0.18.0) - Admin interface
- `pydantic` (2.12.5) - Data validation
- `python-jose` (3.5.0) - JWT handling
- `boto3` (1.42.56) - AWS S3 integration

---

## S3/Cloud Integration

**AWS Configuration:**
- Endpoint: https://sjc1.vultrobjects.com
- Region: sjc1
- Bucket: test1
- Upload Handler: `/app/utils/s3_uploader.py`

---

## Next Steps to Populate Data

1. **Import States** - Use script or API: `/api/v1/states`
2. **Import AHJs** - Create AHJ records with state references
3. **Import Utilities** - Link to AHJs and states
4. **Import Code Types** - Reference data for codes
5. **Import Codes** - Main building codes with associations
6. **Import Labels** - Product labels and certifications
7. **Link Combinations** - Use combination_mapper to associate codes with labels/equipment

---

## Known Issues & Resolutions

**Issue:** 500 Error on admin panel for AHJs
**Cause:** Schema mismatch - `name` column missing from ahjs table
**Resolution:** Database reset script (reset_db.py) dropped and recreated all tables from current models

