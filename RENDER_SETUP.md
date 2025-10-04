# Quick Render Deployment Setup

## Files Created for Deployment

1. ✅ **requirements.txt** - Python dependencies
2. ✅ **build.sh** - Build script for Render
3. ✅ **render.yaml** - Render configuration (Blueprint)
4. ✅ **.env.example** - Environment variables template
5. ✅ **.gitignore** - Git ignore file
6. ✅ **DEPLOYMENT.md** - Full deployment guide

## Settings Updated

✅ **fooddelivery/settings.py** configured for production:
- Environment-based configuration using `python-decouple`
- PostgreSQL database support via `dj-database-url`
- WhiteNoise for static files
- Security settings for production
- Debug mode controlled by environment variable

## Quick Start Deployment

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Ready for Render deployment"
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main
```

### 2. Deploy on Render
1. Go to https://dashboard.render.com
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically:
   - Create PostgreSQL database
   - Deploy your web service
   - Run migrations
   - Collect static files

### 3. Configure Environment Variables
In Render Dashboard, set:
- `ALLOWED_HOSTS` = `your-app-name.onrender.com`
- `DEBUG` = `False`
- `SECRET_KEY` (auto-generated)
- `DATABASE_URL` (auto-configured)

### 4. Create Superuser
Use Render Shell:
```bash
python manage.py createsuperuser
```

## Environment Variables Reference

| Variable | Development | Production (Render) |
|----------|------------|---------------------|
| DEBUG | True | False |
| SECRET_KEY | Any value | Auto-generated |
| ALLOWED_HOSTS | localhost,127.0.0.1 | your-app.onrender.com |
| DATABASE_URL | (empty - uses SQLite) | Auto-set by Render |
| CORS_ALLOWED_ORIGINS | (optional) | Your frontend URLs |

## Important Notes

### Static Files
- ✅ Handled by WhiteNoise
- ✅ Auto-collected during build

### Media Files (User Uploads)
- ⚠️ Not persistent on Render free tier
- 💡 For production, use AWS S3 or Cloudinary

### Database
- ✅ PostgreSQL (256MB on free tier)
- ✅ Persistent across deployments

### Free Tier Limits
- ⚠️ Service sleeps after 15 min inactivity
- ⚠️ 750 hours/month runtime

## Testing Locally with Production Settings

1. Create `.env` file:
```bash
cp .env.example .env
```

2. Set DEBUG=False in .env

3. Run:
```bash
python manage.py collectstatic
python manage.py migrate
python manage.py runserver
```

## Troubleshooting

**Build fails?**
- Check `build.sh` is executable: `chmod +x build.sh`
- Verify all packages in `requirements.txt`

**500 Error?**
- Check Render logs
- Verify environment variables
- Ensure DEBUG=False

**Static files not loading?**
- Check WhiteNoise middleware is enabled
- Run `collectstatic` command

**Database errors?**
- Verify DATABASE_URL is set
- Check database service status

## Next Steps After Deployment

1. ✅ Create superuser
2. ✅ Login to /admin/
3. ✅ Test all functionality
4. ✅ Create test merchant, customer, driver accounts
5. ✅ Add sample restaurants and menu items

For detailed instructions, see DEPLOYMENT.md
