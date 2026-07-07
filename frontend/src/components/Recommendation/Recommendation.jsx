import React, { useState } from 'react';
import { apiService } from '../../services/api';
import './Recommendation.css';

export const Recommendation = () => {
    const [profile, setProfile] = useState({
        age: '',
        occupation: '',
        monthly_income: '',
        state: ''
    });
    const [recommendations, setRecommendations] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [hasSearched, setHasSearched] = useState(false);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setError(null);
        try {
            const data = await apiService.recommendSchemes({
                ...profile,
                age: parseInt(profile.age),
                monthly_income: parseInt(profile.monthly_income)
            });
            setRecommendations(data.recommendations || []);
            setHasSearched(true);
        } catch (err) {
            setError(err.message || 'Failed to generate recommendations. Please check your network and try again.');
        } finally {
            setIsLoading(false);
        }
    };

    const getMatchColor = (score) => {
        switch(score?.toLowerCase()) {
            case 'high': return 'match-high';
            case 'medium': return 'match-medium';
            case 'low': return 'match-low';
            default: return 'match-default';
        }
    };

    return (
        <div className="recommendation-container fade-in">
            <div className="profile-section">
                <h2>🎯 Find Your Schemes</h2>
                <p className="subtitle">Tell us about yourself to discover government benefits you may qualify for.</p>
                <form onSubmit={handleSubmit} className="profile-form">
                    <div className="form-group">
                        <label>Age</label>
                        <input
                            type="number"
                            min="0"
                            required
                            value={profile.age}
                            onChange={e => setProfile({...profile, age: e.target.value})}
                        />
                    </div>
                    <div className="form-group">
                        <label>Occupation</label>
                        <input
                            type="text"
                            required
                            placeholder="e.g., Farmer, Student"
                            value={profile.occupation}
                            onChange={e => setProfile({...profile, occupation: e.target.value})}
                        />
                    </div>
                    <div className="form-group">
                        <label>Monthly Income (₹)</label>
                        <input
                            type="number"
                            min="0"
                            required
                            value={profile.monthly_income}
                            onChange={e => setProfile({...profile, monthly_income: e.target.value})}
                        />
                    </div>
                    <div className="form-group">
                        <label>State</label>
                        <input
                            type="text"
                            required
                            placeholder="e.g., Maharashtra"
                            value={profile.state}
                            onChange={e => setProfile({...profile, state: e.target.value})}
                        />
                    </div>
                    {error && <div className="error-message">{error}</div>}
                    <button type="submit" disabled={isLoading} className="submit-btn" aria-label="Find matching schemes">
                        {isLoading ? 'Searching schemes...' : 'Find Matches'}
                    </button>
                </form>
            </div>

            <div className="results-section">
                <h2>📋 Your Matches</h2>
                <div className="recommendations-list">
                    {!hasSearched && !isLoading && (
                        <div className="empty-state">
                            <span className="empty-icon">🔍</span>
                            <p>Fill out your profile to see matched schemes.</p>
                        </div>
                    )}
                    
                    {hasSearched && recommendations.length === 0 && !isLoading && (
                        <div className="empty-state">
                            <span className="empty-icon">😔</span>
                            <p>We couldn't find any exact matches based on your profile right now.</p>
                        </div>
                    )}

                    {recommendations.map((rec, idx) => (
                        <div key={idx} className="scheme-card fade-in">
                            <div className="scheme-header">
                                <h3>{rec.name}</h3>
                                <div className="badges">
                                    <span className="category-badge">{rec.category || 'General'}</span>
                                    {rec.eligibility_match_score && (
                                        <span className={`match-badge ${getMatchColor(rec.eligibility_match_score)}`}>
                                            {rec.eligibility_match_score} Match
                                        </span>
                                    )}
                                </div>
                            </div>
                            
                            <div className="scheme-section highlight-section">
                                <h4>Why it matches you</h4>
                                <p>{rec.reason}</p>
                            </div>
                            
                            <div className="scheme-section">
                                <h4>Key Benefits</h4>
                                <p>{rec.benefits}</p>
                            </div>

                            <div className="scheme-section">
                                <h4>How to Apply</h4>
                                <p>{rec.application_guidance || 'Check official government portals for application details.'}</p>
                            </div>
                            
                            <div className="scheme-section">
                                <h4>Required Documents</h4>
                                <ul className="docs-list">
                                    {rec.documents_required.map((doc, i) => (
                                        <li key={i}>{doc}</li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};
