---
name: typescript_generics_guide
description: Guide for using TypeScript generics effectively
arguments:
  - name: file_path
    description: Path to TypeScript file to analyze
    required: false
  - name: complexity_level
    description: Complexity - basic, intermediate, or advanced
    required: false
---

Provide a comprehensive guide for using TypeScript generics effectively.
{if file_path}
Analyze code in: {file_path}
{endif}
{if complexity_level}
Complexity level: {complexity_level}
{endif}

Cover:
- Basic generic syntax and usage
- Generic constraints (extends, keyof)
- Generic utility types
- Conditional types
- Mapped types
- Generic function overloads

Include:
- Practical examples
- Common patterns and anti-patterns
- When to use generics vs other type features
- Advanced generic techniques
