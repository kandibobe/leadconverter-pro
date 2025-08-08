# LeadConverter Pro

LeadConverter Pro is a full‑stack web application for managing lead conversion.
It includes a FastAPI backend, a Vue 3 frontend and a PostgreSQL database, all
orchestrated through Docker Compose.

## Features
- FastAPI backend with PostgreSQL storage
- Vue 3 frontend powered by Vite
- Dockerized development environment
- Log summarization script with optional OpenAI integration

## Installation
### Clone the repository
```bash
git clone <repository-url>
cd leadconverter-pro
```

### Configure environment variables
Copy the example file and adjust the values to your needs. At minimum provide a
strong `SECRET_KEY`.
```bash
cp .env.example .env
```
```env
SECRET_KEY=your_super_secret_key_32_chars_long_replace_me
```
Other variables include database credentials (`POSTGRES_USER`,
`POSTGRES_PASSWORD`, `POSTGRES_DB`) and the frontend base URL
(`VITE_API_BASE_URL`). See `.env.example` for all available options.

### Build the Docker images
```bash
docker-compose build
```

## Development
Start the complete stack using Docker Compose:
```bash
docker-compose up
```
The backend will be available at <http://localhost:8000> and the frontend at
<http://localhost:5173>.

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

## Log summarization and AI assistance
A helper script is provided for inspecting JSON logs and optionally sending a
summary to an OpenAI model such as GPT-3.5 or GPT-4.

Run the summarizer:
```bash
python scripts/log_summarizer.py path/to/log.json
```

Send the summary to OpenAI:
```bash
python scripts/log_summarizer.py path/to/log.json --send --model gpt-3.5-turbo
```

Example prompts:
- "Проанализируй лог и предложи, как исправить."
- "Найди необычные паттерны в этих логах."


