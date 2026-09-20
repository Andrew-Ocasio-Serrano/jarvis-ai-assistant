# Security

## Secrets management
- API key (GROQ_API_KEY) stored only in .env, never in source code
- .env excluded via .gitignore; verified with a manual grep for the
  key prefix before every push
- .env.example documents required variables without exposing values

## Threat model — V1 scope

V1's attack surface is intentionally small: a local CLI process holding
one API credential, no persistent storage, no network listener beyond
outbound calls to Groq, and no user data retained beyond the current
session.

Considered and mitigated:
- API key exposure via commit history → .gitignore + manual pre-push
  check for the key prefix
- Raw error output leaking implementation details on misconfiguration →
  initially failed (see below), now fixed via lazy client initialization
  so validate_config() always runs before any SDK call is attempted

A real failure found during testing: Step 8 of the build process
(deliberately removing the .env file to test error handling) initially
produced a raw groq.GroqError traceback instead of the intended clean
message. Root cause: the Groq client was instantiated at module-import
time, before main.py's own configuration check ran. This meant a
missing credential surfaced as an unhandled exception from a third-party
library rather than an intentional, informative error — a real gap
between designed behavior and actual behavior. Fixed via lazy
initialization: the client is now built only when ask_jarvis() is first
called, guaranteeing validate_config() runs first in every code path.

Considered, not yet mitigated (deferred):
- Uncontrolled API spend from repeated or malformed calls — no rate
  limiting or usage caps implemented in V1
- Adversarial/malicious prompt input — not a meaningful risk yet, since
  V1 has no tools or external data access for a prompt injection to act
  on; becomes relevant starting V3 (tool-calling)

## Deferred to future versions
- Authentication (V4+, once external services/accounts are involved)
- Rate limiting on API usage
- Audit logging (meaningful starting V3, once tool-calling exists)
- Least-privilege scoping per integration (V4+)