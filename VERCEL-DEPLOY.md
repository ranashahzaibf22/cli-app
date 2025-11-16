# Vercel Deployment Guide for StyleSense.AI Frontend

## Overview
This guide provides step-by-step instructions for deploying the Next.js 14 frontend to Vercel.

## Prerequisites
- Vercel account (sign up at https://vercel.com)
- GitHub repository
- Backend API deployed and accessible (Railway URL)

## Deployment Configuration

Vercel automatically detects and configures Next.js projects. No `vercel.json` is required for basic Next.js deployments.

### Auto-Detection Features:
- ✅ Framework: Next.js 14
- ✅ Build command: `npm run build`
- ✅ Output directory: `.next`
- ✅ Install command: `npm install`
- ✅ Development command: `npm run dev`

## Step-by-Step Deployment

### Step 1: Import Project to Vercel

1. Go to https://vercel.com/dashboard
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Vercel will auto-detect Next.js

### Step 2: Configure Project Settings

**Root Directory:**
- If monorepo: Set to `frontend`
- If standalone: Leave as `/`

**Framework Preset:**
- Vercel will auto-detect "Next.js"
- No manual selection needed

**Build Settings:**
- Build Command: `npm run build` (auto-detected)
- Output Directory: `.next` (auto-detected)
- Install Command: `npm install` (auto-detected)

### Step 3: Configure Environment Variables

Click "Environment Variables" and add:

```bash
# Required: Backend API URL (from Railway)
NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app

# Optional: Application Name
NEXT_PUBLIC_APP_NAME=StyleSense.AI
```

**Important Notes:**
- Variables starting with `NEXT_PUBLIC_` are exposed to the browser
- No trailing slash in API URL
- Use HTTPS URL from Railway, not HTTP
- These variables are built into the application at build time

### Step 4: Deploy

1. Click "Deploy"
2. Vercel will:
   - Clone repository
   - Install dependencies
   - Build Next.js application
   - Deploy to edge network
3. Wait 1-3 minutes for deployment

### Step 5: Get Your Frontend URL

After deployment completes:
- Production URL: `https://your-app.vercel.app`
- Vercel provides automatic HTTPS
- App is deployed to global edge network

### Step 6: Update Backend CORS

**Important:** Add frontend URL to backend CORS_ORIGINS:

In Railway backend environment variables:
```bash
CORS_ORIGINS=https://your-app.vercel.app,https://your-app-git-main-username.vercel.app
```

Include both:
- Main production URL
- Git branch preview URLs (optional)

Then redeploy backend for CORS changes to take effect.

## Verification

### 1. Homepage
Visit: `https://your-app.vercel.app`

Expected: Homepage loads without errors

### 2. API Connection
1. Open browser DevTools (F12)
2. Go to Console tab
3. Navigate app pages
4. Check for API errors

**Good**: No CORS errors, API calls succeed
**Bad**: CORS errors, connection refused

### 3. Check Build Logs
1. Go to Vercel dashboard
2. Click on deployment
3. View "Building" logs
4. Ensure no build errors

## Advanced Configuration

### Custom Domain

1. Go to Project Settings → Domains
2. Click "Add"
3. Enter your domain: `yourdomain.com`
4. Follow DNS configuration instructions

**DNS Records:**
```
# For root domain (yourdomain.com)
A Record: 76.76.21.21

# For www subdomain
CNAME: cname.vercel-dns.com
```

Wait 24-48 hours for DNS propagation.

### Environment Variables per Environment

Vercel supports different values per environment:

1. Go to Project Settings → Environment Variables
2. Add variable
3. Select environments:
   - Production (main branch)
   - Preview (PR branches)
   - Development (local)

Example:
```bash
# Production
NEXT_PUBLIC_API_URL=https://api.production.com

# Preview
NEXT_PUBLIC_API_URL=https://api-staging.railway.app

# Development
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Preview Deployments

Vercel automatically creates preview deployments for:
- Every git branch
- Every pull request
- Every commit

**Access previews:**
- URL format: `https://your-app-git-branch-username.vercel.app`
- Listed in Deployments tab
- Automatic cleanup after PR merge

### Production Branch

By default, `main` branch is production.

**Change production branch:**
1. Go to Settings → Git
2. Select different branch
3. Save changes

## Monitoring

### Analytics

Enable Vercel Analytics:
1. Go to Analytics tab
2. Enable "Web Analytics"
3. View real-time visitor data
4. Track Core Web Vitals

### Logs

View function logs:
1. Go to Deployments
2. Click on deployment
3. Click "Functions" tab
4. View runtime logs

### Speed Insights

Enable Speed Insights:
1. Go to Speed Insights tab
2. Enable feature
3. View performance metrics
4. Track page load times

## Troubleshooting

### Build Fails

**Issue**: `npm install` fails
**Solution**:
- Check package.json for syntax errors
- Ensure all dependencies are listed
- Check Node.js version compatibility (v18+)

**Issue**: TypeScript errors during build
**Solution**:
- Fix TypeScript errors locally first
- Run `npm run build` locally
- Push fixes to repository

**Issue**: Environment variable not found
**Solution**:
- Ensure variable starts with `NEXT_PUBLIC_`
- Redeploy after adding variables
- Check variable name spelling

### Runtime Errors

**Issue**: API calls fail with CORS error
**Solution**:
```
1. Check backend CORS_ORIGINS includes Vercel URL
2. Ensure NEXT_PUBLIC_API_URL is correct
3. Verify backend is accessible (check Railway)
4. Check browser console for exact error
```

**Issue**: Images don't load
**Solution**:
- Check `next.config.mjs` image domains
- Add Railway domain to allowed domains:
```javascript
images: {
  remotePatterns: [
    {
      protocol: 'https',
      hostname: 'your-backend.up.railway.app',
    },
  ],
}
```

**Issue**: 404 errors on refresh
**Solution**:
- Next.js handles this automatically
- If using custom server, ensure proper routing
- Check next.config.mjs for output: 'standalone'

### Performance Issues

**Issue**: Slow page loads
**Solution**:
- Use Next.js Image component for images
- Implement code splitting
- Enable static generation where possible
- Use Vercel Analytics to identify bottlenecks

## Optimization

### Image Optimization

Next.js automatically optimizes images:
```tsx
import Image from 'next/image'

<Image 
  src="/path/to/image.jpg"
  width={500}
  height={300}
  alt="Description"
/>
```

### Caching

Vercel automatically caches:
- Static pages
- API routes (with proper headers)
- Images
- Static assets

### Edge Functions

For faster response times:
```javascript
export const config = {
  runtime: 'edge',
}
```

## Continuous Deployment

Vercel automatically deploys on git push:
1. Push to GitHub
2. Vercel detects change
3. Builds and deploys
4. Deployment notification sent

**Deployment notifications:**
- GitHub PR comments
- Email notifications
- Slack integration (optional)
- Discord webhooks (optional)

## Vercel CLI

Install Vercel CLI:
```bash
npm i -g vercel
```

### Common Commands

```bash
# Login to Vercel
vercel login

# Deploy to preview
vercel

# Deploy to production
vercel --prod

# View logs
vercel logs

# List deployments
vercel ls

# Environment variables
vercel env ls
vercel env add
vercel env rm

# Link local project
vercel link

# Pull environment variables
vercel env pull
```

## Cost & Limits

### Hobby Plan (Free)
- ✅ Unlimited deployments
- ✅ 100GB bandwidth/month
- ✅ Automatic HTTPS
- ✅ Preview deployments
- ❌ No team features

### Pro Plan ($20/month)
- ✅ 1TB bandwidth/month
- ✅ Team collaboration
- ✅ Advanced analytics
- ✅ Password protection
- ✅ Priority support

## Integration with Backend

After both deployments are complete:

### 1. Update Frontend Environment
```bash
NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app
```

### 2. Update Backend CORS
```bash
CORS_ORIGINS=https://your-frontend.vercel.app
```

### 3. Test End-to-End
1. Visit frontend URL
2. Try logging in
3. Test API calls
4. Check browser console for errors
5. Verify data loads correctly

## Security

### Environment Variables
- Never commit `.env.local` files
- Use Vercel dashboard for production variables
- Rotate secrets regularly
- Use HTTPS only

### CORS Configuration
- List specific domains, avoid wildcards
- Update on domain changes
- Include www and non-www versions if needed

### Headers
Add security headers in `next.config.mjs`:
```javascript
async headers() {
  return [
    {
      source: '/:path*',
      headers: [
        {
          key: 'X-Frame-Options',
          value: 'DENY',
        },
        {
          key: 'X-Content-Type-Options',
          value: 'nosniff',
        },
      ],
    },
  ]
}
```

## Support Resources

- Vercel Docs: https://vercel.com/docs
- Next.js Docs: https://nextjs.org/docs
- Vercel Support: support@vercel.com
- Status Page: https://www.vercel-status.com

## Checklist

- [ ] Vercel account created
- [ ] GitHub repository connected
- [ ] Root directory configured (if monorepo)
- [ ] Environment variables set
- [ ] NEXT_PUBLIC_API_URL points to Railway backend
- [ ] Build successful
- [ ] Deployment successful
- [ ] Frontend accessible at Vercel URL
- [ ] Backend CORS updated with Vercel URL
- [ ] End-to-end testing complete
- [ ] No console errors
- [ ] Images loading correctly
- [ ] API calls working
- [ ] Custom domain configured (optional)

## Next Steps

1. Test all application features
2. Set up custom domain (optional)
3. Enable Vercel Analytics
4. Configure preview deployments
5. Set up monitoring and alerts
6. Document deployment process for team
