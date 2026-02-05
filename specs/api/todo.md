# API Specification: Todo Application

**Feature Branch**: `todo-fullstack-app`
**Created**: 2026-02-05
**Status**: Draft

## Authentication Endpoints

### POST /api/auth/register
Register a new user account

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response**:
- 201 Created: User successfully registered
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "created_at": "2026-02-05T10:00:00Z"
}
```
- 400 Bad Request: Invalid input data
- 409 Conflict: Email already exists

### POST /api/auth/login
Authenticate user and return JWT token

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response**:
- 200 OK: Authentication successful
```json
{
  "access_token": "jwt-token-string",
  "token_type": "bearer",
  "expires_in": 3600
}
```
- 400 Bad Request: Invalid input data
- 401 Unauthorized: Invalid credentials

### POST /api/auth/logout
Logout user and invalidate token

**Headers**:
- Authorization: Bearer {token}

**Response**:
- 200 OK: Successfully logged out
- 401 Unauthorized: Invalid/expired token

## Todo Endpoints

### GET /api/todos
Retrieve all todos for the authenticated user

**Headers**:
- Authorization: Bearer {token}

**Query Parameters**:
- status: Filter by status (optional: "active", "completed")
- sort: Sort by field (optional: "created_at", "updated_at", "title")
- order: Sort order (optional: "asc", "desc", default: "desc")
- limit: Number of results to return (optional, default: 20)
- offset: Number of results to skip (optional, default: 0)

**Response**:
- 200 OK: Successfully retrieved todos
```json
{
  "todos": [
    {
      "id": "uuid-string",
      "title": "Sample Todo",
      "description": "Description of the todo",
      "status": "active",
      "created_at": "2026-02-05T10:00:00Z",
      "updated_at": "2026-02-05T10:00:00Z",
      "user_id": "user-uuid-string"
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0
}
```
- 401 Unauthorized: Invalid/expired token

### POST /api/todos
Create a new todo for the authenticated user

**Headers**:
- Authorization: Bearer {token}

**Request Body**:
```json
{
  "title": "New Todo",
  "description": "Description of the new todo",
  "status": "active"
}
```

**Response**:
- 201 Created: Todo successfully created
```json
{
  "id": "uuid-string",
  "title": "New Todo",
  "description": "Description of the new todo",
  "status": "active",
  "created_at": "2026-02-05T10:00:00Z",
  "updated_at": "2026-02-05T10:00:00Z",
  "user_id": "user-uuid-string"
}
```
- 400 Bad Request: Invalid input data
- 401 Unauthorized: Invalid/expired token

### GET /api/todos/{id}
Retrieve a specific todo by ID

**Headers**:
- Authorization: Bearer {token}

**Parameters**:
- id: UUID of the todo to retrieve

**Response**:
- 200 OK: Todo found and returned
```json
{
  "id": "uuid-string",
  "title": "Sample Todo",
  "description": "Description of the todo",
  "status": "active",
  "created_at": "2026-02-05T10:00:00Z",
  "updated_at": "2026-02-05T10:00:00Z",
  "user_id": "user-uuid-string"
}
```
- 401 Unauthorized: Invalid/expired token
- 404 Not Found: Todo does not exist or belongs to another user

### PUT /api/todos/{id}
Update an existing todo

**Headers**:
- Authorization: Bearer {token}

**Parameters**:
- id: UUID of the todo to update

**Request Body**:
```json
{
  "title": "Updated Todo",
  "description": "Updated description",
  "status": "completed"
}
```

**Response**:
- 200 OK: Todo successfully updated
```json
{
  "id": "uuid-string",
  "title": "Updated Todo",
  "description": "Updated description",
  "status": "completed",
  "created_at": "2026-02-05T10:00:00Z",
  "updated_at": "2026-02-05T11:00:00Z",
  "user_id": "user-uuid-string"
}
```
- 400 Bad Request: Invalid input data
- 401 Unauthorized: Invalid/expired token
- 404 Not Found: Todo does not exist or belongs to another user

### DELETE /api/todos/{id}
Delete a specific todo

**Headers**:
- Authorization: Bearer {token}

**Parameters**:
- id: UUID of the todo to delete

**Response**:
- 204 No Content: Todo successfully deleted
- 401 Unauthorized: Invalid/expired token
- 404 Not Found: Todo does not exist or belongs to another user

## Error Response Format

All error responses follow this format:
```json
{
  "detail": "Human-readable error message"
}
```

## Authentication Requirements

- All `/api/todos/*` endpoints require a valid JWT token in the Authorization header
- Unauthorized requests return 401 status code
- Tokens must be validated on every request to ensure they are not expired
- Requests must be scoped to the authenticated user only