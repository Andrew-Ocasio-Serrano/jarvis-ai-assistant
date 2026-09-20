# JARVIS — Personal AI Assistant (V1)

## Overview
A modular personal AI assistant, built to evolve from a simple text-based
LLM interface (V1) into a multimodal personal agent with memory, tool use,
and external integrations across future versions.

## Objective
Build the foundational version of a personal AI assistant: accept
natural-language text input and return contextual responses via an LLM
API, with the engineering and security habits in place to support future
versions.

### V1 Goals
- Establish project architecture
- Integrate an LLM API
- Accept text input, generate natural-language responses
- Implement basic error handling
- Protect API credentials
- Establish a Git-based development workflow

## Architecture

```
User (CLI)
   │
   ▼
config/settings.py   (loads + validates API key)
   │
   ▼
app/client.py         (lazily builds Groq client, wraps the API call)
   │
   ▼
Groq API (openai/gpt-oss-20b)
   │
   ▼
app/cli.py             (prints response, loops)
```

The client, settings, and CLI logic are deliberately separated by
responsibility (separation of concerns), so a change to one layer doesn't
cascade through the others. This was validated twice during V1's build:
the project originally targeted the Anthropic API and switched to Groq
mid-build after evaluating cost tradeoffs — the swap required changing
only `client.py`, with zero changes to `cli.py` or `main.py`.

A second, more important architectural lesson came from a real bug:
the Groq client was originally constructed at module-import time. Because
`main.py` imports `app.cli`, which imports `app.client`, the client was
being built — and failing on a missing API key — before `main.py`'s own
`validate_config()` check ever ran. The result was a raw SDK traceback
instead of the intended clean error message. Fixed via lazy
initialization: the client is now built on first use inside
`ask_jarvis()`, not on import, so configuration validation always runs
first. This is documented in more detail in `docs/CHANGELOG.md`.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application language |
| Groq API | LLM inference (`openai/gpt-oss-20b`) |
| python-dotenv | Environment configuration |
| pytest | Testing |
| Git / GitHub | Version control, portfolio |

**Why Groq:** originally built against the Anthropic API, switched after
evaluating cost for a low-volume prototype — Groq's free tier removed
billing risk entirely for V1's scope, with no functional downside.

**Why `openai/gpt-oss-20b`:** initial model selection (Llama 3.x) returned
a 404 — not available on this account's access tier. Verified actual
available models via the Groq API's `/models` endpoint rather than
assuming documentation matched account access, and selected
`openai/gpt-oss-20b` for its balance of speed and general-purpose quality.

## Installation

```bash
git clone https://github.com/Andrew-Ocasio-Serrano/jarvis-ai-assistant.git
cd jarvis-ai-assistant
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and add your Groq API key:

```
GROQ_API_KEY=your_key_here
```

Get a free key at [console.groq.com](https://console.groq.com).

## Usage

```bash
python main.py
```
Type a message and press Enter. Type `exit` or `quit` to stop.

## Testing

Run `pytest` from the project root. An empty `conftest.py` at the root
ensures `app`/`config` resolve correctly regardless of where pytest is
invoked from.

Current coverage (`tests/test_client.py`):
- `ask_jarvis()` returns a non-empty string for a simple prompt
- `ask_jarvis()` handles a distinct, short factual prompt correctly

**Tradeoff, made deliberately:** these tests make live calls to the Groq
API rather than mocking the client. This trades speed and offline
testability for confidence that the real integration works end-to-end —
appropriate for V1's small scope; mocking becomes worth revisiting once
test volume grows in later versions.

## Security

See [SECURITY.md](SECURITY.md) for the full threat model.

## Screenshots

See `docs/screenshots/` for the full build documentation, numbered
01–10, covering project setup through the first GitHub push.

## Limitations

- No memory — each session is stateless
- No external integrations, no tool-calling
- No system prompt constraining response behavior — during functional
  testing, an ambiguous long-form input (a narrative paragraph) caused
  the model to continue the story creatively rather than analyze or
  summarize it. This is expected given no instruction was given on how
  to interpret ambiguous input, and is a known V1 limitation rather than
  a bug.

## Roadmap

- **V2** — Controlled memory (SQLite-backed, not freely written by the model)
- **V3** — Tool-calling
- **V4** — Calendar/task integration
- **V5** — Email integration
- **V6** — Voice and image input
- **V7** — Messaging integrations (WhatsApp Business API)
- **V8** — Full autonomous morning briefing + secure automation

## Lessons Learned

[TODO — finish once V1 is pushed to GitHub. Draft points to expand:
naming/discovery conventions matter more than they seem (a single
misnamed test file cost real debugging time); import-time side effects
in Python can silently bypass your own error handling, and lazy
initialization is the fix; verifying live API access against
documentation, rather than trusting docs blindly, caught a real
account-specific gap.]