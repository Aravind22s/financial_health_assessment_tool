"""
Financial Health Assessment Engine
Calculates financial ratios and overall health score
"""
from decimal import Decimal
from ..models import FinancialMetrics, IndustryBenchmark


class FinancialHealthEngine:
    """Engine for calculating financial health metrics"""
    
    def calculate_metrics(self, financial_data):
        """Calculate all financial metrics from raw data"""
        raw_data = financial_data.raw_data
        balance_sheet = raw_data.get('balance_sheet', {})
        income_statement = raw_data.get('income_statement', {})
        cash_flow = raw_data.get('cash_flow', {})
        
        # Extract key values
        values = self._extract_values(balance_sheet, income_statement, cash_flow)
        
        # Calculate ratios
        metrics = FinancialMetrics.objects.create(
            company=financial_data.company,
            financial_data=financial_data,
            current_ratio=self._calculate_current_ratio(values),
            quick_ratio=self._calculate_quick_ratio(values),
            gross_margin=self._calculate_gross_margin(values),
            net_margin=self._calculate_net_margin(values),
            roa=self._calculate_roa(values),
            roe=self._calculate_roe(values),
            inventory_turnover=self._calculate_inventory_turnover(values),
            receivables_days=self._calculate_receivables_days(values),
            payables_days=self._calculate_payables_days(values),
            debt_to_equity=self._calculate_debt_to_equity(values),
            interest_coverage=self._calculate_interest_coverage(values),
            cash_flow_stability=self._calculate_cash_flow_stability(values),
            cash_conversion_cycle=self._calculate_cash_conversion_cycle(values),
        )
        
        # Calculate overall health score
        metrics.health_score = self._calculate_health_score(metrics, financial_data.company.industry)
        metrics.save()
        
        return metrics
    
    def _extract_values(self, balance_sheet, income_statement, cash_flow):
        """Extract and sum relevant values from financial statements"""
        values = {}
        
        # Balance Sheet
        values['current_assets'] = self._sum_matching(balance_sheet, ['current asset', 'cash', 'receivable', 'inventory'])
        values['inventory'] = self._sum_matching(balance_sheet, ['inventory'])
        values['current_liabilities'] = self._sum_matching(balance_sheet, ['current liab', 'payable'])
        values['total_assets'] = self._sum_matching(balance_sheet, ['total asset']) or values['current_assets']
        values['total_liabilities'] = self._sum_matching(balance_sheet, ['total liab', 'debt', 'loan'])
        values['equity'] = self._sum_matching(balance_sheet, ['equity', 'capital'])
        values['receivables'] = self._sum_matching(balance_sheet, ['receivable', 'debtors'])
        values['payables'] = self._sum_matching(balance_sheet, ['payable', 'creditors'])
        
        # Income Statement
        values['revenue'] = self._sum_matching(income_statement, ['revenue', 'sales', 'turnover'])
        values['cogs'] = self._sum_matching(income_statement, ['cost of goods', 'cogs', 'cost of sales'])
        values['gross_profit'] = self._sum_matching(income_statement, ['gross profit'])
        values['net_income'] = self._sum_matching(income_statement, ['net income', 'net profit', 'profit after tax'])
        values['operating_income'] = self._sum_matching(income_statement, ['operating income', 'ebit'])
        values['interest_expense'] = self._sum_matching(income_statement, ['interest expense', 'interest paid'])
        
        # Derived values
        if not values['gross_profit'] and values['revenue'] and values['cogs']:
            values['gross_profit'] = values['revenue'] - values['cogs']
        
        if not values['equity'] and values['total_assets'] and values['total_liabilities']:
            values['equity'] = values['total_assets'] - values['total_liabilities']
        
        return values
    
    def _sum_matching(self, data_dict, keywords):
        """Sum values from dictionary where keys match keywords"""
        total = 0
        for key, value in data_dict.items():
            key_lower = key.lower()
            if any(keyword in key_lower for keyword in keywords):
                try:
                    total += float(value)
                except:
                    pass
        return total if total > 0 else None
    
    def _calculate_current_ratio(self, values):
        """Current Assets / Current Liabilities"""
        current_assets = values.get('current_assets') or 0
        current_liabilities = values.get('current_liabilities') or 0
        if current_liabilities > 0:
            return round(float(current_assets) / float(current_liabilities), 2)
        return None
    
    def _calculate_quick_ratio(self, values):
        """(Current Assets - Inventory) / Current Liabilities"""
        current_assets = values.get('current_assets') or 0
        inventory = values.get('inventory') or 0
        current_liabilities = values.get('current_liabilities') or 0
        if current_liabilities > 0:
            quick_assets = float(current_assets) - float(inventory)
            return round(quick_assets / float(current_liabilities), 2)
        return None
    
    def _calculate_gross_margin(self, values):
        """(Gross Profit / Revenue) * 100"""
        revenue = values.get('revenue') or 0
        gross_profit = values.get('gross_profit') or 0
        if revenue > 0:
            return round((float(gross_profit) / float(revenue)) * 100, 2)
        return None
    
    def _calculate_net_margin(self, values):
        """(Net Income / Revenue) * 100"""
        revenue = values.get('revenue') or 0
        net_income = values.get('net_income') or 0
        if revenue > 0:
            return round((float(net_income) / float(revenue)) * 100, 2)
        return None
    
    def _calculate_roa(self, values):
        """(Net Income / Total Assets) * 100"""
        total_assets = values.get('total_assets') or 0
        net_income = values.get('net_income') or 0
        if total_assets > 0:
            return round((float(net_income) / float(total_assets)) * 100, 2)
        return None
    
    def _calculate_roe(self, values):
        """(Net Income / Equity) * 100"""
        equity = values.get('equity') or 0
        net_income = values.get('net_income') or 0
        if equity > 0:
            return round((float(net_income) / float(equity)) * 100, 2)
        return None
    
    def _calculate_inventory_turnover(self, values):
        """COGS / Average Inventory"""
        inventory = values.get('inventory') or 0
        cogs = values.get('cogs') or 0
        if inventory > 0:
            return round(float(cogs) / float(inventory), 2)
        return None
    
    def _calculate_receivables_days(self, values):
        """(Receivables / Revenue) * 365"""
        revenue = values.get('revenue') or 0
        receivables = values.get('receivables') or 0
        if revenue > 0:
            return round((float(receivables) / float(revenue)) * 365, 2)
        return None
    
    def _calculate_payables_days(self, values):
        """(Payables / COGS) * 365"""
        cogs = values.get('cogs') or 0
        payables = values.get('payables') or 0
        if cogs > 0:
            return round((float(payables) / float(cogs)) * 365, 2)
        return None
    
    def _calculate_debt_to_equity(self, values):
        """Total Liabilities / Equity"""
        equity = values.get('equity') or 0
        liabilities = values.get('total_liabilities') or 0
        if equity > 0:
            return round(float(liabilities) / float(equity), 2)
        return None
    
    def _calculate_interest_coverage(self, values):
        """Operating Income / Interest Expense"""
        interest_expense = values.get('interest_expense') or 0
        operating_income = values.get('operating_income') or 0
        if interest_expense > 0:
            return round(float(operating_income) / float(interest_expense), 2)
        return None
    
    def _calculate_cash_flow_stability(self, values):
        """Simplified cash flow stability score (0-100)"""
        # This is a simplified version - in production, would analyze historical cash flows
        score = 50  # Base score
        
        net_income = values.get('net_income') or 0
        if net_income > 0:
            score += 20
        
        current_ratio = self._calculate_current_ratio(values)
        if current_ratio and current_ratio > 1.5:
            score += 15
        elif current_ratio and current_ratio > 1.0:
            score += 10
        
        return min(score, 100)
    
    def _calculate_cash_conversion_cycle(self, values):
        """Receivables Days + Inventory Days - Payables Days"""
        receivables_days = self._calculate_receivables_days(values) or 0
        inventory_turnover = self._calculate_inventory_turnover(values)
        inventory_days = (365 / inventory_turnover) if inventory_turnover and inventory_turnover > 0 else 0
        payables_days = self._calculate_payables_days(values) or 0
        
        return round(receivables_days + inventory_days - payables_days, 2)
    
    def _calculate_health_score(self, metrics, industry):
        """Calculate overall financial health score (0-100)"""
        score = 0
        weights = {
            'liquidity': 20,
            'profitability': 30,
            'efficiency': 20,
            'solvency': 20,
            'cash_flow': 10
        }
        
        # Get industry benchmark
        try:
            benchmark = IndustryBenchmark.objects.get(industry=industry)
        except IndustryBenchmark.DoesNotExist:
            benchmark = None
        
        # Liquidity Score
        liquidity_score = 0
        if metrics.current_ratio:
            if metrics.current_ratio >= 2.0:
                liquidity_score = 100
            elif metrics.current_ratio >= 1.5:
                liquidity_score = 80
            elif metrics.current_ratio >= 1.0:
                liquidity_score = 60
            else:
                liquidity_score = 40
        score += (liquidity_score * weights['liquidity']) / 100
        
        # Profitability Score
        profitability_score = 0
        if metrics.net_margin:
            if benchmark and benchmark.avg_net_margin:
                if metrics.net_margin >= benchmark.avg_net_margin:
                    profitability_score = 100
                else:
                    profitability_score = min((metrics.net_margin / benchmark.avg_net_margin) * 100, 100)
            else:
                # Without benchmark
                if metrics.net_margin >= 15:
                    profitability_score = 100
                elif metrics.net_margin >= 10:
                    profitability_score = 80
                elif metrics.net_margin >= 5:
                    profitability_score = 60
                else:
                    profitability_score = 40
        score += (profitability_score * weights['profitability']) / 100
        
        # Efficiency Score
        efficiency_score = 50  # Default
        if metrics.receivables_days:
            if metrics.receivables_days <= 30:
                efficiency_score = 100
            elif metrics.receivables_days <= 60:
                efficiency_score = 70
            elif metrics.receivables_days <= 90:
                efficiency_score = 50
            else:
                efficiency_score = 30
        score += (efficiency_score * weights['efficiency']) / 100
        
        # Solvency Score
        solvency_score = 50
        if metrics.debt_to_equity:
            if metrics.debt_to_equity <= 0.5:
                solvency_score = 100
            elif metrics.debt_to_equity <= 1.0:
                solvency_score = 80
            elif metrics.debt_to_equity <= 2.0:
                solvency_score = 60
            else:
                solvency_score = 40
        score += (solvency_score * weights['solvency']) / 100
        
        # Cash Flow Score
        if metrics.cash_flow_stability:
            score += (metrics.cash_flow_stability * weights['cash_flow']) / 100
        
        return int(min(score, 100))
