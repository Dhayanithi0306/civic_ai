import React, { useState } from 'react';
import { Layout } from './components/Layout/Layout';
import { Chat } from './components/Chat/Chat';
import { Complaint } from './components/Complaint/Complaint';
import { Recommendation } from './components/Recommendation/Recommendation';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('chat');

  return (
    <Layout activeTab={activeTab} setActiveTab={setActiveTab}>
      <div className="tab-content fade-in">
        {activeTab === 'chat' && <Chat />}
        {activeTab === 'report' && <Complaint />}
        {activeTab === 'schemes' && <Recommendation />}
      </div>
    </Layout>
  );
}

export default App;
