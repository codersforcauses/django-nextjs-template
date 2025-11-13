# Django + Next.js Template

Django + Nextjs Template: Standardised CFC Tech Stack

---

### Prerequisites

- **Node.js 18+** and **npm** - [Download here](https://nodejs.org/)
- **uv 0.8+** (Python package manager) - [Installation guide](https://docs.astral.sh/uv/getting-started/installation/)

### Installation Steps

#### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <project-name>
```

#### 2. Install Prerequisites
**MacOS:**
```bash
brew install uv 
```
**Ubuntu**
```bash
apt install astral-uv
```
Otherwise, look at the [installation guide](https://docs.astral.sh/uv/getting-started/installation/) 
#### 3. Set Up Environment Variables
Before proceeding, create your environment files by copying the examples:
```bash
cp ./client/.env.example ./client/.env && cp ./server/.env.example ./server/.env
```

#### 4. Set Up the Backend (Django)
```bash
cd server
uv sync
source .venv/bin/activate
python manage.py migrate
python manage.py createsuperuser  
python manage.py runserver
```

**Backend (`.env` in `server/`)**
```env
APP_NAME=DjangoAPI
APP_ENV=DEVELOPMENT
API_SECRET_KEY=your-secret-key-here
API_ALLOWED_HOSTS=.localhost 127.0.0.1 [::1]

POSTGRES_HOST=localhost
POSTGRES_NAME=your_db_name
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_PORT=5432

DJANGO_SUPERUSER_PASSWORD=Password123
DJANGO_SUPERUSER_EMAIL=admin@test.com
DJANGO_SUPERUSER_USERNAME=admin

FRONTEND_URL=http://localhost:3000
```

**Frontend (`.env` in `client/`)**
```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

#### 6. Set Up the Frontend (Next.js)
```bash
cd client
npm install
npm run dev
```

#### 7. Verify Installation
- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend API: [http://localhost:8000](http://localhost:8000)
- Admin panel: [http://localhost:8000/admin](http://localhost:8000/admin)

---

## Development Commands

### Backend (Django)
```bash
cd server

# Run development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Reset database (nuclear option)
./nuke.sh
```

### Frontend (Next.js)
```bash
cd client

# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linting
npm run lint

# Fix linting issues
npm run lint:fix

# Type checking
npm run typecheck

# Format code
npm run format
```

---

## Server

### Create and run migrations

If the models are updated, be sure to create a migration:

```bash
python manage.py makemigrations # create migration
python manage.py migrate # apply migrations
```

### Nuke the DB

If you run into migration conflicts that you can't be bothered to fix, run `nuke.sh` to clear your database. Then, run migrations again.

## Other

### Update Dependencies

You can run `npm install` and `uv sync` in the respective `client` and `server` folders to install the newest dependencies.

### Changing env vars

Edit the `.env` file in the respective directory (client or server).