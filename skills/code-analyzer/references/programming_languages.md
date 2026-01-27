# 编程语言支持配置参考

本文档详细说明了源代码分析器支持的编程语言配置，包括语法模式、抽象语法树结构、代码元素提取规则和特定语言的处理策略。

---

## 目录

1. [支持语言概览](#支持语言概览)
2. [Python语言配置](#python语言配置)
3. [JavaScript语言配置](#javascript语言配置)
4. [TypeScript语言配置](#typescript语言配置)
5. [Java语言配置](#java语言配置)
6. [C/C++语言配置](#cc语言配置)
7. [Go语言配置](#go语言配置)
8. [Rust语言配置](#rust语言配置)
9. [其他语言配置](#其他语言配置)
10. [语言扩展指南](#语言扩展指南)

---

## 支持语言概览

### 语言支持矩阵

| 编程语言 | 文件扩展名 | 支持级别 | 解析器 | 文档生成 |
|---------|-----------|---------|--------|---------|
| Python | .py, .pyi | 完整 | AST原生 | 完整 |
| JavaScript | .js, .jsx | 完整 | 正则+AST | 完整 |
| TypeScript | .ts, .tsx | 完整 | 正则+AST | 完整 |
| Java | .java | 完整 | 正则+AST | 完整 |
| C/C++ | .c, .cpp, .h | 基础 | 正则 | 基础 |
| Go | .go | 完整 | 正则+AST | 完整 |
| Rust | .rs | 完整 | 正则+AST | 完整 |
| PHP | .php | 基础 | 正则 | 基础 |
| Ruby | .rb | 基础 | 正则 | 基础 |
| Shell | .sh, .bash | 基础 | 正则 | 基础 |

### 文件扩展名映射

```python
EXTENSION_MAP = {
    # Python
    '.py': Language.PYTHON,
    '.pyi': Language.PYTHON,
    
    # JavaScript/TypeScript
    '.js': Language.JAVASCRIPT,
    '.jsx': Language.JAVASCRIPT,
    '.ts': Language.TYPESCRIPT,
    '.tsx': Language.TYPESCRIPT,
    
    # Java
    '.java': Language.JAVA,
    
    # C/C++
    '.c': Language.C,
    '.cpp': Language.CPP,
    '.cc': Language.CPP,
    '.cxx': Language.CPP,
    '.h': Language.C,
    '.hpp': Language.CPP,
    
    # C#
    '.cs': Language.CSHARP,
    
    # Go
    '.go': Language.GO,
    
    # Rust
    '.rs': Language.RUST,
    
    # PHP
    '.php': Language.PHP,
    
    # Ruby
    '.rb': Language.RUBY,
    
    # Shell
    '.sh': Language.SHELL,
    '.bash': Language.SHELL
}
```

---

## Python语言配置

### AST节点类型

Python标准库提供完整的AST支持，以下是常用的节点类型：

| 节点类型 | 说明 | 提取内容 |
|---------|------|---------|
| `ast.Module` | 模块根节点 | 所有定义 |
| `ast.ClassDef` | 类定义 | 类名、基类、方法、装饰器 |
| `ast.FunctionDef` | 函数定义 | 函数名、参数、返回值、函数体 |
| `ast.AsyncFunctionDef` | 异步函数定义 | 同FunctionDef |
| `ast.Assign` | 赋值语句 | 变量名、值 |
| `ast.Import` | 导入语句 | 导入的模块 |
| `ast.ImportFrom` | 从模块导入 | 模块名、导入名 |
| `ast.Expr` | 表达式语句 | 表达式值 |
| `ast.Return` | 返回语句 | 返回值 |
| `ast.If` | 条件语句 | 条件、真假分支 |
| `ast.For` | for循环 | 迭代变量、迭代对象、循环体 |
| `ast.While` | while循环 | 条件、循环体 |
| `ast.Try` | try语句 | try/except/finally块 |
| `ast.With` | with语句 | 上下文项、with_body |
| `ast.Raise` | raise语句 | 异常对象 |
| `ast.Assert` | assert语句 | 测试条件、消息 |

### 关键字列表

```python
KEYWORDS = {
    # 控制流关键字
    'if', 'elif', 'else',
    'for', 'while', 'do',
    'break', 'continue',
    'return', 'yield',
    
    # 定义关键字
    'def', 'class', 'lambda',
    
    # 导入导出
    'import', 'from', 'as',
    
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
    
    # 其他
    'assert', 'del',
    
    # 结构化模式匹配（3.10+）
    'match', 'case',
    
    # 类型提示
    'type', 'final',
}
```

### 字符串模式

```python
# 单引号字符串
message = 'This is a string'

# 双引号字符串
message = "This is a string"

# 三引号字符串（多行/文档字符串）
"""
This is a
multi-line string
"""

# 原始字符串（不转义）
path = r'C:\Users\Admin'

# 字节字符串
data = b'Hello'

# 格式字符串（f-string）
greeting = f'Hello, {name}!'
```

### 注释模式

```python
# 单行注释
def func():  # 行内注释

# 多行注释（实际上是多行字符串）
"""
This is a
multi-line comment
"""
```

### 类型注解模式

```python
# 变量注解
name: str = "John"
age: int = 25

# 函数参数和返回值注解
def greet(name: str, age: int) -> str:
    return f"Hello, {name}"

# 复杂类型
from typing import List, Dict, Optional, Union

def process(items: List[Dict[str, Union[str, int]]]) -> Optional[str]:
    pass

# 泛型
from typing import TypeVar, Generic

T = TypeVar('T')

class Container(Generic[T]):
    def __init__(self, value: T):
        self.value = value
```

### 装饰器模式

```python
# 装饰器定义
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper

# 装饰器使用
@my_decorator
@another_decorator
def my_function():
    pass
```

### 文档字符串格式

#### Google风格

```python
def func(arg1, arg2):
    """
    简短描述。

    详细描述，可以跨越多行。

    参数:
        arg1: 参数1的描述
        arg2: 参数2的描述

    返回:
        返回值的描述

    异常:
        ExceptionType: 异常描述

    示例:
        示例代码
    """
    pass
```

#### reST风格

```python
class MyClass:
    """
    类描述。

    :ivar attribute: 属性描述
    :param param: 参数描述
    """
    pass
```

#### NumPy风格

```python
def func(array, axis=None):
    """
    简短描述。

    详细描述。

    Parameters
    ----------
    array : type
        参数描述
    axis : int, optional
        参数描述

    Returns
    -------
    result : type
        返回值描述
    """
    pass
```

---

## JavaScript语言配置

### AST节点类型

JavaScript没有内置AST支持，使用自定义解析。以下是常用的模式：

| 模式类型 | 说明 | 匹配示例 |
|---------|------|---------|
| ClassDeclaration | 类声明 | `class MyClass {}` |
| FunctionDeclaration | 函数声明 | `function myFunc() {}` |
| ArrowFunction | 箭头函数 | `() => {}` |
| VariableDeclaration | 变量声明 | `const x = 1` |
| ImportDeclaration | 导入声明 | `import x from 'y'` |
| ExportDeclaration | 导出声明 | `export { x }` |

### 关键字列表

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
    
    // 其他
    'void', 'null', 'true', 'false', 'in', 'of', 'yield',
    'delete', 'with', 'enum', 'export', 'extends', 'import', 'super',
    
    // 严格模式保留字
    'implements', 'interface', 'package', 'private',
    'protected', 'public', 'static',
}
```

### 字符串模式

```javascript
// 单引号字符串
const msg = 'Hello World';

// 双引号字符串
const msg = "Hello World";

// 模板字符串（反引号）
const name = 'World';
const msg = `Hello, ${name}!`;

// 多行模板字符串
const multiLine = `This is
a multi-line
string`;
```

### 注释模式

```javascript
// 单行注释

/* 多行注释 */

/**
 * JSDoc注释
 * @param {string} param - 参数描述
 * @returns {number} 返回值描述
 */
```

### JSDoc标签

```javascript
/**
 * 函数描述
 * 
 * @param {string} paramName - 参数描述
 * @param {number} [optionalParam] - 可选参数
 * @param {Object} options - 选项对象
 * @param {string} options.prop1 - 属性1描述
 * @param {boolean} [options.prop2=false] - 可选属性
 * @returns {string} 返回值描述
 * @throws {Error} 可能抛出的错误
 * @example
 * // 使用示例
 * myFunction('test', { prop1: 'value' });
 */
function myFunction(paramName, options) {
    // 函数实现
}
```

### 类定义模式

```javascript
/**
 * 类描述
 * 
 * @class
 * @property {string} prop1 - 属性1描述
 */
class MyClass {
    /**
     * 构造函数描述
     * @param {string} param - 参数描述
     */
    constructor(param) {
        /** @property {string} name - 名称 */
        this.name = param;
    }
    
    /**
     * 方法描述
     * @returns {void}
     */
    myMethod() {
        // 方法实现
    }
}
```

---

## TypeScript语言配置

### 扩展的JSDoc标签

TypeScript在JavaScript基础上增加了类型相关的标签：

```typescript
/**
 * 函数描述
 * 
 * @template T - 泛型参数描述
 * @param {T} item - 参数描述
 * @returns {T} 返回值描述
 * @typeParam T - 泛型参数描述
 */
function identity<T>(item: T): T {
    return item;
}

/**
 * 接口描述
 * 
 * @interface
 * @template T - 泛型参数
 */
interface MyInterface<T> {
    /** @property {T} value - 值属性 */
    value: T;
    /** @method */
    method(): T;
}

/**
 * 类型别名描述
 * 
 * @typedef {Object} MyType
 * @property {string} name - 名称属性
 * @property {number} age - 年龄属性
 */

/**
 * 泛型约束
 * 
 * @extends MyBaseClass
 * @implements MyInterface
 */
class MyClass extends MyBaseClass implements MyInterface {
    // 实现
}
```

### 类型注解模式

```typescript
// 基本类型
const name: string = "John";
const age: number = 25;
const isActive: boolean = true;
const notValue: null = null;
const notDefined: undefined = undefined;

// 数组类型
const numbers: number[] = [1, 2, 3];
const strings: Array<string> = ["a", "b", "c"];

// 对象类型
interface User {
    name: string;
    age: number;
    email?: string;  // 可选属性
}

const user: User = {
    name: "John",
    age: 25
};

// 联合类型
let id: string | number;
id = "abc";
id = 123;

// 交叉类型
type Person = { name: string } & { age: number };

// 函数类型
type Callback = (data: string) => void;
interface Handler {
    (event: Event): void;
}

// 泛型
class Container<T> {
    constructor(public value: T) {}
    
    getValue(): T {
        return this.value;
    }
}

// 字面量类型
type Status = "pending" | "active" | "completed";
```

### 接口定义模式

```typescript
/**
 * 接口描述
 * 
 * @interface
 */
interface IUserService {
    /**
     * 获取用户方法
     * @param {string} id - 用户ID
     * @returns {Promise<IUser>} 用户信息
     */
    getUser(id: string): Promise<IUser>;
    
    /**
     * 创建用户方法
     * @param {IUserInput} data - 用户数据
     * @returns {Promise<IUser>} 创建的用户
     */
    createUser(data: IUserInput): Promise<IUser>;
}
```

---

## Java语言配置

### AST节点类型（通过正则提取）

| 元素类型 | 模式示例 | 说明 |
|---------|---------|------|
| Class | `class MyClass {}` | 类定义 |
| Interface | `interface MyInterface {}` | 接口定义 |
| Enum | `enum MyEnum {}` | 枚举定义 |
| Method | `returnType methodName() {}` | 方法定义 |
| Field | `type fieldName;` | 字段定义 |
| Constructor | `ClassName(params) {}` | 构造函数 |

### 关键字列表

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
    'default', 'assert',
};
```

### 注释模式

```java
// 单行注释

/* 多行注释 */

/**
 * Javadoc注释
 * @author 作者名
 * @version 版本号
 * @since 起始版本
 * @param 参数名 参数描述
 * @return 返回值描述
 * @throws 异常类 异常描述
 * @exception 异常类 异常描述
 * @see 引用内容
 * {@code 代码}
 * {@link 引用}
 */
```

### 注解模式

```java
// 内置注解
@Override
@Deprecated
@SuppressWarnings("unused")

// 自定义注解
@MyAnnotation
@MyAnnotation(value = "test")
@MyAnnotation(name = "test", value = "test")

// 元注解
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
@Documented
@Inherited
public @interface MyAnnotation {
    String name() default "";
    String value() default "";
}
```

### 类定义模式

```java
/**
 * 类描述
 * 
 * @author 作者
 * @version 1.0
 * @since 1.0
 */
public class MyClass extends BaseClass implements MyInterface1, MyInterface2 {
    
    // 字段
    /** 字段描述 */
    private String myField;
    
    /**
     * 构造函数描述
     * @param param 参数描述
     */
    public MyClass(String param) {
        this.myField = param;
    }
    
    /**
     * 方法描述
     * @param args 可变参数
     * @return 返回值描述
     * @throws ExceptionType 异常描述
     */
    public ReturnType myMethod(String... args) throws ExceptionType {
        // 方法实现
    }
}
```

---

## C/C++语言配置

### AST节点类型（通过正则提取）

| 元素类型 | 模式示例 | 说明 |
|---------|---------|------|
| Class | `class MyClass {}` | 类定义 |
| Struct | `struct MyStruct {}` | 结构体定义 |
| Function | `ReturnType funcName() {}` | 函数定义 |
| Namespace | `namespace MyNS {}` | 命名空间 |
| Template | `template<typename T>` | 模板定义 |
| Include | `#include <header>` | 头文件包含 |

### 关键字列表

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
    'auto', 'register', 'goto',
};
```

### 注释模式

```cpp
// 单行注释

/* 多行注释 */

/**
 * Doxygen文档注释
 * @file 文件名
 * @brief 简要描述
 * @param[in] paramName 参数描述
 * @param[out] paramName 参数描述
 * @return 返回值描述
 * @exception exception 异常描述
 * @note 附加说明
 * @warning 警告信息
 */
```

### 头文件包含模式

```cpp
// 系统头文件
#include <iostream>
#include <vector>
#include <map>

// 本地头文件
#include "myheader.h"
#include "./path/to/header.h"

// 条件包含
#ifdef _WIN32
#include <windows.h>
#endif
```

### 模板定义模式

```cpp
/**
 * @brief 类模板描述
 * 
 * @tparam T 模板参数描述
 */
template<typename T>
class MyContainer {
private:
    std::vector<T> data;
    
public:
    /**
     * @brief 构造函数
     */
    MyContainer() = default;
    
    /**
     * @brief 添加元素
     * @param item 要添加的元素
     */
    void add(const T& item) {
        data.push_back(item);
    }
    
    /**
     * @brief 获取元素
     * @param index 元素索引
     * @return T 返回的元素
     */
    T get(size_t index) const {
        return data[index];
    }
};
```

---

## Go语言配置

### AST节点类型（通过正则提取）

| 元素类型 | 模式示例 | 说明 |
|---------|---------|------|
| Package | `package mypackage` | 包声明 |
| Function | `func myFunc() {}` | 函数定义 |
| Method | `func (r Receiver) Method() {}` | 方法定义 |
| Struct | `type MyStruct struct {}` | 结构体定义 |
| Interface | `type MyInterface interface {}` | 接口定义 |
| Type | `type MyType int` | 类型别名 |

### 关键字列表

```go
KEYWORDS = {
    // 程序结构
    'package', 'import', 'const', 'var', 'type',
    
    // 函数和结构
    'func',
    
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

### 注释模式

```go
// 单行注释

/* 多行注释 */

/**
 * 包文档注释
 * 
 * 这个包的详细描述
 * 可以跨越多行
 */
package mypackage

/**
 * 函数描述
 * 
 * @param paramName 参数描述
 * @return 返回值描述
 * @example
 * 示例代码
 */
func MyFunction(paramName string) ReturnType {
    // 函数实现
}
```

### 导入模式

```go
// 单行导入
import "fmt"
import "os"

// 导入块
import (
    "fmt"
    "os"
    "strings"
)

// 别名导入
import (
    f "fmt"
    myos "os"
)

// 点导入
import (
    . "fmt"
)

// 空白导入
import (
    _ "net/http/pprof"
)
```

### 结构体定义模式

```go
/**
 * 结构体描述
 * 
 * 结构体的详细描述
 * 可以跨越多行
 */
type MyStruct struct {
    // 字段描述
    Field1 string `json:"field1"`
    
    // 字段描述
    Field2 int `json:"field2"`
    
    // 私有字段
    privateField string
}

/**
 * 接口描述
 * 
 * 接口的详细描述
 */
type MyInterface interface {
    // 方法描述
    Method1(param string) int
    // 方法描述
    Method2() error
}
```

---

## Rust语言配置

### AST节点类型（通过正则提取）

| 元素类型 | 模式示例 | 说明 |
|---------|---------|------|
| Crate | `mod mymodule` | 模块声明 |
| Struct | `struct MyStruct {}` | 结构体定义 |
| Enum | `enum MyEnum {}` | 枚举定义 |
| Trait | `trait MyTrait {}` | trait定义 |
| Function | `fn my_func() {}` | 函数定义 |
| Impl | `impl MyStruct {}` | 实现块 |

### 关键字列表

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
    
    // 2021版关键字
    'try',
};
```

### 注释模式

```rust
// 单行注释

/* 多行注释 */

/** 
 * 内部文档注释 
 * 用于文档item的内部说明
 */

/**
 * 外部文档注释
 * 
 * # 参数
 * 
 * - `param1`: 参数1描述
 * - `param2`: 参数2描述
 * 
 * # 返回值
 * 
 * 返回值描述
 * 
 * # 示例
 * 
 * ```rust
 * let result = my_function();
 * ```
 */
fn my_function(param1: Type1, param2: Type2) -> ReturnType {
    // 函数实现
}
```

### 属性模式

```rust
// 条件编译
#[cfg(feature = "debug")]
fn debug_function() {}

#[allow(unused)]
fn unused_function() {}

// 衍生
#[derive(Debug, Clone, PartialEq)]
struct MyStruct {
    field: String,
}

// 属性宏
#[my_macro(attr = "value")]
fn macro_function() {}

// 内联
#[inline]
#[inline(always)]
#[inline(never)]
fn inlined_function() {}
```

### 结构体定义模式

```rust
/**
 * 结构体描述
 * 
 * 结构体的详细描述
 */
#[derive(Debug)]
pub struct MyStruct {
    /// 字段描述
    pub field1: String,
    
    /// 字段描述
    field2: i32,
    
    /// 借用字段
    ref_field: &str,
}

/**
 * 枚举描述
 * 
 * 枚举的详细描述
 */
pub enum MyEnum {
    /// 简单变体
    Simple,
    
    /// 元组变体
    Tuple(i32, String),
    
    /// 结构体变体
    Struct { x: i32, y: i32 },
}

/**
 * trait描述
 * 
 * trait的详细描述
 */
pub trait MyTrait {
    /**
     * 方法描述
     * @param param 参数描述
     * @returns 返回值描述
     */
    fn method(&self, param: Type) -> ReturnType;
}
```

---

## 其他语言配置

### PHP语言配置

```php
<?php
/**
 * PHP文件文档
 * 
 * PHP代码注释
 */

// 单行注释
# 单行注释

/*
 * 多行注释
 */

/**
 * 函数描述
 * 
 * @param string $paramName 参数描述
 * @return returnType 返回值描述
 */
function myFunction($paramName) {
    // 函数实现
}

/**
 * 类描述
 * 
 * @class
 */
class MyClass {
    /** @property string $prop1 属性描述 */
    public $prop1;
    
    /**
     * 方法描述
     * @return void
     */
    public function myMethod() {
        // 方法实现
    }
}
```

### Ruby语言配置

```ruby
# Ruby文件文档
# 
# Ruby代码注释

=begin
多行注释
=end

def my_method(param)
  # 方法实现
end

# 类定义
class MyClass
  # 属性描述
  attr_reader :name
  
  def initialize(name)
    @name = name
  end
  
  # 方法描述
  def my_method
    # 方法实现
  end
end
```

### Shell语言配置

```bash
#!/bin/bash
# Shell脚本文档
#
# Shell脚本注释

# 单行注释

# 函数定义
# @function 函数名
# @description 函数描述
my_function() {
    # 函数实现
    echo "Hello, $1"
}

# 变量
MY_VAR="value"

# 调用函数
my_function "World"
```

---

## 语言扩展指南

### 添加新语言支持

要添加对新编程语言的支持，需要实现以下步骤：

#### 1. 添加语言枚举值

```python
class Language(Enum):
    # ... 现有语言
    NEW_LANGUAGE = "new_language"
```

#### 2. 添加文件扩展名映射

```python
EXTENSION_MAP = {
    # ... 现有映射
    '.new_ext': Language.NEW_LANGUAGE,
}
```

#### 3. 实现解析器类

```python
class NewLanguageParser:
    """新语言解析器"""
    
    def parse(self, content: str, file_path: str) -> Dict[str, Any]:
        """
        解析新语言源代码
        
        Returns:
            Dict[str, Any]: 包含classes、functions、variables等
        """
        result = {
            'classes': [],
            'functions': [],
            'variables': [],
            'constants': [],
            'imports': [],
            'comments': []
        }
        
        # 实现解析逻辑
        # 提取类定义
        class_pattern = r'class\s+(\w+)'
        for match in re.finditer(class_pattern, content):
            result['classes'].append({
                'name': match.group(1),
                'line_number': content[:match.start()].count('\n') + 1,
                'methods': [],
                'file_path': file_path
            })
        
        # 提取函数定义
        func_pattern = r'func\s+(\w+)'
        for match in re.finditer(func_pattern, content):
            result['functions'].append({
                'name': match.group(1),
                'line_number': content[:match.start()].count('\n') + 1,
                'file_path': file_path
            })
        
        # 提取注释
        result['comments'] = self._extract_comments(content)
        
        return result
    
    def _extract_comments(self, content: str) -> List[Dict]:
        """提取注释"""
        comments = []
        lines = content.splitlines()
        
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('#'):
                comments.append({
                    'line': i,
                    'content': line.strip()[1:].strip()
                })
        
        return comments
```

#### 4. 注册解析器

```python
class ASTParser:
    def _init_parsers(self):
        self.parsers = {
            # ... 现有解析器
            Language.NEW_LANGUAGE: NewLanguageParser(),
        }
```

#### 5. 更新文档生成器

```python
class MarkdownGenerator:
    def _generate_overview(self, analysis_result: Dict) -> str:
        # 更新语言分布统计
        language_dist = statistics.get('language_distribution', {})
        if 'New Language' in language_dist:
            # 处理新语言
            pass
```

### 配置验证

```python
class LanguageConfigValidator:
    """语言配置验证器"""
    
    def validate_language_support(self, language: str) -> bool:
        """验证是否支持该语言"""
        return language in [e.value for e in Language]
    
    def validate_file_extension(self, extension: str) -> bool:
        """验证文件扩展名"""
        return extension in self.EXTENSION_MAP
    
    def get_language_info(self, language: str) -> Dict[str, Any]:
        """获取语言信息"""
        return {
            'extensions': self._get_extensions(language),
            'keywords': self._get_keywords(language),
            'comment_style': self._get_comment_style(language),
            'parser_class': self._get_parser_class(language)
        }
```
