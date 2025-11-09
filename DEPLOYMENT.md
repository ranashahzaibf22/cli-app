# Deployment Configuration Guide

This document explains how to deploy the StyleSense.AI application to Railway (backend) and Vercel (frontend).

## Overview

The project is a **monorepo** with two main components:
- **Backend**: Python FastAPI application (`/backend` directory)
- **Frontend**: Next.js application (`/frontend` directory)

## Railway Deployment (Backend)

### Prerequisites
- Railway account (https://railway.app)
- PostgreSQL database (can be provisioned on Railway)
- Redis instance (can be provisioned on Railway)

### Option 1: Deploy via Railway Dashboard (Recommended)

1. **Create a New Project** in Railway

2. **Add Backend Service**:
   - Click "New Service" → "GitHub Repo"
   - Select your repository
   - **Important**: Set the **Root Directory** to `backend`
   - Railway will auto-detect the Python application

3. **Configure Environment Variables**:
   ```
   DATABASE_URL=<your-postgres-connection-string>
   REDIS_URL=<your-redis-connection-string>
   SECRET_KEY=<generate-a-secure-key>
   CORS_ORIGINS=https://your-frontend-domain.vercel.app,https://www.your-domain.com
   PORT=8000
   ```

4. **Add Database Services**:
   - Click "New Service" → "Database" → "PostgreSQL"
   - Click "New Service" → "Database" → "Redis"
   - Railway will automatically provide connection strings

5. **Deploy**:
   - Railway will automatically deploy when you push to your main branch
   - The backend will be available at: `https://your-app.up.railway.app`

### Option 2: Deploy via Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login to Railway
railway login

# Link to your project
railway link

# Set root directory for the service
railway service

# Deploy
railway up
```

### Configuration Files

The `/backend` directory contains:
- `railway.toml`: Railway service configuration
- `nixpacks.toml`: Nixpacks build configuration  
- `Procfile`: Process startup command
- `requirements.txt`: Python dependencies
- `Dockerfile`: Docker configuration (alternative deployment method)

### Health Check

Railway will monitor: `https://your-app.up.railway.app/api/health`

Expected response:
```json
{
  "status": "healthy",
  "service": "stylesense-api"
}
```

## Vercel Deployment (Frontend)

### Prerequisites
- Vercel account (https://vercel.com)
- Backend API URL from Railway

### Deploy via Vercel Dashboard

1. **Import Project**:
   - Go to https://vercel.com/new
   - Import your GitHub repository
   - **Important**: Set **Root Directory** to `frontend`

2. **Configure Build Settings**:
   - Framework Preset: `Next.js`
   - Build Command: `npm run build` (auto-detected)
   - Output Directory: `.next` (auto-detected)
   - Install Command: `npm install` (auto-detected)

3. **Configure Environment Variables**:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app
   ```

4. **Deploy**:
   - Click "Deploy"
   - Your frontend will be available at: `https://your-app.vercel.app`

### Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel

# Deploy to production
vercel --prod
```

### Configuration File

The root `/vercel.json` configures:
- Framework detection
- Build and install commands
- Output directory
- Security headers
- Regional deployment (Singapore/Asia)

## Monorepo Deployment Notes

### Why Separate Services?

This monorepo contains two distinct applications:
- **Backend** (Python/FastAPI) - requires Python runtime
- **Frontend** (Next.js/React) - requires Node.js runtime

Railway and Vercel handle these best as separate services.

### Railway Monorepo Setup

When deploying from a monorepo to Railway:

1. **Create separate Railway services** for backend and frontend (if deploying both to Railway)
2. **Set the Root Directory** for each service:
   - Backend service: root directory = `backend`
   - Frontend service: root directory = `frontend`
3. Railway will then correctly detect the application type in each subdirectory

### Alternative: Root-Level Deployment

If you want to deploy from the repository root (not recommended for this project):

1. Railway needs to know which app to run
2. Use the root-level configuration files:
   - `/railway.toml` - Points to backend
   - `/nixpacks.toml` - Configures Python build

However, this approach is more complex and not recommended for this monorepo structure.

## Architecture Diagram

```
┌─────────────────────┐
│                     │
│  GitHub Repository  │
│   (Monorepo)        │
│                     │
└──────────┬──────────┘
           │
     ┌─────┴──────┐
     │            │
     ▼            ▼
┌─────────┐  ┌──────────┐
│ Railway │  │  Vercel  │
│         │  │          │
│ Backend │  │ Frontend │
│ Service │  │ Service  │
└────┬────┘  └────┬─────┘
     │            │
     │  API calls │
     │◄───────────┤
     │            │
     ▼            ▼
  Backend      Frontend
   API          Web App
```

## Environment Variables Reference

### Backend (Railway)

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `REDIS_URL` | Redis connection string | `redis://host:6379/0` |
| `SECRET_KEY` | JWT secret key | `your-secret-key-min-32-chars` |
| `CORS_ORIGINS` | Allowed CORS origins | `https://app.vercel.app` |
| `PORT` | Server port (Railway sets this) | `8000` |
| `GROQ_API_KEY` | Groq API key (optional) | `gsk_...` |

### Frontend (Vercel)

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `https://api.railway.app` |

## Testing Deployment

### Backend Health Check

```bash
curl https://your-backend.up.railway.app/api/health
```

Expected:
```json
{
  "status": "healthy",
  "service": "stylesense-api"
}
```

### API Documentation

- Swagger UI: `https://your-backend.up.railway.app/api/docs`
- ReDoc: `https://your-backend.up.railway.app/api/redoc`

### Frontend

Visit: `https://your-app.vercel.app`

## Troubleshooting

### Railway Issues

1. **"Script start.sh not found"**
   - Solution: Set the Root Directory to `backend` in Railway service settings
   - Or use the provided `Procfile`, `railway.toml`, or `nixpacks.toml`

2. **"Could not determine how to build"**
   - Solution: Ensure `requirements.txt` is in the backend directory
   - Set Root Directory to `backend` in Railway settings

3. **Build fails**
   - Check Railway logs for specific errors
   - Ensure all dependencies in `requirements.txt` are compatible
   - Verify Python version (3.10) is specified

4. **Database connection errors**
   - Verify `DATABASE_URL` environment variable is set
   - Check PostgreSQL service is running in Railway
   - Ensure database tables are created (alembic migrations)

### Vercel Issues

1. **Build fails**
   - Check build logs in Vercel dashboard
   - Verify `package.json` has correct scripts
   - Ensure Node.js version is compatible (18+)

2. **API calls failing**
   - Verify `NEXT_PUBLIC_API_URL` is set correctly
   - Check CORS settings on backend
   - Ensure backend is deployed and healthy

3. **Environment variables not working**
   - Prefix browser-accessible variables with `NEXT_PUBLIC_`
   - Redeploy after adding new environment variables

## CI/CD Integration

### Automatic Deployments

Both Railway and Vercel support automatic deployments:

- **Railway**: Auto-deploys on push to main branch (configurable)
- **Vercel**: Auto-deploys on push to main branch (production) and PRs (preview)

### GitHub Actions (Optional)

You can add GitHub Actions for:
- Running tests before deployment
- Automated code quality checks
- Database migrations

Example `.github/workflows/deploy.yml`:
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run backend tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest
      - name: Run frontend tests
        run: |
          cd frontend
          npm install
          npm test
```

## Monitoring and Logs

### Railway Logs

View logs in Railway dashboard:
- Service → Deployments → View Logs
- Real-time log streaming available

### Vercel Logs

View logs in Vercel dashboard:
- Project → Deployments → View Function Logs
- Real-time logs for serverless functions

## Scaling

### Railway

- Vertical scaling: Upgrade plan for more resources
- Horizontal scaling: Available on Pro plans

### Vercel

- Automatic scaling for frontend
- Edge network deployment
- Serverless functions scale automatically

## Security Considerations

1. **Environment Variables**: Never commit secrets to Git
2. **CORS**: Configure allowed origins properly
3. **HTTPS**: Both Railway and Vercel provide free SSL
4. **API Keys**: Rotate regularly, use secret management

## Cost Optimization

### Railway
- Free tier: $5/month credit
- Database included in some plans
- Monitor usage to avoid overages

### Vercel
- Free tier: Hobby plan for personal projects
- Pro plan: For production/commercial use
- Bandwidth and build time limits on free tier

## Support Resources

- **Railway Documentation**: https://docs.railway.app
- **Vercel Documentation**: https://vercel.com/docs
- **Next.js Documentation**: https://nextjs.org/docs
- **FastAPI Documentation**: https://fastapi.tiangolo.com

## Summary

For this monorepo:

1. **Deploy Backend to Railway**:
   - Set root directory to `backend`
   - Add PostgreSQL and Redis services
   - Configure environment variables
   - Use provided configuration files

2. **Deploy Frontend to Vercel**:
   - Set root directory to `frontend`
   - Add backend API URL as environment variable
   - Vercel auto-detects Next.js

3. **Connect Services**:
   - Set `NEXT_PUBLIC_API_URL` in Vercel to Railway backend URL
   - Add Vercel frontend URL to `CORS_ORIGINS` in Railway

This setup provides a production-ready deployment with:
- ✅ Automatic HTTPS
- ✅ Auto-scaling
- ✅ CI/CD integration
- ✅ Health monitoring
- ✅ Global CDN (Vercel)
- ✅ Managed databases (Railway)
