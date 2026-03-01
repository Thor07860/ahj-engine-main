from sqlalchemy import text
from app.core.database import engine

with engine.connect() as conn:
    # Overall count
    total = conn.execute(text('SELECT COUNT(*) FROM labels')).scalar()
    print(f'✓ Total Labels Imported: {total}')
    print()
    
    # Sample labels
    samples = conn.execute(text('''
        SELECT id, upc_code, name, description, length, width, background_color, text_color
        FROM labels 
        LIMIT 5
    ''')).fetchall()
    
    print('Sample Labels:')
    for label in samples:
        print(f'  [{label[0]}] {label[1]} - {label[2]}')
        if label[3]:
            desc = label[3][:50] + '...' if len(label[3]) > 50 else label[3]
            print(f'      Description: {desc}')
        if label[4] and label[5]:
            print(f'      Size: {label[4]}" x {label[5]}"')
        print(f'      Colors: {label[6]} on {label[7]}')
        print()
    
    # Color distribution
    colors = conn.execute(text('''
        SELECT background_color, COUNT(*) as count 
        FROM labels 
        GROUP BY background_color 
        ORDER BY count DESC
    ''')).fetchall()
    
    print('Color Distribution:')
    for color, count in colors:
        print(f'  {color}: {count} labels')
