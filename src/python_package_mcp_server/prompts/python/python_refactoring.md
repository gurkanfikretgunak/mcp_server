---
name: python_refactoring
description: Refactor Python code following PEP 8 and best practices
arguments:
  - name: file_path
    description: Path to Python file(s) to refactor
    required: true
  - name: refactoring_type
    description: Type - extract_function, extract_class, simplify_logic, or improve_naming
    required: false
---

Refactor Python code in '{file_path}' following PEP 8 and best practices.
{if refactoring_type}
Refactoring type: {refactoring_type}
{endif}

Focus on:
- Extracting functions and classes
- Simplifying complex logic
- Improving naming conventions
- Code organization and modularity
- Following PEP 8 style guide
- Adding type hints where appropriate
- Improving error handling

Provide:
- Refactored code examples
- Explanation of improvements
- Before/after comparisons
- Testing considerations
- Performance implications if any
