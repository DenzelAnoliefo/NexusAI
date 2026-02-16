# NexusChat — Product Requirements Document

> Real-Time Chat Application
> Author: Denzel Anoliefo
> Date: February 16, 2026
> Status: Planning

---

## Table of Contents

1. [Tech Stack & Justification](#1-tech-stack--justification)
2. [System Architecture Overview](#2-system-architecture-overview)
3. [Data Models & Schema Design](#3-data-models--schema-design)
4. [API Specification](#4-api-specification)
5. [WebSocket Protocol Specification](#5-websocket-protocol-specification)
6. [Authentication & Authorization](#6-authentication--authorization)
7. [Frontend Architecture](#7-frontend-architecture)
8. [Feature Specifications](#8-feature-specifications)
9. [Non-Functional Requirements](#9-non-functional-requirements)
10. [Engineering Execution Plan](#10-engineering-execution-plan)

---

## 1. Tech Stack & Justification

### Frontend

| Technology | Purpose | Why |
|---|---|---|
| **React 18+** | UI framework | #1 most in-demand frontend framework (~57% market share, ~126K job listings). Non-negotiable for full-stack roles. |
| **TypeScript** | Type safety | Expected in 80%+ of modern frontend roles. Shows engineering maturity. |
| **Vite** | Build tool / dev server | Industry standard for React SPAs. Sub-second HMR, faster than CRA/Webpack. |
| **TailwindCSS** | Styling | Dominant utility-first CSS framework. Faster development than CSS modules or styled-components. |
| **React Router v6** | Client-side routing | Standard routing library for React SPAs. |
| **Zustand** | Client state management | Lightweight, minimal boilerplate. Preferred over Redux for small-to-mid apps. Shows you know modern alternatives. |
| **TanStack Query (React Query)** | Server state management | Industry standard for data fetching, caching, and synchronization. Separates server state from client state. |
| **Socket.IO Client** | WebSocket abstraction | Auto-reconnection, event-based API, room support, fallback transports. Pairs with python-socketio on backend. |
| **React Hook Form + Zod** | Form handling + validation | Performant forms (uncontrolled components), schema-based validation shared with backend concepts. |
| **Vitest + React Testing Library** | Testing | Vitest is Vite-native (fast), RTL is the React testing standard. |

### Backend

| Technology | Purpose | Why |
|---|---|---|
| **FastAPI** | Web framework | You already have it. Tier 2 and surging in demand (especially AI/ML-adjacent roles). Async-native, auto-generates OpenAPI docs, excellent WebSocket support. Differentiates you from the "every bootcamp grad uses Express" crowd. |
| **Python 3.13** | Language | You already have it. Python + TypeScript across the stack shows cross-language versatility. |
| **python-socketio** | Real-time server | Socket.IO server implementation for Python. Integrates with FastAPI's ASGI server. Gives you rooms, namespaces, auto-reconnection — the same real-time primitives the industry uses. |
| **SQLAlchemy 2.0 (async)** | ORM | Industry-standard Python ORM. Async mode pairs perfectly with FastAPI's async architecture. |
| **Alembic** | Database migrations | The migration tool for SQLAlchemy. Lets you version-control your schema changes. |
| **Pydantic v2** | Data validation / serialization | Already included with FastAPI. Used for request/response schemas, settings management, and data validation. |
| **Passlib + bcrypt** | Password hashing | Industry standard. bcrypt is the recommended hashing algorithm. |
| **python-jose** | JWT tokens | JWT encoding/decoding for stateless authentication. |
| **Redis (via redis-py with async)** | Caching, sessions, pub/sub | In-memory data store. Used for: (1) caching user/room data, (2) Socket.IO adapter for multi-process WebSocket scaling, (3) online presence tracking. |
| **Uvicorn** | ASGI server | You already have it. Production-grade async server for FastAPI. |
| **pytest + httpx** | Testing | pytest is the Python testing standard. httpx provides async test client for FastAPI. |

### Database

| Technology | Purpose | Why |
|---|---|---|
| **PostgreSQL 16** | Primary database | #1 most popular database for new projects. ACID-compliant, supports JSON columns, full-text search, excellent at relational data. |
| **Redis 7** | Cache + real-time layer | See above. Every production stack uses Redis. |

### DevOps / Infrastructure

| Technology | Purpose | Why |
|---|---|---|
| **Docker** | Containerization | 92% adoption. Expected knowledge for full-stack roles in 2026. |
| **Docker Compose** | Multi-container orchestration | Run PostgreSQL, Redis, backend, and frontend with one command. |
| **GitHub Actions** | CI/CD | Most popular CI/CD platform. Automate tests, linting, and builds on every push. |
| **Nginx** | Reverse proxy | Production-grade proxy. Routes HTTP and WebSocket traffic. Serves static frontend files. |

### Project Structure (Final)

```
NexusAI/
├── docker-compose.yml
├── .github/
│   └── workflows/
│       └── ci.yml
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── alembic/
│   │   └── versions/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app factory, Socket.IO mount
│   │   ├── config.py            # Pydantic Settings (env vars)
│   │   ├── database.py          # Async SQLAlchemy engine + session
│   │   ├── dependencies.py      # Dependency injection (get_db, get_current_user)
│   │   ├── models/              # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── room.py
│   │   │   ├── message.py
│   │   │   └── room_member.py
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── room.py
│   │   │   ├── message.py
│   │   │   └── auth.py
│   │   ├── routers/             # REST API route handlers
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── rooms.py
│   │   │   └── messages.py
│   │   ├── services/            # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── user_service.py
│   │   │   ├── room_service.py
│   │   │   └── message_service.py
│   │   ├── sockets/             # Socket.IO event handlers
│   │   │   ├── __init__.py
│   │   │   └── chat.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── security.py      # JWT helpers, password hashing
│   └── tests/
│       ├── conftest.py
│       ├── test_auth.py
│       ├── test_users.py
│       ├── test_rooms.py
│       └── test_messages.py
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.ts
│   ├── index.html
│   ├── public/
│   └── src/
│       ├── main.tsx             # React entry point
│       ├── App.tsx              # Root component + router
│       ├── api/                 # API client (axios/fetch wrappers)
│       │   ├── client.ts        # Base HTTP client with interceptors
│       │   ├── auth.ts
│       │   ├── users.ts
│       │   ├── rooms.ts
│       │   └── messages.ts
│       ├── hooks/               # Custom React hooks
│       │   ├── useAuth.ts
│       │   ├── useSocket.ts
│       │   ├── useChat.ts
│       │   └── useOnlineStatus.ts
│       ├── stores/              # Zustand stores
│       │   ├── authStore.ts
│       │   └── chatStore.ts
│       ├── components/          # Reusable UI components
│       │   ├── ui/              # Generic (Button, Input, Avatar, Modal, etc.)
│       │   ├── chat/            # Chat-specific (MessageBubble, MessageInput, etc.)
│       │   └── layout/          # Layout (Sidebar, Header, etc.)
│       ├── pages/               # Route-level page components
│       │   ├── LoginPage.tsx
│       │   ├── RegisterPage.tsx
│       │   ├── ChatPage.tsx
│       │   └── SettingsPage.tsx
│       ├── lib/                 # Utilities
│       │   ├── socket.ts        # Socket.IO client singleton
│       │   ├── utils.ts
│       │   └── constants.ts
│       ├── types/               # TypeScript type definitions
│       │   └── index.ts
│       └── tests/
│           └── ...
└── nginx/
    └── nginx.conf
```

---

## 2. System Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT (Browser)                      │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              React SPA (TypeScript + Vite)             │  │
│  │                                                        │  │
│  │  ┌──────────┐  ┌──────────────┐  ┌────────────────┐  │  │
│  │  │  Zustand  │  │ TanStack     │  │  Socket.IO     │  │  │
│  │  │  Store    │  │ Query Cache  │  │  Client        │  │  │
│  │  └──────────┘  └──────────────┘  └───────┬────────┘  │  │
│  └──────────────────────────────────────────┼────────────┘  │
│                    HTTP REST │               │ WebSocket     │
└────────────────────────────┼───────────────┼────────────────┘
                             │               │
                    ┌────────▼───────────────▼────────┐
                    │          Nginx (Reverse Proxy)   │
                    │   :80 → frontend static files    │
                    │   /api/* → backend :8000          │
                    │   /socket.io/* → backend :8000    │
                    └────────┬───────────────┬────────┘
                             │               │
                    ┌────────▼───────────────▼────────┐
                    │     FastAPI + python-socketio     │
                    │          (Uvicorn ASGI)           │
                    │                                   │
                    │  ┌─────────┐  ┌───────────────┐  │
                    │  │  REST   │  │  Socket.IO     │  │
                    │  │ Routes  │  │  Events        │  │
                    │  └────┬────┘  └──────┬────────┘  │
                    │       │              │            │
                    │  ┌────▼──────────────▼────────┐  │
                    │  │     Service Layer           │  │
                    │  └────┬──────────────┬────────┘  │
                    └───────┼──────────────┼───────────┘
                            │              │
               ┌────────────▼──┐    ┌──────▼──────────┐
               │  PostgreSQL   │    │     Redis        │
               │               │    │                  │
               │  - users      │    │  - session cache │
               │  - rooms      │    │  - online users  │
               │  - messages   │    │  - Socket.IO     │
               │  - members    │    │    adapter        │
               └───────────────┘    └─────────────────┘
```

### Request Flow: Sending a Message

```
1. User types message in <MessageInput />
2. Component calls socket.emit("send_message", { room_id, content })
3. Socket.IO client sends WebSocket frame to server
4. Nginx proxies /socket.io/* to FastAPI backend
5. python-socketio receives "send_message" event
6. Server-side handler:
   a. Validates the JWT token from the socket session
   b. Calls message_service.create_message(user_id, room_id, content)
   c. Service layer inserts row into PostgreSQL via SQLAlchemy
   d. Service returns the created Message object
   e. Handler emits "new_message" to all clients in the Socket.IO room
7. All connected clients in that room receive "new_message" event
8. React components update via Zustand store or direct state
9. <MessageBubble /> renders the new message with sender info and timestamp
```

### Request Flow: Loading Chat History (REST)

```
1. User navigates to a room → ChatPage mounts
2. TanStack Query fires GET /api/rooms/{room_id}/messages?cursor=...&limit=50
3. Nginx proxies to FastAPI
4. FastAPI auth dependency extracts + validates JWT from Authorization header
5. Router calls message_service.get_messages(room_id, cursor, limit)
6. Service queries PostgreSQL with cursor-based pagination (WHERE id < cursor ORDER BY id DESC LIMIT 50)
7. Returns serialized messages via Pydantic schema
8. TanStack Query caches the response, component renders message list
9. User scrolls up → triggers next page fetch (infinite scroll)
```

---

## 3. Data Models & Schema Design

### Entity Relationship Diagram

```
┌──────────────┐       ┌──────────────────┐       ┌──────────────┐
│    users     │       │   room_members   │       │    rooms     │
├──────────────┤       ├──────────────────┤       ├──────────────┤
│ id (PK)      │──┐    │ id (PK)          │    ┌──│ id (PK)      │
│ email        │  │    │ user_id (FK)     │────┘  │ name         │
│ username     │  └───▶│ room_id (FK)     │───────│ description  │
│ display_name │       │ role             │       │ is_direct    │
│ avatar_url   │       │ joined_at        │       │ created_by   │
│ password_hash│       │ last_read_at     │       │ created_at   │
│ is_online    │       └──────────────────┘       │ updated_at   │
│ last_seen_at │                                   └──────────────┘
│ created_at   │                                          │
│ updated_at   │       ┌──────────────────┐               │
└──────────────┘       │    messages      │               │
        │              ├──────────────────┤               │
        │              │ id (PK)          │               │
        └─────────────▶│ sender_id (FK)   │               │
                       │ room_id (FK)     │◀──────────────┘
                       │ content          │
                       │ message_type     │
                       │ parent_id (FK)   │──┐ (self-referencing
                       │ is_edited        │  │  for replies)
                       │ created_at       │  │
                       │ updated_at       │──┘
                       └──────────────────┘
```

### Table: `users`

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PK, default gen_random_uuid() | Unique user identifier |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | User's email address |
| `username` | VARCHAR(50) | UNIQUE, NOT NULL, INDEX | Unique handle (e.g., @denzel) |
| `display_name` | VARCHAR(100) | NOT NULL | Display name shown in chat |
| `avatar_url` | VARCHAR(500) | NULLABLE | URL to profile picture |
| `password_hash` | VARCHAR(255) | NOT NULL | bcrypt-hashed password |
| `is_online` | BOOLEAN | DEFAULT false | Current online status |
| `last_seen_at` | TIMESTAMP(tz) | NULLABLE | Last activity timestamp |
| `created_at` | TIMESTAMP(tz) | DEFAULT now(), NOT NULL | Account creation time |
| `updated_at` | TIMESTAMP(tz) | DEFAULT now(), NOT NULL | Last profile update |

### Table: `rooms`

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PK, default gen_random_uuid() | Unique room identifier |
| `name` | VARCHAR(100) | NOT NULL | Room display name |
| `description` | VARCHAR(500) | NULLABLE | Room description/topic |
| `is_direct` | BOOLEAN | DEFAULT false, NOT NULL | True = 1-on-1 DM, False = group room |
| `created_by` | UUID | FK → users.id, NOT NULL | User who created the room |
| `created_at` | TIMESTAMP(tz) | DEFAULT now(), NOT NULL | Room creation time |
| `updated_at` | TIMESTAMP(tz) | DEFAULT now(), NOT NULL | Last update |

### Table: `room_members`

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PK, default gen_random_uuid() | Unique membership identifier |
| `user_id` | UUID | FK → users.id, NOT NULL | The member |
| `room_id` | UUID | FK → rooms.id, NOT NULL | The room |
| `role` | VARCHAR(20) | DEFAULT 'member', NOT NULL | 'owner', 'admin', 'member' |
| `joined_at` | TIMESTAMP(tz) | DEFAULT now(), NOT NULL | When user joined |
| `last_read_at` | TIMESTAMP(tz) | NULLABLE | Last message the user has read (for unread counts) |

**Unique constraint:** `(user_id, room_id)` — a user can only be in a room once.

### Table: `messages`

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PK, default gen_random_uuid() | Unique message identifier |
| `sender_id` | UUID | FK → users.id, NOT NULL | Who sent it |
| `room_id` | UUID | FK → rooms.id, NOT NULL, INDEX | Which room it belongs to |
| `content` | TEXT | NOT NULL | Message body (plaintext, max 5000 chars enforced at app layer) |
| `message_type` | VARCHAR(20) | DEFAULT 'text', NOT NULL | 'text', 'image', 'system' (e.g., "User joined") |
| `parent_id` | UUID | FK → messages.id, NULLABLE | If this is a reply, points to the parent message |
| `is_edited` | BOOLEAN | DEFAULT false | Whether the message has been edited |
| `created_at` | TIMESTAMP(tz) | DEFAULT now(), NOT NULL, INDEX | When the message was sent |
| `updated_at` | TIMESTAMP(tz) | DEFAULT now(), NOT NULL | Last edit time |

**Index:** Composite index on `(room_id, created_at DESC)` — this is the primary query pattern for loading chat history.

---

## 4. API Specification

### Base URL: `/api/v1`

All endpoints return JSON. All authenticated endpoints require `Authorization: Bearer <token>` header.

---

### Authentication Endpoints

#### `POST /api/v1/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "email": "denzel@example.com",
  "username": "denzel",
  "display_name": "Denzel Anoliefo",
  "password": "SecurePass123!"
}
```

**Validation Rules:**
- `email`: Valid email format, max 255 chars, must be unique
- `username`: 3-50 chars, alphanumeric + underscores only, must be unique
- `display_name`: 1-100 chars
- `password`: Min 8 chars, at least 1 uppercase, 1 lowercase, 1 digit

**Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "denzel@example.com",
  "username": "denzel",
  "display_name": "Denzel Anoliefo",
  "avatar_url": null,
  "created_at": "2026-02-16T12:00:00Z"
}
```

**Error Responses:**
- `400` — Validation error (weak password, invalid email format)
- `409` — Email or username already taken

---

#### `POST /api/v1/auth/login`

Authenticate and receive JWT tokens.

**Request Body:**
```json
{
  "email": "denzel@example.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-...",
    "email": "denzel@example.com",
    "username": "denzel",
    "display_name": "Denzel Anoliefo",
    "avatar_url": null
  }
}
```

**Token Details:**
- `access_token`: Expires in 30 minutes. Used for all authenticated requests.
- `refresh_token`: Expires in 7 days. Used only to get a new access token.

**Error Responses:**
- `401` — Invalid email or password

---

#### `POST /api/v1/auth/refresh`

Get a new access token using a valid refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401` — Invalid or expired refresh token

---

### User Endpoints

#### `GET /api/v1/users/me`

Get the currently authenticated user's profile.

**Auth:** Required

**Response (200 OK):**
```json
{
  "id": "550e8400-...",
  "email": "denzel@example.com",
  "username": "denzel",
  "display_name": "Denzel Anoliefo",
  "avatar_url": null,
  "is_online": true,
  "last_seen_at": "2026-02-16T12:00:00Z",
  "created_at": "2026-02-16T12:00:00Z"
}
```

---

#### `PATCH /api/v1/users/me`

Update the current user's profile.

**Auth:** Required

**Request Body (all fields optional):**
```json
{
  "display_name": "Denzel A.",
  "avatar_url": "https://..."
}
```

**Response (200 OK):** Updated user object.

---

#### `GET /api/v1/users/search?q=denzel`

Search for users by username or display name (for adding people to rooms).

**Auth:** Required

**Query Parameters:**
- `q` (string, required): Search query, min 2 chars
- `limit` (int, optional): Max results, default 20, max 50

**Response (200 OK):**
```json
[
  {
    "id": "550e8400-...",
    "username": "denzel",
    "display_name": "Denzel Anoliefo",
    "avatar_url": null,
    "is_online": true
  }
]
```

---

### Room Endpoints

#### `POST /api/v1/rooms`

Create a new chat room.

**Auth:** Required

**Request Body:**
```json
{
  "name": "CS Project Team",
  "description": "Discussion for our capstone project",
  "is_direct": false,
  "member_ids": ["user-uuid-1", "user-uuid-2"]
}
```

**For direct messages (1-on-1):**
```json
{
  "is_direct": true,
  "member_ids": ["other-user-uuid"]
}
```

When `is_direct` is true:
- `name` is auto-generated (the other user's display name)
- `member_ids` must contain exactly 1 user ID (the other person)
- If a DM room already exists between these two users, return the existing room instead of creating a duplicate

**Response (201 Created):**
```json
{
  "id": "room-uuid",
  "name": "CS Project Team",
  "description": "Discussion for our capstone project",
  "is_direct": false,
  "created_by": "user-uuid",
  "members": [
    { "id": "user-uuid", "username": "denzel", "display_name": "Denzel Anoliefo", "role": "owner" },
    { "id": "user-uuid-1", "username": "alice", "display_name": "Alice", "role": "member" }
  ],
  "created_at": "2026-02-16T12:00:00Z"
}
```

---

#### `GET /api/v1/rooms`

List all rooms the current user is a member of.

**Auth:** Required

**Response (200 OK):**
```json
[
  {
    "id": "room-uuid",
    "name": "CS Project Team",
    "is_direct": false,
    "last_message": {
      "content": "Hey, anyone working on the report?",
      "sender_username": "alice",
      "created_at": "2026-02-16T14:30:00Z"
    },
    "unread_count": 3,
    "member_count": 5
  }
]
```

**Sorting:** Rooms are sorted by `last_message.created_at DESC` (most recently active rooms first). Rooms with no messages appear at the end, sorted by `created_at DESC`.

---

#### `GET /api/v1/rooms/{room_id}`

Get details of a specific room.

**Auth:** Required (must be a member of the room)

**Response (200 OK):**
```json
{
  "id": "room-uuid",
  "name": "CS Project Team",
  "description": "Discussion for our capstone project",
  "is_direct": false,
  "created_by": "user-uuid",
  "members": [
    { "id": "user-uuid", "username": "denzel", "display_name": "Denzel Anoliefo", "role": "owner", "is_online": true }
  ],
  "created_at": "2026-02-16T12:00:00Z"
}
```

**Error Responses:**
- `403` — User is not a member of this room
- `404` — Room not found

---

#### `POST /api/v1/rooms/{room_id}/members`

Add a member to a room.

**Auth:** Required (must be 'owner' or 'admin' of the room)

**Request Body:**
```json
{
  "user_id": "new-member-uuid"
}
```

**Response (201 Created):** Updated members list.

**Error Responses:**
- `403` — Insufficient permissions
- `409` — User is already a member

---

#### `DELETE /api/v1/rooms/{room_id}/members/{user_id}`

Remove a member from a room (or leave the room if user_id is self).

**Auth:** Required (owner/admin to remove others, any member to leave)

**Response (204 No Content)**

---

### Message Endpoints

#### `GET /api/v1/rooms/{room_id}/messages`

Get message history for a room (cursor-based pagination).

**Auth:** Required (must be a member)

**Query Parameters:**
- `cursor` (UUID, optional): Message ID to paginate from (returns messages BEFORE this one)
- `limit` (int, optional): Number of messages, default 50, max 100

**Response (200 OK):**
```json
{
  "messages": [
    {
      "id": "msg-uuid",
      "sender": {
        "id": "user-uuid",
        "username": "denzel",
        "display_name": "Denzel Anoliefo",
        "avatar_url": null
      },
      "content": "Hey everyone!",
      "message_type": "text",
      "parent_id": null,
      "is_edited": false,
      "created_at": "2026-02-16T14:30:00Z"
    }
  ],
  "next_cursor": "older-msg-uuid-or-null",
  "has_more": true
}
```

**Why cursor-based pagination over offset-based:**
- Offset-based breaks when new messages are inserted (items shift, causing duplicates or skips)
- Cursor-based is stable: "give me 50 messages older than this message ID"
- More performant with large datasets (uses index seek instead of OFFSET scan)

---

#### `PATCH /api/v1/rooms/{room_id}/messages/{message_id}`

Edit a message.

**Auth:** Required (must be the sender of the message)

**Request Body:**
```json
{
  "content": "Updated message content"
}
```

**Response (200 OK):** Updated message object with `is_edited: true`.

**Side Effects:**
- Emits `message_edited` Socket.IO event to all room members

---

#### `DELETE /api/v1/rooms/{room_id}/messages/{message_id}`

Delete a message.

**Auth:** Required (must be sender, or room owner/admin)

**Response (204 No Content)**

**Side Effects:**
- Emits `message_deleted` Socket.IO event to all room members

---

#### `POST /api/v1/rooms/{room_id}/read`

Mark all messages in a room as read (updates `last_read_at` on the room_members row).

**Auth:** Required (must be a member)

**Response (200 OK):**
```json
{
  "last_read_at": "2026-02-16T15:00:00Z"
}
```

---

## 5. WebSocket Protocol Specification

### Connection

```
Socket.IO endpoint: /socket.io/
Transport: WebSocket (with HTTP long-polling fallback)
Authentication: JWT token passed during connection handshake
```

**Connection Handshake:**
```javascript
const socket = io("http://localhost:8000", {
  auth: {
    token: "eyJhbGciOiJIUzI1NiIs..."
  }
});
```

**Server-side connection handler:**
1. Extract JWT from `auth.token`
2. Decode and validate the token
3. If invalid → disconnect with error
4. If valid → store user_id in the socket session
5. Mark user as online in Redis
6. Join the user into all their Socket.IO rooms (one room per chat room they're a member of)
7. Broadcast `user_online` event to all rooms the user is in

---

### Client → Server Events

#### `send_message`

```json
{
  "room_id": "room-uuid",
  "content": "Hello everyone!",
  "parent_id": null
}
```

**Server actions:**
1. Validate user is a member of the room
2. Validate content (non-empty, max 5000 chars)
3. Persist to PostgreSQL
4. Emit `new_message` to the room

---

#### `typing_start`

```json
{
  "room_id": "room-uuid"
}
```

**Server actions:**
1. Broadcast `user_typing` to the room (excluding the sender)
2. Auto-expires after 3 seconds if no `typing_start` is re-emitted

---

#### `typing_stop`

```json
{
  "room_id": "room-uuid"
}
```

**Server actions:**
1. Broadcast `user_stop_typing` to the room (excluding the sender)

---

#### `mark_read`

```json
{
  "room_id": "room-uuid"
}
```

**Server actions:**
1. Update `last_read_at` in `room_members`
2. Optionally emit `read_receipt` to the room

---

### Server → Client Events

#### `new_message`

Emitted to all members of a room when a new message is sent.

```json
{
  "id": "msg-uuid",
  "sender": {
    "id": "user-uuid",
    "username": "denzel",
    "display_name": "Denzel Anoliefo",
    "avatar_url": null
  },
  "room_id": "room-uuid",
  "content": "Hello everyone!",
  "message_type": "text",
  "parent_id": null,
  "is_edited": false,
  "created_at": "2026-02-16T14:30:00Z"
}
```

---

#### `message_edited`

```json
{
  "id": "msg-uuid",
  "room_id": "room-uuid",
  "content": "Updated content",
  "is_edited": true,
  "updated_at": "2026-02-16T14:35:00Z"
}
```

---

#### `message_deleted`

```json
{
  "id": "msg-uuid",
  "room_id": "room-uuid"
}
```

---

#### `user_typing`

```json
{
  "user_id": "user-uuid",
  "username": "denzel",
  "room_id": "room-uuid"
}
```

---

#### `user_stop_typing`

```json
{
  "user_id": "user-uuid",
  "room_id": "room-uuid"
}
```

---

#### `user_online`

```json
{
  "user_id": "user-uuid",
  "username": "denzel"
}
```

---

#### `user_offline`

```json
{
  "user_id": "user-uuid",
  "username": "denzel",
  "last_seen_at": "2026-02-16T15:00:00Z"
}
```

---

#### `error`

```json
{
  "message": "You are not a member of this room",
  "code": "FORBIDDEN"
}
```

---

## 6. Authentication & Authorization

### Authentication Flow

```
┌──────────┐     POST /auth/login       ┌──────────┐
│  Client   │ ──────────────────────────▶│  Server  │
│           │     { email, password }     │          │
│           │                             │          │
│           │   200 { access_token,       │          │
│           │◀──── refresh_token, user }  │          │
│           │                             │          │
│  Stores tokens in memory (access)      │          │
│  and httpOnly cookie (refresh)          │          │
│           │                             │          │
│           │   GET /api/v1/rooms         │          │
│           │──────────────────────────▶  │          │
│           │   Authorization: Bearer AT  │          │
│           │                             │ Decode   │
│           │                             │ Validate │
│           │   200 { rooms: [...] }      │ Extract  │
│           │◀──────────────────────────  │ user_id  │
│           │                             │          │
│  ... 30 min later, AT expires ...       │          │
│           │                             │          │
│           │   GET /api/v1/rooms         │          │
│           │──────────────────────────▶  │          │
│           │   Authorization: Bearer AT  │          │
│           │                             │          │
│           │   401 { token expired }     │          │
│           │◀──────────────────────────  │          │
│           │                             │          │
│  Axios interceptor catches 401          │          │
│           │                             │          │
│           │   POST /auth/refresh        │          │
│           │──────────────────────────▶  │          │
│           │   { refresh_token: RT }     │          │
│           │                             │          │
│           │   200 { access_token: newAT}│          │
│           │◀──────────────────────────  │          │
│           │                             │          │
│  Retries original request with newAT    │          │
└──────────┘                             └──────────┘
```

### JWT Payload Structure

**Access Token:**
```json
{
  "sub": "user-uuid",
  "type": "access",
  "exp": 1708099200,
  "iat": 1708097400
}
```

**Refresh Token:**
```json
{
  "sub": "user-uuid",
  "type": "refresh",
  "exp": 1708702200,
  "iat": 1708097400
}
```

### Authorization Rules

| Resource | Action | Who Can Do It |
|---|---|---|
| Room | Create | Any authenticated user |
| Room | View details | Room members only |
| Room | Add members | Room owner or admin |
| Room | Remove members | Room owner or admin |
| Room | Leave | Any member (owner must transfer ownership first) |
| Message | Send | Room members only |
| Message | Edit | Original sender only |
| Message | Delete | Original sender, or room owner/admin |
| User profile | View | Any authenticated user |
| User profile | Edit | Self only |

---

## 7. Frontend Architecture

### Page Structure & Routing

```
/login              → LoginPage (public)
/register           → RegisterPage (public)
/chat               → ChatPage (protected — redirects to /login if not authenticated)
/chat/:roomId       → ChatPage with specific room open (protected)
/settings           → SettingsPage (protected)
```

### ChatPage Layout (Main Application Shell)

```
┌─────────────────────────────────────────────────────────────────────┐
│  Header Bar                                                [avatar] │
├───────────────┬─────────────────────────────────────────────────────┤
│               │  Room Header: "CS Project Team"  [members] [info]  │
│  Sidebar      ├─────────────────────────────────────────────────────┤
│               │                                                     │
│  [Search]     │                                                     │
│               │              Message Area                           │
│  ● General    │                                                     │
│    CS Project │  ┌──────────────────────────────────────────┐      │
│  ● Alice (DM) │  │  [avatar] Alice              2:30 PM     │      │
│    Bob (DM)   │  │  Hey, anyone working on the report?       │      │
│               │  └──────────────────────────────────────────┘      │
│               │  ┌──────────────────────────────────────────┐      │
│               │  │  [avatar] Denzel             2:31 PM     │      │
│               │  │  Yeah, I just pushed the new API endpoints│      │
│               │  └──────────────────────────────────────────┘      │
│               │                                                     │
│               │  Alice is typing...                                 │
│               ├─────────────────────────────────────────────────────┤
│               │  [Message Input Box                        ] [Send] │
│  [+ New Room] │                                                     │
└───────────────┴─────────────────────────────────────────────────────┘
```

### Component Tree (ChatPage)

```
<ChatPage>
  <Sidebar>
    <SearchBar />
    <RoomList>
      <RoomListItem />    ← one per room, shows name + last message + unread badge
      <RoomListItem />
      ...
    </RoomList>
    <CreateRoomButton />
  </Sidebar>
  <ChatArea>
    <RoomHeader />        ← room name, member avatars, info button
    <MessageList>
      <DateDivider />     ← "February 16, 2026"
      <MessageBubble />   ← individual message with avatar, name, time, content
      <MessageBubble />
      ...
      <TypingIndicator /> ← "Alice is typing..."
    </MessageList>
    <MessageInput />      ← text input + send button
  </ChatArea>
</ChatPage>
```

### State Management Strategy

**Zustand Store (Client State):**
- `authStore`: Current user, tokens, login/logout actions
- `chatStore`: Active room ID, typing users per room, Socket.IO connection status

**TanStack Query (Server State):**
- Room list (with automatic refetching)
- Message history per room (with infinite scroll pagination)
- User search results
- Room details + members

**Why this split:**
- Client state (auth, UI state) doesn't come from the server and doesn't need caching/refetching
- Server state (rooms, messages, users) benefits from TanStack Query's caching, background refetching, and optimistic updates
- This separation is a modern best practice that interviewers look for

### Real-Time Updates Strategy

When a `new_message` Socket.IO event arrives:
1. `useSocket` hook receives the event
2. If the message is for the currently active room → append it to the TanStack Query cache for that room's messages (using `queryClient.setQueryData`)
3. If the message is for a different room → update the room list to show the new last message and increment the unread count
4. Play notification sound if the window is not focused

When a `user_typing` event arrives:
1. Add the user to `chatStore.typingUsers[roomId]`
2. Set a 3-second timeout to remove them (auto-clear if no follow-up typing event)

---

## 8. Feature Specifications

### F1: User Registration & Login

**Registration Form Fields:**
- Email (validated, unique check on blur via debounced API call)
- Username (validated, unique check on blur)
- Display Name
- Password (strength indicator: weak/medium/strong)
- Confirm Password

**Login Form Fields:**
- Email
- Password
- "Remember me" checkbox (extends refresh token to 30 days)

**Post-Login:**
- Store access token in Zustand (memory — cleared on tab close)
- Store refresh token in memory as well (or httpOnly cookie if you add a BFF layer later)
- Redirect to `/chat`
- Establish Socket.IO connection

---

### F2: Room Management

**Create Room Modal:**
- Room name input
- Description input (optional)
- User search + multi-select to add initial members
- "Create" button

**Room Info Panel (slide-out):**
- Room name and description
- Member list with roles (owner/admin/member)
- "Add Member" button (owner/admin only)
- "Leave Room" button
- "Remove Member" button next to each member (owner/admin only)

---

### F3: Real-Time Messaging

**Sending Messages:**
- Type in input box, press Enter (or click Send) to send
- Shift+Enter for newline
- Max 5000 characters (show character count near limit)
- Optimistic UI: message appears instantly in the UI, gets confirmed when server responds

**Receiving Messages:**
- Messages appear in real-time via Socket.IO
- Auto-scroll to bottom when new message arrives (only if user is already at bottom; if scrolled up reading history, show a "New messages ↓" button instead)

**Message Display:**
- Group consecutive messages from the same sender (don't repeat avatar/name for each)
- Show relative timestamps ("2 min ago") that update, with full timestamp on hover
- Different alignment/styling for own messages vs. others

---

### F4: Message History & Infinite Scroll

- Load most recent 50 messages when entering a room
- Scroll up to load older messages (infinite scroll with cursor-based pagination)
- Show a loading spinner while fetching older messages
- Show "Beginning of conversation" when no more messages exist
- Date dividers between messages from different days

---

### F5: Typing Indicators

- Show "Alice is typing..." below the message list
- If multiple people: "Alice and Bob are typing..." or "3 people are typing..."
- Debounce: emit `typing_start` on keypress, but no more than once per 2 seconds
- Auto-clear after 3 seconds of no typing

---

### F6: Online Presence

- Green dot on avatar = online
- Gray dot = offline
- "Last seen 5 min ago" in user profile / room member list
- Online status tracked via Redis (SET with TTL)
- On Socket.IO connect → mark online, broadcast to rooms
- On Socket.IO disconnect → mark offline, broadcast to rooms

---

### F7: Unread Message Counts

- Each room in the sidebar shows an unread badge (e.g., "3")
- Calculated as: count of messages in room WHERE created_at > room_members.last_read_at
- When user opens a room → call `POST /rooms/{id}/read` → badge clears
- Real-time update: when a new message arrives for a non-active room, increment the badge

---

### F8: Direct Messages (1-on-1)

- DM rooms are created via user search
- In the sidebar, DMs show the other user's name and avatar (not a room name)
- DM rooms show online status of the other user in the header
- No duplicate DMs: if a DM room already exists between two users, reuse it

---

### F9: Message Replies (Threading)

- Hover over a message → "Reply" button appears
- Clicking "Reply" shows a reply preview above the input box
- The reply includes a small preview of the parent message
- Reply messages display with a visual link to the parent message

---

### F10: Edit & Delete Messages

- Hover over your own message → "Edit" and "Delete" buttons appear
- Edit: replaces input box content with existing message, shows "Editing" indicator, save on Enter
- Delete: confirmation dialog → removes from all clients in real-time
- Edited messages show "(edited)" label
- Admins/owners can delete any message in their room

---

## 9. Non-Functional Requirements

### Performance

| Metric | Target |
|---|---|
| Time to first meaningful paint | < 1.5 seconds |
| Message send → receive latency | < 200ms (same region) |
| Message history load (50 msgs) | < 300ms |
| WebSocket reconnection time | < 2 seconds |
| Simultaneous users per room | Support 100+ |
| Max message history per room | Unlimited (cursor pagination) |

### Security

- All passwords hashed with bcrypt (12 rounds)
- JWT signed with HS256, secret from environment variable, never hardcoded
- CORS restricted to known frontend origin
- Input sanitization on all user content (prevent XSS)
- Rate limiting on auth endpoints (5 attempts per minute per IP)
- SQL injection prevention via parameterized queries (SQLAlchemy ORM)
- WebSocket connections authenticated via JWT on connect

### Reliability

- Socket.IO auto-reconnection with exponential backoff
- Optimistic UI with rollback on failure
- Database connection pooling (SQLAlchemy async pool)
- Graceful degradation: if WebSocket fails, app still works for reading via REST

### Accessibility

- Semantic HTML throughout
- Keyboard navigation for all interactive elements
- ARIA labels on icons and non-text elements
- Focus management when modals open/close
- Screen reader support for new message announcements

---

## 10. Engineering Execution Plan

This is the step-by-step engineering breakdown. Each step depends on the previous one. Estimated scope is included to help you track momentum, not to serve as deadlines.

---

### Phase 1: Project Foundation

#### Step 1: Backend Project Structure & Configuration

**What you're doing:** Setting up the FastAPI project with proper structure, environment configuration, and dependency management.

**Specific tasks:**
1. Create the full directory structure under `backend/app/` (models, schemas, routers, services, sockets, utils)
2. Create `requirements.txt` with all dependencies pinned to specific versions:
   - fastapi, uvicorn[standard], sqlalchemy[asyncio], asyncpg, alembic, pydantic[email], pydantic-settings, python-jose[cryptography], passlib[bcrypt], python-socketio, redis, httpx, pytest, pytest-asyncio
3. Create `app/config.py` using Pydantic Settings to load from `.env`:
   - DATABASE_URL, REDIS_URL, JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, CORS_ORIGINS
4. Create `.env` file (gitignored) and `.env.example` (committed) with placeholder values
5. Create `app/main.py` with FastAPI app factory: CORS middleware, router includes, lifespan handler for startup/shutdown
6. Create `app/database.py` with async SQLAlchemy engine, async sessionmaker, and Base declarative base
7. Verify the server starts with `uvicorn app.main:app --reload`

**Why this order:** Everything else depends on the config and database connection being established first. You can't write models without a Base, can't write routes without an app instance.

---

#### Step 2: Database Models & Migrations

**What you're doing:** Defining the SQLAlchemy ORM models and setting up Alembic for schema versioning.

**Specific tasks:**
1. Create `app/models/user.py` — User model with all columns from the schema
2. Create `app/models/room.py` — Room model
3. Create `app/models/room_member.py` — RoomMember model with unique constraint on (user_id, room_id)
4. Create `app/models/message.py` — Message model with self-referencing FK for parent_id
5. Create `app/models/__init__.py` — import all models so Alembic sees them
6. Define relationships: User.rooms (via room_members), Room.members, Room.messages, Message.sender, Message.parent/Message.replies
7. Initialize Alembic: `alembic init alembic`
8. Configure `alembic/env.py` to use async engine and import your Base metadata
9. Generate initial migration: `alembic revision --autogenerate -m "initial schema"`
10. Run migration: `alembic upgrade head`
11. Verify tables exist in PostgreSQL using `psql` or a DB client

**Why this order:** Models define the shape of your data. Everything else (services, routes) operates on these models. Alembic ensures schema changes are versioned and reproducible.

---

#### Step 3: Pydantic Schemas

**What you're doing:** Defining the request/response shapes that validate incoming data and serialize outgoing data.

**Specific tasks:**
1. Create `app/schemas/user.py`:
   - `UserCreate` (registration request body)
   - `UserUpdate` (profile update, all fields optional)
   - `UserResponse` (what the API returns — no password_hash)
   - `UserBrief` (minimal: id, username, display_name, avatar_url, is_online — used inside message/room responses)
2. Create `app/schemas/auth.py`:
   - `LoginRequest`
   - `TokenResponse`
   - `RefreshRequest`
3. Create `app/schemas/room.py`:
   - `RoomCreate`
   - `RoomResponse`
   - `RoomListItem` (includes last_message and unread_count)
   - `RoomMemberResponse`
4. Create `app/schemas/message.py`:
   - `MessageCreate`
   - `MessageUpdate`
   - `MessageResponse` (includes sender as UserBrief)
   - `MessageListResponse` (messages array + next_cursor + has_more)

**Why this order:** Schemas depend on knowing the data model. Services and routes depend on schemas for input validation and output serialization.

---

#### Step 4: Authentication Utilities & Dependencies

**What you're doing:** Building the security primitives (password hashing, JWT encode/decode) and the FastAPI dependency that extracts the current user from a request.

**Specific tasks:**
1. Create `app/utils/security.py`:
   - `hash_password(plain: str) -> str` — uses passlib bcrypt
   - `verify_password(plain: str, hashed: str) -> bool`
   - `create_access_token(user_id: str) -> str` — encodes JWT with sub, type, exp, iat
   - `create_refresh_token(user_id: str) -> str`
   - `decode_token(token: str) -> dict` — decodes and validates JWT, raises on expiry/invalid
2. Create `app/dependencies.py`:
   - `get_db()` — async generator yielding a database session
   - `get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User` — extracts Bearer token, decodes it, fetches user from DB, raises 401 if invalid

**Why this order:** Auth dependencies are used by every protected route. You must build these before building any authenticated endpoint.

---

### Phase 2: Core REST API

#### Step 5: Auth Service & Routes

**What you're doing:** Implementing registration, login, and token refresh.

**Specific tasks:**
1. Create `app/services/auth_service.py`:
   - `register(db, user_data: UserCreate) -> User` — check uniqueness, hash password, insert, return
   - `login(db, email: str, password: str) -> tuple[User, str, str]` — verify credentials, generate tokens
   - `refresh(db, refresh_token: str) -> str` — validate refresh token, return new access token
2. Create `app/routers/auth.py`:
   - `POST /auth/register` → calls auth_service.register, returns UserResponse (201)
   - `POST /auth/login` → calls auth_service.login, returns TokenResponse (200)
   - `POST /auth/refresh` → calls auth_service.refresh, returns new access token (200)
3. Register the auth router in `app/main.py` with prefix `/api/v1`
4. Test manually with the FastAPI auto-docs at `/docs`:
   - Register a user
   - Login and get tokens
   - Use the access token in the Authorize button
   - Refresh the token

**Why this order:** Auth is the gateway to everything. You cannot test any other endpoint without being able to create a user and get a token.

---

#### Step 6: User Service & Routes

**What you're doing:** Implementing user profile endpoints and user search.

**Specific tasks:**
1. Create `app/services/user_service.py`:
   - `get_user_by_id(db, user_id) -> User`
   - `update_user(db, user_id, data: UserUpdate) -> User`
   - `search_users(db, query: str, limit: int) -> list[User]` — ILIKE search on username and display_name
2. Create `app/routers/users.py`:
   - `GET /users/me` → return current user profile
   - `PATCH /users/me` → update current user profile
   - `GET /users/search?q=...&limit=...` → search users
3. All endpoints protected with `Depends(get_current_user)`

**Why this order:** User endpoints are simple and let you verify that auth dependencies work end-to-end before building more complex room/message logic.

---

#### Step 7: Room Service & Routes

**What you're doing:** Implementing room CRUD, member management, and DM deduplication logic.

**Specific tasks:**
1. Create `app/services/room_service.py`:
   - `create_room(db, creator_id, data: RoomCreate) -> Room`:
     - If `is_direct`: check if DM already exists between these two users, return existing if so
     - Create room, add creator as owner, add other members
   - `get_user_rooms(db, user_id) -> list[RoomListItem]`:
     - Query all rooms the user is a member of
     - Join with latest message per room (subquery)
     - Calculate unread count per room (messages WHERE created_at > last_read_at)
     - Sort by last message time DESC
   - `get_room_detail(db, room_id, user_id) -> Room`:
     - Verify user is a member (raise 403 if not)
     - Return room with members
   - `add_member(db, room_id, user_id, adder_id) -> RoomMember`:
     - Verify adder is owner/admin
     - Verify target user exists and isn't already a member
   - `remove_member(db, room_id, user_id, remover_id)`:
     - If removing self: just leave
     - If removing other: verify remover is owner/admin
   - `check_membership(db, room_id, user_id) -> bool` — used as a guard in message endpoints
2. Create `app/routers/rooms.py`:
   - `POST /rooms`
   - `GET /rooms`
   - `GET /rooms/{room_id}`
   - `POST /rooms/{room_id}/members`
   - `DELETE /rooms/{room_id}/members/{user_id}`

**Why this order:** Messages belong to rooms. You need rooms to exist before you can send or retrieve messages.

---

#### Step 8: Message Service & Routes

**What you're doing:** Implementing message CRUD with cursor-based pagination.

**Specific tasks:**
1. Create `app/services/message_service.py`:
   - `create_message(db, sender_id, room_id, data: MessageCreate) -> Message`:
     - Verify membership
     - Insert message
     - Return with sender relationship loaded
   - `get_messages(db, room_id, user_id, cursor: UUID | None, limit: int) -> MessageListResponse`:
     - Verify membership
     - Query: `SELECT * FROM messages WHERE room_id = :room_id AND (id < :cursor OR :cursor IS NULL) ORDER BY created_at DESC LIMIT :limit + 1`
     - If result count > limit → has_more = True, pop last item, next_cursor = last item's ID
     - Return messages in chronological order (reverse the DESC result)
   - `update_message(db, message_id, user_id, data: MessageUpdate) -> Message`:
     - Verify sender owns the message
     - Update content, set is_edited = True
   - `delete_message(db, message_id, user_id, room_id) -> None`:
     - Verify sender owns message OR user is room owner/admin
   - `mark_room_read(db, room_id, user_id)`:
     - Update room_members.last_read_at = now()
2. Create `app/routers/messages.py`:
   - `GET /rooms/{room_id}/messages?cursor=...&limit=...`
   - `PATCH /rooms/{room_id}/messages/{message_id}`
   - `DELETE /rooms/{room_id}/messages/{message_id}`
   - `POST /rooms/{room_id}/read`

**Why this order:** Messages are the core data type of a chat app. With this complete, the entire REST API layer is done. You can CRUD users, rooms, members, and messages.

---

#### Step 9: Backend Testing

**What you're doing:** Writing integration tests for all API endpoints.

**Specific tasks:**
1. Create `tests/conftest.py`:
   - Set up a test database (SQLite async or a test PostgreSQL DB)
   - Create fixtures: `test_client` (httpx AsyncClient), `test_db` (session), `test_user` (pre-created user), `auth_headers` (pre-generated JWT)
2. Create `tests/test_auth.py`:
   - Test registration success, duplicate email/username errors, weak password
   - Test login success, wrong password, non-existent user
   - Test token refresh, expired refresh token
3. Create `tests/test_users.py`:
   - Test get profile, update profile, search users
4. Create `tests/test_rooms.py`:
   - Test create room, create DM (and deduplication), list rooms, get room detail
   - Test add member (as owner vs. non-owner), remove member, leave room
5. Create `tests/test_messages.py`:
   - Test send message, get message history (pagination), edit message (own vs. others), delete message
   - Test unread count and mark-as-read
6. Run all tests: `pytest -v`

**Why this order:** Testing before the WebSocket layer ensures your data layer is solid. WebSocket handlers will call the same services, so bugs caught here save debugging time later.

---

### Phase 3: Real-Time Layer

#### Step 10: Socket.IO Server Setup

**What you're doing:** Integrating python-socketio with the FastAPI app and implementing connection lifecycle.

**Specific tasks:**
1. Install and configure python-socketio with async mode
2. In `app/main.py`: create a `socketio.AsyncServer`, wrap FastAPI app with `socketio.ASGIApp`
3. Create `app/sockets/chat.py` — all Socket.IO event handlers:
   - `connect` event handler:
     - Extract JWT from `auth` dict
     - Decode and validate
     - Store user_id in the socket session (`await sio.save_session(sid, {"user_id": user_id})`)
     - Fetch user's room memberships from DB
     - Join the socket into all room IDs: `sio.enter_room(sid, room_id)` for each
     - Set user online in Redis: `SET user:{user_id}:online 1 EX 300`
     - Emit `user_online` to all rooms
   - `disconnect` event handler:
     - Remove online status from Redis
     - Emit `user_offline` to all rooms with `last_seen_at`
   - `send_message` event handler:
     - Get user_id from session
     - Call `message_service.create_message()`
     - Emit `new_message` to the room: `sio.emit("new_message", message_data, room=room_id)`
   - `typing_start` event handler:
     - Emit `user_typing` to the room (skip_sid=sender)
   - `typing_stop` event handler:
     - Emit `user_stop_typing` to the room (skip_sid=sender)
   - `mark_read` event handler:
     - Call `message_service.mark_room_read()`

**Why this order:** The real-time layer builds on top of the service layer. It reuses the same services you already tested, just triggered by Socket.IO events instead of HTTP requests.

---

#### Step 11: Redis Integration for Presence & Pub/Sub

**What you're doing:** Using Redis for online presence tracking and (optionally) the Socket.IO adapter for multi-worker scaling.

**Specific tasks:**
1. Create a Redis connection in `app/main.py` lifespan (startup/shutdown)
2. Online presence:
   - On connect: `SET user:{user_id}:online 1 EX 300` (5 min TTL, refreshed periodically)
   - Heartbeat: client emits a ping every 60 seconds → server refreshes the TTL
   - On disconnect: `DEL user:{user_id}:online`
   - Check presence: `EXISTS user:{user_id}:online`
3. Configure python-socketio to use the Redis adapter (manager): `socketio.AsyncRedisManager("redis://localhost:6379")` — this enables Socket.IO events to be broadcast across multiple Uvicorn workers

**Why this order:** Redis presence is needed for accurate online/offline indicators. The pub/sub adapter is needed if you ever run more than one server process (which Uvicorn does with `--workers`).

---

### Phase 4: Frontend

#### Step 12: Frontend Project Setup

**What you're doing:** Scaffolding the React + TypeScript project with all tooling configured.

**Specific tasks:**
1. Scaffold with Vite: `npm create vite@latest frontend -- --template react-ts`
2. Install dependencies:
   - `npm install react-router-dom zustand @tanstack/react-query socket.io-client react-hook-form zod @hookform/resolvers axios`
   - `npm install -D tailwindcss @tailwindcss/vite`
3. Configure TailwindCSS (tailwind.config.ts, add to CSS)
4. Configure path aliases in `tsconfig.json` and `vite.config.ts` (`@/` → `src/`)
5. Set up the directory structure: `api/`, `hooks/`, `stores/`, `components/`, `pages/`, `lib/`, `types/`
6. Create `src/types/index.ts` — TypeScript interfaces for User, Room, Message, etc. (mirroring your Pydantic schemas)
7. Create `src/lib/constants.ts` — API_BASE_URL, SOCKET_URL
8. Verify: `npm run dev` shows the default Vite page

**Why this order:** You need the project to exist and all tooling working before writing any application code.

---

#### Step 13: API Client & Auth Store

**What you're doing:** Building the HTTP client with JWT interceptor and the authentication state management.

**Specific tasks:**
1. Create `src/api/client.ts`:
   - Axios instance with baseURL = `/api/v1`
   - Request interceptor: attach `Authorization: Bearer <token>` from auth store
   - Response interceptor: on 401, attempt token refresh, retry original request, if refresh fails → logout
2. Create `src/stores/authStore.ts` (Zustand):
   - State: `user`, `accessToken`, `refreshToken`, `isAuthenticated`
   - Actions: `setAuth(user, accessToken, refreshToken)`, `setAccessToken(token)`, `logout()`
   - Persist to localStorage (so user stays logged in on page refresh)
3. Create `src/api/auth.ts`:
   - `register(data)`, `login(data)`, `refreshToken(token)` — call the backend auth endpoints
4. Create `src/hooks/useAuth.ts`:
   - Wraps auth store and API calls
   - `login(email, password)` → calls API → sets store
   - `register(...)` → calls API → auto-login
   - `logout()` → clears store, disconnects socket

**Why this order:** Every frontend feature depends on being able to make authenticated API calls. The auth store and API client are foundational.

---

#### Step 14: Auth Pages (Login & Register)

**What you're doing:** Building the login and registration forms with validation.

**Specific tasks:**
1. Create `src/components/ui/` — basic reusable components:
   - `Button.tsx` (variants: primary, secondary, ghost; sizes: sm, md, lg; loading state)
   - `Input.tsx` (label, error message, icon slot)
   - `Avatar.tsx` (image with fallback to initials)
2. Create `src/pages/LoginPage.tsx`:
   - Form with email + password fields (React Hook Form + Zod validation)
   - Submit → calls `useAuth().login()`
   - Error display for wrong credentials
   - Link to register page
   - Redirect to `/chat` on success
3. Create `src/pages/RegisterPage.tsx`:
   - Form with email, username, display name, password, confirm password
   - Real-time validation feedback
   - Submit → calls `useAuth().register()`
   - Redirect to `/chat` on success
4. Create `src/App.tsx`:
   - React Router setup with public routes (login, register) and protected routes (chat, settings)
   - `<ProtectedRoute>` wrapper that checks `isAuthenticated` and redirects to `/login`
5. Create `src/main.tsx`:
   - Mount React app, wrap with `<QueryClientProvider>` and `<BrowserRouter>`

**Why this order:** You need to be able to log in before you can test any authenticated page. Building auth pages first means you can visually verify the auth flow end-to-end.

---

#### Step 15: Socket.IO Client & Connection Hook

**What you're doing:** Setting up the Socket.IO client singleton and a React hook that manages the connection lifecycle.

**Specific tasks:**
1. Create `src/lib/socket.ts`:
   - Export a function `createSocket(token: string)` that returns a Socket.IO client instance configured with auth token, reconnection settings, and transport preferences
   - Do NOT auto-connect on import (connect only after login)
2. Create `src/hooks/useSocket.ts`:
   - Connects on mount (when user is authenticated), disconnects on unmount
   - Handles reconnection events
   - Exposes `socket` instance and `isConnected` status
   - Listens for `new_message`, `message_edited`, `message_deleted`, `user_typing`, `user_stop_typing`, `user_online`, `user_offline` events
   - Dispatches to appropriate stores/query cache on each event
3. Mount `useSocket` in the top-level authenticated layout (so the socket lives for the entire authenticated session)

**Why this order:** The socket connection must exist before any real-time feature works. This hook is consumed by the chat page and all real-time components.

---

#### Step 16: Chat Layout — Sidebar & Room List

**What you're doing:** Building the main application shell with the sidebar listing all rooms.

**Specific tasks:**
1. Create `src/pages/ChatPage.tsx`:
   - Two-panel layout: Sidebar (left, fixed width) + ChatArea (right, flex grow)
   - Use React Router `<Outlet>` for the chat area (so `/chat` shows an empty state, `/chat/:roomId` shows the conversation)
2. Create `src/components/layout/Sidebar.tsx`:
   - Search bar at top (filters room list client-side)
   - Room list below
   - "New Room" button at bottom
3. Create `src/components/chat/RoomList.tsx`:
   - Fetches rooms via TanStack Query: `GET /api/v1/rooms`
   - Renders a `<RoomListItem>` for each room
4. Create `src/components/chat/RoomListItem.tsx`:
   - Shows room name (or other user's name for DMs)
   - Shows last message preview (truncated)
   - Shows unread count badge
   - Highlights the currently active room
   - Click → navigate to `/chat/:roomId`
5. Create `src/components/chat/CreateRoomModal.tsx`:
   - Modal with room name, description, user search (multi-select)
   - Calls `POST /api/v1/rooms` on submit
   - Invalidates rooms query on success (so list updates)

**Why this order:** The sidebar is the navigation hub. You need it to select rooms before you can build the message area.

---

#### Step 17: Message Area — Display & Infinite Scroll

**What you're doing:** Building the message list with history loading and real-time updates.

**Specific tasks:**
1. Create `src/api/messages.ts`:
   - `getMessages(roomId, cursor?, limit?)` — calls the paginated messages endpoint
2. Create `src/components/chat/ChatArea.tsx`:
   - Wrapper that contains RoomHeader, MessageList, and MessageInput
   - Fetches room details via TanStack Query
3. Create `src/components/chat/RoomHeader.tsx`:
   - Room name, member count, online member avatars
   - "Info" button to open room details panel
4. Create `src/components/chat/MessageList.tsx`:
   - Uses TanStack Query's `useInfiniteQuery` for cursor-based pagination
   - Scroll container with `ref` for scroll position management
   - On mount: scroll to bottom
   - On scroll to top: fetch next page (older messages)
   - On new message (via socket): if at bottom → auto-scroll; if scrolled up → show "New messages ↓" floating button
   - Insert date dividers between messages from different days
5. Create `src/components/chat/MessageBubble.tsx`:
   - Avatar + sender name + timestamp (for first message in a group)
   - Message content
   - "(edited)" label if `is_edited`
   - Reply preview (if `parent_id` exists, show a snippet of the parent message)
   - Hover actions: Reply, Edit (own messages only), Delete (own + admin)
6. Create `src/components/chat/DateDivider.tsx`:
   - Horizontal line with date label ("Today", "Yesterday", "February 14, 2026")

**Why this order:** The message list is the heart of the app. Getting infinite scroll, real-time updates, and scroll position management right is the hardest frontend challenge in this project. Focus on this before adding input features.

---

#### Step 18: Message Input & Sending

**What you're doing:** Building the message input with send, reply, and edit functionality.

**Specific tasks:**
1. Create `src/components/chat/MessageInput.tsx`:
   - Textarea that grows with content (auto-resize)
   - Enter to send, Shift+Enter for newline
   - Character count near 5000 limit
   - Send button (disabled when empty)
   - On submit: emit `send_message` via socket
   - Optimistic update: immediately add message to TanStack Query cache, roll back on error
2. Create `src/stores/chatStore.ts` (Zustand):
   - `activeRoomId`: currently selected room
   - `replyingTo`: message being replied to (or null)
   - `editingMessage`: message being edited (or null)
   - `typingUsers`: `Record<roomId, Set<username>>`
3. Reply mode:
   - When `replyingTo` is set, show a preview bar above the input: "Replying to Denzel" with the parent message snippet and an X to cancel
   - On send, include `parent_id` in the socket event
4. Edit mode:
   - When `editingMessage` is set, populate the input with existing content
   - Show "Editing" indicator above input with X to cancel
   - On submit: call `PATCH /rooms/{roomId}/messages/{messageId}` via REST (not socket)
   - The server emits `message_edited` to all room members via socket
5. Typing indicator emission:
   - On keypress in the input: emit `typing_start` (debounced, max once per 2 seconds)
   - On blur or 3 seconds of inactivity: emit `typing_stop`
6. Create `src/components/chat/TypingIndicator.tsx`:
   - Reads `chatStore.typingUsers[activeRoomId]`
   - Renders "Alice is typing...", "Alice and Bob are typing...", or "3 people are typing..."
   - Animated dots

**Why this order:** The input interacts with the socket (sending), the store (reply/edit state), and the query cache (optimistic updates). It ties together multiple systems, so it comes after those systems are built.

---

#### Step 19: Online Presence & Typing UI

**What you're doing:** Wiring up online/offline indicators and typing indicators across the UI.

**Specific tasks:**
1. Create `src/hooks/useOnlineStatus.ts`:
   - Maintains a `Set<userId>` of online users (updated by `user_online` and `user_offline` socket events)
   - Provides `isOnline(userId): boolean`
2. Update `Avatar.tsx` to accept an `isOnline` prop → renders green/gray dot
3. Update `RoomListItem.tsx`:
   - For DM rooms: show online indicator next to the other user's name
4. Update `RoomHeader.tsx`:
   - For DM rooms: show "Online" or "Last seen 5 min ago"
   - For group rooms: show count of online members
5. Wire typing indicators into the `useSocket` hook:
   - On `user_typing` event → add to `chatStore.typingUsers[roomId]`, set 3-second auto-remove timeout
   - On `user_stop_typing` event → remove from `chatStore.typingUsers[roomId]`

**Why this order:** Presence and typing are polish features that layer on top of the core messaging flow. They depend on the socket hook, the chat store, and the UI components already existing.

---

#### Step 20: Settings Page & Profile Management

**What you're doing:** Building the settings page for profile editing.

**Specific tasks:**
1. Create `src/pages/SettingsPage.tsx`:
   - Display name edit
   - Avatar URL edit (text input for now — file upload is a stretch goal)
   - Email display (read-only)
   - Username display (read-only)
   - "Save" button → calls `PATCH /api/v1/users/me`
   - "Logout" button → calls `useAuth().logout()`
2. Update navigation: add a settings icon/link in the header or sidebar

**Why this order:** Settings is a standalone page with no dependencies on real-time features. It's lower priority than core chat but rounds out the user experience.

---

### Phase 5: DevOps & Deployment

#### Step 21: Docker Setup

**What you're doing:** Containerizing all services so the entire app runs with `docker compose up`.

**Specific tasks:**
1. Create `backend/Dockerfile`:
   - Base image: `python:3.13-slim`
   - Copy requirements.txt, install deps
   - Copy app code
   - CMD: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
2. Create `frontend/Dockerfile`:
   - Multi-stage build: Stage 1 (node:20-alpine) → npm install + npm run build; Stage 2 (nginx:alpine) → copy build output to nginx html dir
3. Create `nginx/nginx.conf`:
   - Serve frontend static files
   - Proxy `/api/*` to backend:8000
   - Proxy `/socket.io/*` to backend:8000 (with WebSocket upgrade headers)
4. Create `docker-compose.yml`:
   ```yaml
   services:
     db:        # PostgreSQL 16
     redis:     # Redis 7
     backend:   # FastAPI app
     frontend:  # Nginx serving React build
   ```
5. Create `.dockerignore` files for both backend and frontend
6. Test: `docker compose up --build` → entire app runs

**Why this order:** Containerization proves your app is deployable and reproducible. Interviewers and hiring managers value this.

---

#### Step 22: CI/CD Pipeline

**What you're doing:** Automating tests, linting, and builds on every push.

**Specific tasks:**
1. Create `.github/workflows/ci.yml`:
   - Trigger: push to main, pull requests
   - Jobs:
     - **backend-test**: Set up Python, install deps, run `pytest`
     - **frontend-test**: Set up Node, install deps, run `npm run lint` + `npm run build` (and `vitest run` if you wrote frontend tests)
     - **docker-build**: Build all Docker images to verify they build successfully
2. Add a status badge to README.md

**Why this order:** CI catches regressions and proves engineering discipline. It's one of the last steps because you need tests and Docker to exist first.

---

#### Step 23: Final Polish & README

**What you're doing:** Making the project portfolio-ready.

**Specific tasks:**
1. Write a comprehensive `README.md`:
   - Project title + one-line description
   - Screenshot or GIF of the app in action
   - Tech stack list with brief justification
   - Architecture diagram (the ASCII one from this PRD)
   - "Getting Started" with prerequisites and setup instructions
   - "Running with Docker" instructions
   - "Running locally" instructions
   - API documentation link (FastAPI auto-docs)
   - Feature list
2. Add error boundary component in React (catch rendering errors gracefully)
3. Add loading states and empty states for all data-fetching components
4. Responsive design: make the sidebar collapsible on mobile
5. Final pass: remove console.logs, unused imports, commented-out code

**Why this order:** Polish is last because it doesn't affect functionality, but it dramatically affects the impression your project makes on a reviewer.

---

### Stretch Goals (Post-MVP, If You Want to Keep Building)

These are NOT in the main plan. Only pursue after the above 23 steps are complete.

- **File/image uploads** — presigned S3 URLs, image preview in messages
- **Message reactions** — emoji reactions on messages (like Slack)
- **Push notifications** — browser Notification API for background messages
- **Email verification** — verify email on registration
- **Password reset flow** — forgot password email with reset link
- **Room roles management UI** — promote/demote members in a room
- **Message search** — full-text search across all messages (PostgreSQL `tsvector`)
- **Voice/video calls** — WebRTC integration (major undertaking)
- **End-to-end encryption** — Signal protocol (major undertaking)
- **Mobile app** — React Native sharing the same API
- **Rate limiting** — slowapi or custom middleware to prevent spam
- **OAuth login** — Google/GitHub SSO
