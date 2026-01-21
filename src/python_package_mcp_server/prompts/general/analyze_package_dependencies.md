---
name: analyze_package_dependencies
description: Analyze package dependencies and suggest updates
arguments:
  - name: package_name
    description: Name of the package to analyze (optional, analyzes all if not provided)
    required: false
---

{if package_name}Analyze the dependencies of the '{package_name}' package. Check for:{else}Analyze all project dependencies. Check for:{endif}
- Outdated packages that need updates
- Security vulnerabilities
- Unused dependencies
- Dependency conflicts
Provide recommendations for updates and improvements.
