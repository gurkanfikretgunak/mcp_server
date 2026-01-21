---
name: typescript_decorator_guide
description: Guide for using TypeScript decorators and metadata
arguments:
  - name: use_case
    description: Use case - class_decorators, method_decorators, or property_decorators
    required: false
---

Provide a comprehensive guide for using TypeScript decorators and metadata.
{if use_case}
Use case: {use_case}
{endif}

Cover:
- Class decorators (class factories, mixins)
- Method decorators (logging, validation)
- Property decorators (observables, validation)
- Parameter decorators
- Decorator factories
- Metadata reflection API

Include:
- Code examples for each type
- Common use cases (Angular, NestJS patterns)
- Best practices and limitations
- Experimental decorators vs standard decorators
