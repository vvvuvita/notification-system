import React, { useState } from 'react';
import NotificationList from './components/NotificationList';
import Preferences from './components/Preferences';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import './App.css';

function App() {
    const [activeTab, setActiveTab] = useState('notifications');

    return (
        <div className="App">
            <header className="app-header">
                <h1> Система уведомлений</h1>
                <nav className="app-nav">
                    <button
                        className={activeTab === 'notifications' ? 'active' : ''}
                        onClick={() => setActiveTab('notifications')}
                    >
                         Уведомления
                    </button>
                    <button
                        className={activeTab === 'preferences' ? 'active' : ''}
                        onClick={() => setActiveTab('preferences')}
                    >
                         Настройки
                    </button>
                </nav>
            </header>

            <main className="app-main">
                {activeTab === 'notifications' && <NotificationList />}
                {activeTab === 'preferences' && <Preferences />}
            </main>

            <ToastContainer position="top-right" autoClose={5000} />
        </div>
    );
}

export default App;