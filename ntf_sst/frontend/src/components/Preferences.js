import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Preferences.css';

function Preferences() {
    const [preferences, setPreferences] = useState({
        push_enabled: true,
        email_enabled: true,
        digest_frequency: 'instant'
    });
    const [loading, setLoading] = useState(true);
    const [saved, setSaved] = useState(false);

    useEffect(() => {
        fetchPreferences();
    }, []);

    const fetchPreferences = async () => {
        try {
            const response = await axios.get('/api/preferences/');
            setPreferences(response.data);
        } catch (err) {
            console.error('Ошибка загрузки настроек:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setPreferences(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.put('/api/preferences/', preferences);
            setSaved(true);
            setTimeout(() => setSaved(false), 3000);
        } catch (err) {
            console.error('Ошибка сохранения:', err);
            alert('Ошибка сохранения настроек');
        }
    };

    if (loading) {
        return <div className="loading">Загрузка настроек...</div>;
    }

    return (
        <div className="preferences-container">
            <h2>⚙️ Настройки уведомлений</h2>

            {saved && <div className="success-message">✅ Настройки сохранены!</div>}

            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>
                        <input
                            type="checkbox"
                            name="email_enabled"
                            checked={preferences.email_enabled}
                            onChange={handleChange}
                        />
                        Получать уведомления по email
                    </label>
                </div>

                <div className="form-group">
                    <label>
                        <input
                            type="checkbox"
                            name="push_enabled"
                            checked={preferences.push_enabled}
                            onChange={handleChange}
                        />
                        Получать push-уведомления
                    </label>
                </div>

                <div className="form-group">
                    <label>Частота сводок:</label>
                    <select
                        name="digest_frequency"
                        value={preferences.digest_frequency}
                        onChange={handleChange}
                    >
                        <option value="instant">Мгновенно</option>
                        <option value="daily">Раз в день</option>
                        <option value="weekly">Раз в неделю</option>
                    </select>
                </div>

                <button type="submit" className="save-btn">Сохранить настройки</button>
            </form>
        </div>
    );
}

export default Preferences;