# Setup Instructions - SME Financial Health Platform

## Step-by-Step Setup Guide

### Step 1: Environment Setup

1. **Copy environment file**
   ```powershell
   cd c:\SME
   Copy-Item .env.example .env
   ```

2. **Edit `.env` file and add your Gemini API key**
   - Get API key from: https://makersuite.google.com/app/apikey
   - Update `GEMINI_API_KEY=your-actual-api-key-here`

### Step 2: Docker Deployment (Easiest)

1. **Start all services**
   ```powershell
   docker-compose up --build
   ```

2. **Wait for services to start** (2-3 minutes)
   - Database initialization
   - Backend migrations
   - Frontend build

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api
   - Admin: http://localhost:8000/admin

4. **Create admin user** (in new terminal)
   ```powershell
   docker-compose exec backend python manage.py createsuperuser
   ```

### Step 3: Load Sample Data (Optional)

1. **Access Django shell**
   ```powershell
   docker-compose exec backend python manage.py shell
   ```

2. **Create industry benchmarks**
   ```python
   from core.models import IndustryBenchmark
   
   # Manufacturing
   IndustryBenchmark.objects.create(
       industry='manufacturing',
       avg_current_ratio=1.5,
       avg_gross_margin=25.0,
       avg_net_margin=10.0,
       avg_debt_to_equity=1.0,
       avg_inventory_turnover=6.0,
       avg_receivables_days=45.0,
       avg_roa=8.0,
       avg_roe=15.0,
       expected_revenue_growth=10.0
   )
   
   # Retail
   IndustryBenchmark.objects.create(
       industry='retail',
       avg_current_ratio=1.3,
       avg_gross_margin=30.0,
       avg_net_margin=5.0,
       avg_debt_to_equity=1.5,
       avg_inventory_turnover=8.0,
       avg_receivables_days=30.0,
       avg_roa=6.0,
       avg_roe=12.0,
       expected_revenue_growth=8.0
   )
   
   # Services
   IndustryBenchmark.objects.create(
       industry='services',
       avg_current_ratio=1.2,
       avg_gross_margin=40.0,
       avg_net_margin=15.0,
       avg_debt_to_equity=0.8,
       avg_inventory_turnover=12.0,
       avg_receivables_days=60.0,
       avg_roa=10.0,
       avg_roe=18.0,
       expected_revenue_growth=12.0
   )
   
   exit()
   ```

### Step 4: Test the Platform

1. **Open browser**: http://localhost:3000

2. **Upload financial data**:
   - Click "Upload Data"
   - Enter company details
   - Upload a sample CSV/Excel file with financial data

3. **View dashboard**:
   - See financial health score
   - Review key metrics

4. **Generate credit assessment**:
   - Navigate to "Credit Assessment"
   - Click "Generate Credit Assessment"

5. **Get recommendations**:
   - Go to "Recommendations"
   - Click "Generate Recommendations"
   - Try switching to Hindi

6. **Create forecast**:
   - Visit "Forecast" page
   - Select forecast period
   - Generate projections

7. **Download report**:
   - Go to "Reports"
   - Select report type and language
   - Generate and download PDF

## Alternative: Local Development Setup

### Backend

```powershell
cd c:\SME\backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup PostgreSQL database
# (Install PostgreSQL first if not installed)
createdb sme_platform

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver
```

### Frontend

```powershell
cd c:\SME\frontend

# Install dependencies
npm install

# Create .env file
echo REACT_APP_API_URL=http://localhost:8000/api > .env

# Start development server
npm start
```

## Troubleshooting

### Docker Issues

**Port already in use:**
```powershell
# Stop existing containers
docker-compose down

# Check what's using the port
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Kill the process or change ports in docker-compose.yml
```

**Database connection errors:**
```powershell
# Restart services
docker-compose restart

# Check logs
docker-compose logs db
docker-compose logs backend
```

### Backend Issues

**Migration errors:**
```powershell
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```

**Static files not loading:**
```powershell
docker-compose exec backend python manage.py collectstatic --noinput
```

### Frontend Issues

**API connection errors:**
- Check `.env` file has correct `REACT_APP_API_URL`
- Verify backend is running
- Check CORS settings in backend

**Build errors:**
```powershell
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Production Deployment

### Security Checklist

- [ ] Change `SECRET_KEY` in `.env`
- [ ] Set `DEBUG=False`
- [ ] Update `ALLOWED_HOSTS`
- [ ] Configure proper database credentials
- [ ] Enable HTTPS/TLS
- [ ] Set up proper CORS origins
- [ ] Configure firewall rules
- [ ] Set up backup strategy
- [ ] Enable logging and monitoring

### Recommended Infrastructure

- **Database**: Managed PostgreSQL (AWS RDS, Azure Database, etc.)
- **Backend**: Container service (AWS ECS, Azure Container Apps, etc.)
- **Frontend**: Static hosting (AWS S3 + CloudFront, Netlify, Vercel)
- **Storage**: Object storage for media files (AWS S3, Azure Blob)
- **Monitoring**: Application monitoring (Sentry, DataDog, etc.)

## Next Steps

1. ✅ Platform is ready to use
2. Upload your financial data
3. Explore all features
4. Generate reports
5. Customize for your needs

For support or questions, refer to README.md or contact the development team.
