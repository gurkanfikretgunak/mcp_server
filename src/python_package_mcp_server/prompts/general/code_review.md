---
name: code_review
description: Review code for best practices and potential issues
arguments:
  - name: file_path
    description: Path to the file to review
    required: true
  - name: language
    description: Programming language (python, dart, typescript)
    required: false
    default: python
---

Review the code in '{file_path}' ({language}). Check for:
- Code quality and best practices
- Potential bugs or issues
- Performance optimizations
- Security concerns
- Code style and formatting
Provide constructive feedback and suggestions.
