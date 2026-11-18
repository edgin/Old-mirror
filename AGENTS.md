# Old TV Mirror — Development Instructions

## Project guidance
- Read docs/AGENTS.md for existing project rules.
- Inspect source code before proposing changes.
- Preserve existing functionality and architecture.
- Do not modify unrelated files.
- Do not invent files, functions, APIs, or test results.

## Controlled workflow
1. ANALYZE: inspect relevant files and verify findings.
2. PLAN: propose minimal changes and verification steps.
3. APPROVAL: stop and wait for explicit user approval.
4. BUILD: implement only the approved changes.
5. REVIEW: inspect the actual implementation.
6. TEST: execute relevant tests and report results.

## Persistent plans
- Proposed plans belong in docs/plans/.
- Approved plans belong in docs/plans/approved/.
- Never treat a proposed plan as approved automatically.
- Only the user can authorize implementation.
- Before building, read the approved plan.
- If implementation requires changes outside the plan, stop and request approval.

## Agent responsibilities
- planner: read-only analysis and planning.
- build: implementation with edit and shell permissions.
- reviewer: independent read-only code review.
- tester: execute approved tests without modifying source code.
- teacher: explain code without modifying it.

## Completion requirements
- Report modified files.
- Report tests actually executed and their results.
- Clearly identify untested functionality.
- Never claim success without verification.
