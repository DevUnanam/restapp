# Deployment Guide for Render

This guide will help you deploy the Food Delivery Django application to Render.

## Prerequisites

1. A GitHub account
2. A Render account (sign up at https://render.com)
3. Git installed on your local machine

## Step 1: Prepare Your Repository

1. Initialize a Git repository (if not already done):
```bash
git init
git add .
git commit -m "Initial commit - Food Delivery App"
```

2. Create a new repository on GitHub and push your code:
```bash
git remote add origin https://github.com/yourusername/your-repo-name.git
git branch -M main
git push -u origin main
```

## Step 2: Set Up Environment Variables Locally

1. Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```

2. Update `.env` with your local settings:
```env
SECRET_KEY=your-local-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

## Step 3: Deploy to Render

### Option A: Using render.yaml (Recommended)

1. Log in to your Render dashboard at https://dashboard.render.com

2. Click on "New +" and select "Blueprint"

3. Connect your GitHub repository

4. Render will automatically detect the `render.yaml` file and create:
   - A PostgreSQL database
   - A web service running your Django application

5. Configure the environment variables in the Render dashboard:
   - `ALLOWED_HOSTS`: Add your Render URL (e.g., `your-app-name.onrender.com`)
   - `SECRET_KEY`: Will be auto-generated
   - `DEBUG`: Set to `False`
   - `DATABASE_URL`: Will be automatically set from the database
   - `CORS_ALLOWED_ORIGINS`: Add allowed frontend URLs if needed

### Option B: Manual Setup

If you prefer manual setup:

1. **Create a PostgreSQL Database:**
   - In Render dashboard, click "New +" → "PostgreSQL"
   - Name it `fooddelivery-db`
   - Choose the free plan
   - Click "Create Database"
   - Copy the "Internal Database URL"

2. **Create a Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure the service:
     - **Name**: `fooddelivery`
     - **Runtime**: `Python 3`
     - **Build Command**: `./build.sh`
     - **Start Command**: `gunicorn fooddelivery.wsgi:application`
     - **Plan**: Free

3. **Set Environment Variables:**
   Go to the "Environment" tab and add:
   ```
   SECRET_KEY=<generate-a-random-secret-key>
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.onrender.com
   DATABASE_URL=<paste-internal-database-url-from-step-1>
   CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
   ```

4. Click "Create Web Service"

## Step 4: Post-Deployment

After deployment completes:

1. **Create a superuser** (use Render Shell):
   - Go to your web service dashboard
   - Click "Shell" tab
   - Run:
   ```bash
   python manage.py createsuperuser
   ```

2. **Access your application:**
   - Your app will be available at: `https://your-app-name.onrender.com`
   - Admin panel: `https://your-app-name.onrender.com/admin/`

## Important Notes

### Static Files
- Static files are served using WhiteNoise
- They are automatically collected during the build process

### Media Files
- User-uploaded files (images) will be lost on Render's free tier after deployments
- For production, consider using:
  - AWS S3
  - Cloudinary
  - DigitalOcean Spaces

### Database
- The free PostgreSQL database has a limit of 256MB
- Database is persistent and won't be deleted on deployments

### Free Tier Limitations
- Web service spins down after 15 minutes of inactivity
- First request after inactivity may take 30-60 seconds
- 750 hours/month of runtime

## Troubleshooting

### Build Fails
- Check the build logs in Render dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify `build.sh` is executable

### Application Errors
- Check the logs in Render dashboard
- Verify all environment variables are set correctly
- Ensure `DEBUG=False` in production

### Database Connection Issues
- Verify `DATABASE_URL` is correctly set
- Check if database service is running
- Ensure internal database URL is used (not external)

### Static Files Not Loading
- Run `python manage.py collectstatic` locally to test
- Check STATICFILES_STORAGE setting
- Verify WhiteNoise middleware is in MIDDLEWARE list

## Updating Your Deployment

To deploy updates:

1. Make your changes locally
2. Commit and push to GitHub:
```bash
git add .
git commit -m "Your update message"
git push origin main
```

3. Render will automatically detect the changes and redeploy

## Custom Domain (Optional)

1. Go to your web service settings
2. Click "Custom Domains"
3. Add your custom domain
4. Update DNS records as instructed
5. Add your custom domain to `ALLOWED_HOSTS` environment variable

## Security Checklist

- ✅ DEBUG is set to False
- ✅ SECRET_KEY is randomly generated and kept secret
- ✅ ALLOWED_HOSTS is properly configured
- ✅ Database credentials are secure
- ✅ HTTPS is enabled (automatic on Render)
- ✅ Security middleware is configured

## Support

For issues:
- Check Render documentation: https://render.com/docs
- Review Django deployment checklist: https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
