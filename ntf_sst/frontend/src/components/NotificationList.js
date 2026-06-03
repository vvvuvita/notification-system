import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './NotificationList.css';

function NotificationList() {
    // Состояния компонента
    const [notifications, setNotifications] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Загружаем уведомления при загрузке компонента
    useEffect(() => {
        fetchNotifications();
    }, []);

    // Функция для получения уведомлений из API
    const fetchNotifications = async () => {
        try {
            setLoading(true);
            // Запрос к Django API
            const response = await axios.get('/api/notifications/');
            setNotifications(response.data.results || response.data);
            setError(null);
        } catch (err) {
            console.error('Ошибка загрузки:', err);
            setError('Не удалось загрузить уведомления');
        } finally {
            setLoading(false);
        }
    };

    // Функция для отметки уведомления как прочитанного
    const markAsRead = async (id) => {
        try {
            await axios.post(`/api/notifications/${id}/mark_read/`);
            // Обновляем список: меняем статус уведомления
            setNotifications(notifications.map(notif =>
                notif.id === id ? { ...notif, is_read: true } : notif
            ));
        } catch (err) {
            console.error('Ошибка:', err);
        }
    };

    // Функция для отметки всех как прочитанных
    const markAllAsRead = async () => {
        try {
            await axios.post('/api/notifications/mark_all_read/');
            setNotifications(notifications.map(notif => ({ ...notif, is_read: true })));
        } catch (err) {
            console.error('Ошибка:', err);
        }
    };

    // Если загрузка
    if (loading) {
        return <div className="loading">Загрузка уведомлений...</div>;
    }

    // Если ошибка
    if (error) {
        return <div className="error">{error}</div>;
    }

    return (
        <div className="notifications-container">
            <div className="notifications-header">
                <h2>📬 Уведомления</h2>
                <button onClick={markAllAsRead} className="mark-all-btn">
                    ✓ Отметить все как прочитанные
                </button>
            </div>

            {notifications.length === 0 ? (
                <div className="empty-state">
                    📭 Нет уведомлений
                </div>
            ) : (
                <ul className="notifications-list">
                    {notifications.map(notification => (
                        <li
                            key={notification.id}
                            className={`notification-item ${notification.is_read ? 'read' : 'unread'}`}
                            onClick={() => !notification.is_read && markAsRead(notification.id)}
                        >
                            <div className="notification-icon">
                                {notification.notification_type === 'comment' && '💬'}
                                {notification.notification_type === 'update' && '✏️'}
                                {notification.notification_type === 'deadline' && '⏰'}
                                {notification.notification_type === 'mention' && '🔔'}
                            </div>
                            <div className="notification-content">
                                <div className="notification-title">
                                    {notification.title}
                                    {!notification.is_read && <span className="badge">Новое</span>}
                                </div>
                                <div className="notification-message">{notification.message}</div>
                                <div className="notification-meta">
                                    <span className="notification-date">
                                        {new Date(notification.created_at).toLocaleString('ru-RU')}
                                    </span>
                                    <a href={notification.link} className="notification-link">
                                        Перейти →
                                    </a>
                                </div>
                            </div>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}

export default NotificationList;