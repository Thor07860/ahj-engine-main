from sqlalchemy import text, inspect
from app.core.database import engine

print("="*70)
print("DATABASE AUDIT - Full System Check")
print("="*70)

with engine.connect() as conn:
    # Get all tables
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print(f"\n✓ Total Tables: {len(tables)}")
    print(f"Tables: {', '.join(sorted(tables))}")
    
    # Check record counts
    print("\n" + "="*70)
    print("DATA COUNTS BY TABLE")
    print("="*70)
    
    counts = {}
    for table in sorted(tables):
        try:
            result = conn.execute(text(f'SELECT COUNT(*) FROM {table}'))
            count = result.scalar()
            counts[table] = count
            status = "✓" if count > 0 else "⚠"
            print(f"{status} {table:30} : {count:5} records")
        except Exception as e:
            print(f"✗ {table:30} : Error - {str(e)[:50]}")
    
    # Check for duplicate states abbreviations
    print("\n" + "="*70)
    print("CHECKING UNIQUE CONSTRAINTS")
    print("="*70)
    
    try:
        duplicates = conn.execute(text('''
            SELECT abbrev, COUNT(*) as cnt 
            FROM states 
            GROUP BY abbrev 
            HAVING COUNT(*) > 1
        ''')).fetchall()
        
        if duplicates:
            print("\n⚠ DUPLICATE STATE ABBREVIATIONS FOUND:")
            for abbrev, cnt in duplicates:
                print(f"  - {abbrev}: {cnt} records")
        else:
            print("\n✓ No duplicate state abbreviations")
    except Exception as e:
        print(f"Error checking duplicates: {e}")
    
    # Show UPC duplicates in labels
    try:
        upc_dupes = conn.execute(text('''
            SELECT upc_code, COUNT(*) as cnt 
            FROM labels 
            GROUP BY upc_code 
            HAVING COUNT(*) > 1
        ''')).fetchall()
        
        if upc_dupes:
            print("\n⚠ DUPLICATE UPC CODES IN LABELS:")
            for upc, cnt in upc_dupes:
                print(f"  - {upc}: {cnt} records")
        else:
            print("✓ No duplicate UPC codes in labels")
    except:
        pass
    
    # Sample data from key tables
    print("\n" + "="*70)
    print("SAMPLE DATA")
    print("="*70)
    
    # States
    states = conn.execute(text('SELECT id, name, abbrev FROM states LIMIT 3')).fetchall()
    print(f"\n✓ Sample States:")
    for s in states:
        print(f"  - {s[0]}: {s[1]} ({s[2]})")
    
    # Codes
    codes = conn.execute(text('SELECT id, title FROM codes LIMIT 3')).fetchall()
    print(f"\n✓ Sample Codes:")
    for c in codes:
        print(f"  - {c[0]}: {c[1][:50]}")
    
    # Labels
    labels = conn.execute(text('SELECT id, upc_code, name FROM labels LIMIT 3')).fetchall()
    print(f"\n✓ Sample Labels:")
    for l in labels:
        print(f"  - {l[0]}: {l[1]} - {l[2]}")
    
    # Equipment & Categories
    equip = conn.execute(text('SELECT id, name FROM equipment LIMIT 3')).fetchall()
    print(f"\n✓ Sample Equipment:")
    for e in equip:
        print(f"  - {e[0]}: {e[1]}")
    
    cat = conn.execute(text('SELECT id, name FROM categories LIMIT 3')).fetchall()
    print(f"\n✓ Sample Categories:")
    for c in cat:
        print(f"  - {c[0]}: {c[1]}")
    
    # Combination Mapper
    mapper = conn.execute(text('SELECT COUNT(*) FROM combination_mapper')).scalar()
    print(f"\n✓ Combination Mappers: {mapper} records")
    
    print("\n" + "="*70)
