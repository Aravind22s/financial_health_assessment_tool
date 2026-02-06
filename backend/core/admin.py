from django.contrib import admin
from .models import (
    Company, FinancialData, FinancialMetrics, 
    CreditAssessment, Recommendation, IndustryBenchmark,
    Forecast, Report
)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry', 'created_at']
    search_fields = ['name', 'registration_number']
    list_filter = ['industry', 'created_at']


@admin.register(FinancialData)
class FinancialDataAdmin(admin.ModelAdmin):
    list_display = ['company', 'file_type', 'period_start', 'period_end', 'processed']
    list_filter = ['file_type', 'processed', 'uploaded_at']
    search_fields = ['company__name']


@admin.register(FinancialMetrics)
class FinancialMetricsAdmin(admin.ModelAdmin):
    list_display = ['company', 'health_score', 'calculated_at']
    list_filter = ['calculated_at']
    search_fields = ['company__name']


@admin.register(CreditAssessment)
class CreditAssessmentAdmin(admin.ModelAdmin):
    list_display = ['company', 'credit_rating', 'credit_score', 'assessed_at']
    list_filter = ['credit_rating', 'assessed_at']
    search_fields = ['company__name']


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ['company', 'category', 'priority', 'title', 'created_at']
    list_filter = ['category', 'priority', 'created_at']
    search_fields = ['company__name', 'title']


@admin.register(IndustryBenchmark)
class IndustryBenchmarkAdmin(admin.ModelAdmin):
    list_display = ['industry', 'avg_gross_margin', 'avg_net_margin', 'updated_at']
    search_fields = ['industry']


@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    list_display = ['company', 'scenario', 'forecast_months', 'created_at']
    list_filter = ['scenario', 'created_at']
    search_fields = ['company__name']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['company', 'report_type', 'language', 'generated_at']
    list_filter = ['report_type', 'language', 'generated_at']
    search_fields = ['company__name']
