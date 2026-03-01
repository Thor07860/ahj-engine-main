#!/usr/bin/env python
"""
Database reset script - Drops and recreates all tables to sync with models
"""

from sqlalchemy import inspect, text
from app.core.database import engine, Base
import sys

# Import all models to register them with SQLAlchemy
from app.models.state import State
from app.models.ahj import AHJ
from app.models.utility import Utility
from app.models.code import Code
from app.models.code_type import CodeType
from app.models.label import Label
from app.models.note import Note
from app.models.formula import Formula
from app.models.combination_mapper import CombinationMapper
from app.models.user import User

def reset_database():
    """Drop and recreate all tables"""
    try:
        print("🔍 Checking existing tables...")
        inspector = inspect(engine)
        existing = inspector.get_table_names()
        print(f"   Found {len(existing)} existing tables")
        
        if existing:
            print("\n🗑️  Dropping all tables...")
            with engine.connect() as conn:
                # Get all table names
                for table_name in reversed(existing):
                    if table_name != 'alembic_version':  # Skip alembic version table
                        print(f"   Dropping table: {table_name}")
                        conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE"))
                conn.commit()
            print("   ✅ All tables dropped!")
        
        print("\n📋 Creating all tables from models...")
        Base.metadata.create_all(bind=engine)
        
        print("\n✅ Verifying tables were created...")
        new_tables = inspector.get_table_names()
        print(f"   Now have {len(new_tables)} tables: {new_tables}")
        
        # Verify critical tables
        required_tables = ['states', 'ahjs', 'utilities', 'codes', 'code_types', 
                          'labels', 'notes', 'formulas', 'combination_mapper', 'users']
        
        missing = [t for t in required_tables if t not in new_tables]
        if missing:
            print(f"\n❌ MISSING TABLES: {missing}")
            return False
        else:
            print(f"\n✅ All required tables exist!")
        
        # Test connection and verify column exists
        print("\n🧪 Testing database connection...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
            tables = [row[0] for row in result]
            print(f"   PostgreSQL confirms {len(tables)} tables exist")
            
            # Check if ahjs table has name column
            columns = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='ahjs'"))
            col_names = [row[0] for row in columns]
            print(f"   AHJ table columns: {col_names}")
            
            if 'name' in col_names:
                print(f"   ✅ 'name' column exists in ahjs table!")
            else:
                print(f"   ❌ 'name' column MISSING in ahjs table!")
                return False
            
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print(f"   Type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*60)
    print("DATABASE RESET")
    print("="*60)
    
    success = reset_database()
    
    print("\n" + "="*60)
    if success:
        print("✅ DATABASE RESET COMPLETE!")
        print("="*60)
        sys.exit(0)
    else:
        print("❌ DATABASE RESET FAILED!")
        print("="*60)
        sys.exit(1)
