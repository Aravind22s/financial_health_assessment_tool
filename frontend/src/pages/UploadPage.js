import React, { useState, useEffect } from 'react';
import { createCompany, uploadFinancialData, processFinancialData } from '../services/api';

function UploadPage() {
    const [step, setStep] = useState(1);
    const [companyData, setCompanyData] = useState({
        name: '',
        industry: 'manufacturing',
        gst_number: '',
        pan_number: '',
        annual_revenue: '',
    });
    const [file, setFile] = useState(null);
    const [periodStart, setPeriodStart] = useState('');
    const [periodEnd, setPeriodEnd] = useState('');
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState({ type: '', text: '' });
    const [companyId, setCompanyId] = useState(null);

    const handleCompanySubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage({ type: '', text: '' });

        try {
            const response = await createCompany(companyData);
            setCompanyId(response.data.id);
            setMessage({ type: 'success', text: 'Company created successfully!' });
            setStep(2);
        } catch (error) {
            setMessage({ type: 'error', text: 'Error creating company. Please try again.' });
        } finally {
            setLoading(false);
        }
    };

    const handleFileUpload = async (e) => {
        e.preventDefault();
        if (!file || !periodStart || !periodEnd) {
            setMessage({ type: 'error', text: 'Please fill all fields' });
            return;
        }

        setLoading(true);
        setMessage({ type: '', text: '' });

        try {
            const formData = new FormData();
            formData.append('company', companyId);
            formData.append('file', file);
            formData.append('file_type', file.name.endsWith('.csv') ? 'csv' : file.name.endsWith('.pdf') ? 'pdf' : 'xlsx');
            formData.append('period_start', periodStart);
            formData.append('period_end', periodEnd);

            const response = await uploadFinancialData(formData);
            const dataId = response.data.id;

            // Process the uploaded data
            setMessage({ type: 'info', text: 'Processing financial data...' });
            await processFinancialData(dataId);

            setMessage({ type: 'success', text: 'Financial data uploaded and processed successfully! You can now view your dashboard.' });
            setStep(3);
        } catch (error) {
            setMessage({ type: 'error', text: 'Error uploading file. Please try again.' });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <div className="card">
                <h1 style={{ marginBottom: '8px' }}>Upload Financial Data</h1>
                <p style={{ color: '#6b7280', marginBottom: '24px' }}>
                    Step {step} of 2: {step === 1 ? 'Company Information' : 'Upload Financial Statements'}
                </p>

                {message.text && (
                    <div className={`alert alert-${message.type}`}>
                        {message.text}
                    </div>
                )}

                {step === 1 && (
                    <form onSubmit={handleCompanySubmit}>
                        <div className="form-group">
                            <label>Company Name *</label>
                            <input
                                type="text"
                                value={companyData.name}
                                onChange={(e) => setCompanyData({ ...companyData, name: e.target.value })}
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label>Industry *</label>
                            <select
                                value={companyData.industry}
                                onChange={(e) => setCompanyData({ ...companyData, industry: e.target.value })}
                                required
                            >
                                <option value="manufacturing">Manufacturing</option>
                                <option value="retail">Retail</option>
                                <option value="agriculture">Agriculture</option>
                                <option value="services">Services</option>
                                <option value="logistics">Logistics</option>
                                <option value="ecommerce">E-commerce</option>
                            </select>
                        </div>

                        <div className="form-group">
                            <label>GST Number</label>
                            <input
                                type="text"
                                value={companyData.gst_number}
                                onChange={(e) => setCompanyData({ ...companyData, gst_number: e.target.value })}
                                placeholder="22AAAAA0000A1Z5"
                            />
                        </div>

                        <div className="form-group">
                            <label>PAN Number</label>
                            <input
                                type="text"
                                value={companyData.pan_number}
                                onChange={(e) => setCompanyData({ ...companyData, pan_number: e.target.value })}
                                placeholder="AAAAA0000A"
                            />
                        </div>

                        <div className="form-group">
                            <label>Annual Revenue (₹)</label>
                            <input
                                type="number"
                                value={companyData.annual_revenue}
                                onChange={(e) => setCompanyData({ ...companyData, annual_revenue: e.target.value })}
                                placeholder="5000000"
                            />
                        </div>

                        <button type="submit" className="btn btn-primary" disabled={loading}>
                            {loading ? 'Creating...' : 'Next: Upload Financial Data'}
                        </button>
                    </form>
                )}

                {step === 2 && (
                    <form onSubmit={handleFileUpload}>
                        <div className="form-group">
                            <label>Financial Statement File (CSV, XLSX, or PDF) *</label>
                            <input
                                type="file"
                                accept=".csv,.xlsx,.xls,.pdf"
                                onChange={(e) => setFile(e.target.files[0])}
                                required
                            />
                            <small style={{ color: '#6b7280', display: 'block', marginTop: '8px' }}>
                                Upload your balance sheet, income statement, or comprehensive financial report
                            </small>
                        </div>

                        <div className="grid" style={{ gridTemplateColumns: '1fr 1fr' }}>
                            <div className="form-group">
                                <label>Period Start Date *</label>
                                <input
                                    type="date"
                                    value={periodStart}
                                    onChange={(e) => setPeriodStart(e.target.value)}
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label>Period End Date *</label>
                                <input
                                    type="date"
                                    value={periodEnd}
                                    onChange={(e) => setPeriodEnd(e.target.value)}
                                    required
                                />
                            </div>
                        </div>

                        <div style={{ display: 'flex', gap: '12px' }}>
                            <button type="button" className="btn btn-secondary" onClick={() => setStep(1)}>
                                Back
                            </button>
                            <button type="submit" className="btn btn-primary" disabled={loading}>
                                {loading ? 'Uploading...' : 'Upload and Process'}
                            </button>
                        </div>
                    </form>
                )}

                {step === 3 && (
                    <div style={{ textAlign: 'center', padding: '40px' }}>
                        <div style={{ fontSize: '48px', marginBottom: '16px' }}>✅</div>
                        <h2 style={{ color: '#10b981', marginBottom: '16px' }}>Success!</h2>
                        <p style={{ color: '#6b7280', marginBottom: '24px' }}>
                            Your financial data has been processed successfully.
                        </p>
                        <a href={`/dashboard?company=${companyId}`}>
                            <button className="btn btn-primary">View Dashboard</button>
                        </a>
                    </div>
                )}
            </div>

            <div className="card">
                <h3 style={{ marginBottom: '12px' }}>Supported File Formats</h3>
                <ul style={{ color: '#6b7280', lineHeight: '1.8' }}>
                    <li><strong>CSV:</strong> Comma-separated values with account names and amounts</li>
                    <li><strong>Excel (XLSX):</strong> Spreadsheets with financial data</li>
                    <li><strong>PDF:</strong> Text-based financial statements (scanned images not supported)</li>
                </ul>
            </div>
        </div>
    );
}

export default UploadPage;
