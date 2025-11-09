# Deployment Guide

## Overview

This guide covers deploying the StyleSense.AI platform to production environments using Railway (backend) and Vercel (frontend).

## Prerequisites

- GitHub account
- Railway account (https://railway.app)
- Vercel account (https://vercel.com)
- Domain name (optional)

## Architecture

```
Frontend (Vercel)
    ↓ HTTPS
Backend API (Railway)
    ↓
Database (Railway PostgreSQL)
    ↓
Redis Cache (Railway Redis)
```

---

## Part 1: Database Setup on Railway

### 1.1 Create PostgreSQL Database

1. Go to Railway Dashboard
2. Click "New Project"
3. Select "Provision PostgreSQL"
4. Wait for deployment
5. Note the connection details:
   - Database URL
   - Host, Port, Database name
   - Username, Password

### 1.2 Create Redis Instance

1. In the same project, click "New"
2. Select "Database" → "Redis"
3. Wait for deployment
4. Note the Redis URL

---

## Part 2: Backend Deployment on Railway

### 2.1 Prepare Backend

Ensure your backend has these files:

**Procfile** (create if missing):
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**railway.json** (optional, for build config):
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 2.2 Deploy to Railway

#### Option A: Deploy from GitHub

1. Push code to GitHub repository
2. Go to Railway Dashboard
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Select the backend directory (if monorepo)

#### Option B: Deploy with Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
cd backend
railway init

# Deploy
railway up
```

### 2.3 Configure Environment Variables

In Railway dashboard, go to your backend service → Variables:

```
# Database
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Redis
REDIS_URL=${{Redis.REDIS_URL}}

# JWT
SECRET_KEY=<generate-strong-secret-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Groq API
GROQ_API_KEY=<your-groq-api-key>

# Application
DEBUG=False
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760

# CORS (update with your frontend domain)
CORS_ORIGINS=https://your-frontend.vercel.app,https://www.your-domain.com

# ML Models
MODEL_DIR=ml_models/models
TRAINING_DATA_DIR=data/datasets/training_images
```

### 2.4 Generate Strong Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2.5 Run Database Migrations

After deployment, run migrations:

```bash
# Using Railway CLI
railway run alembic upgrade head

# Or via Railway dashboard shell
# Navigate to your service → Settings → Terminal
# Then run: alembic upgrade head
```

### 2.6 Get Backend URL

Railway will provide a URL like:
```
https://your-backend-production.up.railway.app
```

Note this URL for frontend configuration.

---

## Part 3: Frontend Deployment on Vercel

### 3.1 Prepare Frontend

Ensure your frontend has:

**vercel.json** (optional):
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "regions": ["iad1"]
}
```

### 3.2 Deploy to Vercel

#### Option A: Deploy from GitHub

1. Go to Vercel Dashboard
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Configure:
   - Framework Preset: Next.js
   - Root Directory: frontend (if monorepo)
   - Build Command: `npm run build`
   - Output Directory: `.next`

#### Option B: Deploy with Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel

# Deploy to production
vercel --prod
```

### 3.3 Configure Environment Variables

In Vercel dashboard, go to your project → Settings → Environment Variables:

```
NEXT_PUBLIC_API_URL=https://your-backend-production.up.railway.app
NEXT_PUBLIC_APP_NAME=StyleSense.AI
```

**Important:** Variables starting with `NEXT_PUBLIC_` are exposed to the browser.

### 3.4 Redeploy

After adding environment variables:
1. Go to Deployments tab
2. Click "..." on latest deployment
3. Select "Redeploy"

---

## Part 4: Domain Configuration (Optional)

### 4.1 Backend Custom Domain

In Railway:
1. Go to backend service → Settings
2. Click "Generate Domain" or "Add Custom Domain"
3. If custom domain:
   - Add domain (e.g., api.yourdomain.com)
   - Add CNAME record in your DNS:
     ```
     CNAME api.yourdomain.com -> your-backend.up.railway.app
     ```

### 4.2 Frontend Custom Domain

In Vercel:
1. Go to project → Settings → Domains
2. Add your domain (e.g., yourdomain.com)
3. Configure DNS as instructed by Vercel
4. Add CNAME or A record:
   ```
   CNAME www.yourdomain.com -> cname.vercel-dns.com
   ```

---

## Part 5: Post-Deployment Configuration

### 5.1 Update CORS Origins

Update backend environment variable:
```
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

Redeploy backend.

### 5.2 SSL/HTTPS

Both Railway and Vercel provide automatic SSL certificates. No configuration needed.

### 5.3 Health Checks

Test your deployment:

```bash
# Backend health
curl https://your-backend.railway.app/api/health

# Frontend
curl https://your-frontend.vercel.app
```

---

## Part 6: Database Seeding

### 6.1 Seed Initial Data

```bash
# Connect to Railway
railway run python

# In Python shell
from app.database import SessionLocal, engine
from app.models import Base
import json

# Create tables
Base.metadata.create_all(bind=engine)

# Load sample data
with open('data/datasets/fashion_items.json') as f:
    items = json.load(f)

# Insert data
db = SessionLocal()
# ... insert items
db.commit()
```

### 6.2 Or use seed script

Create `backend/seed_data.py`:
```python
import json
from app.database import SessionLocal
from app.models import ClothingItem

def seed_database():
    db = SessionLocal()
    
    with open('data/datasets/fashion_items.json') as f:
        items = json.load(f)
    
    for item in items:
        db_item = ClothingItem(**item)
        db.add(db_item)
    
    db.commit()
    print(f"Seeded {len(items)} items")

if __name__ == "__main__":
    seed_database()
```

Run:
```bash
railway run python seed_data.py
```

---

## Part 7: Monitoring and Logs

### 7.1 Railway Logs

View logs in Railway dashboard:
1. Go to your service
2. Click "Deployments"
3. Click on active deployment
4. View build and runtime logs

### 7.2 Vercel Logs

View logs in Vercel dashboard:
1. Go to your project
2. Click "Deployments"
3. Click on deployment
4. View build and function logs

### 7.3 Set Up Alerts

**Railway:**
- Configure health check endpoints
- Set up webhooks for deployment failures

**Vercel:**
- Configure deployment notifications
- Set up integration with Slack/Discord

---

## Part 8: Performance Optimization

### 8.1 Frontend Optimization

**next.config.mjs**:
```javascript
const nextConfig = {
  images: {
    domains: ['your-backend.railway.app'],
    formats: ['image/avif', 'image/webp'],
  },
  compress: true,
  poweredByHeader: false,
  reactStrictMode: true,
}
```

### 8.2 Backend Optimization

**Enable compression:**
```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

**Connection pooling:**
Already configured in SQLAlchemy setup.

### 8.3 CDN Configuration

Vercel automatically uses CDN for static assets.

For backend static files, consider:
- Cloudflare CDN
- AWS CloudFront
- Upload images to cloud storage (S3, Cloudinary)

---

## Part 9: Scaling

### 9.1 Backend Scaling

Railway auto-scales based on:
- CPU usage
- Memory usage
- Request volume

Configure in Railway dashboard:
- Minimum instances: 1
- Maximum instances: 10
- Auto-scale threshold: 80% CPU

### 9.2 Database Scaling

**Vertical scaling:**
- Upgrade Railway PostgreSQL plan
- More CPU, RAM, storage

**Horizontal scaling:**
- Read replicas (Railway Pro plan)
- Connection pooling (PgBouncer)

### 9.3 Redis Scaling

- Upgrade Railway Redis plan
- Enable persistence if needed
- Configure eviction policy

---

## Part 10: Backup and Recovery

### 10.1 Database Backups

Railway PostgreSQL includes:
- Automatic daily backups
- Point-in-time recovery
- Manual backup triggers

To backup manually:
```bash
railway run pg_dump $DATABASE_URL > backup.sql
```

### 10.2 Application Backups

- Code: GitHub repository
- Environment variables: Document separately
- User uploads: Backup to S3/Cloud Storage

---

## Part 11: Security Checklist

- [ ] HTTPS enabled (automatic)
- [ ] Strong SECRET_KEY generated
- [ ] CORS configured with specific origins
- [ ] Database credentials secured
- [ ] Environment variables not in code
- [ ] Rate limiting configured
- [ ] SQL injection protection (SQLAlchemy)
- [ ] XSS protection (React escaping)
- [ ] CSRF protection for state-changing operations
- [ ] Input validation on all endpoints

---

## Part 12: Troubleshooting

### Common Issues

**Build fails:**
- Check requirements.txt/package.json versions
- View build logs for errors
- Ensure Python/Node version compatibility

**Database connection fails:**
- Verify DATABASE_URL is set
- Check database is running
- Test connection with psql

**CORS errors:**
- Update CORS_ORIGINS
- Include both www and non-www domains
- Redeploy backend after changes

**Environment variables not working:**
- Verify variable names (case-sensitive)
- Redeploy after adding variables
- Check NEXT_PUBLIC_ prefix for frontend

---

## Part 13: Cost Optimization

### Railway Costs

- Starter: $5/month (1 service)
- Developer: $20/month (multiple services)
- Team: Custom pricing

**Tips:**
- Use single PostgreSQL for all environments
- Set resource limits
- Monitor usage dashboard

### Vercel Costs

- Hobby: Free (personal projects)
- Pro: $20/month (commercial)
- Enterprise: Custom

**Tips:**
- Optimize images
- Use ISR for static content
- Monitor bandwidth usage

---

## Deployment Checklist

Before going live:

- [ ] Environment variables configured
- [ ] Database migrated and seeded
- [ ] CORS origins updated
- [ ] Health checks passing
- [ ] Custom domains configured (if applicable)
- [ ] SSL certificates active
- [ ] Monitoring and alerts set up
- [ ] Backups scheduled
- [ ] Security review completed
- [ ] Performance testing done
- [ ] Documentation updated
- [ ] Team notified

---

## Support and Resources

**Railway:**
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway
- Status: https://railway.statuspage.io

**Vercel:**
- Docs: https://vercel.com/docs
- Support: support@vercel.com
- Status: https://vercel-status.com

**Project-specific:**
- GitHub Issues
- Documentation in `/docs`
- API Docs: /api/docs endpoint
