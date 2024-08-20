//// src/App.js
//
//import React, { useState, useRef, useEffect } from 'react';
//import { FiSend, FiTrash2, FiDownload, FiSettings } from 'react-icons/fi';
//import axios from 'axios';
//import { parse } from 'node-html-parser';
//import DatabaseUpload from './components/DatabaseUpload';
//import Settings from './components/Settings';
//import './App.css';
//
//const API_URL = 'http://localhost:8000/chat';
//
//function App() {
//  const [messages, setMessages] = useState([]);
//  const [input, setInput] = useState('');
//  const chatbotRef = useRef(null);
//  const [showScrollButton, setShowScrollButton] = useState(false);
//  const [isLoading, setIsLoading] = useState(false);
//  const [showSettings, setShowSettings] = useState(false);
//  const [dbUrl, setDbUrl] = useState('');
//
//  const handleSubmit = async (e) => {
//    e.preventDefault();
//    if (!input.trim() || isLoading) return;
//
//    setMessages(prev => [...prev, { text: input, isUser: true }]);
//    setInput('');
//    setIsLoading(true);
//
//    try {
//      const response = await axios.post(API_URL, {
//        message: input,
//        history: messages,
//        dbUrl: dbUrl || process.env.REACT_APP_DB_URL, // Use the database URL from settings or environment
//      });
//
//      if (response.data.type === 'HTML') {
//        setMessages(prev => [...prev, { html: response.data.data, explanation: response.data.explanation, sql_query: response.data.sql_query, isUser: false }]);
//      } else if (response.data.type === 'TEXT') {
//        setMessages(prev => [...prev, { text: response.data.data, explanation: response.data.explanation, sql_query: response.data.sql_query, isUser: false }]);
//      }
//    } catch (error) {
//      console.error('Error fetching response:', error);
//      setMessages(prev => [...prev, { text: "Sorry, I couldn't process your request.", isUser: false }]);
//    } finally {
//      setIsLoading(false);
//    }
//  };
//
//  const handleSettingsUpdate = (newSettings) => {
//    const newDbUrl = `postgresql://${newSettings.DB_USER}:${newSettings.DB_PASSWORD}@${newSettings.DB_HOST}:${newSettings.DB_PORT}/${newSettings.DB_NAME}`;
//    setDbUrl(newDbUrl);
//  };
//
//  const clearChat = () => {
//    setMessages([]);
//  };
//
//  const handleScroll = () => {
//    const { scrollTop, scrollHeight, clientHeight } = chatbotRef.current;
//    setShowScrollButton(scrollHeight - scrollTop > clientHeight + 100);
//  };
//
//  const scrollToBottom = () => {
//    chatbotRef.current.scrollTop = chatbotRef.current.scrollHeight;
//  };
//
//  useEffect(() => {
//    scrollToBottom();
//  }, [messages]);
//
//  const downloadCSV = (html) => {
//    // Convert HTML table to CSV format
//    const root = parse(html);
//    const rows = root.querySelectorAll('tr');
//    const csvContent = rows.map(row => {
//      const cells = row.querySelectorAll('td, th');
//      return Array.from(cells).map(cell => `"${cell.text.trim()}"`).join(',');
//    }).join('\n');
//
//    // Create a Blob from the CSV content and download it
//    const blob = new Blob([csvContent], { type: 'text/csv' });
//    const url = window.URL.createObjectURL(blob);
//    const a = document.createElement('a');
//    a.setAttribute('hidden', '');
//    a.setAttribute('href', url);
//    a.setAttribute('download', 'export.csv');
//    document.body.appendChild(a);
//    a.click();
//    document.body.removeChild(a);
//  };
//
//  return (
//    <div className="app-container">
//      <div className="chat-container">
//        <h1 className="app-title">Syne SQL Assistant</h1>
//        <button onClick={() => setShowSettings(!showSettings)} className="settings-btn">
//          <FiSettings />
//        </button>
//        {showSettings && (
//          <div className="settings-modal">
//            <Settings onSettingsUpdate={handleSettingsUpdate} />
//          </div>
//        )}
//        <div className="chatbot" ref={chatbotRef} onScroll={handleScroll}>
//          {messages.map((msg, index) => (
//            <div key={index} className={`message ${msg.isUser ? 'user' : 'bot'}`}>
//              {msg.html ? (
//                <>
//                  <div className="html-content" dangerouslySetInnerHTML={{ __html: msg.html }} />
//                  <button className="download-btn" onClick={() => downloadCSV(msg.html)}>
//                    <FiDownload /> Download CSV
//                  </button>
//                </>
//              ) : (
//                msg.text
//              )}
//              {msg.explanation && (
//                <div className="explanation">
//                  <strong>Explanation: </strong>{msg.explanation}
//                </div>
//              )}
//              {msg.sql_query && (
//                <div className="sql-query">
//                  <strong>SQL Query: </strong>{msg.sql_query}
//                </div>
//              )}
//            </div>
//          ))}
//          {isLoading && <div className="message bot">Thinking...</div>}
//        </div>
//        <form onSubmit={handleSubmit} className="input-area">
//          <input
//            type="text"
//            value={input}
//            onChange={(e) => setInput(e.target.value)}
//            placeholder="Ask your SQL question..."
//            className="input-box"
//            disabled={isLoading}
//          />
//          <button type="submit" className="submit-btn" disabled={isLoading}>
//            <FiSend />
//          </button>
//        </form>
//        <button onClick={clearChat} className="clear-btn" disabled={isLoading}>
//          <FiTrash2 /> Clear Chat
//        </button>
//        {showScrollButton && (
//          <button onClick={scrollToBottom} className="scroll-btn">
//            ↓
//          </button>
//        )}
//      </div>
//    </div>
//  );
//}
//
//export default App;
//

// src/App.js

import React, { useState, useRef, useEffect } from 'react';
import { FiSend, FiTrash2, FiDownload, FiSettings } from 'react-icons/fi';
import axios from 'axios';
import { parse } from 'node-html-parser';
import DatabaseUpload from './components/DatabaseUpload';
import Settings from './components/Settings';
import './App.css';

const API_URL = 'http://localhost:8000/chat';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const chatbotRef = useRef(null);
  const [showScrollButton, setShowScrollButton] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [dbUrl, setDbUrl] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    setMessages(prev => [...prev, { text: input, isUser: true }]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post(API_URL, {
        message: input,
        history: messages,
        dbUrl: dbUrl || process.env.REACT_APP_DB_URL, // Use the database URL from settings or environment
      });

      if (response.data.type === 'HTML') {
        setMessages(prev => [...prev, { html: response.data.data, explanation: response.data.explanation, sql_query: response.data.sql_query, isUser: false }]);
      } else if (response.data.type === 'TEXT') {
        setMessages(prev => [...prev, { text: response.data.data, explanation: response.data.explanation, sql_query: response.data.sql_query, isUser: false }]);
      }
    } catch (error) {
      console.error('Error fetching response:', error);
      setMessages(prev => [...prev, { text: "Sorry, I couldn't process your request.", isUser: false }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSettingsUpdate = (newSettings) => {
    const newDbUrl = `postgresql://${newSettings.DB_USER}:${newSettings.DB_PASSWORD}@${newSettings.DB_HOST}:${newSettings.DB_PORT}/${newSettings.DB_NAME}`;
    setDbUrl(newDbUrl);
  };

  const clearChat = () => {
    setMessages([]);
  };

  const handleScroll = () => {
    const { scrollTop, scrollHeight, clientHeight } = chatbotRef.current;
    setShowScrollButton(scrollHeight - scrollTop > clientHeight + 100);
  };

  const scrollToBottom = () => {
    chatbotRef.current.scrollTop = chatbotRef.current.scrollHeight;
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const downloadCSV = (html) => {
    const root = parse(html);
    const rows = root.querySelectorAll('tr');
    const csvContent = rows.map(row => {
      const cells = row.querySelectorAll('td, th');
      return Array.from(cells).map(cell => `"${cell.text.trim()}"`).join(',');
    }).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', 'export.csv');
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  return (
    <div className="app-container">
      <div className="chat-container">
        <h1 className="app-title">SQL Assistant
        {/* Using the absolute path to the favicon */}
          <img src="/artificial-intelligence.png" alt="favicon" style={{ marginLeft: '10px', width: '32px', height: '32px' }} />
        </h1>
        <button onClick={() => setShowSettings(!showSettings)} className="settings-btn">
          <FiSettings />
        </button>
        {showSettings && (
          <div className="settings-modal">
            <Settings onSettingsUpdate={handleSettingsUpdate} />
          </div>
        )}
        <div className="chatbot" ref={chatbotRef} onScroll={handleScroll}>
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.isUser ? 'user' : 'bot'}`}>
              {msg.html ? (
                <>
                  <div className="html-content" dangerouslySetInnerHTML={{ __html: msg.html }} />
                  <button className="download-btn" onClick={() => downloadCSV(msg.html)}>
                    <FiDownload /> Download CSV
                  </button>
                </>
              ) : (
                msg.text
              )}
              {msg.explanation && (
                <div className="explanation">
                  <strong>Explanation: </strong>{msg.explanation}
                </div>
              )}
              {msg.sql_query && (
                <div className="sql-query">
                  <strong>SQL Query: </strong>{msg.sql_query}
                </div>
              )}
            </div>
          ))}
          {isLoading && <div className="message bot">Thinking...</div>}
        </div>
        <form onSubmit={handleSubmit} className="input-area">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask your SQL question..."
            className="input-box"
            disabled={isLoading}
          />
          <button type="submit" className="submit-btn" disabled={isLoading}>
            <FiSend />
          </button>
        </form>
        <button onClick={clearChat} className="clear-btn" disabled={isLoading}>
          <FiTrash2 /> Clear Chat
        </button>
        {showScrollButton && (
          <button onClick={scrollToBottom} className="scroll-btn">
            ↓
          </button>
        )}
      </div>
    </div>
  );
}

export default App;
