"""
Working Capital Optimization Engine
Analyzes and optimizes working capital management
"""
from ..models import Recommendation


class WorkingCapitalEngine:
    """Engine for working capital optimization"""
    
    def generate_recommendations(self, company, metrics):
        """Generate working capital recommendations"""
        recommendations = []
        
        if not metrics:
            return recommendations
        
        # Cash conversion cycle optimization
        if metrics.cash_conversion_cycle and metrics.cash_conversion_cycle > 60:
            rec = Recommendation.objects.create(
                company=company,
                category='working_capital',
                priority='high',
                title='Reduce Cash Conversion Cycle',
                description=f'Cash conversion cycle is {metrics.cash_conversion_cycle} days. Focus on faster collections, optimized inventory, and extended payables to free up working capital.',
                estimated_impact=float(company.annual_revenue) * 0.05 if company.annual_revenue else None,
                implementation_effort='Medium - 3-4 months'
            )
            recommendations.append(rec)
        
        # Accounts receivable management
        if metrics.receivables_days and metrics.receivables_days > 45:
            rec = Recommendation.objects.create(
                company=company,
                category='working_capital',
                priority='high',
                title='Accelerate Receivables Collection',
                description=f'Receivables are outstanding for {metrics.receivables_days} days. Implement automated reminders, offer early payment incentives, or use invoice discounting services.',
                estimated_impact=float(company.annual_revenue) * 0.03 if company.annual_revenue else None,
                implementation_effort='Low - 1-2 months'
            )
            recommendations.append(rec)
        
        # Payables optimization
        if metrics.payables_days and metrics.payables_days < 30:
            rec = Recommendation.objects.create(
                company=company,
                category='working_capital',
                priority='medium',
                title='Optimize Payment Terms with Suppliers',
                description=f'Current payables period is {metrics.payables_days} days. Negotiate extended payment terms with suppliers to improve cash flow without damaging relationships.',
                estimated_impact=float(company.annual_revenue) * 0.02 if company.annual_revenue else None,
                implementation_effort='Low - 1-2 months'
            )
            recommendations.append(rec)
        
        # Liquidity improvement
        if metrics.current_ratio and metrics.current_ratio < 1.2:
            rec = Recommendation.objects.create(
                company=company,
                category='working_capital',
                priority='high',
                title='Improve Liquidity Position',
                description=f'Current ratio is {metrics.current_ratio}, indicating tight liquidity. Consider securing a working capital line of credit, reducing short-term debt, or converting assets to cash.',
                estimated_impact=None,
                implementation_effort='Medium - 2-3 months'
            )
            recommendations.append(rec)
        
        # Invoice discounting suitability
        if metrics.receivables_days and metrics.receivables_days > 60 and company.annual_revenue:
            if float(company.annual_revenue) > 5000000:  # 50 lakhs+
                rec = Recommendation.objects.create(
                    company=company,
                    category='working_capital',
                    priority='medium',
                    title='Consider Invoice Discounting',
                    description=f'With receivables of {metrics.receivables_days} days and significant revenue, invoice discounting could unlock immediate cash flow. Typical cost: 12-18% annually.',
                    estimated_impact=float(company.annual_revenue) * 0.04 if company.annual_revenue else None,
                    implementation_effort='Low - 2-4 weeks'
                )
                recommendations.append(rec)
        
        return recommendations
