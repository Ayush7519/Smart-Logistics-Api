# Smart Logistics API 🚚📦

Smart Logistics API is a scalable backend system built with **Django** and **Django Rest Framework (DRF)** to support logistics operations such as shipments, fleet management, users, notifications, and analytics.

This project follows **clean architecture**, **standardized API responses**, **soft-delete models**, and **production-ready best practices**.

============================================================================

## 🛠 Tech Stack

- **Python** 3.11
- **Django**
- **Django Rest Framework (DRF)**
- **PostgreSQL**
- **UUID-based primary keys**
- **Custom Exception Handling**
- **Request ID Middleware**
- **Soft Delete Architecture**
- **Environment-based configuration**

============================================================================

## 📁 Project Structure

```text
smart-logistics-api/
│
├── backend/
│   ├── analytics/
│   ├── common/              # Shared utilities (responses, exceptions, middleware)
│   ├── config/              # Project settings & configuration
│   ├── core/                # Base models (Soft Delete, BaseModel)
│   ├── fleet/
│   ├── notifications/
│   ├── shipments/
│   ├── users/
│   ├── manage.py
│
├── .env                     # Environment variables (ignored)
├── .gitignore
├── requirements.txt
└── README.md

============================================================================

✅ Key Features Implemented

1. Base Model with Soft Delete

* UUID primary key
* created_at, updated_at
* Soft delete via is_deleted and deleted_at
* Custom QuerySet & Manager
* soft_delete() and hard_delete()

2. Standard API Response Format

All APIs follow a consistent response structure:
{
  "success": true,
  "data": {},
  "error": null,
  "meta": {
    "request_id": "uuid",
    "timestamp": "ISO-8601"
  }
}

3. Global Exception Handling

* Custom BaseAPIException
* Centralized DRF exception handler
* Consistent error responses across the system

4. Request ID Middleware

* Every request gets a unique request_id
* Added to response headers: X-Request-ID
* Included in logs and error responses

5. Environment Configuration

* Secrets managed via .env
* .env and venv/ excluded using .gitignore

========================================================================

⚙️ Setup Instructions

1. Clone the Repository

* git clone https://github.com/Ayush7519/smart-logistics-api.git
* cd smart-logistics-api

2. Create Virtual Environment

* python -m venv venv
* source venv/bin/activate   # macOS/Linux

3. Install Dependencies

* pip install -r requirements.txt

4. Environment Variables

DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_NAME=smartlogistics
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432

5. Run Migrations

* cd backend
* python manage.py makemigrations
* python manage.py migrate

6. Run Development Server

* python manage.py runserver

====================================================================

🔍 Health Check API

Example health endpoint:
* GET /api/health/

Response:
{
  "success": true,
  "data": {
    "status": "ok"
  },
  "error": null,
  "meta": {
    "request_id": "uuid",
    "timestamp": "ISO-8601"
  }
}

===================================================================

🧪 Development Status

✅ Phase 0: Project setup
✅ Phase 1.2: Core infrastructure
⏳ Phase 2: Authentication & Users
⏳ Phase 3: Shipments & Fleet
⏳ Phase 4: Notifications & Analytics

===================================================================

📌 Conventions

* Snake_case for fields
* UUIDs for all primary keys
* Soft delete by default
* Hard delete only when explicitly required
* No direct Model.objects.all() for deleted data

===================================================================

🤝 Contribution

* This project follows a clean commit history and standard Git workflow.
* Create a feature branch
* Commit with clear messages
* Open a pull request

===================================================================

📄 License

* This project is proprietary and under active development.

===================================================================

