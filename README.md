# SME Financial Health Platform

A comprehensive AI-driven financial health assessment platform for small and medium enterprises.

## Features

- 📊 **Financial Health Assessment** - Automated calculation of key financial ratios and health scores
- 💰 **Cost Optimization** - AI-powered recommendations to reduce costs and improve margins
- 📈 **Financial Forecasting** - Revenue and cash flow projections with scenario planning
- 🏦 **Credit Assessment** - Creditworthiness evaluation and loan recommendations
- 📑 **PDF Reports** - Investor-ready reports in multiple languages (English, Hindi)
- 🌐 **Multilingual Support** - Simple explanations for non-finance users

## Tech Stack

- **Backend**: Django 4.2, Django REST Framework, PostgreSQL
- **Frontend**: React 18, Chart.js, Axios
- **AI**: Google Gemini API
- **Data Processing**: Pandas, NumPy, pdfplumber
- **Reports**: ReportLab
- **Deployment**: Docker, Docker Compose

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Docker & Docker Compose (for containerized deployment)

### Option 1: Docker Deployment (Recommended)

1. **Clone and setup**
   ```bash
   cd c:\SME
   copy .env.example .env
   ```

2. **Configure environment variables in `.env`**
   - Add your Gemini API key
   - Update database credentials if needed

3. **Start all services**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api
   - Admin Panel: http://localhost:8000/admin

### Option 2: Local Development

#### Backend Setup

1. **Create virtual environment**
   ```bash
   cd c:\SME\backend
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup database**
   ```bash
   # Create PostgreSQL database
   createdb sme_platform
   ```

4. **Configure environment**
   ```bash
   copy ..\\.env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Load industry benchmarks (optional)**
   ```bash
   python manage.py shell
   ```
   ```python
   from core.models import IndustryBenchmark
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
   # Repeat for other industries
   ```

8. **Start backend server**
   ```bash
   python manage.py runserver
   ```

#### Frontend Setup

1. **Install dependencies**
   ```bash
   cd c:\SME\frontend
   npm install
   ```

2. **Configure API URL**
   Create `.env` file:
   ```
   REACT_APP_API_URL=http://localhost:8000/api
   ```

3. **Start frontend**
   ```bash
   npm start
   ```

4. **Access application**
   - Open http://localhost:3000

## Usage Guide

### 1. Upload Financial Data

1. Navigate to "Upload Data"
2. Enter company information (name, industry, GST, PAN)
3. Upload financial statement (CSV, XLSX, or PDF)
4. Specify the period dates
5. Click "Upload and Process"

### 2. View Dashboard

- See overall financial health score (0-100)
- Review key financial ratios
- Analyze liquidity, profitability, efficiency, and solvency metrics

### 3. Credit Assessment

- Generate credit rating and score
- View risk analysis (cash flow, debt servicing, concentration, compliance)
- Get loan amount and tenure recommendations

### 4. AI Recommendations

- Generate cost optimization suggestions
- Get working capital improvement tips
- View estimated financial impact
- Switch between English and Hindi

### 5. Financial Forecasting

- Generate 6-24 month projections
- View best, base, and worst case scenarios
- Analyze revenue, expense, and cash flow trends

### 6. Generate Reports

- Create PDF reports (Comprehensive, Investor, Lender, Board)
- Choose language (English or Hindi)
- Download and share with stakeholders

## API Endpoints

### Companies
- `GET /api/companies/` - List all companies
- `POST /api/companies/` - Create company
- `GET /api/companies/{id}/` - Get company details

### Financial Data
- `POST /api/financial-data/` - Upload financial data
- `POST /api/financial-data/{id}/process/` - Process uploaded data

### Metrics
- `GET /api/metrics/?company={id}` - Get company metrics
- `GET /api/metrics/latest/?company={id}` - Get latest metrics

### Credit Assessment
- `POST /api/credit-assessments/assess/` - Generate assessment
- `GET /api/credit-assessments/?company={id}` - Get assessments

### Recommendations
- `POST /api/recommendations/generate/` - Generate recommendations
- `GET /api/recommendations/?company={id}` - Get recommendations

### Forecasts
- `POST /api/forecasts/generate/` - Generate forecasts
- `GET /api/forecasts/?company={id}` - Get forecasts

### Reports
- `POST /api/reports/generate/` - Generate PDF report
- `GET /api/reports/?company={id}` - Get reports

## Project Structure

```
SME/
├── backend/
│   ├── sme_platform/          # Django project settings
│   ├── core/                  # Main application
│   │   ├── models.py          # Database models
│   │   ├── views.py           # API views
│   │   ├── serializers.py     # DRF serializers
│   │   ├── engines/           # Financial analysis engines
│   │   │   ├── financial_health.py
│   │   │   ├── credit_risk.py
│   │   │   ├── cost_optimizer.py
│   │   │   ├── working_capital.py
│   │   │   ├── forecasting.py
│   │   │   └── compliance.py
│   │   └── services/          # Business services
│   │       ├── data_ingestion.py
│   │       ├── ai_service.py
│   │       └── report_generator.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── pages/            # React pages
│   │   ├── services/         # API service
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
└── .env.example
```

## Security Features

- ✅ AES-256 encryption at rest (configurable)
- ✅ TLS 1.3 in transit (production)
- ✅ CORS protection
- ✅ CSRF protection
- ✅ SQL injection prevention (Django ORM)
- ✅ XSS protection
- ✅ Secure file upload validation

## Contributing

This is a production-ready platform. For enhancements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

Proprietary - All rights reserved

## Support

For issues or questions, please contact the development team.
