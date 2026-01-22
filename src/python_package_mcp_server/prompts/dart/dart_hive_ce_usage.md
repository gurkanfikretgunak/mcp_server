---
name: dart_hive_ce_usage
description: Comprehensive guide for using hive_ce package (NoSQL database for Dart/Flutter)
arguments:
  - name: file_path
    description: Path to Dart file(s) using hive_ce
    required: false
  - name: focus_area
    description: Specific area - setup, basics, adapters, encryption, performance, or migration
    required: false
  - name: use_case
    description: Use case context - flutter_app, dart_cli, or web
    required: false
---

Comprehensive guide for using the hive_ce package in {if use_case}{use_case}{else}Dart/Flutter applications{endif}.
{if file_path}
Analyze hive_ce usage in: {file_path}
{endif}
{if focus_area}
Focus area: {focus_area}
{endif}

## Package Overview

hive_ce is a lightweight, high-performance NoSQL key-value database written in pure Dart for Flutter and Dart applications. It's a community continuation of Hive v2 with modern enhancements.

**Key Features:**
- Cross-platform support (mobile, desktop, browser)
- High performance with no native dependencies
- Built-in encryption support
- Flutter web WASM support
- DevTools Inspector extension for debugging
- Isolate support through IsolatedHive
- Automatic type adapter generation with @GenerateAdapters annotation
- Extended maximum type ID from 223 to 65,439
- Support for Sets, Duration, Freezed, and constructor parameter defaults
- HiveRegistrar extension for registering all adapters in one call

**Requirements:** Dart 3.0+

## Setup & Installation

### Adding to pubspec.yaml

```yaml
dependencies:
  hive_ce: ^2.18.0
  {if use_case == "flutter_app"}
  hive_ce_flutter: ^2.3.4
  {endif}

dev_dependencies:
  hive_ce_generator: ^2.0.0
  build_runner: ^2.4.0
```

### Initialization

{if use_case == "flutter_app"}
**Flutter Applications:**
```dart
import 'package:hive_ce_flutter/hive_ce_flutter.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Hive.initFlutter();
  // Your app code
  runApp(MyApp());
}
```
{endif}
{if use_case == "dart_cli"}
**Dart CLI Applications:**
```dart
import 'package:hive_ce/hive_ce.dart';

void main() async {
  Hive.init('path/to/data/directory');
  // Your app code
}
```
{endif}
{if use_case == "web"}
**Web Applications:**
```dart
import 'package:hive_ce/hive_ce.dart';

void main() async {
  await Hive.init('web_storage');
  // Your app code
}
```
{endif}
{if !use_case}
**Flutter Applications:**
```dart
import 'package:hive_ce_flutter/hive_ce_flutter.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Hive.initFlutter();
  runApp(MyApp());
}
```

**Dart CLI Applications:**
```dart
import 'package:hive_ce/hive_ce.dart';

void main() async {
  Hive.init('path/to/data/directory');
}
```

**Web Applications:**
```dart
import 'package:hive_ce/hive_ce.dart';

void main() async {
  await Hive.init('web_storage');
}
```
{endif}

## Basic Usage

### Opening Boxes

```dart
// Open a box (synchronous, no await needed)
final box = Hive.box('myBox');

// Open a lazy box (loads values on demand)
final lazyBox = await Hive.openLazyBox('myLazyBox');
```

### CRUD Operations

```dart
// Create/Update
box.put('name', 'David');
box.put('age', 30);
box.put('user', userObject); // Custom objects require type adapters

// Read
final name = box.get('name');
final age = box.get('age', defaultValue: 0);
final user = box.get('user');

// Delete
box.delete('name');
box.deleteAll(['name', 'age']); // Delete multiple keys
box.clear(); // Clear entire box

// Check existence
if (box.containsKey('name')) {
  // Key exists
}
```

### Type-Safe Operations

```dart
// Open typed box
final userBox = await Hive.openBox<User>('users');

// Type-safe operations
userBox.put('user1', User(name: 'John', age: 25));
final user = userBox.get('user1'); // Returns User?
```

## Type Adapters

### Custom Type Adapters

**1. Define your model:**
```dart
import 'package:hive_ce/hive_ce.dart';

part 'user.g.dart';

@HiveType(typeId: 0)
class User extends HiveObject {
  @HiveField(0)
  String name;
  
  @HiveField(1)
  int age;
  
  @HiveField(2)
  String? email; // Nullable field
  
  User({
    required this.name,
    required this.age,
    this.email,
  });
}
```

**2. Generate adapters:**
```bash
dart run build_runner build --delete-conflicting-outputs
```

**3. Register adapters:**
```dart
void main() async {
  await Hive.initFlutter();
  Hive.registerAdapter(UserAdapter());
  await Hive.openBox<User>('users');
  runApp(MyApp());
}
```

### Automatic Adapter Generation

Use `@GenerateAdapters` annotation for automatic generation:

```dart
import 'package:hive_ce/hive_ce.dart';

@GenerateAdapters([
  User,
  Post,
  Comment,
])
class AppAdapters {}

// Register all adapters at once
void main() async {
  await Hive.initFlutter();
  AppAdapters.registerAdapters();
  runApp(MyApp());
}
```

### Built-in Adapters

hive_ce includes adapters for:
- Primitive types (int, double, bool, String)
- Collections (List, Map, Set)
- DateTime, Duration
- Uint8List

### Freezed Support

```dart
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:hive_ce/hive_ce.dart';

part 'user.freezed.dart';
part 'user.g.dart';

@freezed
@HiveType(typeId: 0)
class User with _$User {
  const factory User({
    @HiveField(0) required String id,
    @HiveField(1) required String name,
    @HiveField(2) required int age,
  }) = _User;
}
```

## Advanced Features

### Encryption

```dart
import 'package:hive_ce/hive_ce.dart';

// Create encryption key (store securely!)
final key = Hive.generateSecureKey();

// Open encrypted box
final encryptedBox = await Hive.openBox(
  'secureBox',
  encryptionCipher: HiveAesCipher(key),
);

// Use normally - encryption is transparent
encryptedBox.put('secret', 'sensitive data');
final secret = encryptedBox.get('secret');
```

### IsolatedHive (Isolate Support)

```dart
import 'package:hive_ce/hive_ce.dart';

// Initialize in isolate
await IsolatedHive.init();

// Open boxes in isolate
final box = await IsolatedHive.openBox('myBox');
```

### Lazy Boxes

```dart
// Lazy boxes load values on demand (memory efficient)
final lazyBox = await Hive.openLazyBox('largeBox');

// Values are loaded when accessed
final value = await lazyBox.get('key');
```

### Box Compaction

```dart
// Compact box to reduce file size
await box.compact();

// Auto-compact when box grows too large
if (box.length > 1000) {
  await box.compact();
}
```

### DevTools Inspector

Install the Hive Inspector extension to visually inspect and edit boxes during development.

## Best Practices

### Performance Optimization

- Use lazy boxes for large datasets
- Compact boxes periodically
- Batch operations when possible
- Close boxes when not needed: `await box.close()`
- Use typed boxes for type safety

### Error Handling

```dart
try {
  final box = await Hive.openBox('myBox');
  box.put('key', 'value');
} on HiveError catch (e) {
  print('Hive error: $e');
} catch (e) {
  print('Unexpected error: $e');
}
```

### Data Migration

```dart
// Version your boxes
final box = await Hive.openBox('users', version: 2);

// Handle migration
if (box.version < 2) {
  // Migrate data
  final oldData = box.get('oldKey');
  box.put('newKey', migrateData(oldData));
  box.version = 2;
}
```

### Memory Management

- Close boxes when done: `await box.close()`
- Use lazy boxes for large datasets
- Avoid keeping references to entire boxes in memory
- Clear unused boxes: `await Hive.deleteBoxFromDisk('unusedBox')`

## Common Patterns

### Repository Pattern

```dart
class UserRepository {
  late Box<User> _box;
  
  Future<void> init() async {
    _box = await Hive.openBox<User>('users');
  }
  
  Future<void> saveUser(User user) async {
    await _box.put(user.id, user);
  }
  
  User? getUser(String id) {
    return _box.get(id);
  }
  
  Future<void> deleteUser(String id) async {
    await _box.delete(id);
  }
  
  List<User> getAllUsers() {
    return _box.values.toList();
  }
}
```

### State Management Integration

```dart
// With Provider/Riverpod
class UserNotifier extends StateNotifier<List<User>> {
  late Box<User> _box;
  
  UserNotifier() : super([]) {
    _init();
  }
  
  Future<void> _init() async {
    _box = await Hive.openBox<User>('users');
    state = _box.values.toList();
  }
  
  Future<void> addUser(User user) async {
    await _box.put(user.id, user);
    state = _box.values.toList();
  }
}
```

### Offline-First Apps

```dart
class DataService {
  late Box<Post> _localBox;
  final ApiService _apiService;
  
  Future<List<Post>> getPosts() async {
    // Try API first
    try {
      final posts = await _apiService.fetchPosts();
      // Cache locally
      for (final post in posts) {
        await _localBox.put(post.id, post);
      }
      return posts;
    } catch (e) {
      // Fallback to local cache
      return _localBox.values.toList();
    }
  }
}
```

## Migration Considerations

### Differences from Hive v2/v4

- **Type IDs**: Extended from 223 to 65,439
- **Performance**: Significantly faster (1M writes in ~20s vs ~85s)
- **File Size**: Smaller database files
- **New Features**: Automatic adapter generation, HiveRegistrar, better Freezed support

### Breaking Changes

- Requires Dart 3.0+
- Some API changes from Hive v2
- Type adapter registration may differ

### Migration Steps

1. Update pubspec.yaml to use `hive_ce` instead of `hive`
2. Update imports: `package:hive_ce/hive_ce.dart`
3. Regenerate type adapters if needed
4. Test thoroughly, especially encryption and isolate usage
5. Update type IDs if you were near the 223 limit

## Additional Resources

- Official package: https://pub.dev/packages/hive_ce
- Flutter package: https://pub.dev/packages/hive_ce_flutter
- Generator: https://pub.dev/packages/hive_ce_generator
- Documentation: Check pub.dev package page for latest examples and guides

{if file_path}
## Analysis Request

Please analyze the hive_ce implementation in {file_path} and provide:
- Code review for best practices
- Performance optimization suggestions
- Error handling improvements
- Type adapter usage review
- Migration recommendations if applicable
{endif}
