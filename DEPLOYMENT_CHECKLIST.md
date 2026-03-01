# 🚀 DEPLOYMENT CHECKLIST

**Status:** Ready for Render Deployment  
**Last Updated:** March 1, 2026

---

## Pre-Deployment Verification

### Database ✓
- [x] 22 tables created
- [x] All indices created
- [x] Unique constraints in place (states.abbrev, labels.upc_code)
- [x] Foreign key relationships verified
- [x] No orphaned records

### Data Imports ✓
- [x] 398 Codes imported (code_mapping.xlsx)
- [x] 410 Labels imported (Illumine-i X LabelFriday master data.xlsx)
- [x] 26 Equipment items imported
- [x] 14 Categories imported
- [x] 26 Combination Mappers (equipment↔category links)
- [x] 4 Code Amendments (LOCAL, STATE, STANDARD, INTERNATIONAL)
- [x] 7 Code Categories (Building, Electrical, Fire, Mechanical, Plumbing, Residential, Energy)

### Application Features ✓
- [x] FastAPI backend working
- [x] SQLAdmin admin panel accessible
- [x] Form auto-fill for labels (UPC → Length/Width/Description)
- [x] Color pickers for label colors
- [x] Rich text editor for descriptions
- [x] Dynamic dropdowns pulling from database
- [x] API endpoints for label retrieval
- [x] Database audit script

### Code Quality ✓
- [x] No syntax errors
- [x] All imports resolved
- [x] Database models synchronized
- [x] Migration scripts ready (Alembic)
- [x] Error handling implemented

---

## Deployment Steps

### 1. Prepare GitHub Repository
```bash
# Ensure all files are committed
git add .
git commit -m "AHJ Engine - Ready for Render deployment"
git push origin main
```

**Files to include:**
- ✓ app/ (application code)
- ✓ scripts/import/ (data import scripts)
- ✓ requirements.txt (dependencies)
- ✓ init_db_full.py (database initialization)
- ✓ Procfile (Render configuration)
- ✓ build.sh (build script)
- ✓ SYSTEM_DOCUMENTATION.md (this documentation)

### 2. Create Render Service

**Steps:**
1. Go to https://render.com/dashboard
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Select your branch (main)

### 3. Configure Environment

**Settings in Render Dashboard:**

```
Name: ahj-engine
Runtime: Python 3.11
Build Command: bash build.sh
Start Command: gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

**Environment Variables:**

```
DATABASE_URL = postgresql://user:password@host:5432/dbname
DEBUG = false
SECRET_KEY = generate-a-random-secret-key-here
PYTHONUNBUFFERED = true
```

**How to Generate SECRET_KEY:**
```python
import secrets
print(secrets.token_urlsafe(32))
# Copy output to SECRET_KEY env var
```

### 4. Database Setup

**Option A: Use Render PostgreSQL (Recommended)**
1. Create Render PostgreSQL instance
2. Render auto-generates DATABASE_URL
3. Paste into Web Service environment

**Option B: Use External PostgreSQL**
1. Get connection string from your DB host
2. Format: `postgresql://user:password@hostname:5432/dbname`
3. Paste into environment

### 5. Deploy

**Initial Deploy:**
```
1. Click "Deploy"
2. Watch build process (5-10 minutes)
3. Check logs for:
   ✓ dependencies installed
   ✓ database tables created
   ✓ data imports completed
   ✓ no errors
```

**First Run Actions (Automatic):**
1. Creates all 22 tables
2. Imports reference data (amendments, categories)
3. Imports 398 codes
4. Imports 410 labels
5. Sets up equipment & categories
6. Verifies database integrity

### 6. Access Application

**After Deployment:**
```
Web Interface: https://your-app.onrender.com/admin
API Docs: https://your-app.onrender.com/docs
Health Check: https://your-app.onrender.com/api/v1/label/
```

---

## Post-Deployment Verification

### Immediate Checks

1. **Check Server Status**
   ```
   Visit: https://your-app.onrender.com/docs
   Expected: FastAPI automatic docs page
   ```

2. **Verify Database Connection**
   ```
   Check Render dashboard → Web Service → Logs
   Looking for: "✓ Database initialized" messages
   ```

3. **Access Admin Panel**
   ```
   URL: https://your-app.onrender.com/admin
   Expected: Admin dashboard loading
   ```

4. **Test Database**
   ```
   Go to Admin → Labels
   Expected: 410 label records visible
   Select any label: should show UPC code, dimensions, colors
   ```

### Health Checks

```bash
# Test API endpoint (can do from local machine)
curl https://your-app.onrender.com/api/v1/label/1/details

# Expected response:
{
  "id": 1,
  "upc_code": "LF-001",
  "name": "WRITE IN LABEL",
  "length": 4,
  "width": 1,
  "description": "Write in DC label",
  ...
}
```

---

## Database

### Total Data Volume
- **22 tables** created
- **~12,000 records** total
- **Largest table:** AHJs (10,521 records)
- **Key table for UI:** Labels (410 records)

### Record Breakdown
```
states               : 50
countries           : 249
utilities           : 990
ahjs               : 10,521
codes               : 398 ✓ IMPORTED
labels              : 410 ✓ IMPORTED
equipment           : 26 ✓ IMPORTED
categories          : 14 ✓ IMPORTED
combination_mapper  : 26 ✓ IMPORTED
code_types          : 10
code_amendments     : 4
applicable_code_categories : 7
Others              : various empty tables
```

---

## Monitoring & Maintenance

### Daily Monitoring
- Check error logs: Render Dashboard → Logs
- Monitor response times: Render Dashboard → Metrics
- Watch database size: Render Dashboard → Settings

### Weekly Maintenance
- Backup database (if not auto-backed up)
- Review error patterns
- Check resource usage

### When Adding New Data

**Import Process:**
1. Prepare Excel file in: `data/master/`
2. Create import script in: `scripts/import/`
3. Run locally: `python scripts/import/your_script.py`
4. Test in admin panel
5. If good, push to GitHub and redeploy

---

## Rollback Procedure

If deployment fails:

1. **Check Logs:**
   ```
   Render Dashboard → Web Service → Logs
   Look for error messages
   ```

2. **Common Issues:**
   - DATABASE_URL not set → add to environment variables
   - Dependencies missing → update requirements.txt
   - Migration failed → check Alembic scripts
   - Import script error → check Excel file format

3. **Rollback:**
   ```
   Render Dashboard → Deployments
   Click previous working deployment
   Click "Rollback"
   ```

---

## Support & Troubleshooting

### Issue: Build Fails

**Check:**
1. Are all dependencies in requirements.txt?
2. Is Python version compatible (3.9+)?
3. Does build.sh have execute permissions?

**Fix:**
```bash
# Local test
python init_db_full.py  # Should complete without errors
```

### Issue: Database Connection Failed

**Check:**
1. Is DATABASE_URL set correctly?
2. Is PostgreSQL running?
3. Are credentials correct?

**Fix:**
```
Render Dashboard → Settings → Environment Variables
Verify DATABASE_URL format is correct
```

### Issue: Admin Panel Loads but No Data

**Check:**
1. Are imports running? Check logs
2. Is database initialized? Check table counts

**Fix:**
```
Render Dashboard → Logs → full history
Look for: "Labels Created: 410"
```

---

## Performance Notes

### Expected Performance
- Admin panel load: < 2 seconds
- Label dropdown: < 1 second (410 options)
- Form auto-fill: < 500ms
- Database query: < 100ms

### Database Size
- Current: ~ 50-100 MB
- With file attachments: could grow to 500 MB+
- Render free tier handles up to 10 GB

---

## Success Criteria

Your deployment is successful when:

✓ Web service running without errors  
✓ Admin panel accessible at /admin  
✓ 410 labels visible in database  
✓ Dropdown selectors work  
✓ Form auto-fill working  
✓ API endpoints responding  
✓ Database queries fast (< 100ms)  

---

## Next Steps (Future Development)

1. **Import remaining data:**
   - Notes/Placard descriptions
   - Formulas and calculations
   - Additional code specifications

2. **Add features:**
   - User authentication
   - Multi-language support
   - PDF label generation
   - Mobile app API

3. **Scaling:**
   - Add caching (Redis)
   - Optimize queries
   - Add CDN for static files

---

**Deployment Date:** _____________  
**Deployed By:** _____________  
**Environment:** Render  
**Status:** ☐ Pending ✓ Ready ☐ Deployed ☐ Live

---

For detailed information, see: **SYSTEM_DOCUMENTATION.md**
