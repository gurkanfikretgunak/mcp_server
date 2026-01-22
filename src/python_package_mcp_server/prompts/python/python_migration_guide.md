---
name: python_migration_guide
description: Guide for migrating Python code between versions or patterns
arguments:
  - name: file_path
    description: Path to Python file(s) to migrate
    required: true
  - name: migration_type
    description: Migration type - python2_to_3, sync_to_async, or add_type_hints
    required: false
    default: python2_to_3
---

Guide for migrating Python code in '{file_path}'.
Migration type: {migration_type}

{if migration_type == "python2_to_3"}
Python 2 to 3 migration:
- Update print statements to print() function
- Fix string/bytes handling (unicode vs str)
- Update integer division (// vs /)
- Fix exception handling syntax
- Update dictionary methods (iteritems -> items)
- Fix relative imports
- Update xrange to range
{endif}

{if migration_type == "sync_to_async"}
Synchronous to asynchronous migration:
- Convert functions to async functions
- Replace blocking I/O with async I/O
- Use asyncio.gather() for parallel operations
- Update database queries to async versions
- Handle async context managers
- Update test code for async functions
{endif}

{if migration_type == "add_type_hints"}
Adding type hints:
- Add function parameter types
- Add return type annotations
- Add variable type hints
- Use typing module for complex types
- Ensure mypy/pyright compatibility
{endif}

Provide:
- Step-by-step migration guide
- Code examples before and after
- Common pitfalls and how to avoid them
- Testing strategies for migration
- Tools and resources for migration
