#!/usr/bin/env python
"""
Database initialization script - Creates all tables safely
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

def get_existing_tables():
    """Get list of existing tables in database"""
    inspector = inspect(engine)
    return inspector.get_table_names()

def create_all_tables():
    """Create all tables from models"""
    try:
        print("🔍 Checking existing tables...")
        existing = get_existing_tables()
        print(f"   Found {len(existing)} existing tables: {existing if existing else 'None'}")
        
        print("\n📋 Creating tables from models...")
        Base.metadata.create_all(bind=engine)
        
        print("\n✅ Verifying tables were created...")
        new_tables = get_existing_tables()
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
            
        # Test connection by querying a table
        print("\n🧪 Testing database connection...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
            tables = [row[0] for row in result]
            print(f"   PostgreSQL confirms {len(tables)} tables exist")
            
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print(f"   Type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*60)
    print("DATABASE INITIALIZATION")
    print("="*60)
    
    success = create_all_tables()
    
    print("\n" + "="*60)
    if success:
        print("✅ DATABASE READY!")
        print("="*60)
        sys.exit(0)
    else:
        print("❌ DATABASE INITIALIZATION FAILED!")
        print("="*60)
        sys.exit(1)
