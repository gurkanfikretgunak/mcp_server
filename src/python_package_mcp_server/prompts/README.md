# Prompts Directory

This directory contains all MCP prompts organized by category. Each prompt is defined in a separate `.md` file, making it easy to add, modify, and manage prompts.

## Directory Structure

```
prompts/
├── general/          # General-purpose prompts (cross-language)
├── dart/            # Dart/Flutter-specific prompts
└── typescript/      # TypeScript-specific prompts
```

## Adding a New Prompt

To add a new prompt, simply create a new `.md` file in the appropriate category directory:

1. **Create the file**: `prompts/<category>/your_prompt_name.md`

2. **Add frontmatter** with prompt metadata:
   ```yaml
   ---
   name: your_prompt_name
   description: What this prompt does
   arguments:
     - name: arg1
       description: Argument description
       required: true
     - name: arg2
       description: Optional argument
       required: false
       default: default_value
   ---
   ```

3. **Write the prompt template** below the frontmatter:
   ```markdown
   Your prompt text here. Use {arg1} and {arg2} for placeholders.
   
   {if arg2}
   This section only appears if arg2 is provided.
   {endif}
   ```

4. **That's it!** The prompt will be automatically loaded when the server starts.

## Prompt File Format

### Frontmatter (YAML)

- **name** (required): Unique prompt identifier (must match filename without .md)
- **description** (required): Human-readable description
- **arguments** (optional): List of argument definitions
  - **name**: Argument name
  - **description**: Argument description
  - **required**: true/false
  - **default**: Default value (optional)

### Template Syntax

- **Placeholders**: `{argument_name}` - Replaced with argument value
- **Conditionals**: `{if argument_name}...{endif}` - Include content if argument is provided
- **Conditionals with else**: `{if argument_name}...{else}...{endif}` - Include different content based on argument

### Examples

**Simple prompt:**
```markdown
---
name: simple_prompt
description: A simple prompt
arguments: []
---

This is a simple prompt with no arguments.
```

**Prompt with arguments:**
```markdown
---
name: review_code
description: Review code
arguments:
  - name: file_path
    description: Path to file
    required: true
  - name: language
    description: Programming language
    required: false
    default: python
---

Review the code in '{file_path}' ({language}).
Check for bugs and suggest improvements.
```

**Prompt with conditionals:**
```markdown
---
name: conditional_prompt
description: Prompt with conditional content
arguments:
  - name: include_examples
    description: Include examples
    required: false
---

Analyze the code.
{if include_examples}
Here are some examples:
- Example 1
- Example 2
{endif}
```

## Categories

### General Prompts (`general/`)

Cross-language prompts for common development tasks:
- `analyze_package_dependencies.md`
- `code_review.md`
- `project_setup_guide.md`
- `dependency_audit.md`
- `code_formatting_check.md`

### Dart Prompts (`dart/`)

Dart/Flutter-specific prompts:
- `dart_migration_guide.md`
- `dart_performance_optimization.md`
- `dart_widget_refactoring.md`
- `dart_test_generation.md`
- `dart_null_safety_check.md`
- `dart_architecture_review.md`

### TypeScript Prompts (`typescript/`)

TypeScript-specific prompts:
- `typescript_migration_guide.md`
- `typescript_type_optimization.md`
- `typescript_refactoring.md`
- `typescript_test_generation.md`
- `typescript_config_review.md`
- `typescript_decorator_guide.md`
- `typescript_generics_guide.md`

## Benefits of File-Based Prompts

1. **Easy to Add**: Just create a `.md` file - no Python code changes needed
2. **Easy to Edit**: Edit markdown files directly
3. **Version Control**: Track prompt changes in git
4. **Collaboration**: Non-developers can contribute prompts
5. **Maintainability**: All prompts in one place, organized by category
6. **Hot Reload**: Prompts can be reloaded without restarting server (future feature)

## Template Variables

You can use these placeholders in your prompt templates:

- `{argument_name}` - Replaced with the argument value
- `{if argument_name}...{endif}` - Conditional content block
- `{if argument_name}...{else}...{endif}` - Conditional with alternative content

## Best Practices

1. **Use descriptive names**: Prompt names should clearly indicate their purpose
2. **Clear descriptions**: Help users understand when to use each prompt
3. **Document arguments**: Provide clear descriptions for all arguments
4. **Use defaults**: Set defaults for optional arguments when appropriate
5. **Organize by category**: Place prompts in the appropriate category directory
6. **Test your prompts**: Verify prompts work correctly after adding them

## Reloading Prompts

To reload prompts without restarting the server (if implemented):

```python
from python_package_mcp_server.prompts.loader import get_prompt_loader

loader = get_prompt_loader()
loader.reload()
```

## Troubleshooting

**Prompt not appearing?**
- Check file is in correct category directory
- Verify frontmatter is valid YAML
- Ensure `name` matches filename (without .md)
- Check server logs for errors

**Placeholders not working?**
- Use `{argument_name}` syntax (with curly braces)
- Ensure argument name matches exactly
- Check argument is provided when calling prompt

**Conditionals not working?**
- Use `{if arg}...{endif}` syntax
- Ensure proper nesting (no overlapping blocks)
- Check argument value is truthy
