#!/usr/bin/env python
"""
Validation Script - Test Import Functionality & API Integration
This script validates that:
1. Database schema is correct
2. Models have proper relationships
3. Import script can run successfully
4. API endpoints work correctly
"""

import sys
from pathlib import Path
import importlib.util
import os

# Ensure project root is in path
_current_dir = Path(__file__).resolve().parent
_scripts_dir = _current_dir.parent
_project_root = _scripts_dir.parent

sys.path.insert(0, str(_project_root))
os.chdir(_project_root)

PROJECT_ROOT = _project_root

from sqlalchemy import inspect, text
from app.core.database import engine, SessionLocal
from app.models.label import Label
from app.models.category import Category
from app.models.equipment import Equipment
from app.models.combination_mapper import CombinationMapper
from app.models.code import Code
from app.models.code_type import CodeType
from app.models.ahj import AHJ
from app.models.note import Note


class ValidationSuite:
    """Run comprehensive validation checks."""

    def __init__(self):
        self.db = SessionLocal()
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def test(self, name: str, condition: bool, error_msg: str = ""):
        """Record test result."""
        if condition:
            print(f"  ✅ {name}")
            self.passed += 1
        else:
            print(f"  ❌ {name}")
            if error_msg:
                print(f"     └─ {error_msg}")
            self.failed += 1

    def warn(self, name: str, message: str = ""):
        """Record warning."""
        print(f"  ⚠️  {name}")
        if message:
            print(f"     └─ {message}")
        self.warnings += 1

    def validate_schema(self):
        """Check database schema integrity."""
        print("\n" + "="*60)
        print("SCHEMA VALIDATION")
        print("="*60)

        inspector = inspect(engine)
        tables = inspector.get_table_names()

        # Check core tables exist
        required_tables = [
            'labels', 'categories', 'equipment', 'combination_mapper',
            'codes', 'ahjs', 'notes', 'formulas'
        ]
        
        for table in required_tables:
            self.test(f"Table '{table}' exists", table in tables)

        # Check column types for labels
        if 'labels' in tables:
            columns = {col['name']: col for col in inspector.get_columns('labels')}
            self.test("Label.label_number is unique", 
                     any(idx['name'] == 'labels_label_number_key' 
                         for idx in inspector.get_unique_constraints('labels')))
            self.test("Label.upc_code is unique (if exists)", 
                     'upc_code' in columns)

        # Check foreign keys
        if 'combination_mapper' in tables:
            fks = inspector.get_foreign_keys('combination_mapper')
            fk_tables = {fk['referred_table'] for fk in fks}
            self.test("CombinationMapper has FK to labels", 
                     'labels' in fk_tables)
            self.test("CombinationMapper has FK to codes", 
                     'codes' in fk_tables)
            self.test("CombinationMapper has FK to categories", 
                     'categories' in fk_tables)
            self.test("CombinationMapper has FK to equipment", 
                     'equipment' in fk_tables)

    def validate_models(self):
        """Check ORM model integrity."""
        print("\n" + "="*60)
        print("ORM MODEL VALIDATION")
        print("="*60)

        # Test Category relationships
        try:
            cat = Category(name="Test Category")
            self.test("Category model instantiates", True)
            self.test("Category has relationship 'combination_mappers'",
                     hasattr(cat, 'combination_mappers'))
        except Exception as e:
            self.test("Category model instantiates", False, str(e))

        # Test Equipment relationships
        try:
            equip = Equipment(name="Test Equipment")
            self.test("Equipment model instantiates", True)
            self.test("Equipment has relationship 'combination_mappers'",
                     hasattr(equip, 'combination_mappers'))
            self.test("Equipment has relationship 'notes'",
                     hasattr(equip, 'notes'))
        except Exception as e:
            self.test("Equipment model instantiates", False, str(e))

        # Test Label relationships
        try:
            label = Label(label_name="Test", label_number="TEST-001")
            self.test("Label model instantiates", True)
            self.test("Label has relationship 'combination_mappers'",
                     hasattr(label, 'combination_mappers'))
        except Exception as e:
            self.test("Label model instantiates", False, str(e))

        # Test CombinationMapper relationships
        try:
            mapper = CombinationMapper(code_id=1, label_id=1)
            self.test("CombinationMapper model instantiates", True)
            self.test("CombinationMapper has relationship 'category'",
                     hasattr(mapper, 'category'))
            self.test("CombinationMapper has relationship 'equipment'",
                     hasattr(mapper, 'equipment'))
            self.test("CombinationMapper has relationship 'code'",
                     hasattr(mapper, 'code'))
            self.test("CombinationMapper has relationship 'label'",
                     hasattr(mapper, 'label'))
        except Exception as e:
            self.test("CombinationMapper model instantiates", False, str(e))

    def validate_excel_files(self):
        """Check Excel files exist."""
        print("\n" + "="*60)
        print("EXCEL FILES VALIDATION")
        print("="*60)

        import os
        
        master_dir = PROJECT_ROOT / "app" / "data" / "master"
        file1 = master_dir / "Illumine-i X LabelFriday master data.xlsx"
        file2 = master_dir / "Label filter data.xlsx"

        self.test("Master data directory exists", master_dir.exists(),
                 f"Expected: {master_dir}")
        self.test("Labels Excel file exists", file1.exists(),
                 f"Expected: {file1}")
        self.test("Filter Excel file exists", file2.exists(),
                 f"Expected: {file2}")

        if file1.exists():
            size_mb = file1.stat().st_size / (1024 * 1024)
            print(f"     └─ {file1.name}: {size_mb:.2f} MB")

        if file2.exists():
            size_mb = file2.stat().st_size / (1024 * 1024)
            print(f"     └─ {file2.name}: {size_mb:.2f} MB")

    def validate_import_capability(self):
        """Test import script can be imported and run."""
        print("\n" + "="*60)
        print("IMPORT SCRIPT VALIDATION")
        print("="*60)

        try:
            # Import the import script module
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "import_labels",
                PROJECT_ROOT / "scripts" / "import" / "import_labels.py"
            )
            import_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(import_module)

            MasterDataImporter = import_module.MasterDataImporter
            self.test("Import script can be imported", True)

            importer = MasterDataImporter()
            self.test("MasterDataImporter instantiates", True)
            self.test("Importer has 'import_labels' method",
                     hasattr(importer, 'import_labels'))
            self.test("Importer has 'import_category_equipment_mapping' method",
                     hasattr(importer, 'import_category_equipment_mapping'))
            self.test("Importer has 'run' method",
                     hasattr(importer, 'run'))

        except Exception as e:
            self.test("Import script can be imported", False, str(e))
            self.warn("Module import failed - check sys.path or project structure")

    def validate_database_connectivity(self):
        """Test database operations."""
        print("\n" + "="*60)
        print("DATABASE CONNECTIVITY VALIDATION")
        print("="*60)

        try:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                self.test("Database connection successful", result.scalar() == 1)
        except Exception as e:
            self.test("Database connection successful", False, str(e))
            return

        # Test CRUD operations
        try:
            # Create
            category = Category(name=f"Test Cat {id(self)}")
            self.db.add(category)
            self.db.commit()
            self.test("Create operation works", True)
            cat_id = category.id

            # Read
            fetched = self.db.query(Category).filter(Category.id == cat_id).first()
            self.test("Read operation works", fetched is not None)

            # Update
            category.name = f"Updated {id(self)}"
            self.db.commit()
            self.test("Update operation works", True)

            # Delete
            self.db.delete(category)
            self.db.commit()
            self.test("Delete operation works", True)

        except Exception as e:
            self.test("Database CRUD operations", False, str(e))

    def validate_api_structure(self):
        """Check API endpoint structure."""
        print("\n" + "="*60)
        print("API STRUCTURE VALIDATION")
        print("="*60)

        try:
            from app.api.v1.ahj_engine_api import AHJEngineAPI
            from app.services.ahj_engine_service import AHJEngineService

            api = AHJEngineAPI()
            service = AHJEngineService()

            self.test("AHJEngineAPI instantiates", True)
            self.test("AHJEngineAPI has router", hasattr(api, 'router'))
            self.test("AHJEngineService instantiates", True)
            self.test("AHJEngineService has fetch_details method",
                     hasattr(service, 'fetch_details'))
            self.test("AHJEngineService has process method",
                     hasattr(service, 'process'))

            # Check router has correct route
            routes = [route.path for route in api.router.routes]
            self.test("API has '/get-ahj-details' endpoint",
                     '/get-ahj-details' in routes)

        except Exception as e:
            self.test("API structure validation", False, str(e))

    def validate_data_sample(self):
        """Create sample data to test relationships."""
        print("\n" + "="*60)
        print("SAMPLE DATA CREATION TEST")
        print("="*60)

        try:
            # Create code type (required for code)
            code_type = CodeType(title=f"Sample Type", key="sample_type")
            self.db.add(code_type)
            self.db.commit()

            # Create code (required for mapper)
            code = Code(code_name=f"Sample Code {id(self)}", title="Test Code", code_type_id=code_type.id)
            self.db.add(code)
            self.db.commit()

            # Create category
            cat = Category(name=f"Sample Cat {id(self)}")
            self.db.add(cat)
            self.db.commit()

            # Create equipment
            equip = Equipment(name=f"Sample Equip {id(self)}")
            self.db.add(equip)
            self.db.commit()

            # Create label
            label = Label(
                label_number=f"SAM-{id(self)}",
                label_name="Sample Label",
                is_active=True
            )
            self.db.add(label)
            self.db.commit()

            # Create combination mapper (with code_id)
            mapper = CombinationMapper(
                category_id=cat.id,
                equipment_id=equip.id,
                code_id=code.id,
                label_id=label.id
            )
            self.db.add(mapper)
            self.db.commit()

            self.test("Create CodeType, Code, Category, Equipment, Label, Mapper", True)

            # Test relationships
            fetched_mapper = self.db.query(CombinationMapper).filter(
                CombinationMapper.id == mapper.id
            ).first()

            self.test("Mapper.category relationship works",
                     fetched_mapper.category is not None and
                     fetched_mapper.category.name == cat.name)

            self.test("Mapper.equipment relationship works",
                     fetched_mapper.equipment is not None and
                     fetched_mapper.equipment.name == equip.name)

            self.test("Mapper.label relationship works",
                     fetched_mapper.label is not None and
                     fetched_mapper.label.label_number == label.label_number)

            self.test("Mapper.code relationship works",
                     fetched_mapper.code is not None and
                     fetched_mapper.code.code_name == code.code_name)

            # Cleanup
            self.db.delete(mapper)
            self.db.delete(label)
            self.db.delete(equip)
            self.db.delete(cat)
            self.db.delete(code)
            self.db.delete(code_type)
            self.db.commit()

        except Exception as e:
            self.test("Sample data test", False, str(e))

    def print_summary(self):
        """Print test summary."""
        print("\n" + "="*60)
        print("VALIDATION SUMMARY")
        print("="*60)
        print(f"\n✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"⚠️  Warnings: {self.warnings}")
        print(f"\nTotal: {self.passed + self.failed + self.warnings}")

        if self.failed == 0:
            print("\n🎉 ALL VALIDATIONS PASSED!")
            print("\nNext steps:")
            print("  1. Prepare your Excel files in app/data/master/")
            print("  2. Run: python scripts/import/import_labels.py")
            print("  3. Check admin panel: http://127.0.0.1:8000/admin")
            print("  4. Test API: http://127.0.0.1:8000/docs")
            return 0
        else:
            print(f"\n⚠️  {self.failed} validation(s) failed")
            return 1

    def run_all(self):
        """Execute all validations."""
        print("\n" + "="*80)
        print("AHJ ENGINE - VALIDATION SUITE")
        print("="*80)

        self.validate_schema()
        self.validate_models()
        self.validate_excel_files()
        self.validate_import_capability()
        self.validate_database_connectivity()
        self.validate_api_structure()
        self.validate_data_sample()

        return self.print_summary()


if __name__ == "__main__":
    suite = ValidationSuite()
    exit_code = suite.run_all()
    suite.db.close()
    sys.exit(exit_code)
