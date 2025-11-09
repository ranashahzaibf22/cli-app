# StyleSense.AI Backend

FastAPI backend for the StyleSense.AI virtual fashion try-on platform.

## Railway Deployment

This backend is designed to be deployed to Railway.

### Quick Deploy

1. Create a new Railway project
2. Add a service from GitHub repository
3. **Set Root Directory to: `backend`**
4. Add PostgreSQL and Redis databases
5. Configure environment variables (see below)

### Environment Variables

Required:
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string  
- `SECRET_KEY` - JWT secret key (min 32 characters)
- `CORS_ORIGINS` - Comma-separated allowed origins

Optional:
- `GROQ_API_KEY` - For AI recommendations
- `PORT` - Server port (default: 8000, Railway sets this automatically)

### Configuration Files

- `railway.toml` - Railway service configuration
- `nixpacks.toml` - Build configuration
- `Procfile` - Process definition
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container image (alternative)

### Health Check

Endpoint: `/api/health`

Response:
```json
{
  "status": "healthy",
  "service": "stylesense-api"
}
```

### API Documentation

Once deployed:
- Swagger UI: `https://your-app.railway.app/api/docs`
- ReDoc: `https://your-app.railway.app/api/redoc`

## Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

## Testing

```bash
pytest --cov=app tests/
```

## Project Structure

```
backend/
├── app/
│   ├── routes/      # API endpoints
│   ├── services/    # Business logic
│   ├── utils/       # Utilities
│   ├── main.py      # FastAPI app
│   ├── models.py    # Database models
│   ├── schemas.py   # Pydantic schemas
│   └── config.py    # Configuration
├── ml_models/       # ML implementations
├── data/            # Datasets
├── tests/           # Tests
└── requirements.txt
```

See [DEPLOYMENT.md](../DEPLOYMENT.md) in the root directory for detailed deployment instructions.
