import React, { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { getLatestMetrics, getCompany } from '../services/api';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from 'chart.js';
import { Doughnut, Bar } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

function DashboardPage() {
    const [searchParams] = useSearchParams();
    const companyId = searchParams.get('company');
    const [company, setCompany] = useState(null);
    const [metrics, setMetrics] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (companyId) {
            loadData();
        }
    }, [companyId]);

    const loadData = async () => {
        try {
            const [companyRes, metricsRes] = await Promise.all([
                getCompany(companyId),
                getLatestMetrics(companyId)
            ]);
            setCompany(companyRes.data);
            setMetrics(metricsRes.data);
            setLoading(false);
        } catch (error) {
            console.error('Error loading data:', error);
            setLoading(false);
        }
    };

    const getScoreClass = (score) => {
        if (score >= 75) return 'score-excellent';
        if (score >= 60) return 'score-good';
        if (score >= 45) return 'score-moderate';
        return 'score-poor';
    };

    const getScoreLabel = (score) => {
        if (score >= 75) return 'Excellent';
        if (score >= 60) return 'Good';
        if (score >= 45) return 'Moderate';
        return 'Needs Attention';
    };

    const safeFormat = (value, decimals = 2) => {
        const num = parseFloat(value);
        return !isNaN(num) ? num.toFixed(decimals) : 'N/A';
    };

    if (!companyId) {
        return (
            <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
                <h2 style={{ marginBottom: '16px' }}>No Company Selected</h2>
                <p style={{ color: '#6b7280', marginBottom: '24px' }}>Please select a company from the home page to view the dashboard.</p>
                <Link to="/" className="btn btn-primary">Go to Home Page</Link>
            </div>
        );
    }

    if (loading) {
        return <div className="loading">Loading dashboard...</div>;
    }

    if (!metrics) {
        return (
            <div className="card">
                <h2>No Financial Data</h2>
                <p>Please upload financial data for this company first.</p>
            </div>
        );
    }

    const healthScoreData = {
        labels: ['Score', 'Remaining'],
        datasets: [{
            data: [metrics.health_score, 100 - metrics.health_score],
            backgroundColor: ['#667eea', '#e5e7eb'],
            borderWidth: 0,
        }]
    };

    const ratiosData = {
        labels: ['Current Ratio', 'Quick Ratio', 'Debt/Equity', 'Interest Coverage'],
        datasets: [{
            label: 'Financial Ratios',
            data: [
                metrics.current_ratio || 0,
                metrics.quick_ratio || 0,
                metrics.debt_to_equity || 0,
                metrics.interest_coverage || 0
            ],
            backgroundColor: ['#667eea', '#764ba2', '#f093fb', '#4facfe'],
        }]
    };

    return (
        <div>
            <div className="card">
                <h1>{company?.name} - Financial Dashboard</h1>
                <p style={{ color: '#6b7280' }}>{company?.industry}</p>
            </div>

            <div className="grid">
                <div className="card" style={{ textAlign: 'center' }}>
                    <h3 style={{ marginBottom: '20px' }}>Overall Health Score</h3>
                    <div style={{ maxWidth: '200px', margin: '0 auto' }}>
                        <Doughnut data={healthScoreData} options={{ cutout: '70%' }} />
                    </div>
                    <div style={{ marginTop: '20px' }}>
                        <span className={`score-badge ${getScoreClass(metrics.health_score)}`}>
                            {metrics.health_score}/100
                        </span>
                        <p style={{ marginTop: '8px', color: '#6b7280' }}>{getScoreLabel(metrics.health_score)}</p>
                    </div>
                </div>

                <div className="card">
                    <h3 style={{ marginBottom: '16px' }}>Key Metrics</h3>
                    <div style={{ display: 'grid', gap: '12px' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px', background: '#f9fafb', borderRadius: '8px' }}>
                            <span style={{ fontWeight: '500' }}>Current Ratio</span>
                            <span style={{ color: '#667eea', fontWeight: '600' }}>{safeFormat(metrics.current_ratio)}</span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px', background: '#f9fafb', borderRadius: '8px' }}>
                            <span style={{ fontWeight: '500' }}>Quick Ratio</span>
                            <span style={{ color: '#667eea', fontWeight: '600' }}>{safeFormat(metrics.quick_ratio)}</span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px', background: '#f9fafb', borderRadius: '8px' }}>
                            <span style={{ fontWeight: '500' }}>Gross Margin</span>
                            <span style={{ color: '#667eea', fontWeight: '600' }}>{safeFormat(metrics.gross_margin)}%</span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px', background: '#f9fafb', borderRadius: '8px' }}>
                            <span style={{ fontWeight: '500' }}>Net Margin</span>
                            <span style={{ color: '#667eea', fontWeight: '600' }}>{safeFormat(metrics.net_margin)}%</span>
                        </div>
                    </div>
                </div>
            </div>

            <div className="card">
                <h3 style={{ marginBottom: '20px' }}>Financial Ratios Comparison</h3>
                <Bar data={ratiosData} options={{ responsive: true, plugins: { legend: { display: false } } }} />
            </div>

            <div className="grid">
                <div className="card">
                    <h3 style={{ marginBottom: '12px' }}>Profitability</h3>
                    <div style={{ display: 'grid', gap: '8px' }}>
                        <div><strong>ROA:</strong> {safeFormat(metrics.roa)}%</div>
                        <div><strong>ROE:</strong> {safeFormat(metrics.roe)}%</div>
                        <div><strong>Gross Margin:</strong> {safeFormat(metrics.gross_margin)}%</div>
                        <div><strong>Net Margin:</strong> {safeFormat(metrics.net_margin)}%</div>
                    </div>
                </div>

                <div className="card">
                    <h3 style={{ marginBottom: '12px' }}>Efficiency</h3>
                    <div style={{ display: 'grid', gap: '8px' }}>
                        <div><strong>Inventory Turnover:</strong> {safeFormat(metrics.inventory_turnover)}x</div>
                        <div><strong>Receivables Days:</strong> {safeFormat(metrics.receivables_days, 0)} days</div>
                        <div><strong>Payables Days:</strong> {safeFormat(metrics.payables_days, 0)} days</div>
                        <div><strong>Cash Conversion:</strong> {safeFormat(metrics.cash_conversion_cycle, 0)} days</div>
                    </div>
                </div>

                <div className="card">
                    <h3 style={{ marginBottom: '12px' }}>Solvency</h3>
                    <div style={{ display: 'grid', gap: '8px' }}>
                        <div><strong>Debt to Equity:</strong> {safeFormat(metrics.debt_to_equity)}</div>
                        <div><strong>Interest Coverage:</strong> {safeFormat(metrics.interest_coverage)}x</div>
                        <div><strong>Cash Flow Stability:</strong> {safeFormat(metrics.cash_flow_stability, 0)}/100</div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default DashboardPage;
