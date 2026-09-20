# Changelog

## V1 — September 19, 2026

Built the core pipeline: CLI → settings loader → Groq client → response.
Established repo structure, secrets handling, testing pattern, and
security documentation that future versions build on.

Two real issues surfaced and fixed during the build:
- **Provider pivot**: originally scoped for the Anthropic API, switched
  to Groq mid-build after evaluating cost tradeoffs for a low-volume
  prototype. Validated the client abstraction's design — the swap
  required changing only `client.py`.
- **Import-time client construction bug**: the Groq client was being
  built when `client.py` was imported, before `validate_config()` ever
  ran, causing a raw SDK traceback instead of the intended clean error
  message on a missing API key. Fixed via lazy initialization.

No memory or tools yet — deliberately deferred to keep V1 scoped and
shippable.