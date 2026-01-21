---
name: dart_abstract_base_widget
description: Create abstract base widget classes for Flutter following best practices
arguments:
  - name: widget_name
    description: Name of the abstract base widget to create
    required: true
  - name: file_path
    description: Path where the abstract base widget should be created
    required: false
  - name: widget_type
    description: Type of widget - stateless, stateful, or custom
    required: false
---

Create an abstract base widget class '{widget_name}' for Flutter following Dart/Flutter best practices.
{if file_path}
Target file: {file_path}
{endif}
{if widget_type}
Widget type: {widget_type}
{endif}

Focus on:
- Defining clear abstract methods that subclasses must implement
- Providing common functionality and shared behavior
- Following Effective Dart guidelines for abstract classes
- Proper widget lifecycle management
- Type safety and null safety
- Documentation and API clarity
- Testing considerations for abstract widgets

Provide:
- Complete abstract base widget implementation
- Example concrete implementation
- Usage examples
- Best practices for abstract widget design
- Common patterns and anti-patterns to avoid
- Testing strategies for abstract widgets

Consider:
- Whether to extend StatelessWidget or StatefulWidget
- What methods should be abstract vs concrete
- How to handle common widget properties
- State management if using StatefulWidget
- Widget composition patterns
- Performance implications
- Reusability and extensibility
