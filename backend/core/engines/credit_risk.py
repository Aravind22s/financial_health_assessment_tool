"""
Credit Risk Assessment Engine
Evaluates creditworthiness and generates risk scores
"""
from ..models import CreditAssessment


class CreditRiskEngine:
    """Engine for assessing credit risk and creditworthiness"""
    
    def assess_credit(self, company, metrics):
        """Perform comprehensive credit assessment"""
        
        # Calculate individual risk scores
        cash_flow_risk = self._assess_cash_flow_risk(metrics)
        debt_servicing_risk = self._assess_debt_servicing_risk(metrics)
        concentration_risk = self._assess_concentration_risk(company)
        compliance_risk = self._assess_compliance_risk(company)
        
        # Calculate overall credit score
        credit_score = self._calculate_credit_score(
            metrics, cash_flow_risk, debt_servicing_risk,
            concentration_risk, compliance_risk
        )
        
        # Determine credit rating
        credit_rating = self._determine_credit_rating(credit_score)
        
        # Calculate loan recommendations
        recommended_loan = self._calculate_recommended_loan(company, metrics, credit_score)
        recommended_tenure = self._calculate_recommended_tenure(credit_score)
        probability_of_stress = self._calculate_stress_probability(credit_score, metrics)
        
        # Identify risk factors
        risk_factors = self._identify_risk_factors(metrics, company)
        
        # Create assessment
        assessment = CreditAssessment.objects.create(
            company=company,
            metrics=metrics,
            credit_rating=credit_rating,
            credit_score=credit_score,
            cash_flow_risk=cash_flow_risk,
            debt_servicing_risk=debt_servicing_risk,
            concentration_risk=concentration_risk,
            compliance_risk=compliance_risk,
            recommended_loan_amount=recommended_loan,
            recommended_tenure_months=recommended_tenure,
            probability_of_stress=probability_of_stress,
            risk_factors=risk_factors
        )
        
        return assessment
    
    def _assess_cash_flow_risk(self, metrics):
        """Assess cash flow volatility risk (0-100, lower is better)"""
        risk = 50  # Base risk
        
        if metrics.cash_flow_stability:
            # Invert stability to get risk
            risk = 100 - metrics.cash_flow_stability
        
        # Adjust based on current ratio
        if metrics.current_ratio:
            if metrics.current_ratio < 1.0:
                risk += 20
            elif metrics.current_ratio > 2.0:
                risk -= 20
        
        return max(0, min(100, risk))
    
    def _assess_debt_servicing_risk(self, metrics):
        """Assess ability to service debt (0-100, lower is better)"""
        risk = 50
        
        # Interest coverage ratio
        if metrics.interest_coverage:
            if metrics.interest_coverage >= 5:
                risk = 10
            elif metrics.interest_coverage >= 3:
                risk = 30
            elif metrics.interest_coverage >= 1.5:
                risk = 50
            else:
                risk = 80
        
        # Debt to equity
        if metrics.debt_to_equity:
            if metrics.debt_to_equity > 3:
                risk += 20
            elif metrics.debt_to_equity > 2:
                risk += 10
        
        return max(0, min(100, risk))
    
    def _assess_concentration_risk(self, company):
        """Assess customer/supplier concentration risk"""
        # Simplified - would need additional data in production
        risk = 40  # Moderate default
        
        # Industry-based adjustments
        if company.industry in ['manufacturing', 'retail']:
            risk = 30  # Lower concentration typically
        elif company.industry in ['services']:
            risk = 50  # Higher concentration risk
        
        return risk
    
    def _assess_compliance_risk(self, company):
        """Assess tax and statutory compliance risk"""
        risk = 20  # Low default
        
        # Check if GST/PAN provided
        if not company.gst_number:
            risk += 30
        if not company.pan_number:
            risk += 20
        
        return min(100, risk)
    
    def _calculate_credit_score(self, metrics, cf_risk, debt_risk, conc_risk, comp_risk):
        """Calculate overall credit score (0-100)"""
        # Start with health score
        score = metrics.health_score if metrics.health_score else 50
        
        # Adjust based on risks (average of inverted risks)
        risk_adjustment = (
            (100 - cf_risk) * 0.3 +
            (100 - debt_risk) * 0.4 +
            (100 - conc_risk) * 0.15 +
            (100 - comp_risk) * 0.15
        )
        
        # Weighted combination
        final_score = (score * 0.6) + (risk_adjustment * 0.4)
        
        return int(min(100, max(0, final_score)))
    
    def _determine_credit_rating(self, credit_score):
        """Map credit score to rating band"""
        if credit_score >= 85:
            return 'AAA'
        elif credit_score >= 75:
            return 'AA'
        elif credit_score >= 65:
            return 'A'
        elif credit_score >= 55:
            return 'BBB'
        elif credit_score >= 45:
            return 'BB'
        elif credit_score >= 35:
            return 'B'
        else:
            return 'C'
    
    def _calculate_recommended_loan(self, company, metrics, credit_score):
        """Calculate recommended loan amount"""
        # Base on annual revenue and credit score
        if company.annual_revenue:
            base_amount = float(company.annual_revenue) * 0.25  # 25% of revenue
            
            # Adjust based on credit score
            if credit_score >= 75:
                multiplier = 1.5
            elif credit_score >= 60:
                multiplier = 1.0
            elif credit_score >= 45:
                multiplier = 0.5
            else:
                multiplier = 0.25
            
            return round(base_amount * multiplier, 2)
        
        return None
    
    def _calculate_recommended_tenure(self, credit_score):
        """Calculate recommended loan tenure in months"""
        if credit_score >= 75:
            return 36  # 3 years
        elif credit_score >= 60:
            return 24  # 2 years
        elif credit_score >= 45:
            return 12  # 1 year
        else:
            return 6   # 6 months
    
    def _calculate_stress_probability(self, credit_score, metrics):
        """Calculate probability of financial stress"""
        # Inverse of credit score
        base_prob = (100 - credit_score) / 100
        
        # Adjust based on liquidity
        if metrics.current_ratio and metrics.current_ratio < 1.0:
            base_prob += 0.2
        
        return round(min(1.0, base_prob) * 100, 2)
    
    def _identify_risk_factors(self, metrics, company):
        """Identify specific risk factors"""
        factors = []
        
        if metrics.current_ratio and metrics.current_ratio < 1.0:
            factors.append("Low liquidity - current ratio below 1.0")
        
        if metrics.debt_to_equity and metrics.debt_to_equity > 2.0:
            factors.append("High leverage - debt to equity above 2.0")
        
        if metrics.net_margin and metrics.net_margin < 5:
            factors.append("Low profitability - net margin below 5%")
        
        if metrics.receivables_days and metrics.receivables_days > 90:
            factors.append("Slow collections - receivables over 90 days")
        
        if not company.gst_number:
            factors.append("GST registration not provided")
        
        return factors
