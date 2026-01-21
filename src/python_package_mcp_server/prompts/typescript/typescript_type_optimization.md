---
name: typescript_type_optimization
description: Optimize TypeScript types for better type safety and performance
arguments:
  - name: file_path
    description: Path to TypeScript file(s) to optimize
    required: true
  - name: focus_area
    description: Focus - type_safety, performance, or readability
    required: false
---

Optimize TypeScript types in '{file_path}' for better type safety and performance.
{if focus_area}
Focus area: {focus_area}
{endif}

Review:
- Type safety (avoiding 'any', proper type definitions)
- Type performance (union types, generics efficiency)
- Type readability (clear type names, documentation)
- Generic type usage
- Utility types (Partial, Pick, Omit, etc.)

Provide:
- Optimized type definitions
- Before/after comparisons
- Explanation of improvements
- Best practices for TypeScript types
