"""
Seed sample data for SME Financial Health Platform
Run this script to populate the database with test data
"""
import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sme_platform.settings')
django.setup()

from core.models import Company, FinancialData, FinancialMetrics, IndustryBenchmark
from django.contrib.auth.models import User


def create_sample_companies():
    """Create sample companies"""
    print("Creating sample companies...")
    
    companies = [
        {
            'name': 'TechManufacturing Pvt Ltd',
            'industry': 'manufacturing',
            'registration_number': 'MFG2020001',
            'gst_number': '29ABCDE1234F1Z5',
            'pan_number': 'ABCDE1234F',
            'incorporation_date': date(2020, 1, 15),
            'annual_revenue': Decimal('50000000.00'),
            'employee_count': 150,
            'address': '123 Industrial Area, Bangalore, Karnataka 560001'
        },
        {
            'name': 'RetailMart India',
            'industry': 'retail',
            'registration_number': 'RET2019045',
            'gst_number': '27FGHIJ5678K2L9',
            'pan_number': 'FGHIJ5678K',
            'incorporation_date': date(2019, 6, 10),
            'annual_revenue': Decimal('35000000.00'),
            'employee_count': 85,
            'address': '456 Market Street, Mumbai, Maharashtra 400001'
        },
        {
            'name': 'AgriGrow Solutions',
            'industry': 'agriculture',
            'registration_number': 'AGR2021023',
            'gst_number': '36KLMNO9012P3Q4',
            'pan_number': 'KLMNO9012P',
            'incorporation_date': date(2021, 3, 20),
            'annual_revenue': Decimal('25000000.00'),
            'employee_count': 60,
            'address': '789 Farm Road, Hyderabad, Telangana 500001'
        },
        {
            'name': 'ServicePro Consulting',
            'industry': 'services',
            'registration_number': 'SRV2018067',
            'gst_number': '07RSTUV3456W7X8',
            'pan_number': 'RSTUV3456W',
            'incorporation_date': date(2018, 9, 5),
            'annual_revenue': Decimal('45000000.00'),
            'employee_count': 120,
            'address': '321 Business Park, Delhi 110001'
        }
    ]
    
    created_companies = []
    for company_data in companies:
        company, created = Company.objects.get_or_create(
            registration_number=company_data['registration_number'],
            defaults=company_data
        )
        if created:
            print(f"  ✓ Created: {company.name}")
        else:
            print(f"  - Already exists: {company.name}")
        created_companies.append(company)
    
    return created_companies


def create_financial_metrics(companies):
    """Create financial metrics for companies"""
    print("\nCreating financial metrics...")
    
    metrics_data = {
        'TechManufacturing Pvt Ltd': {
            'current_ratio': Decimal('1.8'),
            'quick_ratio': Decimal('1.2'),
            'gross_margin': Decimal('28.5'),
            'net_margin': Decimal('12.3'),
            'roa': Decimal('9.5'),
            'roe': Decimal('16.8'),
            'inventory_turnover': Decimal('6.5'),
            'receivables_days': Decimal('42.0'),
            'payables_days': Decimal('35.0'),
            'debt_to_equity': Decimal('0.9'),
            'interest_coverage': Decimal('5.2'),
            'cash_flow_stability': Decimal('78.5'),
            'cash_conversion_cycle': Decimal('45.0'),
            'health_score': 82
        },
        'RetailMart India': {
            'current_ratio': Decimal('1.4'),
            'quick_ratio': Decimal('0.9'),
            'gross_margin': Decimal('32.0'),
            'net_margin': Decimal('6.8'),
            'roa': Decimal('7.2'),
            'roe': Decimal('13.5'),
            'inventory_turnover': Decimal('8.2'),
            'receivables_days': Decimal('28.0'),
            'payables_days': Decimal('40.0'),
            'debt_to_equity': Decimal('1.3'),
            'interest_coverage': Decimal('4.1'),
            'cash_flow_stability': Decimal('72.0'),
            'cash_conversion_cycle': Decimal('38.0'),
            'health_score': 75
        },
        'AgriGrow Solutions': {
            'current_ratio': Decimal('1.6'),
            'quick_ratio': Decimal('1.0'),
            'gross_margin': Decimal('22.0'),
            'net_margin': Decimal('8.5'),
            'roa': Decimal('6.8'),
            'roe': Decimal('11.2'),
            'inventory_turnover': Decimal('5.5'),
            'receivables_days': Decimal('55.0'),
            'payables_days': Decimal('45.0'),
            'debt_to_equity': Decimal('1.1'),
            'interest_coverage': Decimal('3.8'),
            'cash_flow_stability': Decimal('68.5'),
            'cash_conversion_cycle': Decimal('52.0'),
            'health_score': 70
        },
        'ServicePro Consulting': {
            'current_ratio': Decimal('2.1'),
            'quick_ratio': Decimal('1.8'),
            'gross_margin': Decimal('42.0'),
            'net_margin': Decimal('16.5'),
            'roa': Decimal('11.2'),
            'roe': Decimal('19.5'),
            'inventory_turnover': Decimal('12.0'),
            'receivables_days': Decimal('58.0'),
            'payables_days': Decimal('30.0'),
            'debt_to_equity': Decimal('0.7'),
            'interest_coverage': Decimal('6.5'),
            'cash_flow_stability': Decimal('85.0'),
            'cash_conversion_cycle': Decimal('60.0'),
            'health_score': 88
        }
    }
    
    for company in companies:
        if company.name in metrics_data:
            # Create a dummy financial data entry first
            financial_data, _ = FinancialData.objects.get_or_create(
                company=company,
                period_start=date.today() - timedelta(days=365),
                period_end=date.today(),
                defaults={
                    'file_type': 'csv',
                    'processed': True
                }
            )
            
            metrics, created = FinancialMetrics.objects.get_or_create(
                company=company,
                financial_data=financial_data,
                defaults=metrics_data[company.name]
            )
            if created:
                print(f"  ✓ Created metrics for: {company.name} (Score: {metrics.health_score})")
            else:
                print(f"  - Metrics already exist for: {company.name}")


def verify_industry_benchmarks():
    """Verify industry benchmarks exist"""
    print("\nVerifying industry benchmarks...")
    
    count = IndustryBenchmark.objects.count()
    if count > 0:
        print(f"  ✓ Found {count} industry benchmarks")
        for benchmark in IndustryBenchmark.objects.all():
            print(f"    - {benchmark.industry}: Current Ratio={benchmark.avg_current_ratio}, Gross Margin={benchmark.avg_gross_margin}%")
    else:
        print("  ⚠ No industry benchmarks found. Please run the benchmark creation script from SETUP.md")


def print_summary():
    """Print summary of seeded data"""
    print("\n" + "="*60)
    print("DATABASE SEEDING COMPLETE")
    print("="*60)
    
    print(f"\n📊 Summary:")
    print(f"  Companies: {Company.objects.count()}")
    print(f"  Financial Metrics: {FinancialMetrics.objects.count()}")
    print(f"  Industry Benchmarks: {IndustryBenchmark.objects.count()}")
    
    print(f"\n🏢 Companies by Industry:")
    for industry, name in Company.INDUSTRY_CHOICES:
        count = Company.objects.filter(industry=industry).count()
        if count > 0:
            print(f"  {name}: {count}")
    
    print(f"\n💯 Health Scores:")
    for metrics in FinancialMetrics.objects.all().order_by('-health_score'):
        print(f"  {metrics.company.name}: {metrics.health_score}/100")
    
    print("\n✅ You can now test the platform with this sample data!")
    print("   Frontend: http://localhost:3000")
    print("   Backend API: http://localhost:8000/api")
    print("   Admin: http://localhost:8000/admin")


def main():
    print("="*60)
    print("SME PLATFORM - SAMPLE DATA SEEDING")
    print("="*60)
    
    try:
        companies = create_sample_companies()
        create_financial_metrics(companies)
        verify_industry_benchmarks()
        print_summary()
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
