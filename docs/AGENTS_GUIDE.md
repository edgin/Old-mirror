# OpenCode Agents — Usage Guide

**Project:** Old Mirror  
**OpenCode version:** 1.19.3

## 1. Available agents

| Agent | Type | Responsibility |
|---|---|---|
| `plan` | Built-in, primary | Analyze tasks and prepare implementation plans |
| `build` | Built-in, primary | Implement features and fix bugs |
| `explore` | Built-in, subagent | Investigate code and find relevant files |
| `general` | Built-in, subagent | Handle general supporting tasks |
| `reviewer` | Custom, subagent | Review code and identify problems |
| `tester` | Custom, subagent | Run tests and verify application behavior |

### Custom agent permissions

- **Reviewer:** Cannot edit files. Shell commands require approval.
- **Tester:** Cannot edit files. Shell commands require approval.

These restrictions help keep code review and testing independent from implementation.

---

## 2. Recommended development workflow

Use this workflow for most features and bug fixes:

```text
         YOUR TASK
             |
             v
          @plan
    Analyze and investigate
    Prepare implementation plan
             |
             v
          @build
     Implement approved plan
             |
             v
        @reviewer
    Inspect changes independently
    Identify bugs and regressions
             |
             v
         @tester
      Run tests and verify
      application behavior
             |
             v
       YOUR DECISION
     Accept or request fixes
```

### Step 1 — Planning

Start with `@plan`.

Example:

```text
@plan

Investigate the camera connection issue.

Trace the frontend-to-backend flow.
Identify relevant files and explain the likely cause.
Propose a minimal implementation plan.

Do not modify any files.
```

Read the proposed plan before proceeding.

### Step 2 — Implementation

After approving the plan, use `@build`.

Example:

```text
@build

Implement the approved camera connection fix.

Keep changes focused.
Preserve existing functionality.
Avoid unrelated refactoring.

Explain which files you changed and why.
Run appropriate checks where possible.
```

### Step 3 — Code review

After implementation, use `@reviewer`.

Example:

```text
@reviewer

Review the current changes.

Look for:
- Functional bugs
- Regressions
- Security problems
- Error-handling issues
- Unnecessary complexity

Do not modify files.

Report findings with file paths and line numbers.
Give an APPROVED or CHANGES REQUIRED verdict.
```

### Step 4 — Testing

Use `@tester` to verify the implementation.

Example:

```text
@tester

Verify the latest implementation.

Inspect the existing test setup.
Run relevant tests.
Check application startup and API behavior where appropriate.

Do not modify source files.
Do not install packages without approval.

Report:
- Commands actually executed
- Tests passed
- Tests failed
- Anything not tested
```

### Step 5 — Fixing problems

If Reviewer or Tester finds problems:

1. Send the findings to `@build`.
2. Ask Build to fix the confirmed issues.
3. Run `@reviewer` again.
4. Run `@tester` again.

Repeat until the important issues are resolved.

---

## 3. When to use each agent

### @explore — Understand the codebase

Use when you don't know where something is implemented.

Example:

```text
@explore

Find where the video stream endpoint is defined.
Trace how the frontend requests the stream.
Explain the complete request flow.

Do not change files.
```

### @plan — Think before coding

Use when you know what you want but need a safe implementation approach.

### @build — Make changes

Use when you have an approved plan or a clearly defined implementation task.

### @reviewer — Inspect the code

Use after implementation to get an independent assessment.

### @tester — Verify functionality

Use when you need evidence that the application or a particular change works.

---

## 4. Important working rules

- Always inspect existing code before changing it.
- Do not assume files, functions, or components exist.
- Preserve the existing project architecture.
- Avoid unnecessary refactoring.
- Do not modify unrelated files.
- Never expose passwords, API keys, or credentials.
- Review shell-command approval requests before accepting them.
- Never claim tests passed unless they were actually executed.
- Distinguish verified results from assumptions.
- A successful code review does not replace testing.
- Passing tests do not replace code review.

---

## 5. Quick reference

| What I need | Agent |
|---|---|
| Find where something is implemented | `@explore` |
| Understand a bug | `@plan` |
| Prepare a technical solution | `@plan` |
| Implement a feature | `@build` |
| Fix a bug | `@build` |
| Review implementation | `@reviewer` |
| Find regressions | `@reviewer` |
| Run tests | `@tester` |
| Verify application behavior | `@tester` |

---

## 6. Complete task prompt template

Use this as a starting point for larger tasks:

```text
I need to implement the following:

[DESCRIBE THE TASK]

WORKFLOW:

1. Use @plan to inspect the relevant code and prepare
   an implementation plan.

2. Do not modify files during planning.

3. After I approve the plan, use @build to implement it.

4. Use @reviewer to independently inspect the changes.
   Reviewer must not modify files.

5. Use @tester to execute relevant tests and verify
   the implementation.
   Tester must not modify files or install packages
   without asking me first.

FINAL REPORT:

- Summary of the implementation
- Files changed
- Review findings
- Tests actually executed
- Test results
- Remaining problems or unverified areas
```

---

## 7. Project configuration locations

```text
old_mirror/
│
├── AGENTS.md
│
├── AGENTS_GUIDE.md
│
└── .opencode/
    ├── .gitignore
    │
    └── agents/
        ├── reviewer.md
        └── tester.md
```

- `AGENTS.md` contains general project instructions.
- `AGENTS_GUIDE.md` documents how to use the agents.
- `.opencode/agents/` contains custom agent definitions.

**Recommended approach:** Use Plan → Build → Reviewer → Tester for significant changes. For small, straightforward tasks, you can use Build directly and then verify the result.
