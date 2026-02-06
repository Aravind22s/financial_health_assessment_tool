import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getCompanies } from '../services/api';

function HomePage() {
    const [companies, setCompanies] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadCompanies();
    }, []);

    const loadCompanies = async () => {
        try {
            const response = await getCompanies();
            setCompanies(response.data.results || response.data);
            setLoading(false);
        } catch (error) {
            console.error('Error loading companies:', error);
            setLoading(false);
        }
    };

    return (
        <div>
            <div className="card" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
                <h1 style={{ fontSize: '36px', marginBottom: '16px' }}>SME Financial Health Platform</h1>
                <p style={{ fontSize: '18px', opacity: 0.9 }}>
                    AI-driven financial analysis and insights for small and medium enterprises
                </p>
            </div>

            <div className="grid" style={{ gridTemplateColumns: 'repeat(3, 1fr)' }}>
                <div className="stat-card">
                    <h3>Financial Health Assessment</h3>
                    <p style={{ marginTop: '12px', opacity: 0.9 }}>
                        Comprehensive analysis of liquidity, profitability, and solvency
                    </p>
                </div>
                <div className="stat-card" style={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' }}>
                    <h3>Credit Risk Evaluation</h3>
                    <p style={{ marginTop: '12px', opacity: 0.9 }}>
                        Creditworthiness assessment and loan recommendations
                    </p>
                </div>
                <div className="stat-card" style={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' }}>
                    <h3>AI-Powered Insights</h3>
                    <p style={{ marginTop: '12px', opacity: 0.9 }}>
                        Multilingual recommendations and forecasting
                    </p>
                </div>
            </div>

            <div className="card">
                <h2 style={{ marginBottom: '20px' }}>Your Companies</h2>
                {loading ? (
                    <div className="loading">Loading companies...</div>
                ) : companies.length > 0 ? (
                    <div>
                        {companies.map((company) => (
                            <div key={company.id} style={{
                                padding: '16px',
                                background: '#f9fafb',
                                borderRadius: '8px',
                                marginBottom: '12px',
                                display: 'flex',
                                justifyContent: 'space-between',
                                alignItems: 'center'
                            }}>
                                <div>
                                    <h3 style={{ color: '#1f2937' }}>{company.name}</h3>
                                    <p style={{ color: '#6b7280', marginTop: '4px' }}>{company.industry}</p>
                                </div>
                                <Link to={`/dashboard?company=${company.id}`}>
                                    <button className="btn btn-primary">View Dashboard</button>
                                </Link>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div style={{ textAlign: 'center', padding: '40px' }}>
                        <p style={{ color: '#6b7280', marginBottom: '20px' }}>No companies found. Upload financial data to get started.</p>
                        <Link to="/upload">
                            <button className="btn btn-primary">Upload Financial Data</button>
                        </Link>
                    </div>
                )}
            </div>

            <div className="card">
                <h2 style={{ marginBottom: '16px' }}>Features</h2>
                <div className="grid">
                    <div>
                        <h3 style={{ color: '#667eea', marginBottom: '8px' }}>📊 Financial Analysis</h3>
                        <p style={{ color: '#6b7280' }}>Automated calculation of key financial ratios and health scores</p>
                    </div>
                    <div>
                        <h3 style={{ color: '#667eea', marginBottom: '8px' }}>💰 Cost Optimization</h3>
                        <p style={{ color: '#6b7280' }}>AI-powered recommendations to reduce costs and improve margins</p>
                    </div>
                    <div>
                        <h3 style={{ color: '#667eea', marginBottom: '8px' }}>📈 Forecasting</h3>
                        <p style={{ color: '#6b7280' }}>Revenue and cash flow projections with scenario planning</p>
                    </div>
                    <div>
                        <h3 style={{ color: '#667eea', marginBottom: '8px' }}>🏦 Credit Assessment</h3>
                        <p style={{ color: '#6b7280' }}>Creditworthiness evaluation and loan recommendations</p>
                    </div>
                    <div>
                        <h3 style={{ color: '#667eea', marginBottom: '8px' }}>📑 Reports</h3>
                        <p style={{ color: '#6b7280' }}>Investor-ready PDF reports in multiple languages</p>
                    </div>
                    <div>
                        <h3 style={{ color: '#667eea', marginBottom: '8px' }}>🌐 Multilingual</h3>
                        <p style={{ color: '#6b7280' }}>Support for English and Hindi with simple explanations</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default HomePage;
