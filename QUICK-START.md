# Quick Deployment Reference

## 🚀 Deploy Backend to Railway

### Option 1: Via Railway Dashboard (Recommended)

1. Go to [Railway](https://railway.app) and create a new project
2. Click "New Service" → "GitHub Repo"
3. Select this repository
4. **⚠️ IMPORTANT: Set "Root Directory" to `backend`**
5. Click "Add variables" and set:
   ```
   DATABASE_URL=<postgresql-url>
   REDIS_URL=<redis-url>
   SECRET_KEY=<your-secret-32+chars>
   CORS_ORIGINS=https://your-frontend.vercel.app
   ```
6. Add PostgreSQL: "New Service" → "Database" → "PostgreSQL"
7. Add Redis: "New Service" → "Database" → "Redis"
8. Deploy!

### Option 2: Via Railway CLI

```bash
cd backend
railway login
railway init
railway up
```

**Health Check**: `https://your-app.up.railway.app/api/health`

---

## 🚀 Deploy Frontend to Vercel

### Option 1: Via Vercel Dashboard (Recommended)

1. Go to [Vercel](https://vercel.com/new)
2. Import this GitHub repository
3. **⚠️ IMPORTANT: Set "Root Directory" to `frontend`**
4. Add environment variable:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app
   ```
5. Deploy!

### Option 2: Via Vercel CLI

```bash
cd frontend
vercel login
vercel
```

---

## 📋 Configuration Files

### Backend (Railway)
- ✅ `backend/railway.json` - Railway config (JSON format)
- ✅ `backend/railway.toml` - Railway config (TOML format)
- ✅ `backend/nixpacks.toml` - Nixpacks build config
- ✅ `backend/Procfile` - Process definition
- ✅ `backend/runtime.txt` - Python 3.10.13
- ✅ `backend/requirements.txt` - Python dependencies
- ✅ `backend/Dockerfile` - Docker alternative

### Frontend (Vercel)
- ✅ `frontend/vercel.json` - Vercel config
- ✅ `frontend/package.json` - Node dependencies
- ✅ `frontend/Dockerfile` - Docker alternative

---

## 🔧 Required Environment Variables

### Backend (Railway)
Copy from `backend/.env.example`:

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | ✅ Yes | PostgreSQL connection string |
| `REDIS_URL` | ✅ Yes | Redis connection string |
| `SECRET_KEY` | ✅ Yes | JWT secret (32+ characters) |
| `CORS_ORIGINS` | ✅ Yes | Allowed CORS origins |
| `PORT` | ⚙️ Auto | Set by Railway |
| `GROQ_API_KEY` | ❌ No | Optional AI features |

### Frontend (Vercel)
Copy from `frontend/.env.local.example`:

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_API_URL` | ✅ Yes | Backend API URL |

---

## ✅ Verification Steps

### Backend
```bash
# Health check
curl https://your-app.up.railway.app/api/health

# Expected response:
# {"status":"healthy","service":"stylesense-api"}

# API Documentation
# https://your-app.up.railway.app/api/docs
```

### Frontend
```bash
# Visit in browser:
# https://your-app.vercel.app

# Check API connection works
```

---

## 🔍 Troubleshooting

### "Script start.sh not found" Error
**Solution**: Set Root Directory to `backend` in Railway service settings

### "Could not determine how to build"
**Solution**: Ensure you're in the `backend` directory or root directory is set

### Database Connection Errors
1. Check `DATABASE_URL` is set correctly
2. Verify PostgreSQL service is running
3. Check connection string format: `postgresql://user:pass@host:5432/db`

### Frontend API Calls Failing
1. Verify `NEXT_PUBLIC_API_URL` is set
2. Check CORS_ORIGINS includes your Vercel domain
3. Ensure backend is deployed and healthy

---

## 📚 Full Documentation

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for complete deployment guide including:
- Detailed step-by-step instructions
- Monorepo deployment patterns
- CI/CD integration
- Monitoring and scaling
- Security best practices
- Cost optimization

---

## 🎯 Monorepo Structure

This is a **monorepo** with separate services:

```
.
├── backend/          ← Python/FastAPI (Railway)
├── frontend/         ← Next.js (Vercel)
├── DEPLOYMENT.md     ← Full deployment guide
└── QUICK-START.md    ← This file
```

**Key Point**: Deploy backend and frontend as **separate services** with their respective root directories set.
