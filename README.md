# Xenyou - AI-First Apartment Matching Platform

Xenyou is a next-generation, AI-first apartment matching platform designed to connect college students with landlords. This project leverages FastAPI for building a robust API and PostgreSQL for managing user data.

## Project Structure

```
xenyou/
├── app/                          # Main application package
│   ├── main.py                   # FastAPI application entry point and router mounting
│   ├── auth.py                   # Authentication logic and utilities
│   ├── config.py                 # Application configuration settings
│   ├── celery_app.py             # Celery configuration for background tasks
│   ├── api/
│   │   └── v1/
│   │       └── routers/          # API route handlers
│   │           ├── auth.py       # Authentication endpoints
│   │           ├── users.py      # User management endpoints
│   │           ├── hostels.py    # Hostel/Property endpoints
│   │           ├── search.py     # Search functionality endpoints
│   │           ├── recommend.py  # Recommendation endpoints
│   │           └── interactions.py # User interaction tracking
│   ├── crud/                     # Database CRUD operations
│   │   └── user.py               # User CRUD operations
│   ├── db/
│   │   ├── session.py            # Database session management and dependency injection
│   │   └── init.sql              # Initial SQL schema setup
│   ├── deps/
│   │   └── dependencies.py       # FastAPI dependency injection helpers
│   ├── models/
│   │   └── models.py             # SQLModel database models (User, StudentProfile, LandlordProfile, etc.)
│   ├── schemas/
│   │   └── schemas.py            # Pydantic validation schemas
│   ├── services/                 # Business logic and external service integrations
│   │   ├── embeddings.py         # Embedding generation and management
│   │   ├── recommender.py        # Recommendation engine logic
│   │   └── scheduler.py          # Task scheduling utilities
│   └── tasks/                    # Celery background tasks
│       ├── recommender.py        # Recommendation training tasks
│       └── train.py              # Model training tasks
├── alembic/                      # Database migration management
│   ├── versions/                 # Migration scripts
│   ├── env.py                    # Alembic environment configuration
│   └── alembic.ini               # Alembic configuration file
├── tests/                        # Test suite
│   └── test_users.py             # User-related unit tests
├── AGENT.md                      # Agent/AI coding instructions
├── init.py                       # Initialization script
├── requirements.txt              # Python dependencies
├── requirements-ml.txt           # Machine learning specific dependencies
├── README.md                     # Project documentation
└── README2.md                    # Additional documentation
```

### Key Components

- **app/main.py** - FastAPI application entry point with router mounting
- **app/models/models.py** - SQLModel definitions including User, StudentProfile, LandlordProfile, AdminProfile, StudentVerification, LandlordVerification, AdminVerification, Property, and related entities
- **app/api/v1/routers/** - API endpoints organized by feature (auth, users, search, recommend, hostels, interactions)
- **app/services/** - Core business logic for embeddings, recommendations, and scheduling
- **app/tasks/** - Celery background tasks for heavy/long-running operations
- **app/crud/** - Database CRUD helpers
- **alembic/** - Database migrations management

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd xenyou
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   - Ensure you have PostgreSQL installed and running.
   - Create a database for the application.
   - Run the SQL commands in `app/db/init.sql` to initialize the database schema.

5. **Run the Application**
   ```bash
   python init.py
   ```

## Usage

- The API is accessible at `http://localhost:8000`.
- Use the `/api/v1/users` endpoint to interact with user-related functionalities.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.