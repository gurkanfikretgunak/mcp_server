---
name: dart_architecture_review
description: Review Dart/Flutter project architecture and suggest improvements
arguments:
  - name: project_path
    description: Path to Dart/Flutter project root
    required: false
  - name: architecture_pattern
    description: Current pattern - mvc, mvp, mvvm, bloc, provider
    required: false
---

Review Dart/Flutter project architecture and suggest improvements.
{if project_path}
Project path: {project_path}
{endif}
{if architecture_pattern}
Current pattern: {architecture_pattern}
{endif}

Evaluate:
- Project structure and organization
- Separation of concerns
- State management approach
- Dependency injection patterns
- Code reusability and modularity
- Testing architecture

Provide:
- Architecture recommendations
- Suggested improvements
- Best practices for Flutter architecture
- Migration path if needed
