---
name: typescript_config_review
description: Review and optimize tsconfig.json configuration
arguments:
  - name: config_path
    description: Path to tsconfig.json (default: tsconfig.json)
    required: false
    default: tsconfig.json
---

Review and optimize TypeScript configuration in '{config_path}'.

Analyze:
- Compiler options (strict mode, target, module)
- Type checking options
- Module resolution settings
- Path mappings and aliases
- Include/exclude patterns

Provide:
- Recommended configuration
- Explanation of each option
- Best practices for tsconfig.json
- Migration recommendations if needed
- Performance optimizations
