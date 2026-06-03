# Система уведомлений и оповещений

Система для мгновенного информирования участников проектов о важных событиях: изменениях в проектах, новых комментариях, истечении сроков.

##  Демо

- **Frontend (React)**: `http://localhost:3000`
- **Backend API (Django)**: `http://localhost:8080`
- **Admin panel**: `http://localhost:8080/admin`

##  Функциональность

-  Email-уведомления (через Brevo)
-  Push-уведомления в реальном времени (WebSocket)
-  Гибкие настройки для каждого пользователя
-  История уведомлений в личном кабинете
-  Ролевая модель (администратор, участник, наблюдатель, гость)
-  Оповещения о дедлайнах (за 24/12/1 час)

##  Технологии

### Backend
- Python 3.12
- Django 5
- Django REST Framework
- Celery 
- Redis 
- PostgreSQL
- Django Channels (WebSocket)

### Frontend
- React 18
- Axios 
- React Toastify 

##  Установка и запуск

```bash
git clone https://github.com/vvvuvita/notification-system.git
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
Создайте файл .env в корне проекта
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
В отдельных терминалах:
redis-server
celery -A core worker --loglevel=info --pool=solo
python manage.py runserver 8080
cd frontend
npm install
npm start