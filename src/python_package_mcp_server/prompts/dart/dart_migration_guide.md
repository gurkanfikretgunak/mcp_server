---
name: dart_migration_guide
description: Generate a migration guide for Dart/Flutter version upgrades
arguments:
  - name: from_version
    description: Current Dart/Flutter version
    required: false
  - name: to_version
    description: Target Dart/Flutter version
    required: false
  - name: file_path
    description: Path to Dart file(s) to migrate
    required: false
---

Generate a comprehensive Dart/Flutter migration guide{if from_version}{if to_version} from {from_version} to {to_version}{endif}{endif}.

Include:
- Breaking changes and deprecations
- Step-by-step migration instructions
- Code examples showing before and after
- Common pitfalls and how to avoid them
- Testing strategies during migration
{if file_path}
Focus on migrating: {file_path}
{endif}
Provide actionable guidance for a smooth migration.
