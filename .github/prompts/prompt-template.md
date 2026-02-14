# Prompt Template for AI Coding Assistant

<!--
This is a template for creating detailed prompts to run with GitHub Copilot or other AI coding assistants.
Edit this file in VS Code, then copy the content to the AI assistant chat.

Instructions:
1. Copy this template to a new file (e.g., .github/prompts/task-name.md)
2. Fill in the sections below with your specific requirements
3. Copy the entire content and paste into Copilot chat
4. Review the generated TODO list before proceeding
-->

## Task Overview
<!-- Brief description of what you want to accomplish -->
[Describe the main goal or task here]

## Context
<!-- Provide relevant background information -->
- Current state: [Describe current situation]
- Related files: [List relevant files or directories]
- Dependencies: [Any tools, libraries, or systems involved]
- Constraints: [Any limitations or requirements to consider]

## Requirements
<!-- List specific requirements or acceptance criteria -->
1. [First requirement]
2. [Second requirement]
3. [Third requirement]

## Expected Behavior
<!-- Describe what should happen after the task is complete -->
- [Expected outcome 1]
- [Expected outcome 2]

## Additional Notes
<!-- Any other relevant information, edge cases, or considerations -->
- [Additional note 1]
- [Additional note 2]


## Instructions for AI Assistant

**IMPORTANT**:

- Create a TODO list for this task - DO NOT implement any changes yet
- Save the TODO list as a markdown file in `.github/todo/` directory (e.g., `.github/todo/task-name-todo.md`)
- The TODO should break down the work into logical, trackable steps
- Each TODO item should have a clear description and acceptance criteria
- Wait for confirmation before proceeding with implementation
- Follow Constitution standards (see `.github/CONSTITUTION.md`)
- Any unknowns should be asked as questions rather than making assumption in the Questions section

**Process**:

1. Read and understand all requirements above
2. Create a comprehensive TODO list using the `manage_todo_list` tool
3. The prompt/prompt-to-todo-prompt.md file must be references on the format of the TODO file
4. Save the TODO list as a markdown file in `.github/todo/` directory
5. Present the TODO list for review
6. Wait for explicit approval before making any code changes
7. Implement changes one TODO item at a time, marking each complete as you go

**Success Criteria**:

- [ ] TODO list created and saved to `.github/todo/` directory
- [ ] TODO list presented for review
- [ ] All requirements understood and captured in TODOs
- [ ] No code changes made until approved
- [ ] Clear plan for implementation provided

