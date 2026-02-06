"""
URL Configuration for Core App
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompanyViewSet, FinancialDataViewSet, FinancialMetricsViewSet,
    CreditAssessmentViewSet, RecommendationViewSet, IndustryBenchmarkViewSet,
    ForecastViewSet, ReportViewSet
)

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'financial-data', FinancialDataViewSet)
router.register(r'metrics', FinancialMetricsViewSet)
router.register(r'credit-assessments', CreditAssessmentViewSet)
router.register(r'recommendations', RecommendationViewSet)
router.register(r'benchmarks', IndustryBenchmarkViewSet)
router.register(r'forecasts', ForecastViewSet)
router.register(r'reports', ReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
