---
name: project_setup_guide
description: Generate a comprehensive project setup guide
arguments:
  - name: include_dependencies
    description: Include dependency installation instructions
    required: false
    default: true
---

Generate a comprehensive project setup guide. Include:
- Prerequisites and requirements
{if include_dependencies}- Dependency installation instructions
{endif}
- Environment setup steps
- Configuration instructions
- How to run the project
- Common troubleshooting tips
Make it clear and easy to follow for new developers.
