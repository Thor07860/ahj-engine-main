#!/usr/bin/env python
"""
Initialize Database - Setup Tables and Seed Initial Data
This script creates all database tables and imports master data from Excel files.
Run this ONCE on first deployment or when setting up a new environment.

Usage:
    python init_db.py
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

def init_database():
    """Initialize database: create tables and import data."""
    
    print("\n" + "="*70)
    print("DATABASE INITIALIZATION")
    print("="*70)
    
    try:
        # Step 1: Create all tables
        print("\n[1/4] Creating database tables...")
        from app.core.database import engine, Base
        Base.metadata.create_all(bind=engine)
        print("✓ All tables created successfully")
        
        # Step 2: Import reference data (CodeAmendments, ApplicableCodeCategories)
        print("\n[2/4] Importing reference data...")
        from app.core.database import SessionLocal
        from app.models.code_amendment import CodeAmendment
        from app.models.applicable_code_category import ApplicableCodeCategory
        
        db = SessionLocal()
        
        # Check if already imported
        existing_amendments = db.query(CodeAmendment).count()
        if existing_amendments == 0:
            amendments = [
                CodeAmendment(name="LOCAL"),
                CodeAmendment(name="STATE"),
                CodeAmendment(name="STANDARD"),
                CodeAmendment(name="INTERNATIONAL"),
            ]
            db.add_all(amendments)
            db.commit()
            print(f"✓ Created {len(amendments)} code amendments")
        else:
            print(f"✓ Code amendments already exist ({existing_amendments} records)")
        
        existing_categories = db.query(ApplicableCodeCategory).count()
        if existing_categories == 0:
            categories = [
                ApplicableCodeCategory(name="Building"),
                ApplicableCodeCategory(name="Electrical"),
                ApplicableCodeCategory(name="Energy"),
                ApplicableCodeCategory(name="Fire"),
                ApplicableCodeCategory(name="Mechanical"),
                ApplicableCodeCategory(name="Plumbing"),
                ApplicableCodeCategory(name="Residential"),
            ]
            db.add_all(categories)
            db.commit()
            print(f"✓ Created {len(categories)} applicable code categories")
        else:
            print(f"✓ Code categories already exist ({existing_categories} records)")
        
        db.close()
        
        # Step 3: Import Excel data (if files exist)
        print("\n[3/4] Importing data from Excel files...")
        
        excel_files = [
            ("scripts/import/import_codes.py", "Codes"),
            ("scripts/import/import_equipment_categories.py", "Equipment & Categories"),
            ("scripts/import/import_labels_new.py", "Labels"),
        ]
        
        for script_path, data_type in excel_files:
            script_file = PROJECT_ROOT / script_path
            if script_file.exists():
                try:
                    # Import and run the script
                    import subprocess
                    result = subprocess.run([sys.executable, str(script_file)], 
                                          capture_output=True, text=True, timeout=60)
                    if result.returncode == 0:
                        print(f"✓ {data_type} imported successfully")
                    else:
                        print(f"⚠ {data_type} import had warnings/errors")
                        if result.stderr:
                            print(f"  Error: {result.stderr[:100]}")
                except Exception as e:
                    print(f"⚠ Could not run {data_type} import: {str(e)[:50]}")
            else:
                print(f"⚠ {data_type} import script not found: {script_path}")
        
        # Step 4: Verify database
        print("\n[4/4] Verifying database...")
        from sqlalchemy import text
        
        with engine.connect() as conn:
            tables = conn.execute(text('''
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public'
            ''')).fetchall()
            
            counts = {}
            for (table_name,) in tables:
                result = conn.execute(text(f'SELECT COUNT(*) FROM {table_name}'))
                count = result.scalar()
                counts[table_name] = count
            
            print(f"✓ Database has {len(counts)} tables")
            
            # Show key table counts
            key_tables = {
                'states': 'States',
                'codes': 'Codes',
                'labels': 'Labels',
                'equipment': 'Equipment',
                'categories': 'Categories',
                'utilities': 'Utilities',
                'ahjs': 'AHJs'
            }
            
            print("\nData Summary:")
            for table_key, table_label in key_tables.items():
                count = counts.get(table_key, 0)
                status = "✓" if count > 0 else "⚠"
                print(f"  {status} {table_label:20} : {count:6} records")
        
        print("\n" + "="*70)
        print("✓ DATABASE INITIALIZATION COMPLETE")
        print("="*70)
        print("\nYour database is ready! You can now:")
        print("  1. Start the API: python -m uvicorn app.main:app --reload")
        print("  2. Access admin panel: http://localhost:8000/admin")
        print("="*70 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n✗ INITIALIZATION FAILED")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
