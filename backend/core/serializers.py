"""
DRF Serializers for SME Platform
"""
from rest_framework import serializers
from .models import (
    Company, FinancialData, FinancialMetrics,
    CreditAssessment, Recommendation, IndustryBenchmark,
    Forecast, Report
)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'industry', 'registration_number', 'gst_number',
            'pan_number', 'incorporation_date', 'annual_revenue',
            'employee_count', 'address', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FinancialDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialData
        fields = [
            'id', 'company', 'file_type', 'file', 'period_start',
            'period_end', 'raw_data', 'processed', 'uploaded_at'
        ]
        read_only_fields = ['id', 'processed', 'uploaded_at']


class FinancialMetricsSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    
    class Meta:
        model = FinancialMetrics
        fields = [
            'id', 'company', 'company_name', 'financial_data',
            'current_ratio', 'quick_ratio', 'gross_margin', 'net_margin',
            'roa', 'roe', 'inventory_turnover', 'receivables_days',
            'payables_days', 'debt_to_equity', 'interest_coverage',
            'cash_flow_stability', 'cash_conversion_cycle', 'health_score',
            'calculated_at'
        ]
        read_only_fields = ['id', 'calculated_at']


class CreditAssessmentSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    
    class Meta:
        model = CreditAssessment
        fields = [
            'id', 'company', 'company_name', 'metrics', 'credit_rating',
            'credit_score', 'cash_flow_risk', 'debt_servicing_risk',
            'concentration_risk', 'compliance_risk', 'recommended_loan_amount',
            'recommended_tenure_months', 'probability_of_stress',
            'risk_factors', 'assessed_at'
        ]
        read_only_fields = ['id', 'assessed_at']


class RecommendationSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    
    class Meta:
        model = Recommendation
        fields = [
            'id', 'company', 'company_name', 'category', 'priority',
            'title', 'description', 'estimated_impact',
            'implementation_effort', 'language', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class IndustryBenchmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustryBenchmark
        fields = [
            'id', 'industry', 'avg_current_ratio', 'avg_gross_margin',
            'avg_net_margin', 'avg_debt_to_equity', 'avg_inventory_turnover',
            'avg_receivables_days', 'avg_roa', 'avg_roe',
            'expected_revenue_growth', 'updated_at'
        ]
        read_only_fields = ['id', 'updated_at']


class ForecastSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    
    class Meta:
        model = Forecast
        fields = [
            'id', 'company', 'company_name', 'scenario', 'forecast_months',
            'revenue_forecast', 'expense_forecast', 'cash_flow_forecast',
            'assumptions', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ReportSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    
    class Meta:
        model = Report
        fields = [
            'id', 'company', 'company_name', 'report_type',
            'file', 'language', 'generated_at'
        ]
        read_only_fields = ['id', 'generated_at']
