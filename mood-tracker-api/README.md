# Mood Tracker API

A Flask REST API backend for a personal mood-tracking app. Users can sign up,
log in, and create, view, edit, and delete their own mood entries. Built with
session-based authentication.

## Description

Users can:
- Sign up and log in with a username and password (passwords hashed with bcrypt)
- Stay logged in across requests via a session cookie
- Create, view, update, and delete mood entries (mood, intensity 1-10, optional note)
- Only see and manage their own mood entries — other users' entries are inaccessible
- Browse their mood entries with pagination

## Installation

From the project root:

```bash
pipenv install
pipenv shell
cd server
```

Set up the database:

```bash
export FLASK_APP=app.py
flask db upgrade
```

Seed example data (4 users, each with 3-6 mood entries; all seeded users
have the password `password123`):

```bash
python3 seed.py
```

## Running the app

From `server/`:

```bash
python3 app.py
```

The API runs at `http://127.0.0.1:5555`.

## Endpoints

| Method | Route | Auth required | Description |
|---|---|---|---|
| POST | `/signup` | No | Create a new user account and log in |
| POST | `/login` | No | Log in with username and password |
| DELETE | `/logout` | Yes | Log out, clearing the session |
| GET | `/check_session` | Yes | Return the currently logged-in user |
| GET | `/mood_entries` | Yes | List the current user's mood entries. Supports `?page=` and `?per_page=` |
| POST | `/mood_entries` | Yes | Create a new mood entry |
| GET | `/mood_entries/<id>` | Yes | View a single mood entry (must belong to the current user) |
| PATCH | `/mood_entries/<id>` | Yes | Update a mood entry (must belong to the current user) |
| DELETE | `/mood_entries/<id>` | Yes | Delete a mood entry (must belong to the current user) |