---
name: code_formatting_check
description: Check if code follows formatting standards
arguments:
  - name: file_path
    description: Path to the file or directory to check
    required: true
  - name: language
    description: Programming language (python, dart, typescript)
    required: true
---

Check if the code in '{file_path}' follows {language} formatting standards. Verify:
- Indentation and spacing
- Line length
- Naming conventions
- Import organization
- Code style guidelines
Report any formatting issues and suggest fixes.
