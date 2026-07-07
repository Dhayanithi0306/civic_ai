// const API_BASE_URL = 'http://localhost:8000';
const API_BASE_URL = import.meta.env.VITE_API_URL;
export const apiService = {
  async chat(message, history = []) {
    const response = await fetch(`${API_BASE_URL}/chat/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, history })
    });
    const result = await response.json();
    if (!response.ok || !result.success) throw new Error(result.message || 'Failed to get chat response');
    return result.data;
  },

  async reportComplaint(complaint) {
    const response = await fetch(`${API_BASE_URL}/complaints/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ complaint })
    });
    const result = await response.json().catch(() => ({}));
    if (!response.ok || !result.success) throw new Error(result.message || 'Failed to submit complaint');
    return result.data;
  },

  async getComplaints() {
    const response = await fetch(`${API_BASE_URL}/complaints/`);
    const result = await response.json();
    if (!response.ok || !result.success) throw new Error(result.message || 'Failed to fetch complaints');
    return result.data;
  },

  async recommendSchemes(profile) {
    const response = await fetch(`${API_BASE_URL}/recommend/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(profile)
    });
    const result = await response.json().catch(() => ({}));
    if (!response.ok || !result.success) throw new Error(result.message || 'Failed to get recommendations');
    return result.data;
  }
};
