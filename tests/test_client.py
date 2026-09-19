import pytest
from app.client import ask_jarvis


def test_client_returns_string_response():
    result = ask_jarvis("Say hello in one word.")
    assert isinstance(result, str)
    assert len(result) > 0


def test_client_handles_short_factual_prompt():
    result = ask_jarvis("What is 2 + 2?")
    assert isinstance(result, str)
    assert len(result) > 0