import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useSearchParams } from 'react-router-dom';
import HomePage from './pages/HomePage';
import UploadPage from './pages/UploadPage';
import DashboardPage from './pages/DashboardPage';
import CreditPage from './pages/CreditPage';
import RecommendationsPage from './pages/RecommendationsPage';
import ForecastPage from './pages/ForecastPage';
import ReportsPage from './pages/ReportsPage';
import './index.css';

function NavLinks() {
    const [searchParams] = useSearchParams();
    const companyId = searchParams.get('company');
    const query = companyId ? `?company=${companyId}` : '';

    return (
        <nav className="nav">
            <Link to={`/${query}`} style={{ fontSize: '20px', fontWeight: 'bold', color: '#667eea' }}>
                SME Financial Platform
            </Link>
            <Link to={`/${query}`}>Home</Link>
            <Link to={`/upload${query}`}>Upload Data</Link>
            <Link to={`/dashboard${query}`}>Dashboard</Link>
            <Link to={`/credit${query}`}>Credit Assessment</Link>
            <Link to={`/recommendations${query}`}>Recommendations</Link>
            <Link to={`/forecast${query}`}>Forecast</Link>
            <Link to={`/reports${query}`}>Reports</Link>
        </nav>
    );
}

function App() {
    return (
        <Router>
            <div className="App">
                <header className="header">
                    <div className="container">
                        <NavLinks />
                    </div>
                </header>

                <div className="container">
                    <Routes>
                        <Route path="/" element={<HomePage />} />
                        <Route path="/upload" element={<UploadPage />} />
                        <Route path="/dashboard" element={<DashboardPage />} />
                        <Route path="/credit" element={<CreditPage />} />
                        <Route path="/recommendations" element={<RecommendationsPage />} />
                        <Route path="/forecast" element={<ForecastPage />} />
                        <Route path="/reports" element={<ReportsPage />} />
                    </Routes>
                </div>
            </div>
        </Router>
    );
}

export default App;
