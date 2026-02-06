"""
Core Django Models for SME Financial Health Platform
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import json


class Company(models.Model):
    """Business profile and registration details"""
    INDUSTRY_CHOICES = [
        ('manufacturing', 'Manufacturing'),
        ('retail', 'Retail'),
        ('agriculture', 'Agriculture'),
        ('services', 'Services'),
        ('logistics', 'Logistics'),
        ('ecommerce', 'E-commerce'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='companies', null=True, blank=True)
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)
    registration_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    gst_number = models.CharField(max_length=15, null=True, blank=True)
    pan_number = models.CharField(max_length=10, null=True, blank=True)
    incorporation_date = models.DateField(null=True, blank=True)
    annual_revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    employee_count = models.IntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class FinancialData(models.Model):
    """Uploaded financial statements and raw data"""
    FILE_TYPE_CHOICES = [
        ('csv', 'CSV'),
        ('xlsx', 'Excel'),
        ('pdf', 'PDF'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='financial_data')
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    file = models.FileField(upload_to='financial_data/%Y/%m/')
    period_start = models.DateField()
    period_end = models.DateField()
    raw_data = models.JSONField(null=True, blank=True)  # Normalized data
    processed = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Financial Data'
        ordering = ['-period_end']
    
    def __str__(self):
        return f"{self.company.name} - {self.period_start} to {self.period_end}"


class FinancialMetrics(models.Model):
    """Computed financial ratios and scores"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='metrics')
    financial_data = models.ForeignKey(FinancialData, on_delete=models.CASCADE, related_name='metrics')
    
    # Liquidity Ratios
    current_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quick_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Profitability Ratios
    gross_margin = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    net_margin = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    roa = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Return on Assets
    roe = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Return on Equity
    
    # Efficiency Ratios
    inventory_turnover = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    receivables_days = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payables_days = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Solvency Ratios
    debt_to_equity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    interest_coverage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Cash Flow
    cash_flow_stability = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cash_conversion_cycle = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Overall Score
    health_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True, blank=True
    )
    
    calculated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Financial Metrics'
        ordering = ['-calculated_at']
    
    def __str__(self):
        return f"{self.company.name} - Score: {self.health_score}"


class CreditAssessment(models.Model):
    """Credit ratings and risk analysis"""
    RATING_CHOICES = [
        ('AAA', 'AAA - Excellent'),
        ('AA', 'AA - Very Good'),
        ('A', 'A - Good'),
        ('BBB', 'BBB - Adequate'),
        ('BB', 'BB - Moderate Risk'),
        ('B', 'B - High Risk'),
        ('C', 'C - Very High Risk'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='credit_assessments')
    metrics = models.ForeignKey(FinancialMetrics, on_delete=models.CASCADE, related_name='credit_assessment')
    
    credit_rating = models.CharField(max_length=5, choices=RATING_CHOICES)
    credit_score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Risk Scores
    cash_flow_risk = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    debt_servicing_risk = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    concentration_risk = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    compliance_risk = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Recommendations
    recommended_loan_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    recommended_tenure_months = models.IntegerField(null=True, blank=True)
    probability_of_stress = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    risk_factors = models.JSONField(default=list)  # List of identified risks
    assessed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Credit Assessments'
        ordering = ['-assessed_at']
    
    def __str__(self):
        return f"{self.company.name} - {self.credit_rating}"


class Recommendation(models.Model):
    """AI-generated recommendations"""
    CATEGORY_CHOICES = [
        ('cost_optimization', 'Cost Optimization'),
        ('working_capital', 'Working Capital'),
        ('financial_product', 'Financial Product'),
        ('compliance', 'Compliance'),
        ('general', 'General'),
    ]
    
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='recommendations')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    estimated_impact = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    implementation_effort = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=10, default='en')  # en, hi
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return f"{self.company.name} - {self.title}"


class IndustryBenchmark(models.Model):
    """Industry-specific benchmark data"""
    industry = models.CharField(max_length=50, unique=True)
    
    # Benchmark Ranges
    avg_current_ratio = models.DecimalField(max_digits=10, decimal_places=2)
    avg_gross_margin = models.DecimalField(max_digits=10, decimal_places=2)
    avg_net_margin = models.DecimalField(max_digits=10, decimal_places=2)
    avg_debt_to_equity = models.DecimalField(max_digits=10, decimal_places=2)
    avg_inventory_turnover = models.DecimalField(max_digits=10, decimal_places=2)
    avg_receivables_days = models.DecimalField(max_digits=10, decimal_places=2)
    avg_roa = models.DecimalField(max_digits=10, decimal_places=2)
    avg_roe = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Growth Expectations
    expected_revenue_growth = models.DecimalField(max_digits=5, decimal_places=2)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Benchmark - {self.industry}"


class Forecast(models.Model):
    """Financial forecasts and scenario planning"""
    SCENARIO_CHOICES = [
        ('best', 'Best Case'),
        ('base', 'Base Case'),
        ('worst', 'Worst Case'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='forecasts')
    scenario = models.CharField(max_length=10, choices=SCENARIO_CHOICES)
    forecast_months = models.IntegerField()
    
    revenue_forecast = models.JSONField()  # Monthly projections
    expense_forecast = models.JSONField()
    cash_flow_forecast = models.JSONField()
    
    assumptions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.company.name} - {self.scenario} - {self.forecast_months}m"


class Report(models.Model):
    """Generated reports"""
    REPORT_TYPE_CHOICES = [
        ('investor', 'Investor Report'),
        ('lender', 'Lender Report'),
        ('board', 'Board Report'),
        ('comprehensive', 'Comprehensive Report'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    file = models.FileField(upload_to='reports/%Y/%m/')
    language = models.CharField(max_length=10, default='en')
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"{self.company.name} - {self.report_type} - {self.generated_at.date()}"
