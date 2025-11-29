# Django + Next.js Template

Django + Nextjs Template: Standardised CFC Tech Stack

---

### Prerequisites

- **Node.js 18+** and **npm** - [Download here](https://nodejs.org/)
- **uv 0.8+** (Python package manager) - [Installation guide](https://docs.astral.sh/uv/getting-started/installation/)

### Installation Steps
If you're on Windows, you might have an easier time using devcontainers - if you're on VSCode, you should be able to install the devcontainers extension, and then open the command pallet with command P, then running `> Dev Containers: Reopen in Container`.
You can skip straight to step 3

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
##### 3.1 On Zsh (MacOS) or Dev Container 
```bash
cp ./client/.env.example ./client/.env && cp ./server/.env.example ./server/.env
```
##### 3.2 On Powershell
```shell
cp .\client\.env.example .\client\.env
cp .\server\.env.example .\server\.env
```
#### 4. Set Up the Backend (Django)
##### 4.1 if you're on zsh (MacOS) or devcontainers:
```bash
cd server
uv sync
source .venv/bin/activate
python manage.py migrate
python manage.py createsuperuser  
python manage.py runserver
```
###### 4.2 If you're on powershell 
Navigate to the server folder in the project:
```shell
cd .\intermediate_team_* # replace with your team number 
cd .\server
```
Set up and source your virtual environment
```shell
uv sync
.\venv\Scripts\Activate.ps1
```
Troubleshooting: Execution Policy Error
If you receive an error message about scripts being disabled on the system, it is due to PowerShell's default execution policy which prevents running local scripts [1]. 
You have a few options to resolve this:
Option 1: Temporarily Bypass the Policy (Recommended for a single session) 
You can bypass the execution policy only for your current PowerShell session by starting a new session with a specific flag: 
```shell
powershell -ExecutionPolicy Bypass -File .\venv\Scripts\Activate.ps1
```

Option 2: Change the Execution Policy for the Current User (More permanent) 
If you frequently use virtual environments and trust the scripts you are running, you can change the execution policy for your user account. This will allow local scripts to run without error in future sessions:
```shell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
  RemoteSigned: This policy allows scripts you write locally to run without a digital signature, but requires scripts downloaded from the internet to be signed by a trusted publisher [2].
  When prompted to confirm the change, type Y and press Enter. 

After setting the policy, you can use the standard activation command again:
```shell
.\venv\Scripts\Activate.ps1
```

Once activated, your PowerShell prompt will change to show the name of your virtual environment in parentheses (e.g., (venv) PS C:\Projects\MyProject>), indicating that you are now working within the isolated environment [1].

##### If you've done step 3, you can safely ignore this.
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
