# 编程语言翻译参考指南

本文档详细说明了各种编程语言的翻译模式、关键字识别和特定语言的处理规则。

---

## 目录

1. [支持语言概览](#支持语言概览)
2. [Python](#python)
3. [JavaScript和TypeScript](#javascript和typescript)
4. [Java](#java)
5. [C和C++](#c和c)
6. [Go](#go)
7. [Rust](#rust)
8. [其他语言](#其他语言)
9. [语言特定规则](#语言特定规则)

---

## 支持语言概览

### 语言支持矩阵

| 编程语言 | 文件扩展名 | 字符串类型 | 注释类型 | 文档字符串 | 智能体支持 |
|---------|-----------|-----------|---------|-----------|-----------|
| Python | .py, .pyi | 单引号、双引号、三引号 | # | ✓ | python-translator |
| JavaScript | .js, .jsx | 单引号、双引号、模板字符串 | //, /* */ | JSDoc | chinese-commentator |
| TypeScript | .ts, .tsx | 单引号、双引号、模板字符串 | //, /* */ | TSDoc | chinese-commentator |
| Java | .java | 双引号 | //, /* */, /** */ | JavaDoc | chinese-commentator |
| C | .c | 双引号 | //, /* */ | Doxygen | go-translator-commenter |
| C++ | .cpp, .h | 双引号、原始字符串 | //, /* */ | Doxygen | go-translator-commenter |
| C# | .cs | 双引号、@"" | //, /* */, /// | XML Doc | go-translator-commenter |
| Go | .go | 反引号、双引号 | // | Godoc | go-translator-commenter |
| Rust | .rs | 双引号、原始字符串 | //, /* */, /// | RustDoc | rust-i18n-translator |
| PHP | .php | 单引号、双引号 | //, /* */, # | PHPDoc | shell-localizer-commenter |
| Ruby | .rb | 单引号、双引号 | #, =begin/=end | RDoc | shell-localizer-commenter |
| Shell | .sh, .bash | 单引号、双引号 | # | - | shell-localizer-commenter |

### 翻译优先级

当智能体选择不同时，根据以下优先级调用：
1. **代码智能体**：python-translator、chinese-commentator
2. **系统编程语言**：go-translator-commenter、rust-i18n-translator
3. **脚本语言**：shell-localizer-commenter

---

## Python

### 文件扩展名

- `.py` - 标准Python文件
- `.pyi` - 类型提示文件

### 字符串模式

#### 单引号字符串

```python
message = 'This is a single-quoted string'
error = 'File not found'
path = 'C:\\Users\\Admin'
```

#### 双引号字符串

```python
message = "This is a double-quoted string"
template = "Hello, {name}!"
sql = "SELECT * FROM users WHERE id = 1"
```

#### 三引号字符串

```python
# 多行字符串
description = """This is a
multi-line string
example."""

# 文档字符串
def function():
    """This is a docstring for the function."""
    pass
```

#### 原始字符串

```python
regex = r'\d{3}-\d{4}-\d{4}'
path = r'C:\Users\Admin\Documents'
```

#### 字节字符串

```python
data = b'Hello, World!'
binary = b'\x48\x65\x6c\x6c\x6f'
```

### 注释模式

#### 行内注释

```python
# This is a single-line comment
result = calculate(x, y)  # Calculate the result
```

#### 多行注释

```python
# This is a multi-line comment
# that spans several lines
# for documentation purposes
```

### 文档字符串模式

#### Google风格

```python
def function(arg1, arg2):
    """
    Short description of the function.
    
    Long description that can span multiple lines
    and provides detailed information.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2
    
    Returns:
        Description of return value
    
    Raises:
        Exception: When something goes wrong
    """
    pass
```

#### reST风格

```python
class MyClass:
    """
    Summary line for class.
    
    Extended description of class.
    
    :ivar attribute: Description of attribute
    :vartype attribute: type
    
    :param param: Description of param
    :type param: type
    """
    pass
```

#### NumPy风格

```python
def function(array, axis=None):
    """
    Summary line.
    
    Extended description of function.
    
    Parameters
    ----------
    array : type
        Description of array
    axis : int, optional
        Description of axis. The default is None.
    
    Returns
    -------
    result : type
        Description of result
    """
    pass
```

### Python关键字（不翻译）

```python
KEYWORDS = {
    # 控制流
    'if', 'elif', 'else',
    'for', 'while', 'do',
    'break', 'continue',
    'return', 'yield',
    
    # 定义
    'def', 'class', 'lambda',
    
    # 导入导出
    'import', 'from', 'as', 'export',
    
    # 异常处理
    'try', 'except', 'finally', 'raise',
    
    # 上下文管理
    'with', 'pass',
    
    # 布尔和空值
    'True', 'False', 'None',
    
    # 运算符
    'and', 'or', 'not', 'in', 'is',
    
    # 异步
    'async', 'await',
    
    # 作用域
    'global', 'nonlocal',
    
    # 类型相关
    'assert', 'del',
    
    # 结构化模式匹配（Python 3.10+）
    'match', 'case',
    
    # 类型提示
    'type', 'final',
}
```

### 特殊处理

#### f-string内部不翻译

```python
name = "John"
message = f"Hello, {name}!"  # 整个字符串不翻译
```

#### 字符串格式化不翻译

```python
message = "Hello, %s!" % name       # printf格式
message = "Hello, {}!".format(name) # str.format
message = f"Hello, {name}!"          # f-string
```

#### 变量引用不翻译

```python
variable_name = "This text can be translated"
print(variable_name)  # variable_name 不翻译
```

---

## JavaScript和TypeScript

### 文件扩展名

- `.js` - JavaScript文件
- `.jsx` - JavaScript React组件
- `.ts` - TypeScript文件
- `.tsx` - TypeScript React组件

### 字符串模式

#### 单引号字符串

```javascript
const message = 'This is a single-quoted string';
const path = 'C:\\Users\\Admin';
```

#### 双引号字符串

```javascript
const message = "This is a double-quoted string";
const json = '{"name": "John", "age": 30}';
```

#### 模板字符串

```javascript
const name = 'World';
const message = `Hello, ${name}!`;  // 内部变量不翻译
const multiline = `
  This is a
  multi-line string
`;
```

#### 标签模板

```javascript
const name = 'John';
const greeting = i18n`Hello, ${name}!`;  // 标签模板
```

### 注释模式

#### 行内注释

```javascript
// This is a single-line comment
const result = calculate(x, y); // Calculate the result
```

#### 多行注释

```javascript
/*
 * This is a multi-line comment
 * that spans several lines
 * for documentation purposes
 */
```

### JSDoc模式

#### 函数文档

```javascript
/**
 * Calculates the sum of two numbers.
 * 
 * This function performs addition and returns
 * the result of the calculation.
 * 
 * @param {number} a - The first number to add
 * @param {number} b - The second number to add
 * @returns {number} The sum of the two numbers
 * @throws {TypeError} If inputs are not numbers
 * 
 * @example
 * const result = add(2, 3);
 * console.log(result); // 5
 */
function add(a, b) {
    return a + b;
}
```

#### 类文档

```javascript
/**
 * Represents a user in the system.
 * 
 * This class provides methods for user authentication,
 * profile management, and authorization.
 * 
 * @property {string} id - The unique user identifier
 * @property {string} name - The user's full name
 * @property {string} email - The user's email address
 */
class User {
    /**
     * Create a new user instance.
     * 
     * @param {string} id - The unique identifier
     * @param {string} name - The user's full name
     * @param {string} email - The user's email address
     */
    constructor(id, name, email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }
    
    /**
     * Authenticates the user with the given password.
     * 
     * @param {string} password - The password to verify
     * @returns {Promise<boolean>} True if authentication succeeds
     * @throws {Error} If password verification fails
     */
    async authenticate(password) {
        // Implementation
    }
}
```

#### TypeScript特定

```typescript
/**
 * Interface for user data.
 * 
 * This interface defines the structure of user objects
 * used throughout the application.
 * 
 * @property id - The unique user identifier
 * @property name - The user's full name
 * @property email - The user's email address
 * @property [optionalProp] - Optional property
 */
interface User {
    id: string;
    name: string;
    email: string;
    optionalProp?: string;
}

/**
 * Type alias for user roles.
 * 
 * This type represents the possible roles a user can have
 * in the system.
 */
type UserRole = 'admin' | 'moderator' | 'user';

/**
 * Generic function to map over an array.
 * 
 * @typeParam T - The type of elements in the array
 * @typeParam U - The type of elements in the result array
 * @param array - The array to map over
 * @param mapper - The function to apply to each element
 * @returns A new array with the mapper function applied
 */
function map<T, U>(array: T[], mapper: (item: T) => U): U[] {
    return array.map(mapper);
}
```

### JavaScript关键字（不翻译）

```javascript
KEYWORDS = {
    // 变量声明
    'const', 'let', 'var',
    
    // 控制流
    'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'default',
    'break', 'continue', 'return', 'throw',
    
    // 异常处理
    'try', 'catch', 'finally',
    
    // 面向对象
    'new', 'this', 'class', 'extends', 'super',
    
    // 模块
    'import', 'export', 'default', 'from',
    
    // 异步
    'async', 'await',
    
    // 类型检查
    'typeof', 'instanceof',
    
    // 其他关键字
    'void', 'null', 'true', 'false', 'in', 'of', 'yield',
    'delete', 'void', 'with',
    
    // 严格模式
    'implements', 'interface', 'package', 'private',
    'protected', 'public', 'static',
};
```

### 特殊处理

#### React JSX内部不翻译

```jsx
const element = <h1>Hello, World!</h1>;  // JSX标签不翻译
```

#### 正则表达式不翻译

```javascript
const pattern = /^[a-zA-Z]+$/;
const match = pattern.test(input);
```

#### 模板字符串变量不翻译

```javascript
const name = getName();
const greeting = `Hello, ${name}!`;  // 变量引用不翻译
```

---

## Java

### 文件扩展名

- `.java` - Java源文件

### 字符串模式

#### 双引号字符串

```java
String message = "This is a string literal";
String path = "C:\\Users\\Admin";
String sql = "SELECT * FROM users WHERE id = 1";
```

#### 字符串拼接

```java
String greeting = "Hello, " + name + "!";  // 字符串部分可翻译
```

### 注释模式

#### 行内注释

```java
// This is a single-line comment
int result = calculate(x, y); // Calculate the result
```

#### 多行注释

```java
/*
 * This is a multi-line comment
 * that spans several lines
 */
```

### JavaDoc模式

#### 类文档

```java
/**
 * Service class for managing user operations.
 * 
 * This class provides business logic for user authentication,
 * profile management, and authorization.
 * 
 * @author Development Team
 * @version 1.5.0
 * @since 2020-01-01
 * 
 * @see UserRepository
 * @see AuthenticationService
 */
public class UserService {
    // Implementation
}
```

#### 方法文档

```java
/**
 * Authenticates a user with the given credentials.
 * 
 * This method validates the username and password,
 * and returns a JWT token upon successful authentication.
 * The token can be used for subsequent API calls.
 *
 * @param username the user's username (must not be null or empty)
 * @param password the user's password (must not be null or empty)
 * @param rememberMe whether to extend the token validity period
 * @return {@link AuthenticationResult} containing the JWT token and user info
 * @throws AuthenticationException if credentials are invalid
 * @throws IllegalArgumentException if parameters are null or empty
 * @deprecated Use {@link #authenticateWithMFA(String, String)} instead
 */
@Deprecated
public AuthenticationResult authenticate(String username, String password, boolean rememberMe) {
    // Implementation
}
```

#### 字段文档

```java
/**
 * The maximum number of login attempts before lockout.
 * 
 * This field defines how many failed login attempts are allowed
 * before the account is temporarily locked for security purposes.
 */
private int maxLoginAttempts = 5;

/**
 * The list of user roles assigned to this user.
 * 
 * This collection contains all roles that have been assigned
 * to the user for access control purposes.
 */
private List<String> roles;
```

#### 参数文档

```java
/**
 * Updates the user's profile information.
 * 
 * @param userId the unique identifier of the user to update
 * @param updates a map containing the profile fields to update
 * @return the updated user profile
 * @throws UserNotFoundException if no user exists with the given ID
 * @throws ValidationException if the updates contain invalid data
 */
public User updateProfile(String userId, Map<String, Object> updates) {
    // Implementation
}
```

### Java关键字（不翻译）

```java
KEYWORDS = {
    // 访问修饰符
    'public', 'private', 'protected',
    
    // 类定义
    'class', 'interface', 'enum', 'abstract', 'extends', 'implements',
    
    // 变量声明
    'final', 'static', 'transient', 'volatile',
    
    // 数据类型
    'void', 'boolean', 'byte', 'char', 'short', 'int', 'long', 'float', 'double',
    
    // 控制流
    'if', 'else', 'switch', 'case', 'default',
    'for', 'while', 'do', 'break', 'continue',
    
    // 异常处理
    'try', 'catch', 'finally', 'throw', 'throws',
    
    // 其他关键字
    'new', 'this', 'super', 'null', 'true', 'false',
    'return', 'package', 'import',
    'synchronized', 'native', 'instanceof',
};
```

### 特殊处理

#### 注解不翻译

```java
@Override
@Transactional(readOnly = true)
public User findById(Long id) {
    // 方法名和注解不翻译
}
```

#### 泛型不翻译

```java
List<String> users = new ArrayList<>();  // 类型参数不翻译
Map<String, User> userMap = new HashMap<>();
```

---

## C和C++

### 文件扩展名

- `.c` - C源文件
- `.cpp`, `.cxx`, `.cc` - C++源文件
- `.h`, `.hpp`, `.hxx` - 头文件

### 字符串模式

#### 双引号字符串

```cpp
std::string message = "This is a string literal";
const char* path = "C:\\Users\\Admin";
```

#### 原始字符串

```cpp
std::string regex = R"(\d{3}-\d{4}-\d{4})";
std::string path = R"(C:\Users\Admin)";
```

#### 宽字符字符串

```cpp
wchar_t* wideString = L"Wide character string";
```

### 注释模式

#### 行内注释（C++）

```cpp
// This is a single-line comment
int result = calculate(x, y); // Calculate the result
```

#### 多行注释

```cpp
/*
 * This is a multi-line comment
 * that spans several lines
 */
```

### Doxygen模式

#### 文件文档

```cpp
/**
 * @file utils.cpp
 * 
 * @brief Utility functions for the application.
 * 
 * This file contains helper functions for string manipulation,
 * date/time formatting, and file operations.
 * 
 * @author Development Team
 * @date 2024-01-01
 */

#include "utils.h"
```

#### 函数文档

```cpp
/**
 * @brief Calculate the sum of two numbers.
 * 
 * This function performs addition of two integer values
 * and returns the result.
 * 
 * @param a The first addend (must be non-negative)
 * @param b The second addend (must be non-negative)
 * @return The sum of a and b
 * @throws std::invalid_argument if inputs are negative
 * 
 * @code
 * int result = add(2, 3);
 * // result is 5
 * @endcode
 */
int add(int a, int b) {
    return a + b;
}
```

#### 类文档

```cpp
/**
 * @class DataProcessor
 * 
 * @brief Processes and transforms data streams.
 * 
 * This class provides methods for reading data from various
 * sources, applying transformations, and writing results.
 * 
 * @author Development Team
 * @version 1.0.0
 */
class DataProcessor {
public:
    /**
     * @brief Default constructor
     * 
     * Creates a new DataProcessor instance with default settings.
     */
    DataProcessor();
    
    /**
     * @brief Processes the input data
     * 
     * @param input The data to process
     * @return ProcessingResult containing the result
     */
    ProcessingResult process(const Data& input);
};
```

### C++关键字（不翻译）

```cpp
KEYWORDS = {
    // 数据类型
    'bool', 'char', 'double', 'float', 'int', 'long', 'short',
    'signed', 'unsigned', 'void', 'wchar_t', 'char16_t', 'char32_t',
    
    // 类和结构
    'class', 'struct', 'union', 'enum',
    
    // 访问控制
    'public', 'private', 'protected',
    
    // 继承和多态
    'virtual', 'override', 'final', 'explicit', 'const', 'constexpr',
    
    // 内存管理
    'new', 'delete', 'malloc', 'free',
    
    // 控制流
    'if', 'else', 'switch', 'case', 'default',
    'for', 'while', 'do', 'break', 'continue',
    
    // 异常处理
    'try', 'catch', 'throw',
    
    // 其他关键字
    'return', 'sizeof', 'typedef', 'using', 'namespace',
    'template', 'typename', 'static', 'extern', 'inline',
    'mutable', 'friend', 'this', 'nullptr', 'true', 'false',
    'alignas', 'alignof', 'decltype', 'noexcept', 'static_assert',
};
```

### C关键字（不翻译）

```c
KEYWORDS = {
    'auto', 'break', 'case', 'char', 'const', 'continue',
    'default', 'do', 'double', 'else', 'enum', 'extern',
    'float', 'for', 'goto', 'if', 'int', 'long', 'register',
    'return', 'short', 'signed', 'sizeof', 'static', 'struct',
    'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while',
};
```

---

## Go

### 文件扩展名

- `.go` - Go源文件

### 字符串模式

#### 双引号字符串

```go
message := "This is a regular string"
path := "C:\\Users\\Admin"
```

#### 反引号字符串（原始字符串）

```go
message := `This is a raw string`
regex := `\d{3}-\d{4}-\d{4}`
```

#### 字符串拼接

```go
greeting := "Hello, " + name + "!"
```

### 注释模式

#### 行内注释

```go
// This is a single-line comment
result := calculate(x, y) // Calculate the result
```

#### 包文档

```go
/*
Package utils provides utility functions for the application.

This package contains helper functions for string manipulation,
date/time formatting, and file operations. It is designed to be
reused across different parts of the application.

Example

  result := utils.Add(2, 3)
  fmt.Println(result) // 5
*/
package utils
```

### Godoc模式

#### 函数文档

```go
// Add calculates the sum of two numbers.
//
// This function performs addition of two integer values
// and returns the result. It is a simple utility function
// that demonstrates basic Go syntax.
//
// Parameters:
//   a: The first number to add
//   b: The second number to add
//
// Returns:
//   The sum of a and b
//
// Example:
//
//   result := Add(2, 3)
//   // result is 5
func Add(a, b int) int {
    return a + b
}
```

#### 类型文档

```go
// User represents a user in the system.
//
// This struct contains all the information about a user,
// including their identification, contact information,
// and access permissions. It is used throughout the
// authentication and authorization system.
type User struct {
    // ID is the unique identifier for the user
    ID string `json:"id"`
    
    // Name is the user's full name
    Name string `json:"name"`
    
    // Email is the user's email address
    Email string `json:"email"`
    
    // Role is the user's role in the system
    Role string `json:"role"`
}

// String returns a string representation of the User.
//
// This method implements the fmt.Stringer interface and
// returns a formatted string containing the user's ID and name.
func (u *User) String() string {
    return fmt.Sprintf("User{ID: %s, Name: %s}", u.ID, u.Name)
}
```

#### 方法文档

```go
// Validate checks if the user data is valid.
//
// This method performs validation on all user fields,
// including checking the email format and ensuring required
// fields are not empty.
//
// Returns:
//   error: nil if valid, otherwise an error describing the issue
func (u *User) Validate() error {
    if u.Email == "" {
        return errors.New("email is required")
    }
    // Additional validation...
    return nil
}
```

### Go关键字（不翻译）

```go
KEYWORDS = {
    // 程序结构
    'package', 'import', 'const', 'var', 'type',
    
    // 函数和结构
    'func', 'struct',
    
    // 接口
    'interface',
    
    // 控制流
    'if', 'else', 'switch', 'case', 'default', 'fallthrough',
    'for', 'range', 'break', 'continue', 'goto',
    
    // 并发
    'go', 'chan',
    
    // 异常处理
    'defer', 'panic', 'recover',
    
    // 流程控制
    'return',
    
    // 映射
    'map',
    
    // 保留字
    'nil', 'true', 'false',
    
    // 内置函数
    'make', 'new', 'len', 'cap', 'append', 'copy', 'delete',
    'panic', 'recover', 'print', 'println', 'printf',
    'complex', 'real', 'imag', 'close',
};
```

---

## Rust

### 文件扩展名

- `.rs` - Rust源文件

### 字符串模式

#### 双引号字符串

```rust
let message = "This is a string literal";
let path = "C:\\Users\\Admin";
```

#### 原始字符串

```rust
let regex = r"\d{3}-\d{4}-\d{4}";
let path = r"C:\Users\Admin";
let quote = r#"This string contains "quotes""#;
```

#### 字节字符串

```rust
let bytes = b"Hello";
let raw_bytes = br"C:\Users\Admin";
```

### 注释模式

#### 行内注释

```rust
// This is a single-line comment
let result = calculate(x, y); // Calculate the result
```

#### 外部文档注释

```rust
/// Calculates the sum of two numbers.
///
/// This function performs addition of two integer values
/// and returns the result. It is a simple utility function.
///
/// # Arguments
///
/// * `a` - The first number to add
/// * `b` - The second number to add
///
/// # Returns
///
/// The sum of a and b
///
/// # Examples
///
/// ```
/// let result = add(2, 3);
/// assert_eq!(result, 5);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

#### 内部文档注释

```rust
/*! Inner documentation comment
 * 
 * This is documentation for the enclosing item,
 * typically used for module-level documentation.
 */
```

### RustDoc模式

#### 结构体文档

```rust
/// Represents a user in the system.
///
/// This struct contains all the information about a user,
/// including their identification, contact information,
/// and access permissions.
///
/// # Fields
///
/// * `id` - The unique identifier for the user
/// * `name` - The user's full name
/// * `email` - The user's email address
///
/// # Example
///
/// ```
/// let user = User::new("123", "John", "john@example.com");
/// ```
pub struct User {
    /// The unique identifier for the user
    pub id: String,
    /// The user's full name
    pub name: String,
    /// The user's email address
    pub email: String,
}
```

#### 特征文档

```rust
/// A trait for types that can be serialized.
///
/// This trait provides methods for converting a type to
/// a serialized format, such as JSON or binary data.
///
/// # Implementing this Trait
///
/// Types that implement this trait must provide implementations
/// for the `serialize` method.
///
/// # Examples
///
/// ```
/// use serde::{Serialize, Serializer};
///
/// #[derive(Serialize)]
/// struct Point {
///     x: i32,
///     y: i32,
/// }
///
/// let point = Point { x: 1, y: 2 };
/// let serialized = serde_json::to_string(&point).unwrap();
/// ```
pub trait Serialize {
    /// Serializes this value into the given serializer.
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer;
}
```

### Rust关键字（不翻译）

```rust
KEYWORDS = {
    // 路径修饰符
    'as', 'pub', 'crate', 'use',
    
    // 声明
    'fn', 'let', 'const', 'static', 'mut', 'ref', 'move',
    
    // 类型定义
    'struct', 'enum', 'trait', 'impl', 'type',
    
    // 控制流
    'if', 'else', 'match', 'loop', 'while', 'for', 'break', 'continue',
    
    // 返回
    'return',
    
    // 异常
    'panic', 'assert', 'unreachable',
    
    // 泛型
    'where', 'dyn',
    
    // 生命周期
    '\'static', '\'a',
    
    // 布尔值
    'true', 'false',
    
    // 特殊类型
    'Self', 'self', 'super',
    
    // 保留关键字
    'abstract', 'become', 'box', 'do', 'final',
    'macro', 'override', 'priv', 'typeof', 'unsized', 'virtual', 'yield',
};
```

---

## 其他语言

### PHP

#### 文件扩展名

- `.php` - PHP脚本文件

#### 字符串模式

```php
$message = 'This is a single-quoted string';
$message = "This is a double-quoted string";
$heredoc = <<<EOT
This is a heredoc string
spanning multiple lines.
EOT;
```

#### 注释模式

```php
// This is a single-line comment
# This is also a single-line comment
/* This is a multi-line comment */
```

#### PHPDoc模式

```php
/**
 * This is a PHPDoc style comment for a class.
 * 
 * @package MyPackage
 * @author Author Name
 * @version 1.0.0
 */
class MyClass {
    /**
     * This is a method description.
     *
     * @param string $paramName Description of parameter
     * @return returnType Description of return value
     * @throws Exception Description of exception
     */
    public function myMethod($paramName) {
        // Implementation
    }
}
```

### Ruby

#### 文件扩展名

- `.rb` - Ruby脚本文件

#### 字符串模式

```ruby
message = 'This is a single-quoted string'
message = "This is a double-quoted string"
heredoc = <<~DOC
  This is a heredoc string
  spanning multiple lines.
DOC
```

#### 注释模式

```ruby
# This is a single-line comment
=begin
This is a multi-line comment
that spans several lines.
=end
```

#### RDoc模式

```ruby
# This is a RDoc style comment for a class.
#
# == Attributes
#
# [name] The name of the item
# [value] The value of the item
#
# == Example
#
#   MyClass.new("test", 123)
#
class MyClass
  # This is a method description
  #
  # @param [String] param_name description of parameter
  # @return [returnType] description of return value
  def my_method(param_name)
    # Implementation
  end
end
```

### Shell

#### 文件扩展名

- `.sh` - Bourne shell脚本
- `.bash` - Bash脚本

#### 字符串模式

```bash
message='This is a single-quoted string'
message="This is a double-quoted string"
```

#### 注释模式

```bash
# This is a single-line comment
```

#### 特殊处理

```bash
#!/bin/bash
# Shebang行不翻译

# 变量不翻译
echo $PATH
echo $HOME

# 命令替换
current_date=$(date +%Y-%m-%d)  # 日期命令不翻译
```

---

## 语言特定规则

### 1. 字符串字面量翻译规则

#### Python

```python
# 翻译用户可见消息
message = "Are you sure you want to delete this file?"  # 翻译
error = "File not found: %s"  # 保留格式符

# 不翻译内部标识符
logger.info("Processing file: %s", filename)  # filename不翻译
```

#### JavaScript

```javascript
// 翻译用户可见消息
message = "Are you sure you want to delete this file?";  // 翻译
error = `Error: ${errorMessage}`;  // 变量引用不翻译

// 不翻译正则表达式
pattern = /^[a-zA-Z]+$/;  // 不翻译
```

### 2. 注释翻译规则

#### 统一注释风格

```python
# 翻译前
# This function calculates the sum of two numbers
def add(a, b):
    return a + b

# 翻译后
# 该函数计算两个数的和
def add(a, b):
    return a + b
```

#### 多行注释

```python
# 翻译前
# This is a multi-line comment
# that provides detailed information
# about the following code

# 翻译后
# 这是一个多行注释
# 为下面的代码提供详细信息
```

### 3. 文档字符串翻译规则

#### 保持结构完整

```python
# 翻译前
def calculate_metrics(data):
    """
    Calculate statistical metrics for the given data.
    
    Args:
        data: A list of numerical values
        precision: Number of decimal places
    
    Returns:
        A dictionary containing the calculated metrics
    
    Raises:
        ValueError: If the input data is empty
    """
    pass

# 翻译后
def calculate_metrics(data):
    """
    计算给定数据的统计指标。
    
    参数:
        data: 数值列表
        precision: 小数位数
    
    返回:
        包含计算指标的字典
    
    异常:
        ValueError: 如果输入数据为空
    """
    pass
```

### 4. 错误消息翻译规则

#### 用户错误消息

```python
# 翻译用户可见错误
raise ValueError("The input data cannot be empty")  # 翻译

# 不翻译错误代码和标识符
raise HTTPError(404, "Not Found", headers)  # 404和HTTPError不翻译
```

### 5. 日志消息翻译规则

```python
# 翻译用户可见日志
logger.info("User %s has logged in", username)  # 消息文本翻译

# 不翻译日志级别
logger.debug("Processing item: %d", item_id)  # debug不翻译
logger.error("Failed to connect to database")  # 消息文本翻译
```

### 6. 测试代码翻译规则

#### 测试描述

```python
# 翻译测试名称和描述
def test_user_authentication_with_valid_credentials():
    """Test that users can authenticate with valid credentials."""
    # 翻译文档字符串
    pass

def test_user_login_success():
    """测试用户使用有效凭据可以成功登录。"""
    pass
```

### 7. 配置字符串翻译规则

#### 配置文件中的描述

```yaml
# 翻译前
app:
  description: "The main application configuration"
  features:
    - name: "Authentication"
      description: "User login and registration"

# 翻译后
app:
  description: "主应用程序配置"
  features:
    - name: "Authentication"
      description: "用户登录和注册"
```

---

## 术语映射示例

### 通用编程术语

| 英文 | 中文 | 适用语言 |
|-----|------|---------|
| function | 函数 | Python, JavaScript, Java, C++, Go, Rust |
| method | 方法 | Python, Java, C++, C# |
| class | 类 | Python, Java, C++, C#, JavaScript |
| variable | 变量 | 所有语言 |
| constant | 常量 | 所有语言 |
| parameter | 参数 | 所有语言 |
| argument | 实参 | 所有语言 |
| return | 返回 | 所有语言 |
| exception | 异常 | Python, Java, C++, C# |
| interface | 接口 | Java, C#, TypeScript, Go |
| abstract | 抽象 | Java, C++, C# |
| inheritance | 继承 | Python, Java, C++, C# |
| polymorphism | 多态 | Python, Java, C++, C# |
| encapsulation | 封装 | Python, Java, C++ |
| module | 模块 | Python, JavaScript |
| package | 包 | Java, Go, Rust |
| namespace | 命名空间 | C++, C# |
| library | 库 | 所有语言 |
| framework | 框架 | 所有语言 |
| API | API/应用程序接口 | 所有语言 |

### 异步编程术语

| 英文 | 中文 | 适用语言 |
|-----|------|---------|
| async | 异步 | Python, JavaScript, TypeScript |
| await | 等待 | Python, JavaScript, TypeScript |
| promise | 承诺/期约 | JavaScript, TypeScript |
| future | 未来/期物 | Python, Java, C++ |
| callback | 回调函数 | JavaScript |
| coroutine | 协程 | Python, Go, Rust |
| thread | 线程 | Java, C++, C#, Python |
| concurrent | 并发 | 所有语言 |
| parallel | 并行 | 所有语言 |

### 数据处理术语

| 英文 | 中文 | 适用语言 |
|-----|------|---------|
| stream | 流 | Java, C#, Python, Go |
| iterator | 迭代器 | Python, Java, C++ |
| generator | 生成器 | Python, JavaScript |
| lambda | lambda/匿名函数 | Python, Java, C#, JavaScript |
| filter | 过滤 | 所有语言 |
| map | 映射/变换 | 所有语言 |
| reduce | 归约 | 所有语言 |
| collection | 集合 | Java, C# |
| array | 数组 | 所有语言 |
| list | 列表 | Python, Java, C# |
| dictionary | 字典 | Python |
| map | 映射/字典 | Java, C++, Go |
| set | 集合 | Python, Java, C++, C# |
