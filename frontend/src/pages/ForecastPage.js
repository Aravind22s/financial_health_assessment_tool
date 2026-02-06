import React, { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { generateForecast, getForecasts, getCompany } from '../services/api';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function ForecastPage() {
    const [searchParams] = useSearchParams();
    const companyId = searchParams.get('company');
    const [company, setCompany] = useState(null);
    const [forecasts, setForecasts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [months, setMonths] = useState(12);
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

            const forecastRes = await getForecasts(companyId);
            setForecasts(forecastRes.data.results || forecastRes.data);
        } catch (error) {
            console.error('Error loading data:', error);
        }
    };

    const handleGenerate = async () => {
        setLoading(true);
        setMessage({ type: '', text: '' });

        try {
            const response = await generateForecast(companyId, months);
            setForecasts(response.data);
            setMessage({ type: 'success', text: 'Forecasts generated successfully!' });
        } catch (error) {
            setMessage({ type: 'error', text: error.response?.data?.error || 'Error generating forecasts' });
        } finally {
            setLoading(false);
        }
    };

    const getChartData = (type) => {
        if (forecasts.length === 0) return null;

        const labels = forecasts[0]?.revenue_forecast?.map(f => f.month) || [];

        const datasets = forecasts.map((forecast, index) => {
            const colors = ['#667eea', '#f59e0b', '#ef4444'];
            const data = type === 'revenue'
                ? forecast.revenue_forecast
                : type === 'expense'
                    ? forecast.expense_forecast
                    : forecast.cash_flow_forecast;

            return {
                label: forecast.scenario.charAt(0).toUpperCase() + forecast.scenario.slice(1) + ' Case',
                data: data.map(d => d.value),
                borderColor: colors[index],
                backgroundColor: colors[index] + '20',
                tension: 0.4
            };
        });

        return { labels, datasets };
    };

    if (!companyId) {
        return (
            <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
                <h2 style={{ marginBottom: '16px' }}>No Company Selected</h2>
                <p style={{ color: '#6b7280', marginBottom: '24px' }}>Please select a company from the home page to view the forecasts.</p>
                <Link to="/" className="btn btn-primary">Go to Home Page</Link>
            </div>
        );
    }

    return (
        <div>
            <div className="card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                        <h1>Financial Forecast - {company?.name}</h1>
                        <p style={{ color: '#6b7280' }}>Revenue, expense, and cash flow projections</p>
                    </div>
                    <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
                        <select
                            value={months}
                            onChange={(e) => setMonths(Number(e.target.value))}
                            style={{ padding: '8px 12px', borderRadius: '8px', border: '1px solid #d1d5db' }}
                        >
                            <option value={6}>6 Months</option>
                            <option value={12}>12 Months</option>
                            <option value={18}>18 Months</option>
                            <option value={24}>24 Months</option>
                        </select>
                        <button className="btn btn-primary" onClick={handleGenerate} disabled={loading}>
                            {loading ? 'Generating...' : 'Generate Forecast'}
                        </button>
                    </div>
                </div>
            </div>

            {message.text && (
                <div className={`alert alert-${message.type}`}>
                    {message.text}
                </div>
            )}

            {forecasts.length === 0 ? (
                <div className="card" style={{ textAlign: 'center', padding: '60px 20px' }}>
                    <h2 style={{ marginBottom: '16px' }}>No Forecasts Yet</h2>
                    <p style={{ color: '#6b7280', marginBottom: '24px' }}>
                        Generate financial forecasts to plan for the future with best, base, and worst case scenarios.
                    </p>
                </div>
            ) : (
                <>
                    <div className="card">
                        <h3 style={{ marginBottom: '20px' }}>Revenue Forecast</h3>
                        {getChartData('revenue') && (
                            <Line data={getChartData('revenue')} options={{ responsive: true, plugins: { legend: { position: 'top' } } }} />
                        )}
                    </div>

                    <div className="card">
                        <h3 style={{ marginBottom: '20px' }}>Expense Forecast</h3>
                        {getChartData('expense') && (
                            <Line data={getChartData('expense')} options={{ responsive: true, plugins: { legend: { position: 'top' } } }} />
                        )}
                    </div>

                    <div className="card">
                        <h3 style={{ marginBottom: '20px' }}>Cash Flow Forecast</h3>
                        {getChartData('cashflow') && (
                            <Line data={getChartData('cashflow')} options={{ responsive: true, plugins: { legend: { position: 'top' } } }} />
                        )}
                    </div>

                    {forecasts.map((forecast) => (
                        <div key={forecast.id} className="card">
                            <h3 style={{ marginBottom: '12px', textTransform: 'capitalize' }}>
                                {forecast.scenario} Case Scenario
                            </h3>
                            <div style={{ background: '#f9fafb', padding: '16px', borderRadius: '8px', whiteSpace: 'pre-line' }}>
                                {forecast.assumptions}
                            </div>
                        </div>
                    ))}
                </>
            )}
        </div>
    );
}

export default ForecastPage;
