# Quick Deployment Guide

This guide provides a quick reference for deploying StyleSense.AI to production.

## ✅ Deployment Files

All necessary deployment files are now correctly configured:

### Backend (Railway)
- ✅ `backend/Dockerfile` - Docker container configuration
- ✅ `backend/.dockerignore` - Optimizes Docker builds  
- ✅ `backend/nixpacks.toml` - Railway Nixpacks configuration (recommended)
- ✅ `backend/railway.json` - Railway service settings

### Frontend (Vercel)
- ✅ `frontend/Dockerfile` - Docker container configuration
- ✅ `frontend/.dockerignore` - Optimizes Docker builds
- ✅ `frontend/next.config.mjs` - Next.js configuration (auto-detected by Vercel)

**Note**: Vercel auto-detects Next.js projects. No `vercel.json` needed.

## 🚀 Quick Deploy

### Backend to Railway

**Method 1: GitHub Integration (Recommended)**

1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select this repository
4. Railway will auto-detect using Nixpacks
5. Add PostgreSQL: "+ New" → "Database" → "PostgreSQL"
6. Add Redis: "+ New" → "Database" → "Redis"
7. Configure environment variables (see below)
8. Deploy! 🚀

**Environment Variables for Backend:**
```bash
# Auto-added by Railway databases
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}

# Required - Generate secure key
SECRET_KEY=<run: python3 -c "import secrets; print(secrets.token_urlsafe(32))">

# Application Settings
DEBUG=False
CORS_ORIGINS=https://your-frontend.vercel.app

# Optional
GROQ_API_KEY=<your-groq-api-key>
PYTHONUNBUFFERED=1
```

### Frontend to Vercel

**Method 1: Vercel Dashboard (Recommended)**

1. Go to [Vercel.com](https://vercel.com)
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. **Root Directory**: Set to `frontend` (if monorepo)
5. Add environment variable:
   ```bash
   NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app
   ```
6. Click "Deploy" 🚀

## 🔗 Connect Frontend to Backend

After both deployments:

1. Copy Railway backend URL
2. Update Vercel: `NEXT_PUBLIC_API_URL=<railway-url>`
3. Update Railway: `CORS_ORIGINS=<vercel-url>`

## �� Verify Deployment

**Backend:**
```bash
curl https://your-backend.up.railway.app/api/health
```

**Frontend:**
Visit: `https://your-frontend.vercel.app`

## 📖 Detailed Guides

- **Backend**: [RAILWAY-DEPLOY.md](RAILWAY-DEPLOY.md)
- **Frontend**: [VERCEL-DEPLOY.md](VERCEL-DEPLOY.md)

**Happy Deploying! 🚀**
