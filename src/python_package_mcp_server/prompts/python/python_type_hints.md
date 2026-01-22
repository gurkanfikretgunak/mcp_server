---
name: python_type_hints
description: Add or improve type hints in Python code following PEP 484
arguments:
  - name: file_path
    description: Path to Python file(s) to add type hints to
    required: true
  - name: strictness
    description: Type hint strictness - basic, standard, or strict
    required: false
    default: standard
---

Add or improve type hints in Python code in '{file_path}' following PEP 484, 526, 544, 585, and 604.
Strictness level: {strictness}

Focus on:
- Function parameter and return type annotations
- Variable type annotations
- Generic types (list[T], dict[K, V])
- Optional and Union types
- Protocol types for structural subtyping
- TypedDict for dictionary structures
- Type aliases for complex types

Guidelines:
- Use typing module for complex types
- Avoid 'Any' type when possible
- Use Union or Protocol instead of Any
- Add type hints incrementally
- Ensure compatibility with mypy or pyright

Provide:
- Type-annotated code examples
- Explanation of type choices
- Migration path from untyped code
- Common patterns and best practices
