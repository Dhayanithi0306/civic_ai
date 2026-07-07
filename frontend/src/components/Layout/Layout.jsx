import React from 'react';
import './Layout.css';

export const Layout = ({ children, activeTab, setActiveTab }) => {
    return (
        <div className="app-layout">
            <header className="app-header">
                <div className="header-content">
                    <h1>CivicAI</h1>
                    <p className="subtitle">Your Smart Government Assistant</p>
                </div>
                <nav className="app-nav">
                    <button 
                        className={`nav-btn ${activeTab === 'chat' ? 'active' : ''}`}
                        onClick={() => setActiveTab('chat')}
                    >
                        Chat Assistant
                    </button>
                    <button 
                        className={`nav-btn ${activeTab === 'report' ? 'active' : ''}`}
                        onClick={() => setActiveTab('report')}
                    >
                        Report Issue
                    </button>
                    <button 
                        className={`nav-btn ${activeTab === 'schemes' ? 'active' : ''}`}
                        onClick={() => setActiveTab('schemes')}
                    >
                        Find Schemes
                    </button>
                </nav>
            </header>
            <main className="app-main">
                {children}
            </main>
        </div>
    );
};
