# Todo Application

A full-stack todo application with authentication, CRUD operations, and responsive UI.

## Features

- User registration and authentication with JWT tokens
- Create, read, update, and delete todo items
- User-specific data isolation (users only see their own todos)
- Filtering and sorting of todos
- Responsive UI that works on desktop and mobile
- Secure authentication with password hashing

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: SQLModel with SQLite (PostgreSQL in production)
- **Authentication**: JWT tokens with password hashing
- **Dependencies**: 
  - fastapi
  - uvicorn
  - sqlmodel
  - python-jose[cryptography]
  - passlib[bcrypt]
  - python-dotenv

### Frontend
- **Framework**: Next.js 16+
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Custom auth context

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Authenticate user and return JWT token
- `POST /api/auth/logout` - Logout user

### Todos
- `GET /api/todos` - Get all todos for authenticated user
- `POST /api/todos` - Create a new todo
- `GET /api/todos/{id}` - Get a specific todo
- `PUT /api/todos/{id}` - Update a specific todo
- `DELETE /api/todos/{id}` - Delete a specific todo

## Project Structure

```
project/
├── backend/
│   ├── src/
│   │   ├── main.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   └── todo.py
│   │   ├── database/
│   │   │   └── database.py
│   │   ├── auth/
│   │   │   └── auth.py
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   └── todos.py
│   │   └── services/
│   │       └── todo_service.py
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── login/
│   │   │   ├── register/
│   │   │   ├── dashboard/
│   │   │   └── todos/
│   │   ├── components/
│   │   └── lib/
│   │       └── auth.tsx
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   └── tailwind.config.js
├── specs/
│   ├── features/
│   ├── api/
│   ├── database/
│   └── ui/
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install --break-system-packages -r requirements.txt
```

4. Run the backend server:
```bash
python main.py
```

The backend will be available at `http://localhost:8000`.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## Environment Variables

For the backend, create a `.env` file in the backend directory with the following variables:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./todo_app.db
```

## Running Tests

Backend tests can be run with:
```bash
cd backend
python -m pytest
```

## Security Features

- JWT tokens for authentication
- Passwords are hashed using bcrypt
- All API endpoints require authentication
- Users can only access their own data
- Input validation on all endpoints
- SQL injection protection through ORM

## Database Schema

The application uses two main tables:

### users
- id (UUID, primary key)
- email (VARCHAR, unique, not null)
- password_hash (VARCHAR, not null)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

### todos
- id (UUID, primary key)
- title (VARCHAR, not null)
- description (TEXT, optional)
- status (VARCHAR, default 'active')
- user_id (UUID, foreign key to users)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

## API Usage Examples

### Register a new user
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### Create a todo
```bash
curl -X POST http://localhost:8000/api/todos/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"title": "My Todo", "description": "A sample todo", "status": "active"}'
```

### Get all todos
```bash
curl -X GET http://localhost:8000/api/todos/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Frontend Pages

- `/` - Home page (redirects to login or dashboard)
- `/login` - User login page
- `/register` - User registration page
- `/dashboard` - User dashboard with stats
- `/todos` - Todo list page with filtering/sorting
- `/todos/new` - Create new todo page
- `/todos/[id]` - Edit todo page

## Authentication Flow

1. User registers or logs in
2. JWT token is returned and stored locally
3. Token is sent with all authenticated requests
4. Backend validates token on each request
5. User data is scoped to authenticated user only