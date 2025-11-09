# Railway Deployment Guide for StyleSense.AI Backend

## Overview
This guide provides step-by-step instructions for deploying the FastAPI backend to Railway.

## Prerequisites
- Railway account (sign up at https://railway.app)
- GitHub repository connected to Railway
- PostgreSQL and Redis databases (can be provisioned on Railway)

## Deployment Options

Railway supports two deployment methods:
1. **Nixpacks (Recommended)** - Auto-detects Python and builds optimally
2. **Dockerfile** - Uses custom Dockerfile for more control

This project is configured for **Nixpacks** with custom configuration.

## Configuration Files

### 1. `nixpacks.toml`
Custom Nixpacks configuration for Python/FastAPI:
- Specifies Python 3.10, gcc, g++, and PostgreSQL
- Installs dependencies from requirements.txt
- Starts with uvicorn using $PORT from Railway

### 2. `railway.json`
Railway service configuration:
- Uses NIXPACKS builder
- Configures restart policy (ON_FAILURE, max 10 retries)
- Sets replica count to 1

### 3. `Dockerfile`
Fallback Docker configuration if Nixpacks is not used:
- Python 3.10 slim base
- Installs system dependencies
- Uses $PORT environment variable

## Step-by-Step Deployment

### Step 1: Create Railway Project

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Select the `backend` directory as the root

### Step 2: Add Database Services

#### PostgreSQL Database
1. In your Railway project, click "+ New"
2. Select "Database" → "Add PostgreSQL"
3. Wait for provisioning
4. Railway automatically adds `DATABASE_URL` environment variable

#### Redis Cache
1. Click "+ New" again
2. Select "Database" → "Add Redis"
3. Wait for provisioning
4. Railway automatically adds `REDIS_URL` environment variable

### Step 3: Configure Environment Variables

Go to your backend service → Variables tab and add:

```bash
# Database (automatically added by Railway)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Redis (automatically added by Railway)
REDIS_URL=${{Redis.REDIS_URL}}

# JWT Configuration
SECRET_KEY=<generate-secure-key-here>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Groq API (optional)
GROQ_API_KEY=<your-groq-api-key>

# Application Settings
DEBUG=False
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760
ALLOWED_EXTENSIONS=jpg,jpeg,png,webp

# CORS (update with your frontend URL)
CORS_ORIGINS=https://your-frontend.vercel.app

# ML Models
MODEL_DIR=ml_models/models
TRAINING_DATA_DIR=data/datasets/training_images

# Python Settings
PYTHONUNBUFFERED=1
```

#### Generate Secure SECRET_KEY:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 4: Deploy

1. Railway will automatically deploy after detecting changes
2. Monitor the build logs in the Railway dashboard
3. Wait for deployment to complete (typically 2-5 minutes)

### Step 5: Get Your Backend URL

1. Go to your backend service in Railway
2. Click "Settings" → "Networking"
3. Click "Generate Domain"
4. Your API will be available at: `https://your-app.up.railway.app`

### Step 6: Initialize Database

After deployment, you may need to initialize the database:

**Option 1: Using Railway CLI**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Run database initialization
railway run python seed_data.py
```

**Option 2: The app auto-creates tables**
The FastAPI app automatically creates database tables on startup via:
```python
Base.metadata.create_all(bind=engine)
```

## Verification

### 1. Health Check
```bash
curl https://your-app.up.railway.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "stylesense-api"
}
```

### 2. API Documentation
Visit: `https://your-app.up.railway.app/api/docs`

You should see the Swagger UI with all endpoints.

### 3. Root Endpoint
```bash
curl https://your-app.up.railway.app/
```

Expected response:
```json
{
  "message": "StyleSense.AI API",
  "version": "1.0.0",
  "docs": "/api/docs"
}
```

## Monitoring

### View Logs
1. Go to Railway dashboard
2. Click on your backend service
3. Click "Deployments" tab
4. Select active deployment
5. View build and runtime logs

### Common Log Patterns to Monitor
- `Application startup complete` - App started successfully
- `Uvicorn running on` - Server is listening
- Database connection errors - Check DATABASE_URL
- Import errors - Check requirements.txt

## Troubleshooting

### Build Fails

**Issue**: Dependencies fail to install
**Solution**: 
- Check requirements.txt for version conflicts
- View build logs for specific error
- Ensure Python 3.10 is specified in nixpacks.toml

**Issue**: Out of memory during build
**Solution**:
- Upgrade Railway plan for more resources
- Large ML libraries (TensorFlow) require significant memory

### Runtime Errors

**Issue**: Database connection fails
**Solution**:
- Verify DATABASE_URL is set correctly
- Ensure PostgreSQL service is running
- Check if database is in same Railway project

**Issue**: Application crashes on startup
**Solution**:
- Check runtime logs for Python errors
- Verify all environment variables are set
- Check CORS_ORIGINS format (comma-separated, no spaces)

**Issue**: Port binding error
**Solution**:
- Ensure Dockerfile uses `${PORT:-8000}`
- Verify nixpacks.toml uses `$PORT`
- Railway automatically sets PORT variable

### CORS Errors

**Issue**: Frontend can't connect to backend
**Solution**:
- Update CORS_ORIGINS with frontend domain
- Format: `https://your-app.vercel.app` (no trailing slash)
- Redeploy backend after changing CORS_ORIGINS

## Scaling

### Vertical Scaling
- Go to Settings → Resources
- Increase CPU/Memory allocation
- Restart service for changes to take effect

### Horizontal Scaling
- Currently configured for 1 replica
- Update `numReplicas` in railway.json
- Requires Railway Pro plan

## Custom Domain (Optional)

1. Go to Settings → Networking
2. Click "Custom Domain"
3. Enter your domain (e.g., `api.yourdomain.com`)
4. Add CNAME record in your DNS:
   ```
   CNAME api.yourdomain.com -> your-app.up.railway.app
   ```
5. Wait for DNS propagation (5-60 minutes)
6. Update CORS_ORIGINS with new domain

## Cost Optimization

- **Starter Plan**: $5/month (1 service, limited resources)
- **Developer Plan**: $20/month (multiple services, better resources)
- Free trial: $5 credit

### Tips to Reduce Costs:
1. Use shared PostgreSQL for dev/staging
2. Monitor resource usage in dashboard
3. Set resource limits appropriately
4. Use Railway's sleep feature for dev environments

## Continuous Deployment

Railway automatically deploys on git push:
1. Push code to GitHub
2. Railway detects changes
3. Builds and deploys automatically
4. No manual intervention needed

### Disable Auto-Deploy:
1. Go to Settings → Service
2. Toggle "Auto-Deploy" off
3. Manual deploys via Railway CLI or dashboard

## Railway CLI Commands

```bash
# Deploy manually
railway up

# View logs
railway logs

# Run command in Railway environment
railway run <command>

# Open service in browser
railway open

# Environment variables
railway variables
```

## Next Steps

After successful backend deployment:
1. Copy the Railway URL
2. Deploy frontend to Vercel
3. Set `NEXT_PUBLIC_API_URL` in Vercel to Railway URL
4. Test end-to-end integration

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Railway Status: https://status.railway.app

## Checklist

- [ ] Railway account created
- [ ] GitHub repository connected
- [ ] PostgreSQL database provisioned
- [ ] Redis database provisioned
- [ ] All environment variables configured
- [ ] SECRET_KEY generated and set
- [ ] CORS_ORIGINS configured with frontend URL
- [ ] Deployment successful
- [ ] Health check endpoint working
- [ ] API docs accessible
- [ ] Database initialized
- [ ] Logs showing no errors
