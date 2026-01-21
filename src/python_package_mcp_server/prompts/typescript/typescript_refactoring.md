---
name: typescript_refactoring
description: Refactor TypeScript code following best practices
arguments:
  - name: file_path
    description: Path to TypeScript file(s) to refactor
    required: true
  - name: refactoring_type
    description: Type - extract_function, extract_interface, or simplify_types
    required: false
---

Refactor TypeScript code in '{file_path}' following best practices.
{if refactoring_type}
Refactoring type: {refactoring_type}
{endif}

Focus on:
- Extracting functions and interfaces
- Simplifying complex types
- Improving type safety
- Code organization and modularity
- Following TypeScript style guide

Provide:
- Refactored code examples
- Explanation of improvements
- Type safety benefits
- Testing considerations
