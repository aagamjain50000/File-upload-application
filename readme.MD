## Built With
List the major frameworks, libraries, and tools used to develop this project:
- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/) for database ORM
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/) 

## Getting Started
To get a local copy up and running, follow these steps:

### Prerequisites
Ensure you have the following installed:
- **Python 3.8+**
- **PostgreSQL**
- **Docker (if using Docker for deployment)**
- **Git**

### Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name



2. **Create a Virtual Environment**
    
    python -m venv venv
    source venv/bin/activate  # On Linux/Mac
    venv\Scripts\activate  # On Windows

3. **Install Dependencies**

    `pip install -r requirements.txt`

4. **Set Up the Database**

    Ensure PostgreSQL is running.
    Create a database:
        `CREATE DATABASE your_database_name;`

5. **Apply Migrations**
    `alembic upgrade head`

### Environment Variables

Create a .env file in the root directory and add the following environment variables:
    `DATABASE_URL=postgresql://username:password@localhost:5432/your_database_name`

### Usage
    
    Run the Development Server

    `uvicorn app.main:app --reload`
    
    The server will be running at http://localhost:8000.

NOTE: API Documentation Visit /docs for automatically generated API documentation via Swagger UI, or /redoc for ReDoc.