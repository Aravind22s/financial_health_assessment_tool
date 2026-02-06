import React, { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { generateRecommendations, getRecommendations, getCompany } from '../services/api';

function RecommendationsPage() {
    const [searchParams] = useSearchParams();
    const companyId = searchParams.get('company');
    const [company, setCompany] = useState(null);
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(false);
    const [language, setLanguage] = useState('en');
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

            const recsRes = await getRecommendations(companyId);
            setRecommendations(recsRes.data.results || recsRes.data);
        } catch (error) {
            console.error('Error loading data:', error);
        }
    };

    const handleGenerate = async () => {
        setLoading(true);
        setMessage({ type: '', text: '' });

        try {
            const response = await generateRecommendations(companyId, language);
            setRecommendations(response.data);
            setMessage({ type: 'success', text: 'Recommendations generated successfully!' });
        } catch (error) {
            setMessage({ type: 'error', text: error.response?.data?.error || 'Error generating recommendations' });
        } finally {
            setLoading(false);
        }
    };

    const getPriorityIcon = (priority) => {
        if (priority === 'high') return '🔴';
        if (priority === 'medium') return '🟡';
        return '🟢';
    };

    const getCategoryIcon = (category) => {
        const icons = {
            cost_optimization: '💰',
            working_capital: '💵',
            financial_product: '🏦',
            compliance: '📋',
            general: '📊'
        };
        return icons[category] || '📊';
    };

    if (!companyId) {
        return (
            <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
                <h2 style={{ marginBottom: '16px' }}>No Company Selected</h2>
                <p style={{ color: '#6b7280', marginBottom: '24px' }}>Please select a company from the home page to view AI recommendations.</p>
                <Link to="/" className="btn btn-primary">Go to Home Page</Link>
            </div>
        );
    }

    return (
        <div>
            <div className="card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                        <h1>AI Recommendations - {company?.name}</h1>
                        <p style={{ color: '#6b7280' }}>Actionable insights to improve financial health</p>
                    </div>
                    <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                        <select
                            value={language}
                            onChange={(e) => setLanguage(e.target.value)}
                            style={{ padding: '8px 12px', borderRadius: '8px', border: '1px solid #d1d5db' }}
                        >
                            <option value="en">English</option>
                            <option value="hi">हिंदी</option>
                        </select>
                        <button className="btn btn-primary" onClick={handleGenerate} disabled={loading}>
                            {loading ? 'Generating...' : 'Generate Recommendations'}
                        </button>
                    </div>
                </div>
            </div>

            {message.text && (
                <div className={`alert alert-${message.type}`}>
                    {message.text}
                </div>
            )}

            {recommendations.length === 0 ? (
                <div className="card" style={{ textAlign: 'center', padding: '60px 20px' }}>
                    <h2 style={{ marginBottom: '16px' }}>No Recommendations Yet</h2>
                    <p style={{ color: '#6b7280', marginBottom: '24px' }}>
                        Generate AI-powered recommendations to optimize costs, improve working capital, and enhance financial health.
                    </p>
                </div>
            ) : (
                <>
                    <div className="card">
                        <h3 style={{ marginBottom: '16px' }}>Summary</h3>
                        <div className="grid" style={{ gridTemplateColumns: 'repeat(3, 1fr)' }}>
                            <div style={{ textAlign: 'center', padding: '20px', background: '#fef3c7', borderRadius: '8px' }}>
                                <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#92400e' }}>
                                    {recommendations.filter(r => r.priority === 'high').length}
                                </div>
                                <div style={{ color: '#78350f', marginTop: '4px' }}>High Priority</div>
                            </div>
                            <div style={{ textAlign: 'center', padding: '20px', background: '#dbeafe', borderRadius: '8px' }}>
                                <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#1e40af' }}>
                                    {recommendations.filter(r => r.priority === 'medium').length}
                                </div>
                                <div style={{ color: '#1e3a8a', marginTop: '4px' }}>Medium Priority</div>
                            </div>
                            <div style={{ textAlign: 'center', padding: '20px', background: '#d1fae5', borderRadius: '8px' }}>
                                <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#065f46' }}>
                                    {recommendations.filter(r => r.priority === 'low').length}
                                </div>
                                <div style={{ color: '#064e3b', marginTop: '4px' }}>Low Priority</div>
                            </div>
                        </div>
                    </div>

                    <div className="card">
                        <h3 style={{ marginBottom: '20px' }}>Recommendations</h3>
                        {recommendations.map((rec) => (
                            <div key={rec.id} className={`recommendation-card priority-${rec.priority}`}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '8px' }}>
                                    <h4 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                        <span>{getCategoryIcon(rec.category)}</span>
                                        {rec.title}
                                    </h4>
                                    <span style={{
                                        padding: '4px 12px',
                                        borderRadius: '12px',
                                        fontSize: '12px',
                                        fontWeight: '600',
                                        background: rec.priority === 'high' ? '#fee2e2' : rec.priority === 'medium' ? '#fef3c7' : '#d1fae5',
                                        color: rec.priority === 'high' ? '#991b1b' : rec.priority === 'medium' ? '#92400e' : '#065f46'
                                    }}>
                                        {getPriorityIcon(rec.priority)} {rec.priority.toUpperCase()}
                                    </span>
                                </div>
                                <p>{rec.description}</p>
                                {rec.estimated_impact && (
                                    <div style={{ marginTop: '12px', padding: '12px', background: 'white', borderRadius: '8px' }}>
                                        <strong>Estimated Impact:</strong> ₹{rec.estimated_impact.toLocaleString('en-IN')}
                                        {rec.implementation_effort && (
                                            <span style={{ marginLeft: '20px' }}>
                                                <strong>Effort:</strong> {rec.implementation_effort}
                                            </span>
                                        )}
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </>
            )}
        </div>
    );
}

export default RecommendationsPage;
