# leadconverter-pro

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd leadconverter-pro
   ```
2. Copy the example environment file and adjust values if necessary:
   ```bash
   cp .env.example .env
   ```
3. Build the Docker images:
   ```bash
   docker-compose build
   ```

## Environment configuration

The `.env` file controls the configuration for the database, backend and frontend services. The default values will start a local PostgreSQL instance and connect the applications to it. At minimum you should provide a strong `SECRET_KEY` for FastAPI:

```
SECRET_KEY=your_super_secret_key_32_chars_long_replace_me
```

Other variables include database credentials (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`) and the base URL used by the frontend (`VITE_API_BASE_URL`). See `.env.example` for all available options.

## Development

The project is designed to run via Docker Compose which starts PostgreSQL, the FastAPI backend and the Vue frontend in watch mode.

Start the stack:

```bash
docker-compose up
```

The backend will be available at `http://localhost:8000` and the frontend at `http://localhost:5173`.

### Running without Docker

Backend:

```bash
cd backend
python -m venv env
source env/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

### Testing

This repository does not include automated tests. Linting and formatting scripts are available in the frontend `package.json`.
