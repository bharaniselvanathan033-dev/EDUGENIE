"""
EduGenie: Google Gemini Powered Learning Assistant
FastAPI Backend

API Endpoints:
  POST /api/qa          — AI Question & Answer
  POST /api/explain     — Simple explanation of difficult concepts
  POST /api/quiz        — Quiz generator
  POST /api/summarize   — Educational text summarizer
  POST /api/learning-path — Personalized learning recommendations
  GET  /api/health      — Health check

The Gemini API key is read from the GEMINI_API_KEY environment variable
and is NEVER exposed to the frontend.
"""

import os
import json
import re
from typing import Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import google.generativeai as genai

# ------------------------------------------------------------------ #
# Configuration                                                       #
# ------------------------------------------------------------------ #

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*").split(",")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI(
    title="EduGenie API",
    description="Google Gemini Powered Learning Assistant Backend",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------ #
# Request / Response Models                                          #
# ------------------------------------------------------------------ #


class GenerateRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=5000)
    level: str = Field("beginner", pattern="^(beginner|intermediate|advanced)$")


class QARequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=5000)
    level: str = Field("beginner", pattern="^(beginner|intermediate|advanced)$")


class GenerateResponse(BaseModel):
    status: str = "success"
    data: Any


# ------------------------------------------------------------------ #
# Gemini Helper                                                       #
# ------------------------------------------------------------------ #

LEVEL_CONTEXT = {
    "beginner": "The learner is a beginner. Use very simple language, relatable everyday analogies, and avoid jargon. Keep things encouraging and easy to follow.",
    "intermediate": "The learner has some background knowledge. You can use domain terminology (with brief definitions) and discuss how components interact.",
    "advanced": "The learner is advanced. Use precise technical language, discuss edge cases, trade-offs, and reference underlying theory or research directions.",
}


def call_gemini(prompt: str) -> str:
    """Call the Gemini API and return the text response. Raises HTTPException on failure."""
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is not configured on the server. Set it in your .env file.",
        )
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 2048,
            },
        )
        text = response.text
        if not text:
            raise HTTPException(status_code=502, detail="Gemini returned an empty response.")
        return text
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Gemini API error: {exc}")


def call_gemini_json(prompt: str) -> Any:
    """Call Gemini and parse the response as JSON. Strips markdown code fences if present."""
    raw = call_gemini(prompt)
    # Strip markdown ```json ... ``` fences
    cleaned = re.sub(r"^```(?:json)?\s*", "", raw.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r"\s*```$", "", cleaned.strip())
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=502,
            detail="The AI returned a response that could not be parsed as JSON. Please try again.",
        )


# ------------------------------------------------------------------ #
# Prompts                                                             #
# ------------------------------------------------------------------ #


def qa_prompt(question: str, level: str) -> str:
    return (
        f"You are EduGenie, a friendly and knowledgeable AI tutor. "
        f"{LEVEL_CONTEXT[level]}\n\n"
        f"Answer this student question clearly and thoroughly:\n"
        f"\"{question}\"\n\n"
        f"Structure your answer with:\n"
        f"- A direct answer (2-3 sentences)\n"
        f"- A short elaboration with key details\n"
        f"- A real-world example or analogy\n"
        f"Keep the total answer under 300 words. Use plain text (no markdown headers)."
    )


def explain_prompt(topic: str, level: str) -> str:
    return (
        f"You are EduGenie, an AI learning assistant. "
        f"{LEVEL_CONTEXT[level]}\n\n"
        f"Explain the concept of \"{topic}\" in a structured way. "
        f"Respond with ONLY a JSON object (no markdown, no code fences) in this exact format:\n"
        f"""```json
{{
  "title": "Human-readable title for the concept",
  "overview": "A 2-3 sentence plain-English overview of what {topic} is",
  "keyPoints": ["Point 1", "Point 2", "Point 3", "Point 4"],
  "analogy": "A relatable everyday analogy that makes the concept click",
  "deeperDetail": "A paragraph going deeper into the concept, appropriate for the learner's level"
}}
```"""
    )


def quiz_prompt(topic: str, level: str) -> str:
    n_questions = 5 if level == "beginner" else 6
    return (
        f"You are EduGenie, an AI quiz generator. "
        f"{LEVEL_CONTEXT[level]}\n\n"
        f"Create a {n_questions}-question multiple-choice quiz about \"{topic}\". "
        f"Each question must have exactly 4 options with one correct answer. "
        f"Respond with ONLY a JSON object (no markdown, no code fences) in this exact format:\n"
        f"""```json
{{
  "questions": [
    {{
      "question": "The question text",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correctIndex": 0,
      "explanation": "Why the correct answer is correct"
    }}
  ]
}}
```
Generate exactly {n_questions} questions."""
    )


def summary_prompt(notes: str, level: str) -> str:
    return (
        f"You are EduGenie, an AI text summarizer for students. "
        f"{LEVEL_CONTEXT[level]}\n\n"
        f"Summarize the following study notes. Extract the main idea, key points, and takeaways. "
        f"Respond with ONLY a JSON object (no markdown, no code fences) in this exact format:\n"
        f"""```json
{{
  "title": "A short descriptive title for the notes",
  "mainIdea": "The central idea in 1-2 sentences",
  "keyPoints": ["Key point 1", "Key point 2", "Key point 3"],
  "takeaways": ["Takeaway 1", "Takeaway 2", "Takeaway 3"]
}}
```

Notes to summarize:
\"{notes}\""""
    )


def learning_path_prompt(topic: str, level: str) -> str:
    n_steps = 4 if level == "beginner" else (5 if level == "intermediate" else 6)
    return (
        f"You are EduGenie, an AI learning path builder. "
        f"{LEVEL_CONTEXT[level]}\n\n"
        f"Create a {n_steps}-step learning path for studying \"{topic}\". "
        f"Each step should build on the previous one. Include free, accessible resources. "
        f"Respond with ONLY a JSON object (no markdown, no code fences) in this exact format:\n"
        f"""```json
{{
  "title": "Learning Path: {topic}",
  "steps": [
    {{
      "name": "Step name",
      "description": "What to learn and why",
      "resources": ["Resource 1 (free)", "Resource 2 (free)"]
    }}
  ]
}}
```
Generate exactly {n_steps} steps."""
    )


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "gemini_configured": bool(GEMINI_API_KEY),
        "model": GEMINI_MODEL,
    }


@app.post("/api/qa", response_model=GenerateResponse)
async def qa(req: QARequest):
    answer = call_gemini(qa_prompt(req.question, req.level))
    return GenerateResponse(data={"answer": answer})


@app.post("/api/explain", response_model=GenerateResponse)
async def explain(req: GenerateRequest):
    data = call_gemini_json(explain_prompt(req.topic, req.level))
    return GenerateResponse(data=data)


@app.post("/api/quiz", response_model=GenerateResponse)
async def quiz(req: GenerateRequest):
    data = call_gemini_json(quiz_prompt(req.topic, req.level))
    return GenerateResponse(data=data)


@app.post("/api/summarize", response_model=GenerateResponse)
async def summarize(req: GenerateRequest):
    data = call_gemini_json(summary_prompt(req.topic, req.level))
    return GenerateResponse(data=data)


@app.post("/api/learning-path", response_model=GenerateResponse)
async def learning_path(req: GenerateRequest):
    data = call_gemini_json(learning_path_prompt(req.topic, req.level))
    return GenerateResponse(data=data)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
