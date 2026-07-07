import React, { useState, useEffect } from 'react';
import { apiService } from '../../services/api';
import './Complaint.css';

export const Complaint = () => {
    const [complaintText, setComplaintText] = useState('');
    const [complaints, setComplaints] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        loadComplaints();
    }, []);

    const loadComplaints = async () => {
        try {
            const data = await apiService.getComplaints();
            setComplaints(data);
            setError(null);
        } catch (err) {
            setError('Failed to load past complaints. Please refresh the page.');
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!complaintText.trim()) return;

        setIsLoading(true);
        setError(null);
        try {
            await apiService.reportComplaint(complaintText);
            setComplaintText('');
            await loadComplaints(); // Refresh the list
        } catch (err) {
            setError(err.message || 'We could not process this complaint. Please ensure it clearly describes a civic issue and try again.');
        } finally {
            setIsLoading(false);
        }
    };

    const getSeverityColor = (severity) => {
        switch(severity?.toLowerCase()) {
            case 'high': return 'severity-high';
            case 'medium': return 'severity-medium';
            case 'low': return 'severity-low';
            default: return 'severity-default';
        }
    };

    return (
        <div className="complaint-container fade-in">
            <div className="complaint-form-section">
                <h2>📝 Report a Civic Issue</h2>
                <p className="subtitle">Describe your issue in plain language. Our AI will automatically categorize and file it for you.</p>
                
                <form onSubmit={handleSubmit} className="complaint-form">
                    <textarea
                        value={complaintText}
                        onChange={(e) => setComplaintText(e.target.value)}
                        placeholder="E.g., There is a large pothole on Main Street near the central park that is causing traffic jams."
                        rows={5}
                        disabled={isLoading}
                        className="complaint-textarea"
                        aria-label="Complaint description"
                    />
                    {error && <div className="error-message">{error}</div>}
                    
                    <button type="submit" disabled={isLoading || !complaintText.trim()} className="submit-btn" aria-label="Submit complaint">
                        {isLoading ? 'Analyzing complaint...' : 'File Complaint'}
                    </button>
                </form>
            </div>

            <div className="complaints-list-section">
                <h2>📋 Recent Reports</h2>
                <div className="complaints-grid">
                    {complaints.length === 0 ? (
                        <div className="empty-state">
                            <span className="empty-icon">📫</span>
                            <p>No complaints have been reported yet.</p>
                        </div>
                    ) : (
                        complaints.map(complaint => (
                            <div key={complaint.id} className="complaint-card fade-in">
                                <div className="complaint-header">
                                    <span className={`category-badge`}>{complaint.category}</span>
                                    <span className={`severity-badge ${getSeverityColor(complaint.severity)}`}>
                                        {complaint.severity} Priority
                                    </span>
                                </div>
                                <h3 className="complaint-summary">{complaint.summary}</h3>
                                <div className="complaint-details">
                                    <p><strong>Location:</strong> {complaint.location}</p>
                                    <p><strong>Status:</strong> <span className="status-indicator">{complaint.status}</span></p>
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
};
