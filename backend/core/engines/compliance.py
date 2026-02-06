"""
Compliance Monitoring Engine
Checks tax and statutory compliance
"""
from ..models import Recommendation


class ComplianceEngine:
    """Engine for monitoring tax and compliance"""
    
    def check_compliance(self, company):
        """Check compliance status and generate alerts"""
        issues = []
        
        # GST compliance
        if not company.gst_number:
            issues.append({
                'type': 'GST',
                'severity': 'high',
                'message': 'GST registration number not provided'
            })
        
        # PAN compliance
        if not company.pan_number:
            issues.append({
                'type': 'PAN',
                'severity': 'medium',
                'message': 'PAN number not provided'
            })
        
        # Company registration
        if not company.registration_number:
            issues.append({
                'type': 'Registration',
                'severity': 'medium',
                'message': 'Company registration number not provided'
            })
        
        return issues
    
    def generate_compliance_recommendations(self, company):
        """Generate compliance-related recommendations"""
        recommendations = []
        issues = self.check_compliance(company)
        
        for issue in issues:
            if issue['type'] == 'GST':
                rec = Recommendation.objects.create(
                    company=company,
                    category='compliance',
                    priority='high',
                    title='Complete GST Registration',
                    description='GST registration is mandatory for businesses with turnover above ₹40 lakhs (₹20 lakhs for services). Ensure compliance to avoid penalties.',
                    estimated_impact=None,
                    implementation_effort='Low - 1-2 weeks'
                )
                recommendations.append(rec)
        
        return recommendations
