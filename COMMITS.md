# Commit Message Guidelines

This project follows [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages.

## Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes that affect the build system or external dependencies (example scopes: uv, pip)
- **ci**: Changes to our CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files
- **revert**: Reverts a previous commit

## Scope

The scope should be the name of the package affected (as perceived by the person reading the changelog):

- `server`: Core server implementation
- `resources`: Resource handlers
- `tools`: Tool implementations
- `security`: Security features (auth, policy, audit)
- `transports`: Transport layer (stdio, http)
- `config`: Configuration management
- `cli`: CLI interface
- `docs`: Documentation
- `tests`: Test files

## Subject

- Use imperative, present tense: "change" not "changed" nor "changes"
- Don't capitalize the first letter
- No dot (.) at the end
- Maximum 72 characters

## Body

- Use imperative, present tense: "change" not "changed" nor "changes"
- Include the motivation for the change and contrast it with previous behavior
- Wrap at 72 characters
- Reference issues and pull requests liberally

## Footer

- Reference issues and pull requests that this commit closes
- Breaking changes should start with `BREAKING CHANGE:` followed by a description

## Examples

### Simple commit
```
feat(resources): add project index resource
```

### Commit with body
```
fix(tools): handle missing package names in install tool

Previously, the install tool would fail silently when no packages
were provided. Now it returns a proper error message.

Fixes #123
```

### Breaking change
```
feat(security): change authentication mechanism

BREAKING CHANGE: Authentication now requires API key in header
instead of query parameter. Update your client configuration.
```

### Multiple scopes
```
feat(resources,tools): add codebase search functionality

- Add codebase://search resource
- Add search_codebase tool
- Update project scanner with search capabilities
```

## Commit Message Best Practices

1. **Be specific**: Clearly describe what changed and why
2. **Be concise**: Keep the subject line under 72 characters
3. **Use present tense**: "Add feature" not "Added feature"
4. **Reference issues**: Link to related issues or PRs
5. **Group related changes**: One logical change per commit
6. **Write meaningful messages**: Future you (and others) will thank you

## Examples by Type

### Feature
```
feat(resources): add dependency tree visualization resource
```

### Bug Fix
```
fix(tools): prevent command injection in package manager wrapper
```

### Documentation
```
docs(readme): add troubleshooting section
```

### Refactoring
```
refactor(server): simplify resource registration logic
```

### Performance
```
perf(scanner): cache project structure to avoid repeated scans
```

### Test
```
test(tools): add integration tests for install tool
```

### Build
```
build(deps): update mcp SDK to version 1.25.0
```

### CI
```
ci(github): add automated testing workflow
```

### Chore
```
chore: update .gitignore to exclude log files
```
