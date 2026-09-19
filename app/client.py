from groq import Groq
from config.settings import GROQ_API_KEY

MODEL = "openai/gpt-oss-20b"

_client = None

def get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=GROQ_API_KEY)
    return _client

def ask_jarvis(prompt: str) -> str:
    client = get_client()
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content