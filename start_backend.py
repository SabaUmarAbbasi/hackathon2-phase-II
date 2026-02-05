import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Change to the backend directory to make relative imports work
os.chdir(os.path.join(project_root, 'backend'))

# Add the src directory to the path
src_dir = os.path.join(project_root, 'backend', 'src')
sys.path.insert(0, src_dir)

# Import and create database tables first
from backend.src.database.database import create_db_and_tables

# Create the database tables
create_db_and_tables()

# Now import and run the app
from backend.src.main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)