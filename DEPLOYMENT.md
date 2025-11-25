# Deployment Checklist for Render.com

## Pre-Deployment Steps

### 1. Create GitHub Repository
```bash
cd "C:\Users\hp\.gemini\antigravity\scratch\Video Tracker"
git init
git add .
git commit -m "Initial commit - Video Tracker v1.0"
```

Then create a new repository on GitHub and push:
```bash
git remote add origin https://github.com/YOUR_USERNAME/video-tracker.git
git branch -M main
git push -u origin main
```

### 2. Sign up for Render.com
- Go to https://render.com
- Sign up with your GitHub account

### 3. Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Render will auto-detect `render.yaml`
4. Click "Apply"

### 4. Configure Environment Variables
In Render dashboard, add these environment variables:

**Required:**
- `ADMIN_PASSWORD` - Your admin password (e.g., "mySecurePassword123")

**Optional (for email functionality):**
- `MAIL_SERVER` - smtp.gmail.com
- `MAIL_PORT` - 587
- `MAIL_USERNAME` - your-email@gmail.com
- `MAIL_PASSWORD` - your-gmail-app-password
- `MAIL_DEFAULT_SENDER` - your-email@gmail.com

**Optional (for MongoDB):**
- `MONGODB_URI` - Your MongoDB Atlas connection string

### 5. Deploy
- Click "Manual Deploy" → "Deploy latest commit"
- Wait for build to complete (3-5 minutes)
- Your app will be live at: `https://video-tracker-XXXX.onrender.com`

## Post-Deployment

### Access Your App
- **Public URL**: `https://your-app-name.onrender.com`
- **Admin Panel**: `https://your-app-name.onrender.com/admin`
- **Login**: Use the ADMIN_PASSWORD you set

### View Contact Form Messages
1. Go to Render Dashboard
2. Click on your service
3. Click "Logs" tab
4. Search for "NEW CONTACT FORM SUBMISSION"

### Add Your First Book
1. Go to `/admin`
2. Enter a YouTube playlist URL
3. Click "Add Book"
4. Wait for it to process

## Troubleshooting

### Build Fails
- Check Render logs for errors
- Ensure `requirements.txt` is correct
- Verify Python version compatibility

### App Crashes
- Check Render logs
- Verify environment variables are set
- Check MongoDB connection if using

### Contact Form Not Working
- Messages are always logged to Render console
- Check Logs tab for submissions
- For email: verify Gmail app password is correct

## Free Tier Limitations
- App sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds
- 750 hours/month free
- Consider upgrading for production use
