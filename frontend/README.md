# StyleSense.AI Frontend

Next.js 14 frontend for the StyleSense.AI virtual fashion try-on platform.

## Vercel Deployment

This frontend is designed to be deployed to Vercel.

### Quick Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/ranashahzaibf22/cli-app&root-directory=frontend)

1. Click the "Deploy with Vercel" button above, or:
2. Go to https://vercel.com/new
3. Import your GitHub repository
4. **Set Root Directory to: `frontend`**
5. Configure environment variables
6. Deploy!

### Environment Variables

Required:
- `NEXT_PUBLIC_API_URL` - Backend API URL (e.g., `https://your-backend.railway.app`)

### Configuration

The root-level `vercel.json` configures:
- Framework: Next.js
- Build/install commands
- Output directory
- Security headers
- Regional deployment

### Local Development

```bash
# Install dependencies
npm install

# Set up environment
cp .env.local.example .env.local
# Edit .env.local with your configuration

# Start development server
npm run dev
```

Visit: `http://localhost:3000`

### Build and Test

```bash
# Build for production
npm run build

# Start production server
npm start

# Run tests
npm test

# Lint code
npm run lint
```

## Project Structure

```
frontend/
├── app/           # Next.js 14 App Router pages
├── components/    # React components
├── lib/           # Utilities and API client
├── public/        # Static assets
└── package.json
```

## Features

- Server-side rendering (SSR)
- Static site generation (SSG)
- API routes
- Image optimization
- TypeScript support
- Tailwind CSS styling
- Zustand state management

See [DEPLOYMENT.md](../DEPLOYMENT.md) in the root directory for detailed deployment instructions.
