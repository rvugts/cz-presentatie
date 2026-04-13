---
name: run-prompt
description: Execute one or more saved prompt files from the prompts directory in fresh subagent contexts. Use when running prompts by number or name, or when continuing a generate-prompt workflow.
argument-hint: Prompt number, prompt name, or multiple prompt numbers
---

# Run Prompt

## Objective

Execute one or more prompts from `./prompts/` as delegated sub-tasks with fresh context. Support single prompt execution and sequential execution of multiple prompts.

For Copilot compatibility, use `runSubagent` to create the fresh execution context instead of assuming an implicit "new agent context" primitive.

## Before Executing

Gather minimal context first:

- Check workspace changes with `get_changed_files`; if unavailable, use non-interactive git status in the terminal
- Inspect available prompt files with `file_search` using `prompts/*.md`
- Use workspace-root absolute paths whenever a tool requires an absolute filesystem path

## Input

The user can specify prompts in any of these forms.

**Single prompt**

- Empty input: run the most recently created prompt
- A prompt number such as `001`, `5`, or `42`
- A partial filename such as `user-auth` or `dashboard`

**Multiple prompts**

- Multiple numbers such as `005 006 007`
- Multiple prompts are always executed sequentially

## Process

### Step 1: Parse Arguments

Parse the user's input into prompt selectors.

Examples:

- `005` → single prompt `005`
- `005 006 007` → sequential prompt list `[005, 006, 007]`
- empty input → most recent prompt

### Step 2: Resolve Prompt Files

Resolve each selector to exactly one prompt file.

Use these rules:

1. If the input is empty or `last`, determine the most recent prompt with a non-interactive terminal command such as `ls -t ./prompts/*.md | head -1`
2. If the input is numeric, zero-pad to three digits and use `file_search` with a pattern such as `prompts/005-*.md`
3. If the input is text, use `file_search` with a pattern such as `prompts/*dashboard*.md`

Matching rules:

- If exactly one match exists, use it
- If multiple matches exist, ask the user to choose with `vscode_askQuestions`
- If no matches exist, report the error and list available prompts from `./prompts/`

Only match files directly inside `./prompts/`. Do not treat `./prompts/completed/` as runnable input.

### Step 3: Execute Prompt Content With a Fresh Subagent Context

For each resolved prompt file:

1. Read the complete prompt file with `read_file`
2. Invoke `runSubagent` with a prompt that includes:
    - The prompt file path
    - The exact prompt contents
    - A directive to execute the prompt in the current workspace
    - A directive to make code changes if the prompt asks for them
    - A directive to return a concise result summary including changed files, tests run, and blockers
3. Wait for completion and capture the returned summary

Use a short description such as `Run prompt 005` for the subagent call.

For multiple prompts, execute them one at a time in order. If any prompt fails, stop immediately and report the failure without executing the remaining prompts.

### Step 4: Archive Each Executed Prompt

After a prompt completes successfully:

1. Ensure `./prompts/completed/` exists
2. Archive the prompt by moving it to `./prompts/completed/` with the same filename
3. Create a sidecar execution record in `./prompts/completed/` named `[prompt-name].execution.md`

The execution record should include:

- Original prompt path
- Archive path
- Execution status
- Execution date
- Subagent result summary
- Changed files, if any

If an archive target already exists, append a numeric suffix before moving the file so nothing is overwritten.

Because workspace file tools do not provide a generic rename operation, use a non-interactive terminal command for the move if necessary. Never use interactive git or shell workflows.

### Step 5: Commit Resulting Changes

After all successful prompt executions finish:

1. Inspect changed files with `get_changed_files`; if unavailable, use `git status --short`
2. Stage only the specific changed files plus the archived prompt file and execution record
3. Never use `git add .`
4. Determine the most appropriate commit type based on the changes: `fix`, `feat`, `refactor`, `style`, `docs`, `test`, or `chore`
5. Create one commit for the whole run with format `[type]: [description]`

If there are no file changes to commit, skip the commit step and simply report that no commit was necessary.

Prefer built-in git tooling when available. If git tools are unavailable, use non-interactive terminal commands.

## Execution Template For `runSubagent`

When invoking `runSubagent`, use a prompt shaped like this:

```text
Execute the following saved prompt from ./prompts/005-example.md in the current workspace.

Follow the prompt exactly. Use tools as needed. If the prompt requires code changes, make them. If it requires analysis, produce the requested output. Return a concise summary with:
- status
- files changed
- tests or verification performed
- blockers or follow-up items

Saved prompt contents:

[full prompt file contents]
```

## Output

### Single Prompt Output

```text
Executed: ./prompts/005-implement-feature.md
Archived to: ./prompts/completed/005-implement-feature.md
Execution record: ./prompts/completed/005-implement-feature.execution.md

Results:
[summary of what the sub-task accomplished]

Commit:
[commit hash and message, or "No commit created"]
```

### Sequential Output

```text
Executed sequentially:

1. ./prompts/005-setup-database.md -> Success
2. ./prompts/006-create-migrations.md -> Success
3. ./prompts/007-seed-data.md -> Success

Archived to: ./prompts/completed/

Results:
[consolidated summary showing progression through each step]

Commit:
[commit hash and message, or "No commit created"]
```

## Critical Notes

- Sequential execution means one prompt completes before the next starts
- Archive prompts only after successful completion
- If any prompt fails, stop the sequence and report the failure clearly
- Keep the main conversation lean by delegating the actual work to `runSubagent`
- Always use workspace-root absolute paths when calling tools that require absolute paths
- Always use non-interactive git commands if terminal git is required
- Always use `git add -- <specific-files>` rather than `git add .`

## Success Criteria

- Prompt selectors resolve to the intended files in `./prompts/`
- Each prompt is executed in a fresh subagent context via `runSubagent`
- Sequential runs stop on first failure
- Successful prompts are archived into `./prompts/completed/`
- Each successful prompt gets an execution record
- A commit is created only when there are actual changes to commit
- The final response clearly reports what ran, what changed, and whether a commit was created
