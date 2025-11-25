# Email Configuration Guide for Contact Form

## Option 1: View Messages in Render Logs (No Setup Required)

When deployed on Render.com, all contact form submissions are automatically logged to the console. You can view them:

1. Go to your Render dashboard
2. Click on your "video-tracker" service
3. Click on "Logs" tab
4. Look for messages starting with "NEW CONTACT FORM SUBMISSION"

## Option 2: Configure Gmail SMTP (Recommended for Production)

To receive contact form messages via email:

### Step 1: Enable Gmail App Password

1. Go to your Google Account settings
2. Navigate to Security → 2-Step Verification (enable if not already)
3. Go to Security → App passwords
4. Generate a new app password for "Mail"
5. Copy the 16-character password

### Step 2: Configure Environment Variables on Render

Add these environment variables in your Render dashboard:

```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-char-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### Step 3: Verify

Messages will be sent to `tellitaudio@gmail.com` and you'll also see them in Render logs.

## For Local Development

Create a `.env` file with the same variables:

```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

Then install python-dotenv:
```bash
pip install python-dotenv
```

## Troubleshooting

- **"Less secure app access"**: Not needed if using App Passwords
- **Still not working**: Check Render logs for error messages
- **Gmail blocking**: Make sure you're using an App Password, not your regular password
