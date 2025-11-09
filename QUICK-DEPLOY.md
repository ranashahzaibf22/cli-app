# Quick Deployment Guide

This guide provides a quick reference for deploying StyleSense.AI to production.

## ✅ Pre-Deployment Checklist

All necessary deployment files are now included:

- ✅ `backend/.dockerignore` - Optimizes Docker builds
- ✅ `backend/Procfile` - Railway deployment configuration
- ✅ `backend/railway.json` - Railway build configuration
- ✅ `backend/Dockerfile` - Backend container definition
- ✅ `frontend/.dockerignore` - Optimizes frontend builds
- ✅ `frontend/vercel.json` - Vercel deployment configuration
- ✅ `frontend/Dockerfile` - Frontend container definition
- ✅ `docker-compose.yml` - Local development setup

## 🚀 Quick Deploy

### Option 1: Deploy to Railway + Vercel (Recommended)

**Backend (Railway):**
1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select this repository
4. Railway will auto-detect the backend
5. Add environment variables from `backend/.env.example`
6. Deploy!

**Frontend (Vercel):**
1. Go to [Vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Import this repository
4. Set root directory to `frontend`
5. Add environment variable: `NEXT_PUBLIC_API_URL=<your-railway-backend-url>`
6. Deploy!

### Option 2: Local Development with Docker

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

## 📋 Environment Variables

**Backend (.env):**
```bash
DATABASE_URL=postgresql://user:password@host:5432/db
REDIS_URL=redis://host:6379/0
SECRET_KEY=<generate-with-openssl-rand-hex-32>
GROQ_API_KEY=<your-groq-api-key>
CORS_ORIGINS=https://your-frontend-domain.com
```

**Frontend (.env.local):**
```bash
NEXT_PUBLIC_API_URL=https://your-backend-domain.com
NEXT_PUBLIC_APP_NAME=StyleSense.AI
```

## 🔍 Verify Deployment

Run the verification script:
```bash
./verify-deployment.sh
```

## 📖 Full Documentation

For detailed deployment instructions, see:
- [docs/DEPLOYMENT-GUIDE.md](docs/DEPLOYMENT-GUIDE.md)
- [README.md](README.md)

## 🆘 Troubleshooting

**Build fails:**
- Check that all environment variables are set
- Verify Docker is running (for local deployment)
- Check logs: `docker compose logs backend` or `docker compose logs frontend`

**Database connection fails:**
- Verify DATABASE_URL is correct
- Check that PostgreSQL is running
- Ensure database exists

**CORS errors:**
- Update CORS_ORIGINS in backend environment variables
- Include your frontend domain
- Redeploy backend after changes

## 🎯 Next Steps

After deployment:
1. Seed the database: `docker compose exec backend python seed_data.py`
2. Test API: Visit `https://your-backend/api/docs`
3. Test frontend: Visit `https://your-frontend`
4. Configure custom domains (optional)

## 📊 Health Checks

**Backend:**
```bash
curl https://your-backend-domain.com/api/health
```

**Frontend:**
```bash
curl https://your-frontend-domain.com
```

## 🔐 Security Notes

- Never commit `.env` files
- Use strong SECRET_KEY (32+ random characters)
- Enable HTTPS (automatic on Railway/Vercel)
- Configure CORS with specific origins only
- Regularly update dependencies

---

For questions or issues, please refer to the full [DEPLOYMENT-GUIDE.md](docs/DEPLOYMENT-GUIDE.md).
