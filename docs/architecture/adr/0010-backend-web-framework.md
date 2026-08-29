# 0010 — Backend web framework

**Scope.** Which Python web framework the HTTP/API-exposing containers use.
Not a `REGISTER.md` requirement ID — this is GIVEN directly from the kickoff
prompt's own brief ("Backend: Python. Justify the framework in an ADR; do not
reflex-pick FastAPI"), and shaped by `REG-08` (a published OpenAPI spec is
itself a named challenge deliverable).

## Context

`HLD.md` §3 lists ~20 containers with genuinely heterogeneous runtime shapes:
HTTP/REST-facing services (Registry Portal's onboarding API, `REG-08`;
Authorization/PDP's policy checks; Audit/Oversight's read-only dashboard
queries), a real-time signalling service (Live View Gateway's WebRTC/HLS
negotiation, `VMS-09`), and high-concurrency, I/O-bound edge services
(Connector SDK and Edge Agent managing up to ~2,353 concurrent outbound
camera connections per Netram node, per `CAPACITY.md` §6.1). Not every
container needs this decision — GPU-bound workers (Analytics Runtime) and
batch jobs (Merkle Tree Builder) need an async runtime and a task/queue
library, not a web framework; that is a separate, smaller, later choice.

## Options considered

1. **Django + Django REST Framework.** Batteries-included, mature ORM, an
   admin panel that's a genuine head start on P5's ops screens, enormous
   ecosystem — about as "boring" as Python web frameworks get. But its async
   support (ASGI, async views) is a retrofit onto a synchronous-by-design
   core, not its ecosystem's strength — a poor fit for the Connector
   SDK/Edge Agent's thousands-of-concurrent-connections workload, which is a
   textbook async-I/O problem.
2. **Flask** (+ an extension or hand-written OpenAPI). Extremely mature,
   minimal, stable API surface for over a decade — genuinely boring in the
   best sense. But synchronous by default (async support is a bolt-on, not
   core), and has no built-in OpenAPI generation — `REG-08`'s "published spec
   is itself a deliverable" becomes extra hand-written work rather than a
   by-product of the code.
3. **FastAPI** (Starlette/ASGI + Pydantic). Async-native from its
   foundations — a direct fit for the edge services' concurrency shape.
   Generates `REG-08`'s OpenAPI spec automatically from type-annotated code.
   Pydantic models double as the domain-model layer already established in
   `HLD.md`'s ubiquitous language. By 2026 it has a long enough adoption and
   stability track record to count as boring-by-now rather than novel — the
   kickoff's "don't reflex-pick" warning is heeded by *this* comparison
   existing, not by picking something else out of contrarianism.

## Decision

Option 3, FastAPI, uniformly across every container that exposes an HTTP or
WebSocket surface. Non-API containers (inference workers, batch jobs) are
explicitly out of this decision's scope — asyncio plus a task/queue library,
chosen later, not a web framework.

## Consequences

- `REG-08`'s OpenAPI specification is generated from the code, not
  hand-authored separately — removes a whole category of drift between the
  spec and the implementation.
- The Connector SDK and Edge Agent (WS-2) get native async I/O for
  high-concurrency outbound connections without a retrofit.
- Pydantic becomes the one data-modelling library spanning domain entities
  (`HLD.md` §1), request/response schemas, and (later) the message shapes on
  the Metadata Event Bus — one library, not three.
- Every API-exposing container shares one set of patterns (dependency
  injection for auth/jurisdiction checks, request validation, testing
  approach) — a deliberate uniformity choice, not an oversight.

## Reversibility cost

One-way-ish once several services are written against it — request/response
handling, dependency-injection style and testing approach all follow from
this choice. Sequenced first, before any other code, for exactly that reason.

## Revisit trigger

The WS-6 load test shows an async-runtime-attributable bottleneck in the
Connector SDK/Edge Agent under real concurrent-connection load — i.e., the
framework itself is the binding constraint, not the application code running
on top of it.

## What this does not cover

- The dependency-management tool (`uv`, pinned via `pyproject.toml`) — a
  mechanical, easily-reversed choice, not load-bearing enough for its own
  ADR.
- The database, message-queue and spatial-store products — already
  deferred by [ADR 0003](0003-viewshed-representation.md) and
  [ADR 0004](0004-vendor-connector-port.md), not decided here either.
- The async task/queue library for non-API workers — a later, separate,
  smaller decision.
