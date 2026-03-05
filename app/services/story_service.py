import requests
from typing import List, Optional
from app.core.config import (
    LLM_API_KEY,
    LLM_API_ENDPOINT,
    LLM_MODEL,
)

# NOTE FOR STUDENTS:
# During the guest lecture demo this project used the lecturer's Azure OpenAI setup.
# In your own environment you must configure your own LLM provider.
#
# Possible options include:
# - OpenAI API
# - Azure OpenAI
# - Local models using Ollama
# - HuggingFace Inference API
#
# Update the configuration in config.py and this service depending on the
# provider you choose.


def generate_story(
    place_name: str,
    place_type: str,
    country: str = "Namibia",
    nearby_suggestions: Optional[List[str]] = None,
    rewrite_hint: Optional[str] = None,
) -> str:

    suggestions_text = ""
    if nearby_suggestions:
        suggestions_text = (
            "\nAlso mention 1–2 nearby places as quick recommendations: "
            + ", ".join(nearby_suggestions[:2])
            + "."
        )

    hint_text = ""
    if rewrite_hint:
        hint_text = f"\nExtra instruction: {rewrite_hint}"

    prompt = f"""
You are an AI tour guide.

Create an engaging spoken narration for a tourist
who is passing by a place.

Place name: {place_name}
Type: {place_type}
Country: {country}

Keep it friendly, natural, and short (under ~80 words).
Do NOT mention exact coordinates.
{suggestions_text}
{hint_text}
""".strip()

    # If students have not configured an LLM yet, return a fallback narration
    if not LLM_API_KEY or not LLM_API_ENDPOINT or not LLM_MODEL:
        base = f"You are near {place_name}. It’s a notable {place_type or 'place'} in {country}. Enjoy the surroundings!"
        if nearby_suggestions:
            base += f" If you have time, you could also check out {nearby_suggestions[0]}."
        return base

    url = f"{LLM_API_ENDPOINT}"

    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful AI tour guide. Keep responses friendly, natural, and concise."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 180,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LLM_API_KEY}",
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    except Exception:
        base = f"You are passing by {place_name}, a fascinating {place_type or 'spot'} in {country}. Take a moment to enjoy the view and local atmosphere."
        if nearby_suggestions:
            base += f" Nearby, you might also enjoy {nearby_suggestions[0]}."
        return base