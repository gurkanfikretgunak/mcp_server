---
name: dart_performance_optimization
description: Analyze and optimize Dart code for performance
arguments:
  - name: file_path
    description: Path to Dart file(s) to optimize
    required: true
  - name: focus_area
    description: Focus area - build_performance, runtime_performance, or memory
    required: false
---

Analyze and optimize Dart code in '{file_path}' for performance.
{if focus_area}
Focus area: {focus_area}
{endif}

Review:
- Build performance (widget rebuilds, const constructors)
- Runtime performance (async operations, collections)
- Memory usage (disposal, caching strategies)
- Code patterns that impact performance

Provide:
- Specific optimization recommendations
- Before/after code examples
- Performance metrics to track
- Best practices for Dart/Flutter performance
