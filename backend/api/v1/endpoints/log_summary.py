"""Endpoints for log summarization."""

import os

import openai
from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter()


@router.post("/summarize-log")
async def summarize_log(file: UploadFile = File(...)):
    """Summarize an uploaded log file using OpenAI."""
    try:
        content_bytes = await file.read()
        log_text = content_bytes.decode("utf-8")
    except Exception as exc:  # pragma: no cover - simple validation
        raise HTTPException(status_code=400, detail="Unable to read uploaded file") from exc

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")

    openai.api_key = api_key
    prompt = (
        "Summarize the following application log entries in a concise manner:\n" + log_text
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes logs.",
                },
                {"role": "user", "content": prompt},
            ],
        )
    except Exception as exc:  # pragma: no cover - API errors
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    summary = response.choices[0].message["content"].strip()
    return {"summary": summary}
