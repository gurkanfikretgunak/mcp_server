---
name: python_performance_optimization
description: Optimize Python code for better performance
arguments:
  - name: file_path
    description: Path to Python file(s) to optimize
    required: true
  - name: optimization_focus
    description: Focus area - algorithm, data_structures, i_o, or profiling
    required: false
---

Optimize Python code in '{file_path}' for better performance.
{if optimization_focus}
Optimization focus: {optimization_focus}
{endif}

Areas to analyze:
- Algorithm efficiency (time/space complexity)
- Data structure choices (list vs set vs dict)
- Loop optimization and comprehensions
- I/O operations (file, network, database)
- Memory usage and garbage collection
- Caching strategies
- Parallel processing opportunities

Provide:
- Performance bottlenecks identified
- Optimization suggestions with code examples
- Before/after performance comparisons
- Profiling recommendations
- Trade-offs between readability and performance
- When to use C extensions or Cython
