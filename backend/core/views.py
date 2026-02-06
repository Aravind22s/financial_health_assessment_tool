"""
API Views for SME Platform
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import (
    Company, FinancialData, FinancialMetrics,
    CreditAssessment, Recommendation, IndustryBenchmark,
    Forecast, Report
)
from .serializers import (
    CompanySerializer, FinancialDataSerializer, FinancialMetricsSerializer,
    CreditAssessmentSerializer, RecommendationSerializer, IndustryBenchmarkSerializer,
    ForecastSerializer, ReportSerializer
)
from .services.data_ingestion import DataIngestionService
from .engines.financial_health import FinancialHealthEngine
from .engines.credit_risk import CreditRiskEngine
from .engines.cost_optimizer import CostOptimizerEngine
from .engines.working_capital import WorkingCapitalEngine
from .engines.forecasting import ForecastingEngine
from .services.ai_service import AIService
from .services.report_generator import ReportGenerator


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class FinancialDataViewSet(viewsets.ModelViewSet):
    queryset = FinancialData.objects.all()
    serializer_class = FinancialDataSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        company_id = self.request.query_params.get('company')
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        return queryset
    
    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        """Process uploaded financial data"""
        financial_data = self.get_object()
        
        try:
            # Ingest and normalize data
            service = DataIngestionService()
            normalized_data = service.process_file(financial_data)
            
            financial_data.raw_data = normalized_data
            financial_data.processed = True
            financial_data.save()
            
            # Calculate financial metrics
            engine = FinancialHealthEngine()
            metrics = engine.calculate_metrics(financial_data)
            
            return Response({
                'status': 'success',
                'message': 'Data processed successfully',
                'metrics_id': metrics.id
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class FinancialMetricsViewSet(viewsets.ModelViewSet):
    queryset = FinancialMetrics.objects.all()
    serializer_class = FinancialMetricsSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        company_id = self.request.query_params.get('company')
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        return queryset
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get latest metrics for a company"""
        company_id = request.query_params.get('company')
        if not company_id:
            return Response({'error': 'company parameter required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        metrics = FinancialMetrics.objects.filter(company_id=company_id).order_by('-calculated_at').first()
        if not metrics:
            return Response({'error': 'No metrics found'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(metrics)
        return Response(serializer.data)


class CreditAssessmentViewSet(viewsets.ModelViewSet):
    queryset = CreditAssessment.objects.all()
    serializer_class = CreditAssessmentSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        company_id = self.request.query_params.get('company')
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        return queryset
    
    @action(detail=False, methods=['post'])
    def assess(self, request):
        """Perform credit assessment for a company"""
        company_id = request.data.get('company_id')
        if not company_id:
            return Response({'error': 'company_id required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        company = get_object_or_404(Company, id=company_id)
        metrics = FinancialMetrics.objects.filter(company=company).first()
        
        if not metrics:
            return Response({'error': 'No financial metrics found. Please process financial data first.'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            engine = CreditRiskEngine()
            assessment = engine.assess_credit(company, metrics)
            
            serializer = self.get_serializer(assessment)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_400_BAD_REQUEST)


class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        company_id = self.request.query_params.get('company')
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        return queryset
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate AI recommendations for a company"""
        company_id = request.data.get('company_id')
        language = request.data.get('language', 'en')
        
        if not company_id:
            return Response({'error': 'company_id required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        company = get_object_or_404(Company, id=company_id)
        
        try:
            # Get latest metrics and assessment
            metrics = FinancialMetrics.objects.filter(company=company).first()
            assessment = CreditAssessment.objects.filter(company=company).first()
            
            # Generate cost optimization recommendations
            cost_engine = CostOptimizerEngine()
            cost_recs = cost_engine.generate_recommendations(company, metrics)
            
            # Generate working capital recommendations
            wc_engine = WorkingCapitalEngine()
            wc_recs = wc_engine.generate_recommendations(company, metrics)
            
            # Use AI to enhance recommendations
            ai_service = AIService()
            all_recs = cost_recs + wc_recs
            enhanced_recs = ai_service.enhance_recommendations(company, all_recs, language)
            
            serializer = self.get_serializer(enhanced_recs, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_400_BAD_REQUEST)


class IndustryBenchmarkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IndustryBenchmark.objects.all()
    serializer_class = IndustryBenchmarkSerializer
    
    @action(detail=False, methods=['get'])
    def by_industry(self, request):
        """Get benchmark for specific industry"""
        industry = request.query_params.get('industry')
        if not industry:
            return Response({'error': 'industry parameter required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        benchmark = get_object_or_404(IndustryBenchmark, industry=industry)
        serializer = self.get_serializer(benchmark)
        return Response(serializer.data)


class ForecastViewSet(viewsets.ModelViewSet):
    queryset = Forecast.objects.all()
    serializer_class = ForecastSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        company_id = self.request.query_params.get('company')
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        return queryset
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate financial forecast for a company"""
        company_id = request.data.get('company_id')
        months = request.data.get('months', 12)
        
        if not company_id:
            return Response({'error': 'company_id required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        company = get_object_or_404(Company, id=company_id)
        
        try:
            engine = ForecastingEngine()
            forecasts = engine.generate_forecasts(company, months)
            
            serializer = self.get_serializer(forecasts, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_400_BAD_REQUEST)


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        company_id = self.request.query_params.get('company')
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        return queryset
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate PDF report for a company"""
        company_id = request.data.get('company_id')
        report_type = request.data.get('report_type', 'comprehensive')
        language = request.data.get('language', 'en')
        
        if not company_id:
            return Response({'error': 'company_id required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        company = get_object_or_404(Company, id=company_id)
        
        try:
            generator = ReportGenerator()
            report = generator.generate_report(company, report_type, language)
            
            serializer = self.get_serializer(report)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, 
                          status=status.HTTP_400_BAD_REQUEST)
