import requests
from django.conf import settings


def gemini_generate_question(role_name):
    if not settings.GEMINI_API_KEY:
        return f"Explain one important concept every {role_name} should know and include a practical example."
    prompt = f"Generate one concise text interview question for a {role_name}. Return only the question."
    return _call_gemini(prompt)


def gemini_evaluate_answer(question, answer):
    if not settings.GEMINI_API_KEY:
        return {
            "score": 70,
            "feedback": "Demo feedback: configure GEMINI_API_KEY to receive AI evaluation. The answer was saved successfully.",
        }
    prompt = (
        "Evaluate this interview answer. Return a score from 0 to 100 and short feedback.\n"
        f"Question: {question}\nAnswer: {answer}"
    )
    text = _call_gemini(prompt)
    score = _extract_score(text)
    return {"score": score, "feedback": text}


def _call_gemini(prompt):
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{settings.GEMINI_MODEL}:generateContent?key={settings.GEMINI_API_KEY}"
    )
    response = requests.post(
        url,
        json={"contents": [{"parts": [{"text": prompt}]}]},
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()


def _extract_score(text):
    for token in text.replace("/", " ").replace(":", " ").split():
        if token.isdigit():
            return max(0, min(100, int(token)))
    return 70
