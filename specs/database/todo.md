# Database Specification: Todo Application

**Feature Branch**: `todo-fullstack-app`
**Created**: 2026-02-05
**Status**: Draft

## Database Schema

### Users Table
Stores user account information

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for email lookup (for authentication)
CREATE INDEX idx_users_email ON users(email);
```

### Todos Table
Stores todo items associated with users

```sql
CREATE TABLE todos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'completed')),
    user_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Index for user_id to efficiently query user's todos
CREATE INDEX idx_todos_user_id ON todos(user_id);

-- Index for status to efficiently filter by status
CREATE INDEX idx_todos_status ON todos(status);

-- Composite index for efficient filtering by user and status
CREATE INDEX idx_todos_user_id_status ON todos(user_id, status);

-- Index for sorting by creation date
CREATE INDEX idx_todos_created_at ON todos(created_at);

-- Index for sorting by update date
CREATE INDEX idx_todos_updated_at ON todos(updated_at);
```

## Relationships

- One user can have many todos (one-to-many relationship)
- Todos are linked to users via foreign key constraint
- When a user is deleted, all their todos are automatically deleted (CASCADE)

## Data Types

- UUID: Used for primary keys to ensure global uniqueness
- VARCHAR(255): For titles and emails with reasonable length limits
- TEXT: For descriptions that may be longer
- TIMESTAMP WITH TIME ZONE: For consistent time storage across timezones
- VARCHAR with CHECK constraint: For status field to ensure data integrity

## Constraints

- Unique constraint on user email to prevent duplicate accounts
- NOT NULL constraints on required fields
- Foreign key constraint to maintain referential integrity
- CHECK constraint on status field to ensure valid values only
- Default values for timestamps and status

## Indexing Strategy

- Primary indexes on all ID fields for fast lookups
- Index on user_id for efficient retrieval of user-specific data
- Index on status for filtering operations
- Composite index for combined user and status filtering
- Timestamp indexes for sorting operations

## Security Considerations

- Passwords must be stored as hashed values (never plaintext)
- User data is isolated by user_id in all queries
- Foreign key constraints prevent orphaned records
- Cascade deletion ensures data consistency when users are removed