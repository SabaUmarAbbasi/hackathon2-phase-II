# Todo Application Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-02-05 16:57:00

## Active Technologies

- Backend: FastAPI, SQLModel, Python 3.12
- Database: SQLite (development), PostgreSQL (production)
- Frontend: Next.js 16+, TypeScript, Tailwind CSS
- Authentication: JWT tokens with bcrypt hashing
- Dependencies: 
  - Backend: fastapi, uvicorn, sqlmodel, python-jose[cryptography], passlib[bcrypt], python-dotenv
  - Frontend: next, react, react-dom, typescript, tailwindcss

## Project Structure

```text
.
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
│   │   └── todo.md
│   ├── api/
│   │   └── todo.md
│   ├── database/
│   │   └── todo.md
│   ├── ui/
│   │   └── todo.md
│   ├── todo-plan.md
│   └── todo-tasks.md
├── README.md
├── SUMMARY.md
└── CLAUDE.md
```

## Commands

### Backend
- Start server: `cd backend && python3 start_backend.py`
- Install deps: `cd backend && pip install --break-system-packages -r requirements.txt`

### Frontend
- Install deps: `cd frontend && npm install`
- Start dev server: `cd frontend && npm run dev`

## Code Style

### Python
- Follow PEP 8 guidelines
- Use type hints where possible
- Follow FastAPI/SQLModel conventions

### TypeScript/React
- Use functional components with hooks
- Follow Next.js 16+ App Router patterns
- Use Tailwind CSS utility classes

## Recent Changes

- Multi-user todo application with JWT authentication
- Full CRUD operations for authenticated users
- User data isolation (each user sees only their own todos)
- Responsive UI with Next.js and Tailwind CSS
- Secure authentication with password hashing

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->