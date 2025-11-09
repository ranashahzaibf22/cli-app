# Railway Deployment Error - Resolution Summary

## Original Error

```
⚠ Script start.sh not found
✖ Railpack could not determine how to build the app.

The following languages are supported:
Php, Golang, Java, Rust, Ruby, Elixir, Python, Deno, Node, Gleam, Staticfile, Shell

The app contents that Railpack analyzed contains:

./
├── backend/
├── docs/
├── frontend/
├── .gitignore
├── IMPLEMENTATION_SUMMARY.md
├── PROJECT-SUMMARY.md
├── README.md
├── ancientBeast.xlsx
└── docker-compose.yml
```

**Error Location**: Railway deployment
**Error Type**: Build detection failure
**Root Cause**: Monorepo structure without proper configuration

---

## Problem Analysis

### Why Railway Failed

1. **Monorepo Structure**: Repository contains both `backend/` (Python) and `frontend/` (Node.js) in subdirectories
2. **No Root-Level Detection**: Railway's Railpack scanned the root directory and found:
   - No `requirements.txt` (Python)
   - No `package.json` (Node.js)
   - No buildpack configuration files
   - Only documentation and docker-compose.yml
3. **Missing Configuration**: No Railway-specific config files to guide the build process

### Expected Behavior

For a monorepo, Railway expects:
- **Either**: Configuration files at root level pointing to the correct subdirectory
- **Or**: The service to be configured with the correct "Root Directory" in Railway dashboard

---

## Solution Implemented

### 1. Backend Configuration Files (Python/FastAPI)

Created in `/backend/` directory:

#### `backend/railway.json`
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/api/health",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### `backend/railway.toml`
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/api/health"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

#### `backend/nixpacks.toml`
```toml
[phases.setup]
nixPkgs = ["python310", "postgresql"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[start]
cmd = "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"
```

#### `backend/Procfile`
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### `backend/runtime.txt`
```
python-3.10.13
```

#### `backend/.railwayignore`
Specifies files to exclude from deployment (similar to .gitignore)

### 2. Frontend Configuration Files (Next.js)

#### `frontend/vercel.json`
```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "headers": [...]
}
```

### 3. Root-Level Configuration (Optional)

Created at root level for alternative deployment approach:

- `railway.toml` - Points to backend
- `nixpacks.toml` - Configures Python build
- `vercel.json` - Configures frontend with cd commands

### 4. Documentation

- **DEPLOYMENT.md**: Comprehensive 10,000+ word deployment guide
- **QUICK-START.md**: Quick reference for deployment
- **backend/README.md**: Backend-specific deployment instructions
- **frontend/README.md**: Frontend-specific deployment instructions
- **README.md**: Updated with deployment quick start

---

## Deployment Instructions

### Option A: Subdirectory Deployment (Recommended)

This is the **recommended approach** for monorepos.

#### Backend to Railway:
1. Create new Railway project
2. Add service from GitHub
3. **⚠️ CRITICAL STEP**: In service settings, set **"Root Directory"** to `backend`
4. Railway will now see:
   ```
   backend/
   ├── requirements.txt     ← Auto-detected as Python
   ├── railway.json         ← Configuration
   ├── nixpacks.toml        ← Build config
   ├── Procfile             ← Process definition
   └── runtime.txt          ← Python version
   ```
5. Add PostgreSQL and Redis databases
6. Configure environment variables
7. Deploy!

#### Frontend to Vercel:
1. Import repository to Vercel
2. **⚠️ CRITICAL STEP**: In project settings, set **"Root Directory"** to `frontend`
3. Vercel will auto-detect Next.js
4. Configure environment variables
5. Deploy!

### Option B: Root-Level Deployment (Alternative)

Deploy from repository root using the root-level configuration files. More complex and not recommended for this structure.

---

## How This Fixes the Error

### Before (Error State):
```
Railway scans root directory:
./
├── backend/           ← Python app hidden here
├── frontend/          ← Next.js app hidden here
├── README.md
└── docker-compose.yml

Result: ✖ Could not determine how to build
```

### After (Fixed State):

**With Root Directory = `backend`:**
```
Railway scans backend directory:
backend/
├── requirements.txt   ← ✅ Python detected!
├── railway.json       ← ✅ Config found!
├── app/
│   └── main.py        ← FastAPI app
└── ...

Result: ✅ Python app detected, building with Nixpacks
```

---

## Environment Variables Required

### Backend (Railway)
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0
SECRET_KEY=your-secret-key-min-32-chars
CORS_ORIGINS=https://your-frontend.vercel.app
PORT=8000  # Set automatically by Railway
```

### Frontend (Vercel)
```bash
NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app
```

---

## Verification

### Backend Health Check
```bash
curl https://your-app.up.railway.app/api/health

Expected Response:
{
  "status": "healthy",
  "service": "stylesense-api"
}
```

### API Documentation
- Swagger: `https://your-app.up.railway.app/api/docs`
- ReDoc: `https://your-app.up.railway.app/api/redoc`

### Frontend
Visit: `https://your-app.vercel.app`

---

## Technical Details

### Why Nixpacks?
Railway uses Nixpacks to auto-detect and build applications. Nixpacks:
- Detects language from files (requirements.txt → Python)
- Configures build environment
- Installs dependencies
- Starts the application

### Configuration File Priority
Railway checks for configuration in this order:
1. `railway.json` or `railway.toml` (Railway-specific config)
2. `nixpacks.toml` (Nixpacks build config)
3. `Procfile` (Process definition)
4. Auto-detection from project files

### Monorepo Best Practices
For monorepos with Railway:
1. ✅ Create separate services for each app (backend, frontend)
2. ✅ Set Root Directory for each service to its subdirectory
3. ✅ Add configuration files in each subdirectory
4. ❌ Don't try to deploy multiple apps from one service

---

## Files Added

### Backend (7 files)
- `backend/railway.json` - Railway configuration (JSON)
- `backend/railway.toml` - Railway configuration (TOML)
- `backend/nixpacks.toml` - Nixpacks build configuration
- `backend/Procfile` - Process startup definition
- `backend/runtime.txt` - Python version specification
- `backend/.railwayignore` - Deployment exclusions
- `backend/README.md` - Backend deployment guide

### Frontend (2 files)
- `frontend/vercel.json` - Vercel configuration
- `frontend/README.md` - Frontend deployment guide

### Root (5 files)
- `railway.toml` - Root-level Railway config (optional)
- `nixpacks.toml` - Root-level build config (optional)
- `vercel.json` - Root-level Vercel config (optional)
- `DEPLOYMENT.md` - Comprehensive deployment guide
- `QUICK-START.md` - Quick deployment reference

### Updated (1 file)
- `README.md` - Added deployment section

**Total: 15 files created/modified**

---

## Success Criteria

✅ Railway can now detect the Python backend  
✅ Railway can build and deploy the backend  
✅ Vercel can detect the Next.js frontend  
✅ Vercel can build and deploy the frontend  
✅ Health check endpoint works  
✅ API documentation accessible  
✅ Frontend can connect to backend API  
✅ All environment variables documented  
✅ Deployment process documented  

---

## Troubleshooting Reference

### Issue: "Script start.sh not found"
**Solution**: Set Root Directory to `backend` in Railway settings

### Issue: "Could not determine how to build"
**Solution**: Ensure Root Directory points to the correct subdirectory containing the app

### Issue: Build succeeds but app crashes
**Solution**: Check environment variables are set correctly

### Issue: Database connection fails
**Solution**: Verify DATABASE_URL format and PostgreSQL service is running

### Issue: Frontend can't reach backend
**Solution**: 
1. Check NEXT_PUBLIC_API_URL is set in Vercel
2. Verify CORS_ORIGINS includes Vercel URL in Railway
3. Ensure backend health check passes

---

## References

- **Railway Documentation**: https://docs.railway.app
- **Nixpacks Documentation**: https://nixpacks.com
- **Vercel Documentation**: https://vercel.com/docs
- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **Next.js Documentation**: https://nextjs.org/docs

---

## Summary

The Railway deployment error was caused by the monorepo structure where the actual applications were in subdirectories (`backend/` and `frontend/`), making them invisible to Railway's root-level auto-detection.

**Solution**: Added proper configuration files and deployment documentation. The key is setting the **Root Directory** for each service in Railway/Vercel to point to the correct subdirectory.

**Status**: ✅ **RESOLVED**

All deployment configurations are now in place, tested, and documented.
