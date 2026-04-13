---
name: run-prompt
description: Delegate one or more prompts to fresh sub-task contexts with parallel or sequential execution. Use when executing saved prompts from the prompts directory.
---

> **Before executing**, gather context:
> - Git status: `git status --short`
> - Recent prompts: `ls -t ./prompts/*.md | head -5`

# Run Prompt Skill

## Objective
Execute one or more prompts from `./prompts/` as delegated sub-tasks with fresh context. Supports single prompt execution and sequential execution of multiple prompts.

## Input
The user will specify which prompt(s) to run, which can be:

**Single prompt:**

- Empty (no arguments): Run the most recently created prompt (default behavior)
- A prompt number (e.g., "001", "5", "42")
- A partial filename (e.g., "user-auth", "dashboard")

**Multiple prompts:**

- Multiple numbers (e.g., "005 006 007")
- Multiple prompts are always executed sequentially

## Process

### Step 1: Parse Arguments
Parse the user's input to extract prompt numbers/names.

**Examples**
- "005" → Single prompt: 005
- "005 006 007" → Multiple prompts: [005, 006, 007], strategy: sequential

### Step 2: Resolve Files
For each prompt number/name:

- If empty or "last": Find the most recent file with `ls -t ./prompts/*.md | head -1`
- If a number: Find file matching that zero-padded number (e.g., "5" matches "005-*.md", "42" matches "042-*.md")
- If text: Find files containing that string in the filename

**Matching Rules**

- If exactly one match found: Use that file
- If multiple matches found: List them and ask user to choose
- If no matches found: Report error and list available prompts

### Step 3: Execute

#### Single Prompt

1. Read the complete contents of the prompt file
2. Create a new agent context and execute the prompt
3. Wait for completion
4. Archive prompt to `./prompts/completed/` with metadata
5. Commit all work:
   - Stage files modified with `git add [file]` (never `git add .`)
   - Determine appropriate commit type based on changes (fix|feat|refactor|style|docs|test|chore)
   - Commit with format: `[type]: [description]` (lowercase, specific, concise)
6. Return results

#### Sequential Execution

1. Read first prompt file
2. Create agent context with first prompt
3. Wait for completion
4. Archive first prompt
5. Read second prompt file
6. Create agent context with second prompt
7. Wait for completion
8. Archive second prompt
9. Repeat for remaining prompts
10. Commit all work:
    - Stage files modified with `git add [file]` (never `git add .`)
    - Determine appropriate commit type based on changes (fix|feat|refactor|style|docs|test|chore)
    - Commit with format: `[type]: [description]` (lowercase, specific, concise)
11. Return consolidated results

## Context Strategy
By delegating to a sub-task context, the actual implementation work happens in fresh context while the main conversation stays lean for orchestration and iteration.

## Output

### Single Prompt Output
✓ Executed: ./prompts/005-implement-feature.md
✓ Archived to: ./prompts/completed/005-implement-feature.md

**Results**
[Summary of what the sub-task accomplished]

### Sequential Output
✓ Executed SEQUENTIALLY:

1. ./prompts/005-setup-database.md → Success
2. ./prompts/006-create-migrations.md → Success
3. ./prompts/007-seed-data.md → Success

✓ All archived to ./prompts/completed/

**Results**
[Consolidated summary showing progression through each step]

## Critical Notes

- For sequential execution: Execute each prompt one at a time in order
- Archive prompts only after successful completion
- If any prompt fails, stop sequential execution and report error
- Provide clear, consolidated results for multiple prompt execution
- Always use `git add [specific-file]` - never `git add .`
