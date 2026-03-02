"""
AHJ Engine Application Package
Initializes database tables and core configuration on module import
"""

# Initialize database tables when app module is imported
try:
    from app.core.database import init_db
    init_db()
except Exception as e:
    print(f"[WARNING] Database initialization during import failed: {e}")
    # Don't fail on import - allow app to start and retry on first request
    pass
