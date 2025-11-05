# Library Service

A full-stack Django REST API for managing a library: book inventory, borrowings/returns, users, payments (Stripe), and Telegram notifications.  
Supports JWT authentication, admin/staff roles, daily overdue checks, and Docker deployment.

---

## Features

- **Books CRUD**: List/create/update/delete books (admin), search books (all users)
- **Users**: Register, JWT login, manage profile, custom user model (email login)
- **Borrowings**: Borrow, filter/search returns, auto-create Stripe payment
- **Returns**: Update inventory, create fine in case of late return
- **Payments**: Stripe integration for all operations; webhook support
- **Notifications**: Telegram bot integration for instant alerts
- **Overdue Checks**: Daily scheduled check and notification
- **Admin**: Full browsing in `/admin/`

---

## Quickstart

1. **Clone & Install**
    ```
    git clone <repo-url>
    cd library-service
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

2. **.env Configuration**
    ```
    SECRET_KEY=your-super-secret
    DEBUG=True
    ALLOWED_HOSTS=127.0.0.1,localhost
    STRIPE_SECRET_KEY=sk_test_...
    STRIPE_PUBLISHABLE_KEY=pk_test_...
    TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
    TELEGRAM_CHAT_ID=your-chat-id
    REDIS_HOST=localhost
    REDIS_PORT=6379
    ```

3. **Run Database Migrations**
    ```
    python manage.py migrate
    python manage.py createsuperuser
    ```

4. **Start Development Server**
    ```
    python manage.py runserver
    ```

5. **Run Django-Q cluster for async/scheduled tasks**
    ```
    python manage.py qcluster
    ```

6. **(Optional) Setup scheduled tasks:**
    ```
    python manage.py setup_schedule
    ```

---

## API Endpoints

- Books:        `/api/books/`
- Users:        `/api/users/` (`register/`, `token/`, `me/`)
- Borrowings:   `/api/borrowings/`
- Payments:     `/api/payments/`
- Admin:        `/admin/`
- API Docs:     `/api/docs/`

---

## Tech Stack

- Python 3.13, Django 4.2, DRF
- PostgreSQL or SQLite (default)
- Stripe Payments (sandbox)
- Docker, Redis (for queue/scheduling)
- Telegram Bot API

---

## Docker (Optional)

1. **Start all services in Docker:**
    ```
    docker-compose up --build
    ```
2. Access:  
    - API:   `http://localhost:8000/`
    - Admin: `http://localhost:8000/admin/`

---

## Testing

Run tests:

