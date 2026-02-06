"""
Financial Forecasting Engine
Generates revenue, expense, and cash flow forecasts
"""
from ..models import Forecast
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json


class ForecastingEngine:
    """Engine for financial forecasting and scenario planning"""
    
    def generate_forecasts(self, company, months=12):
        """Generate forecasts for all scenarios"""
        forecasts = []
        
        # Get historical data
        historical_data = self._get_historical_data(company)
        
        # Generate for each scenario
        for scenario in ['best', 'base', 'worst']:
            forecast = self._generate_scenario_forecast(
                company, historical_data, months, scenario
            )
            forecasts.append(forecast)
        
        return forecasts
    
    def _get_historical_data(self, company):
        """Extract historical financial data"""
        from ..models import FinancialData
        
        historical = {
            'revenue': [],
            'expenses': [],
            'growth_rate': 0
        }
        
        # Get recent financial data
        recent_data = FinancialData.objects.filter(
            company=company,
            processed=True
        ).order_by('-period_end')[:12]
        
        for data in recent_data:
            if data.raw_data:
                income_stmt = data.raw_data.get('income_statement', {})
                
                # Extract revenue
                revenue = self._extract_revenue(income_stmt)
                if revenue:
                    historical['revenue'].append(revenue)
                
                # Extract expenses
                expenses = self._extract_expenses(income_stmt)
                if expenses:
                    historical['expenses'].append(expenses)
        
        # Calculate average growth rate
        if len(historical['revenue']) >= 2:
            recent_rev = historical['revenue'][0]
            old_rev = historical['revenue'][-1]
            periods = len(historical['revenue'])
            historical['growth_rate'] = ((recent_rev / old_rev) ** (1/periods) - 1) * 100
        
        return historical
    
    def _extract_revenue(self, income_statement):
        """Extract total revenue from income statement"""
        for key, value in income_statement.items():
            if any(term in key.lower() for term in ['revenue', 'sales', 'turnover']):
                try:
                    return float(value)
                except:
                    pass
        return None
    
    def _extract_expenses(self, income_statement):
        """Extract total expenses from income statement"""
        total = 0
        for key, value in income_statement.items():
            if any(term in key.lower() for term in ['expense', 'cost', 'expenditure']):
                try:
                    total += float(value)
                except:
                    pass
        return total if total > 0 else None
    
    def _generate_scenario_forecast(self, company, historical, months, scenario):
        """Generate forecast for a specific scenario"""
        # Determine growth rates based on scenario
        if scenario == 'best':
            revenue_growth = (historical.get('growth_rate', 10) + 5) / 100
            expense_growth = (historical.get('growth_rate', 10) - 2) / 100
        elif scenario == 'base':
            revenue_growth = historical.get('growth_rate', 10) / 100
            expense_growth = historical.get('growth_rate', 10) / 100
        else:  # worst
            revenue_growth = (historical.get('growth_rate', 10) - 5) / 100
            expense_growth = (historical.get('growth_rate', 10) + 3) / 100
        
        # Get base values
        base_revenue = historical['revenue'][0] if historical['revenue'] else float(company.annual_revenue or 1000000)
        base_expenses = historical['expenses'][0] if historical['expenses'] else base_revenue * 0.7
        
        # Generate monthly projections
        revenue_forecast = []
        expense_forecast = []
        cash_flow_forecast = []
        
        current_date = datetime.now()
        monthly_revenue = base_revenue / 12
        monthly_expenses = base_expenses / 12
        
        for i in range(months):
            month_date = current_date + relativedelta(months=i)
            
            # Apply growth
            projected_revenue = monthly_revenue * ((1 + revenue_growth/12) ** i)
            projected_expenses = monthly_expenses * ((1 + expense_growth/12) ** i)
            projected_cash_flow = projected_revenue - projected_expenses
            
            revenue_forecast.append({
                'month': month_date.strftime('%Y-%m'),
                'value': round(projected_revenue, 2)
            })
            
            expense_forecast.append({
                'month': month_date.strftime('%Y-%m'),
                'value': round(projected_expenses, 2)
            })
            
            cash_flow_forecast.append({
                'month': month_date.strftime('%Y-%m'),
                'value': round(projected_cash_flow, 2)
            })
        
        # Create assumptions text
        assumptions = self._generate_assumptions(scenario, revenue_growth, expense_growth, company.industry)
        
        # Create forecast object
        forecast = Forecast.objects.create(
            company=company,
            scenario=scenario,
            forecast_months=months,
            revenue_forecast=revenue_forecast,
            expense_forecast=expense_forecast,
            cash_flow_forecast=cash_flow_forecast,
            assumptions=assumptions
        )
        
        return forecast
    
    def _generate_assumptions(self, scenario, revenue_growth, expense_growth, industry):
        """Generate assumptions text for the forecast"""
        assumptions = f"""
Forecast Scenario: {scenario.upper()}

Key Assumptions:
- Revenue Growth Rate: {revenue_growth*100:.1f}% annually
- Expense Growth Rate: {expense_growth*100:.1f}% annually
- Industry: {industry}
- Seasonality: Not factored (uniform monthly distribution)
- External Factors: Stable economic conditions assumed

Scenario Details:
"""
        
        if scenario == 'best':
            assumptions += """
- Strong market demand
- Successful new product launches
- Improved operational efficiency
- Favorable market conditions
"""
        elif scenario == 'base':
            assumptions += """
- Steady market conditions
- Consistent operational performance
- Normal competitive environment
- No major disruptions
"""
        else:  # worst
            assumptions += """
- Market headwinds
- Increased competition
- Rising input costs
- Potential operational challenges
"""
        
        return assumptions.strip()
