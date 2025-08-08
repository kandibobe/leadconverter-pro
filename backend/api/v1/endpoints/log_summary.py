"""Endpoints for log summarization."""

import logging

import openai
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Security
from fastapi.security.api_key import APIKeyHeader

from app.core.config import settings


logger = logging.getLogger(__name__)
router = APIRouter()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_api_key(api_key: str = Security(api_key_header)) -> str:
    """Retrieve and validate API key from headers."""
    expected_key = settings.LOG_SUMMARY_API_KEY
    if not expected_key:
        logger.error("LOG_SUMMARY_API_KEY not configured")
        raise HTTPException(status_code=500, detail="Log summary API key not configured")
    if api_key != expected_key:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return api_key

@router.post("/summarize-log")
async def summarize_log(
    file: UploadFile = File(...), api_key: str = Depends(get_api_key)
):
    """Summarize an uploaded log file using OpenAI.

    Requires a valid token passed via the `X-API-Key` header.
    """
    try:
        content_bytes = await file.read()
        log_text = content_bytes.decode("utf-8")
    except Exception as exc:  # pragma: no cover - simple validation
        raise HTTPException(status_code=400, detail="Unable to read uploaded file") from exc

    api_key = settings.OPENAI_API_KEY
    if not api_key:
         logger.error("OPENAI_API_KEY not configured")
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
        logger.exception("OpenAI summarization failed")
        raise HTTPException(status_code=502, detail="OpenAI request failed") from exc

    summary = response.choices[0].message["content"].strip()
    return {"summary": summary}
