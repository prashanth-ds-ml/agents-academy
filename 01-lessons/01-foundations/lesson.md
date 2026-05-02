# Lesson 1 - What an agent really is

## Outcome

By the end of this lesson, you should be able to explain the difference between a chatbot, a workflow, and an agent in simple language.

## Core idea

An LLM is not automatically an agent.

- A **chatbot** answers.
- A **workflow** follows predefined steps.
- An **agent** can observe, decide, act, and use feedback from results.

## Mental model

Use this loop:

1. Observe the current state
2. Decide the next action
3. Act with a tool or a response
4. Observe the result
5. Repeat until done

## Key concepts

### 1. Model

The LLM reasons over text and chooses what to do next.

### 2. Tools

Tools are controlled functions that let the model do real work like reading a file or listing a folder.

### 3. State

State is everything the agent needs to remember right now: task, files created, messages, tool results, and constraints.

### 4. Memory

Memory is what you keep across time. This can live in files, notes, a database, or an Obsidian vault.

### 5. Loop

The loop is what makes the system an agent instead of just a one-shot prompt.

## Simple examples

### Chatbot

Input: "Explain what an agent is."

Output: an explanation only.

### Workflow

Input: "Create a report."

Behavior:
1. Read a file
2. Summarize it
3. Save output

The steps are fixed.

### Agent

Input: "Organize this folder and summarize what you changed."

Behavior:
1. Inspect folder
2. Decide categories
3. Move files
4. Re-check folder
5. Report changes

The next step depends on the result of the previous step.

## Why agents fail

Common reasons:

- unclear tool boundaries
- no stopping condition
- unsafe file access
- too much trust in the model
- weak state tracking

## First design rule

Keep the model responsible for **deciding** and keep Python responsible for **doing**.

## Practice prompt

Write your own answer to this:

> "What is the difference between a chatbot, a workflow, and an agent?"

Try to explain it in 5 lines without jargon.

## After this lesson

Open:

- `exercises.md`
- `..\..\02-projects\project-01-goal-planner\README.md`
