import React, { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { assessCredit, getCreditAssessments, getCompany } from '../services/api';

function CreditPage() {
    const [searchParams] = useSearchParams();
    const companyId = searchParams.get('company');
    const [company, setCompany] = useState(null);
    const [assessment, setAssessment] = useState(null);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState({ type: '', text: '' });

    useEffect(() => {
        if (companyId) {
            loadData();
        }
    }, [companyId]);

    const loadData = async () => {
        try {
            const companyRes = await getCompany(companyId);
            setCompany(companyRes.data);

            const assessmentRes = await getCreditAssessments(companyId);
            if (assessmentRes.data.results && assessmentRes.data.results.length > 0) {
                setAssessment(assessmentRes.data.results[0]);
            } else if (assessmentRes.data.length > 0) {
                setAssessment(assessmentRes.data[0]);
            }
        } catch (error) {
            console.error('Error loading data:', error);
        }
    };

    const handleAssess = async () => {
        setLoading(true);
        setMessage({ type: '', text: '' });

        try {
            const response = await assessCredit(companyId);
            setAssessment(response.data);
            setMessage({ type: 'success', text: 'Credit assessment completed successfully!' });
        } catch (error) {
            setMessage({ type: 'error', text: error.response?.data?.error || 'Error performing assessment' });
        } finally {
            setLoading(false);
        }
    };

    const getRatingColor = (rating) => {
        if (rating.startsWith('A')) return '#10b981';
        if (rating.startsWith('B')) return '#f59e0b';
        return '#ef4444';
    };

    const getRiskColor = (risk) => {
        if (risk < 30) return '#10b981';
        if (risk < 60) return '#f59e0b';
        return '#ef4444';
    };

    if (!companyId) {
        return (
            <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
                <h2 style={{ marginBottom: '16px' }}>No Company Selected</h2>
                <p style={{ color: '#6b7280', marginBottom: '24px' }}>Please select a company from the home page to view the credit assessment.</p>
                <Link to="/" className="btn btn-primary">Go to Home Page</Link>
            </div>
        );
    }

    return (
        <div>
            <div className="card">
                <h1>Credit Assessment - {company?.name}</h1>
                <p style={{ color: '#6b7280' }}>Evaluate creditworthiness and get loan recommendations</p>
            </div>

            {message.text && (
                <div className={`alert alert-${message.type}`}>
                    {message.text}
                </div>
            )}

            {!assessment && (
                <div className="card" style={{ textAlign: 'center', padding: '60px 20px' }}>
                    <h2 style={{ marginBottom: '16px' }}>No Credit Assessment Found</h2>
                    <p style={{ color: '#6b7280', marginBottom: '24px' }}>
                        Generate a credit assessment to evaluate creditworthiness and get loan recommendations.
                    </p>
                    <button className="btn btn-primary" onClick={handleAssess} disabled={loading}>
                        {loading ? 'Assessing...' : 'Generate Credit Assessment'}
                    </button>
                </div>
            )}

            {assessment && (
                <>
                    <div className="grid">
                        <div className="card" style={{ textAlign: 'center', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
                            <h3 style={{ opacity: 0.9, marginBottom: '12px' }}>Credit Rating</h3>
                            <div style={{ fontSize: '48px', fontWeight: 'bold', marginBottom: '8px' }}>
                                {assessment.credit_rating}
                            </div>
                            <p style={{ opacity: 0.9 }}>Score: {assessment.credit_score}/100</p>
                        </div>

                        <div className="card">
                            <h3 style={{ marginBottom: '16px' }}>Loan Recommendations</h3>
                            <div style={{ display: 'grid', gap: '12px' }}>
                                <div>
                                    <strong>Recommended Amount:</strong>
                                    <div style={{ fontSize: '24px', color: '#667eea', fontWeight: '600', marginTop: '4px' }}>
                                        ₹{assessment.recommended_loan_amount?.toLocaleString('en-IN') || 'N/A'}
                                    </div>
                                </div>
                                <div>
                                    <strong>Recommended Tenure:</strong>
                                    <div style={{ fontSize: '20px', color: '#667eea', marginTop: '4px' }}>
                                        {assessment.recommended_tenure_months} months
                                    </div>
                                </div>
                                <div>
                                    <strong>Stress Probability:</strong>
                                    <div style={{ fontSize: '20px', color: getRiskColor(assessment.probability_of_stress), marginTop: '4px' }}>
                                        {assessment.probability_of_stress}%
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="card">
                        <h3 style={{ marginBottom: '16px' }}>Risk Analysis</h3>
                        <div className="grid">
                            <div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                                    <span>Cash Flow Risk</span>
                                    <span style={{ fontWeight: '600', color: getRiskColor(assessment.cash_flow_risk) }}>
                                        {assessment.cash_flow_risk}/100
                                    </span>
                                </div>
                                <div style={{ background: '#e5e7eb', borderRadius: '8px', height: '8px', overflow: 'hidden' }}>
                                    <div style={{
                                        width: `${assessment.cash_flow_risk}%`,
                                        height: '100%',
                                        background: getRiskColor(assessment.cash_flow_risk),
                                        transition: 'width 0.3s ease'
                                    }}></div>
                                </div>
                            </div>

                            <div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                                    <span>Debt Servicing Risk</span>
                                    <span style={{ fontWeight: '600', color: getRiskColor(assessment.debt_servicing_risk) }}>
                                        {assessment.debt_servicing_risk}/100
                                    </span>
                                </div>
                                <div style={{ background: '#e5e7eb', borderRadius: '8px', height: '8px', overflow: 'hidden' }}>
                                    <div style={{
                                        width: `${assessment.debt_servicing_risk}%`,
                                        height: '100%',
                                        background: getRiskColor(assessment.debt_servicing_risk),
                                        transition: 'width 0.3s ease'
                                    }}></div>
                                </div>
                            </div>

                            <div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                                    <span>Concentration Risk</span>
                                    <span style={{ fontWeight: '600', color: getRiskColor(assessment.concentration_risk) }}>
                                        {assessment.concentration_risk}/100
                                    </span>
                                </div>
                                <div style={{ background: '#e5e7eb', borderRadius: '8px', height: '8px', overflow: 'hidden' }}>
                                    <div style={{
                                        width: `${assessment.concentration_risk}%`,
                                        height: '100%',
                                        background: getRiskColor(assessment.concentration_risk),
                                        transition: 'width 0.3s ease'
                                    }}></div>
                                </div>
                            </div>

                            <div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                                    <span>Compliance Risk</span>
                                    <span style={{ fontWeight: '600', color: getRiskColor(assessment.compliance_risk) }}>
                                        {assessment.compliance_risk}/100
                                    </span>
                                </div>
                                <div style={{ background: '#e5e7eb', borderRadius: '8px', height: '8px', overflow: 'hidden' }}>
                                    <div style={{
                                        width: `${assessment.compliance_risk}%`,
                                        height: '100%',
                                        background: getRiskColor(assessment.compliance_risk),
                                        transition: 'width 0.3s ease'
                                    }}></div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {assessment.risk_factors && assessment.risk_factors.length > 0 && (
                        <div className="card">
                            <h3 style={{ marginBottom: '16px' }}>Identified Risk Factors</h3>
                            <ul style={{ color: '#6b7280', lineHeight: '1.8' }}>
                                {assessment.risk_factors.map((factor, index) => (
                                    <li key={index}>{factor}</li>
                                ))}
                            </ul>
                        </div>
                    )}

                    <div className="card" style={{ textAlign: 'center' }}>
                        <button className="btn btn-primary" onClick={handleAssess} disabled={loading}>
                            {loading ? 'Reassessing...' : 'Refresh Assessment'}
                        </button>
                    </div>
                </>
            )}
        </div>
    );
}

export default CreditPage;
