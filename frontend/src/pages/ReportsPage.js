import React, { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { generateReport, getReports, getCompany } from '../services/api';

function ReportsPage() {
    const [searchParams] = useSearchParams();
    const companyId = searchParams.get('company');
    const [company, setCompany] = useState(null);
    const [reports, setReports] = useState([]);
    const [loading, setLoading] = useState(false);
    const [reportType, setReportType] = useState('comprehensive');
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

            const reportsRes = await getReports(companyId);
            setReports(reportsRes.data.results || reportsRes.data);
        } catch (error) {
            console.error('Error loading data:', error);
        }
    };

    const handleGenerate = async () => {
        setLoading(true);
        setMessage({ type: '', text: '' });

        try {
            const response = await generateReport(companyId, reportType, language);
            setReports([response.data, ...reports]);
            setMessage({ type: 'success', text: 'Report generated successfully!' });
        } catch (error) {
            setMessage({ type: 'error', text: error.response?.data?.error || 'Error generating report' });
        } finally {
            setLoading(false);
        }
    };

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('en-IN', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    };

    if (!companyId) {
        return (
            <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
                <h2 style={{ marginBottom: '16px' }}>No Company Selected</h2>
                <p style={{ color: '#6b7280', marginBottom: '24px' }}>Please select a company from the home page to view the reports.</p>
                <Link to="/" className="btn btn-primary">Go to Home Page</Link>
            </div>
        );
    }

    return (
        <div>
            <div className="card">
                <h1>Reports - {company?.name}</h1>
                <p style={{ color: '#6b7280' }}>Generate and download PDF reports</p>
            </div>

            <div className="card">
                <h3 style={{ marginBottom: '20px' }}>Generate New Report</h3>

                <div className="grid" style={{ gridTemplateColumns: '1fr 1fr 1fr auto' }}>
                    <div className="form-group">
                        <label>Report Type</label>
                        <select value={reportType} onChange={(e) => setReportType(e.target.value)}>
                            <option value="comprehensive">Comprehensive Report</option>
                            <option value="investor">Investor Report</option>
                            <option value="lender">Lender Report</option>
                            <option value="board">Board Report</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label>Language</label>
                        <select value={language} onChange={(e) => setLanguage(e.target.value)}>
                            <option value="en">English</option>
                            <option value="hi">हिंदी</option>
                        </select>
                    </div>

                    <div></div>

                    <div className="form-group">
                        <label>&nbsp;</label>
                        <button className="btn btn-primary" onClick={handleGenerate} disabled={loading}>
                            {loading ? 'Generating...' : 'Generate Report'}
                        </button>
                    </div>
                </div>

                {message.text && (
                    <div className={`alert alert-${message.type}`} style={{ marginTop: '20px' }}>
                        {message.text}
                    </div>
                )}
            </div>

            <div className="card">
                <h3 style={{ marginBottom: '20px' }}>Report Types</h3>
                <div className="grid">
                    <div style={{ padding: '16px', background: '#f9fafb', borderRadius: '8px' }}>
                        <h4 style={{ color: '#667eea', marginBottom: '8px' }}>📊 Comprehensive Report</h4>
                        <p style={{ color: '#6b7280', fontSize: '14px' }}>
                            Complete financial analysis with all metrics, assessments, and recommendations
                        </p>
                    </div>
                    <div style={{ padding: '16px', background: '#f9fafb', borderRadius: '8px' }}>
                        <h4 style={{ color: '#667eea', marginBottom: '8px' }}>💼 Investor Report</h4>
                        <p style={{ color: '#6b7280', fontSize: '14px' }}>
                            Focused on profitability, growth potential, and investment highlights
                        </p>
                    </div>
                    <div style={{ padding: '16px', background: '#f9fafb', borderRadius: '8px' }}>
                        <h4 style={{ color: '#667eea', marginBottom: '8px' }}>🏦 Lender Report</h4>
                        <p style={{ color: '#6b7280', fontSize: '14px' }}>
                            Credit assessment, risk analysis, and loan servicing capacity
                        </p>
                    </div>
                    <div style={{ padding: '16px', background: '#f9fafb', borderRadius: '8px' }}>
                        <h4 style={{ color: '#667eea', marginBottom: '8px' }}>📈 Board Report</h4>
                        <p style={{ color: '#6b7280', fontSize: '14px' }}>
                            Executive summary with key insights and strategic recommendations
                        </p>
                    </div>
                </div>
            </div>

            {reports.length > 0 && (
                <div className="card">
                    <h3 style={{ marginBottom: '20px' }}>Generated Reports</h3>
                    <div style={{ display: 'grid', gap: '12px' }}>
                        {reports.map((report) => (
                            <div key={report.id} style={{
                                padding: '16px',
                                background: '#f9fafb',
                                borderRadius: '8px',
                                display: 'flex',
                                justifyContent: 'space-between',
                                alignItems: 'center'
                            }}>
                                <div>
                                    <h4 style={{ color: '#1f2937', marginBottom: '4px' }}>
                                        {report.report_type.charAt(0).toUpperCase() + report.report_type.slice(1)} Report
                                    </h4>
                                    <p style={{ color: '#6b7280', fontSize: '14px' }}>
                                        Generated on {formatDate(report.generated_at)} • {report.language === 'hi' ? 'Hindi' : 'English'}
                                    </p>
                                </div>
                                <a href={report.file} download>
                                    <button className="btn btn-primary">
                                        📥 Download PDF
                                    </button>
                                </a>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

export default ReportsPage;
