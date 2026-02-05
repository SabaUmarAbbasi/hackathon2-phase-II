import uvicorn
from backend.src.main import app
from backend.src.database.database import create_db_and_tables

if __name__ == "__main__":
    # Create database tables on startup
    create_db_and_tables()
    
    # Run the application
    uvicorn.run(app, host="0.0.0.0", port=8000)