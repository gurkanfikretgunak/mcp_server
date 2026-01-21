---
name: dart_null_safety_check
description: Check Dart code for null safety compliance and migration needs
arguments:
  - name: file_path
    description: Path to Dart file(s) to check
    required: true
---

Check Dart code in '{file_path}' for null safety compliance.

Analyze:
- Null safety migration status
- Potential null pointer exceptions
- Proper use of nullable (?) and non-nullable types
- Null-aware operators (??, ?., !)
- Required vs optional parameters

Provide:
- Migration recommendations
- Code fixes for null safety issues
- Best practices for null handling
- Examples of safe null patterns
