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

### Secure API endpoint

The `POST /summarize-log` API endpoint requires an access token. Set the
`LOG_SUMMARY_API_KEY` environment variable and include its value in the
`X-API-Key` header when making requests.

## Testing
This repository currently does not include automated tests. Linting and
formatting scripts are available in the frontend `package.json`.