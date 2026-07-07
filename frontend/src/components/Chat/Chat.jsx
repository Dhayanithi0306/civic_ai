import React, { useState, useRef, useEffect } from 'react';
import { apiService } from '../../services/api';
import { LoadingSpinner } from '../Common/LoadingSpinner';
import './Chat.css';

export const Chat = () => {
    const [messages, setMessages] = useState([
        { role: 'assistant', content: 'Hello! I am CivicAI, your Government Digital Assistant. How can I help you understand schemes, eligibility, or applications today?' }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = input.trim();
        setInput('');
        
        const newMessages = [...messages, { role: 'user', content: userMessage }];
        setMessages(newMessages);
        setIsLoading(true);

        try {
            // Keep history to last 5 interactions to save tokens
            const history = newMessages.slice(-5).map(m => ({
                role: m.role,
                content: m.content
            }));
            
            const response = await apiService.chat(userMessage, history);
            setMessages(prev => [...prev, { role: 'assistant', content: response.reply }]);
        } catch (error) {
            setMessages(prev => [...prev, { 
                role: 'assistant', 
                content: 'I apologize, but I am having trouble connecting to my service right now. Please try again in a few moments.',
                isError: true
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-messages">
                {messages.map((msg, index) => (
                    <div key={index} className={`message-bubble ${msg.role} ${msg.isError ? 'error-bubble' : ''}`}>
                        <div className="message-content">
                            {msg.content.split('\n').map((line, i) => (
                                <p key={i}>{line.startsWith('- ') ? <li>{line.substring(2)}</li> : line}</p>
                            ))}
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="message-bubble assistant typing-indicator-container">
                        <div className="typing-indicator" aria-live="polite">
                            <span>Preparing response...</span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>
            
            <form onSubmit={handleSend} className="chat-input-form">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask about schemes, eligibility, or required documents..."
                    disabled={isLoading}
                    className="chat-input"
                    autoFocus
                />
                <button type="submit" disabled={isLoading || !input.trim()} className="send-btn">
                    <span className="send-icon">➤</span> Send
                </button>
            </form>
        </div>
    );
};
