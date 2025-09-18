# Deploying Bookstore on Render

This guide will help you deploy your Django bookstore application on Render.

## Prerequisites

1. A GitHub account
2. A Render account (free at https://render.com)
3. Your Django project pushed to a GitHub repository

## Deployment Steps

### 1. Push Your Code to GitHub

If you haven't already, push your project to GitHub:

```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### 2. Deploy on Render

#### Option A: Using render.yaml (Recommended)

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" and select "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` file and create the service
5. Click "Apply" to deploy

#### Option B: Manual Setup

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `bookstore` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn bookstore.wsgi:application`
   - **Plan**: Free

5. Add Environment Variables:
   - `PYTHON_VERSION`: `3.11.0`
   - `DJANGO_SETTINGS_MODULE`: `bookstore.settings`
   - `SECRET_KEY`: Generate a new secret key (you can use Django's `get_random_secret_key()`)
   - `WEB_CONCURRENCY`: `4`

6. Click "Create Web Service"

### 3. Configure Database (Optional)

For production, consider using a PostgreSQL database:

1. In Render Dashboard, create a new "PostgreSQL" service
2. Copy the database URL
3. Add it as an environment variable `DATABASE_URL` in your web service

### 4. Domain Configuration

Your app will be available at: `https://your-app-name.onrender.com`

## Environment Variables

Make sure these environment variables are set in Render:

- `SECRET_KEY`: Your Django secret key
- `DJANGO_SETTINGS_MODULE`: `bookstore.settings`
- `PYTHON_VERSION`: `3.11.0`
- `WEB_CONCURRENCY`: `4`

## Troubleshooting

### Common Issues:

1. **Build fails**: Check the build logs in Render dashboard
2. **Static files not loading**: Ensure `whitenoise` is properly configured
3. **Database connection**: Verify `DATABASE_URL` is set correctly
4. **Import errors**: Check that all dependencies are in `requirements.txt`

### Checking Logs:

1. Go to your service in Render dashboard
2. Click on "Logs" tab
3. Check for any error messages

## Local Development

To run locally with the same settings:

```bash
cd bookstore
python manage.py runserver
```

## Security Notes

- Never commit sensitive information like secret keys
- Use environment variables for configuration
- Keep dependencies updated
- Enable HTTPS in production (Render handles this automatically)
