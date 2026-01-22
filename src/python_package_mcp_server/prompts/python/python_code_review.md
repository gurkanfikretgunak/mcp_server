---
name: python_code_review
description: Review Python code for best practices and PEP 8 compliance
arguments:
  - name: file_path
    description: Path to Python file(s) to review
    required: true
  - name: focus_areas
    description: Comma-separated focus areas - style, performance, security, type_hints, or all
    required: false
    default: all
---

Review Python code in '{file_path}' for best practices and PEP 8 compliance.
Focus areas: {focus_areas}

Check for:
- PEP 8 style guide compliance
- Proper naming conventions (snake_case, PascalCase, etc.)
- Code organization and structure
- Error handling and exception management
- Type hints usage (PEP 484)
- Documentation (docstrings)
- Performance considerations
- Security best practices
- Test coverage

Provide:
- Specific issues found with line numbers
- Suggestions for improvement
- Code examples for fixes
- References to relevant PEPs and best practices
