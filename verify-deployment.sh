#!/bin/bash
# Deployment Verification Script
# This script checks if all necessary deployment files are in place

echo "=== StyleSense.AI Deployment Verification ==="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Track overall status
all_good=true

# Function to check file
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 exists"
    else
        echo -e "${RED}✗${NC} $1 is missing"
        all_good=false
    fi
}

# Function to check directory
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 exists"
    else
        echo -e "${RED}✗${NC} $1 is missing"
        all_good=false
    fi
}

echo "Backend Deployment Files:"
check_file "backend/Dockerfile"
check_file "backend/.dockerignore"
check_file "backend/nixpacks.toml"
check_file "backend/railway.json"
check_file "backend/requirements.txt"
check_file "backend/.env.example"
check_file "backend/app/main.py"

echo ""
echo "Frontend Deployment Files:"
check_file "frontend/Dockerfile"
check_file "frontend/.dockerignore"
check_file "frontend/package.json"
check_file "frontend/.env.local.example"
check_file "frontend/next.config.mjs"

echo ""
echo "Docker Compose:"
check_file "docker-compose.yml"

echo ""
echo "Critical Directories:"
check_dir "backend/app"
check_dir "backend/ml_models"
check_dir "backend/data"
check_dir "backend/uploads"
check_dir "frontend/app"
check_dir "frontend/lib"

echo ""
echo "Documentation:"
check_file "README.md"
check_file "docs/DEPLOYMENT-GUIDE.md"

echo ""
if [ "$all_good" = true ]; then
    echo -e "${GREEN}All deployment files are present!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Deploy backend to Railway: https://railway.app"
    echo "2. Deploy frontend to Vercel: https://vercel.com"
    echo "3. Configure environment variables"
    echo "4. Test deployments"
    exit 0
else
    echo -e "${RED}Some deployment files are missing!${NC}"
    echo "Please create the missing files before deploying."
    exit 1
fi
