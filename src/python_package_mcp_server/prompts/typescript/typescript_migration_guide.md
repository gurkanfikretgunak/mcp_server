---
name: typescript_migration_guide
description: Generate migration guide for JavaScript to TypeScript or TypeScript version upgrades
arguments:
  - name: from_language
    description: Source - javascript or TypeScript version
    required: false
  - name: to_version
    description: Target TypeScript version
    required: false
  - name: file_path
    description: Path to file(s) to migrate
    required: false
---

Generate a comprehensive TypeScript migration guide{if from_language} from {from_language}{endif}{if to_version} to TypeScript {to_version}{endif}.

Include:
- Type annotations and type definitions
- Configuration setup (tsconfig.json)
- Step-by-step migration process
- Common JavaScript patterns and TypeScript equivalents
- Handling dynamic types and any
- Module system migration (CommonJS to ES modules)
{if file_path}
Focus on migrating: {file_path}
{endif}
Provide code examples and best practices.
