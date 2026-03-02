from sqlalchemy import text
from app.core.database import engine

with engine.connect() as conn:
    # Check unique values
    ln_query = conn.execute(text('SELECT COUNT(DISTINCT label_number) FROM labels WHERE label_number IS NOT NULL')).scalar()
    lname_query = conn.execute(text('SELECT COUNT(DISTINCT label_name) FROM labels WHERE label_name IS NOT NULL')).scalar()
    name_query = conn.execute(text('SELECT COUNT(DISTINCT name) FROM labels WHERE name IS NOT NULL')).scalar()
    
    print(f'Unique label_number values: {ln_query}')
    print(f'Unique label_name values: {lname_query}')
    print(f'Unique name (Label Type) values: {name_query}')
    
    # Show unique names
    names = conn.execute(text('SELECT DISTINCT name FROM labels ORDER BY name')).fetchall()
    print(f'\nLabel Types (name field):')
    for n in names:
        print(f'  - {n[0]}')
    
    # Show unique label_numbers
    print(f'\nSample label_number values:')
    lns = conn.execute(text('SELECT DISTINCT label_number FROM labels WHERE label_number IS NOT NULL LIMIT 10')).fetchall()
    for ln in lns:
        print(f'  - {ln[0]}')
