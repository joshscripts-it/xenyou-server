# Xenyou - AI-First Apartment Matching Platform

Xenyou is a next-generation, AI-first apartment matching platform designed to connect college students with landlords. This project leverages FastAPI for building a robust API and PostgreSQL for managing user data.

## Project Structure

```
xenyou
├── app
│   ├── main.py                # Entry point of the FastAPI application
│   ├── api
│   │   └── v1
│   │       └── users.py       # User-related API endpoints
│   ├── core
│   │   └── config.py          # Configuration settings
│   ├── db
│   │   ├── session.py         # Database session management
│   │   └── init.sql           # SQL commands for database initialization
│   ├── models
│   │   └── user.py            # User model definition
│   ├── schemas
│   │   └── user.py            # Pydantic schemas for user data
│   ├── crud
│   │   └── user.py            # CRUD operations for User model
│   └── deps
│       └── dependencies.py     # Dependency functions for route handlers
├── alembic
│   ├── versions                # Migration scripts for database schema changes
│   └── env.py                 # Alembic environment configuration
├── tests
│   └── test_users.py          # Unit tests for user-related API endpoints
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Project configuration file
└── README.md                  # Project documentation
```

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
   uvicorn app.main:app --reload
   ```

## Usage

- The API is accessible at `http://localhost:8000`.
- Use the `/api/v1/users` endpoint to interact with user-related functionalities.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.