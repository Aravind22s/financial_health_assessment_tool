"""
Cost Optimization Engine
Analyzes expenses and generates cost-saving recommendations
"""
from ..models import Recommendation


class CostOptimizerEngine:
    """Engine for identifying cost optimization opportunities"""
    
    def generate_recommendations(self, company, metrics):
        """Generate cost optimization recommendations"""
        recommendations = []
        
        if not metrics:
            return recommendations
        
        # Analyze expense ratios
        if metrics.gross_margin and metrics.gross_margin < 30:
            rec = Recommendation.objects.create(
                company=company,
                category='cost_optimization',
                priority='high',
                title='Improve Gross Margin',
                description=f'Current gross margin is {metrics.gross_margin}%, which is below industry standards. Consider negotiating better supplier terms, reducing production costs, or optimizing pricing strategy.',
                estimated_impact=float(company.annual_revenue) * 0.05 if company.annual_revenue else None,
                implementation_effort='Medium - 3-6 months'
            )
            recommendations.append(rec)
        
        # Analyze operating efficiency
        if metrics.receivables_days and metrics.receivables_days > 60:
            rec = Recommendation.objects.create(
                company=company,
                category='cost_optimization',
                priority='high',
                title='Reduce Receivables Collection Period',
                description=f'Average collection period is {metrics.receivables_days} days. Implement stricter credit policies, offer early payment discounts, or consider invoice factoring to improve cash flow.',
                estimated_impact=float(company.annual_revenue) * 0.03 if company.annual_revenue else None,
                implementation_effort='Low - 1-2 months'
            )
            recommendations.append(rec)
        
        # Inventory optimization
        if metrics.inventory_turnover and metrics.inventory_turnover < 4:
            rec = Recommendation.objects.create(
                company=company,
                category='cost_optimization',
                priority='medium',
                title='Optimize Inventory Management',
                description=f'Inventory turnover is {metrics.inventory_turnover}x per year, indicating slow-moving stock. Implement just-in-time inventory, reduce obsolete stock, and improve demand forecasting.',
                estimated_impact=float(company.annual_revenue) * 0.02 if company.annual_revenue else None,
                implementation_effort='Medium - 2-4 months'
            )
            recommendations.append(rec)
        
        # Debt optimization
        if metrics.debt_to_equity and metrics.debt_to_equity > 1.5:
            rec = Recommendation.objects.create(
                company=company,
                category='cost_optimization',
                priority='high',
                title='Optimize Debt Structure',
                description=f'Debt-to-equity ratio is {metrics.debt_to_equity}, indicating high leverage. Consider refinancing high-interest debt, extending payment terms, or raising equity to reduce interest burden.',
                estimated_impact=float(company.annual_revenue) * 0.04 if company.annual_revenue else None,
                implementation_effort='High - 6-12 months'
            )
            recommendations.append(rec)
        
        # Profitability improvement
        if metrics.net_margin and metrics.net_margin < 10:
            rec = Recommendation.objects.create(
                company=company,
                category='cost_optimization',
                priority='medium',
                title='Improve Net Profit Margin',
                description=f'Net margin is {metrics.net_margin}%. Review operating expenses, eliminate non-essential costs, automate processes, and focus on high-margin products/services.',
                estimated_impact=float(company.annual_revenue) * 0.06 if company.annual_revenue else None,
                implementation_effort='Medium - 3-6 months'
            )
            recommendations.append(rec)
        
        return recommendations
