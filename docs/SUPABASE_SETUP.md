# 🗄️ Supabase Database Integration Guide

## Setup Instructions

### 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up or log in
3. Click "New Project"
4. Choose your organization
5. Set project name (e.g., "moodify-db")
6. Set strong database password
7. Choose region closest to your users
8. Click "Create new project"

### 2. Get Database Connection Details

From your Supabase dashboard:

1. Go to Settings → Database
2. Find "Connection string" section
3. Copy the URI (it looks like):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   ```

### 3. Configure Environment Variables

Add these to your Render environment variables:

```bash
# Required
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres

# Optional - for additional security
SUPABASE_URL=https://[PROJECT-REF].supabase.co
SUPABASE_ANON_KEY=[YOUR-ANON-KEY]
SUPABASE_SERVICE_KEY=[YOUR-SERVICE-KEY]
```

### 4. Install Required Packages

The required packages are already in requirements.txt:
- `psycopg2-binary` - PostgreSQL adapter
- `dj-database-url` - Database URL parsing

### 5. Update Settings

Your Django settings are already configured to use `DATABASE_URL` environment variable, so no code changes needed!

## Benefits of Supabase

### ✅ **Persistence**
- Data survives app restarts/redeployments
- No data loss on Render free tier sleep cycles
- Professional-grade PostgreSQL database

### ✅ **Performance**  
- Fast SSD storage
- Optimized for read/write performance
- Connection pooling available

### ✅ **Features**
- Real-time subscriptions (for future features)
- Built-in authentication (if needed)
- Row Level Security (RLS)
- Automatic backups

### ✅ **Scalability**
- Starts free, scales as you grow
- No connection limits on paid plans
- Multi-region availability

### ✅ **Developer Experience**
- Web-based SQL editor
- Database browser
- API auto-generation
- Logs and monitoring

## Migration Process

### Current Data Backup (If Any)

If you have existing data on Render's SQLite:

```bash
# 1. Backup current data
python manage.py dumpdata > backup.json

# 2. After Supabase setup, restore data
python manage.py loaddata backup.json
```

### Fresh Start (Recommended)

Since you're early in development:

```bash
# 1. Set DATABASE_URL in Render
# 2. Deploy to trigger migration
# 3. Create superuser
python manage.py createsuperuser
```

## Security Best Practices

### 🔒 **Database Security**

1. **Strong Password**: Use generated password from Supabase
2. **Environment Variables**: Never commit database URLs to code
3. **Connection Limits**: Monitor connection usage
4. **SSL**: Always use SSL connections (enabled by default)

### 🔒 **Row Level Security (Optional)**

```sql
-- Enable RLS on sensitive tables
ALTER TABLE mood_tracker_userprofile ENABLE ROW LEVEL SECURITY;

-- Create policy for user data isolation
CREATE POLICY "Users can only see own data" ON mood_tracker_userprofile
    FOR ALL USING (auth.uid() = user_id);
```

## Monitoring & Maintenance

### 📊 **Supabase Dashboard**

Monitor from your Supabase project:
- Database usage and performance
- Active connections
- Query performance
- Storage usage

### 📊 **Django Integration**

```python
# Optional: Add database health check
# In your health endpoint
from django.db import connection

def database_health():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            return {"database": "healthy"}
    except Exception as e:
        return {"database": f"error: {e}"}
```

## Cost Estimation

### 🆓 **Free Tier**
- Up to 500MB database storage
- Up to 2GB bandwidth
- Up to 50MB file storage
- Perfect for development and small apps

### 💰 **Pro Tier ($25/month)**
- 8GB database storage
- 250GB bandwidth
- 100GB file storage
- Daily backups
- No connection limits

## Troubleshooting

### Common Issues

**Connection Timeout**
```python
# Increase timeout in settings
DATABASES['default']['OPTIONS'] = {
    'connect_timeout': 30,
}
```

**Too Many Connections**
```python
# Use connection pooling
DATABASES['default']['CONN_MAX_AGE'] = 600
```

**Migration Issues**
```bash
# Reset migrations if needed
python manage.py migrate --fake
python manage.py migrate
```

## Next Steps After Setup

1. **Set DATABASE_URL** in Render environment variables
2. **Deploy** to trigger automatic migration
3. **Create superuser** via Render console or script
4. **Test** the application thoroughly
5. **Monitor** database performance in Supabase dashboard

Your data will now be safe, persistent, and professionally managed! 🎉
