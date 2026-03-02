# AHJ Engine — Single Run & Overview Guide

This is the **single file** you need to understand and run the project.

## 1) What this project does (top to bottom)

This project is a FastAPI-based backend for AHJ/regulatory intelligence and admin data management.

### Core purpose
- Store and manage regulatory master data (Countries, States, AHJs, Utilities).
- Store code catalogs (code types, categories, standards/local codes).
- Store equipment/category/label data for mappings.
- Expose APIs for lookup and AHJ engine workflows.
- Provide an SQLAdmin web panel for CRUD and operations.

### Architecture flow
1. **App entrypoint**: `app/main.py`
   - Starts FastAPI app
   - Registers routers under `/api/v1/*`
   - Mounts SQLAdmin under `/admin`
2. **Database layer**: `app/core/database.py`
   - SQLAlchemy engine/session/base models
3. **Models**: `app/models/*`
   - Define tables and relationships
4. **Services**: `app/services/*`
   - Business logic used by APIs/admin
5. **Schemas**: `app/schemas/*`
   - Request/response models
6. **Migrations**: `alembic/*`
   - Versioned schema changes
7. **Master data imports**: `scripts/import/*`
   - Reads Excel files from `data/master/`
   - Populates DB tables

### Data source
Excel master files are under: `data/master/`
- `Regulatory data.xlsx`
- `code mapping.xlsx`
- `Equipment Category and types.xlsx`
- `Illumine-i X LabelFriday master data.xlsx`

---

## 2) What was fixed recently

- Fixed schema drift causing admin 500 errors (missing columns).
- Added/updated Alembic migrations to align DB with model expectations.
- Fixed import blockers:
  - Country import now handles `iso3` safely.
  - Label length/width schema mismatch resolved.
  - Combination mapper nullability mismatch resolved.
- Improved label admin dropdown refresh so options are loaded dynamically when form opens.
- Added a one-command master import runner.

---

## 3) One-command setup/import

Run this from project root:

```bash
python scripts/import/import_all_master_data.py
```

What it does in order:
1. `alembic upgrade head`
2. Import regulatory data
3. Import codes
4. Import equipment/categories
5. Import labels

If this command completes, tables + master data are ready for dropdowns and admin usage.

---

## 4) Run the application

```bash
uvicorn app.main:app --reload
```

Access:
- API root: `http://127.0.0.1:8000/`
- Admin panel: `http://127.0.0.1:8000/admin/`

---

## 5) Quick validation commands

Check Alembic head:

```bash
python -m alembic current
```

Expected: current revision should show `(head)`.

---

## 6) Notes

- Keep these dependency files (do not delete):
  - `requirements.txt`
  - `requirements.frozen.txt`
- If data appears empty again, rerun:
  - `python scripts/import/import_all_master_data.py`
