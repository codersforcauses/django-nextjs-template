# Django + Next.js Template

Django + Nextjs Template: Standardised CFC Tech Stack

---

## Quick Start (Dev Container)

The easiest way to get started is using the VS Code Dev Container:

1. **Prerequisites**:  
   - [Docker Desktop](https://www.docker.com/products/docker-desktop/)  
   - [VS Code](https://code.visualstudio.com/)  
   - [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

2. **Open in Dev Container**:
   - Clone this repository
   - Open the project in VS Code
   - When prompted, click "Reopen in Container" or use `Ctrl+Shift+P` → "Dev Containers: Reopen in Container"

3. **Start the application**:
   ```bash
   # Terminal 1: Start the frontend
   cd client && npm run dev

   # Terminal 2: Start the backend
   cd server && python manage.py runserver
   ```

4. **Access the application**:
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:8000](http://localhost:8000)
   - Admin panel: [http://localhost:8000/admin](http://localhost:8000/admin)

---
## Local Development Setup

**Note**: Only follow these steps if you're NOT using the dev container.

### Installation Steps

#### 1. Install Prerequisites

- **Node.js 20+** and **npm** - [Download here](https://nodejs.org/)
- **Python 3.12+** - [Download here](https://python.org/)
- **Poetry** (Python package manager) - [Installation guide](https://python-poetry.org/docs/#installation)

#### 2. Clone the Repository
```bash
git clone <your-repo-url>
cd <project-name>
```

#### 3. Set Up Environment Variables

The client and server are configured by `.env` files, local to your device and not tracked by git.
To set these up you can simply copy the `.env.example` files in each to a new `.env` file.

Run the command below to do this automatically (system dependant).
```bash
cp ./client/.env.example ./client/.env && cp ./server/.env.example ./server/.env
```

#### 4. Set Up the Backend (Django)
```bash
cd server
poetry install

eval $(poetry env activate) #Bash/Zsh/Csh
Invoke-Expression (poetry env activate) #Powershell

python manage.py migrate
python manage.py createsuperuser  # optional
python manage.py runserver
```

#### 5. Set Up the Frontend (Next.js)
```bash
cd client
npm install
npm run dev
```

#### 6. Verify Installation
- Frontend: [http://localhost:3000](http://localhost:3000)
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

You can run `npm install` and `poetry install` in the respective `client` and `server` folders to install the newest dependencies.

### Editing Docker stuff

If you modify anything in the `docker` folder, you need to add the `--build` flag or Docker won't give you the latest changes.

### Changing env vars

Edit the `.env` file in the respective directory (client or server).