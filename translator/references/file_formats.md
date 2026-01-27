# 文档格式参考指南

本文档详细说明了各种文档格式的翻译处理规范，包括结构识别、翻译策略和格式验证。

---

## 目录

1. [Markdown格式](#markdown格式)
2. [YAML格式](#yaml格式)
3. [JSON格式](#json格式)
4. [API文档格式](#api文档格式)
5. [代码文档格式](#代码文档格式)
6. [配置文件格式](#配置文件格式)

---

## Markdown格式

### 概述

Markdown是一种轻量级标记语言，广泛用于技术文档、README文件和API说明。翻译时需要保持其格式结构不变。

### 支持的元素

| 元素类型 | 语法示例 | 翻译处理 |
|---------|---------|---------|
| 标题 | `# Title` | 翻译标题文本，跳过`#`符号 |
| 段落 | `这是一段文字` | 完整翻译，保持换行 |
| 粗体 | `**text**` | 翻译内部文本，保留格式 |
| 斜体 | `*text*` | 翻译内部文本，保留格式 |
| 链接 | `[链接文本](url)` | 翻译链接文本，保留URL |
| 图片 | `![alt](url)` | 翻译alt文本，保留URL |
| 代码块 | ````code```` | 不翻译代码内容 |
| 行内代码 | `` `code` `` | 不翻译代码内容 |
| 列表 | `- item` | 翻译列表项，保留标记 |
| 引用 | `> text` | 翻译引用文本，保留`>` |
| 表格 | `\|col\|` | 翻译表格内容，保留结构 |
| 水平线 | `---` | 不翻译，保持原样 |

### 翻译规则

#### 标题处理

```markdown
# 系统架构设计

## 1. 概述

本文档描述了系统的整体架构...
```

**翻译后：**

```markdown
# 系统架构设计

## 1. 概述

本文档描述了系统的整体架构...
```

**注意事项：**
- 保留标题层级（`#`数量不变）
- 保留标题编号（如果存在）
- 跳过特殊字符（如`!`、`@`、`#`等）

#### 链接处理

```markdown
[API Reference](https://api.example.com/docs)
```

**翻译后：**

```markdown
[API 参考](https://api.example.com/docs)
```

**注意事项：**
- 翻译链接文本
- 保持URL不变
- 处理相对路径链接

#### 代码块处理

```markdown
下面是Python示例代码：

```python
def hello_world():
    """Print a greeting message."""
    print("Hello, World!")
```

**翻译后：**

```markdown
下面是Python示例代码：

```python
def hello_world():
    """Print a greeting message."""
    print("Hello, World!")
```

**注意事项：**
- 代码块内容不翻译
- 代码块的语言标识保持不变
- 代码块中的注释需要翻译

### 特殊格式处理

#### 任务列表

```markdown
- [x] 已完成任务
- [ ] 未完成的任务
```

**翻译后：**

```markdown
- [x] 已完成任务
- [ ] 未完成的任务
```

#### 锚点链接

```markdown
## 2. 详细设计

请参阅[详细设计](#2-详细设计)部分。
```

**翻译后：**

```markdown
## 2. 详细设计

请参阅[详细设计](#2-详细设计)部分。
```

**注意事项：**
- 锚点链接需要与标题翻译同步更新

---

## YAML格式

### 概述

YAML是一种人类可读的数据序列化格式，常用于配置文件、Ansible剧本和Kubernetes资源定义。

### 结构识别

```yaml
# 应用配置
app:
  name: MyApplication          # 应用名称
  version: 1.0.0               # 版本号
  description: A sample app    # 应用描述
  
  server:
    host: localhost            # 服务器地址
    port: 8080                 # 端口号
    
  features:
    - authentication           # 认证功能
    - logging                  # 日志功能
```

### 翻译规则

#### 可翻译字段

| 字段类型 | 示例 | 是否翻译 |
|---------|------|---------|
| 描述字段 | `description: "用户管理模块"` | 是 |
| 注释内容 | `# 用户管理模块` | 是 |
| 标题字段 | `title: Welcome` | 是 |
| 提示字段 | `message: "操作成功"` | 是 |
| 错误消息 | `error: "File not found"` | 是 |

#### 不可翻译字段

| 字段类型 | 示例 | 原因 |
|---------|------|------|
| 键名 | `app:`, `server:` | 配置标识符 |
| 路径 | `localhost:8080` | 网络地址 |
| 文件扩展名 | `.conf`, `.yaml` | 文件格式标识 |
| 环境变量 | `$APP_NAME` | 系统变量 |
| 布尔值 | `true`, `false` | 语言关键字 |
| 数字值 | `8080`, `1.0.0` | 数值数据 |

### 多行文本处理

```yaml
# 单行翻译
description: "This is a short description"

# 多行文本
long_description: |
  This is a long description
  that spans multiple lines.
  Each line should be translated.
```

**翻译后：**

```yaml
# 单行翻译
description: "这是一个简短的描述"

# 多行文本
long_description: |
  这是一个长描述
  跨越多行。
  每一行都应该被翻译。
```

### 数组元素翻译

```yaml
features:
  - name: Authentication      # 功能名称
    description: User login   # 功能描述
  - name: Authorization
    description: Access control
```

**翻译后：**

```yaml
features:
  - name: Authentication      # 功能名称
    description: 用户登录     # 功能描述
  - name: Authorization
    description: 访问控制
```

---

## JSON格式

### 概述

JSON是一种轻量级的数据交换格式，常用于API响应、配置文件和前端资源。

### 结构识别

```json
{
  "name": "MyApplication",
  "version": "1.0.0",
  "description": "A sample application",
  "config": {
    "server": {
      "host": "localhost",
      "port": 8080
    }
  },
  "features": [
    "authentication",
    "logging"
  ]
}
```

### 翻译规则

#### 可翻译字段

根据JSON结构中字段的值类型和用途判断：
- 字符串类型的描述字段
- 数组中的文本元素
- 嵌套对象中的描述信息

#### 不可翻译字段

- 键名（对象属性名）
- 数值类型的数据
- 布尔值
- null值
- 路径和URL字符串
- 变量引用

### 国际化JSON处理

```json
{
  "en": {
    "welcome": "Welcome to our application",
    "login": "Please login",
    "messages": {
      "success": "Operation successful",
      "error": "An error occurred"
    }
  },
  "zh-CN": {
    "welcome": "欢迎使用我们的应用",
    "login": "请登录",
    "messages": {
      "success": "操作成功",
      "error": "发生错误"
    }
  }
}
```

**处理策略：**
- 只翻译`en`部分的内容
- 保留`zh-CN`部分（如果已存在）
- 不翻译键名

### 数组JSON处理

```json
{
  "navigation": [
    {
      "label": "Home",
      "url": "/home"
    },
    {
      "label": "About",
      "url": "/about"
    }
  ]
}
```

**翻译后：**

```json
{
  "navigation": [
    {
      "label": "首页",
      "url": "/home"
    },
    {
      "label": "关于",
      "url": "/about"
    }
  ]
}
```

---

## API文档格式

### OpenAPI/Swagger

#### 结构识别

```yaml
openapi: 3.0.0
info:
  title: User Management API
  version: 1.0.0
  description: API for managing users

paths:
  /users:
    get:
      summary: Get all users
      description: Retrieve a list of all users
      parameters:
        - name: page
          in: query
          description: Page number
          schema:
            type: integer
      responses:
        '200':
          description: Successful response
```

#### 翻译规则

| 字段 | 是否翻译 | 说明 |
|-----|---------|------|
| `info.title` | 是 | API标题 |
| `info.description` | 是 | API描述 |
| `info.version` | 否 | 版本号 |
| `paths.summary` | 是 | 接口摘要 |
| `paths.description` | 是 | 接口描述 |
| `paths.operationId` | 否 | 操作标识符 |
| `parameters.name` | 否 | 参数名 |
| `parameters.description` | 是 | 参数描述 |
| `parameters.schema.type` | 否 | 数据类型 |
| `responses.description` | 是 | 响应描述 |
| `tags.name` | 是 | 标签名称 |

#### 翻译示例

**翻译前：**

```yaml
/users:
  get:
    summary: Get all users
    description: Retrieve a list of all registered users in the system.
    parameters:
      - name: page
        in: query
        description: The page number for pagination
      - name: limit
        in: query
        description: The number of items per page
    responses:
      '200':
        description: A list of users
```

**翻译后：**

```yaml
/users:
  get:
    summary: 获取所有用户
    description: 检索系统中所有已注册用户的列表。
    parameters:
      - name: page
        in: query
        description: 分页的页码
      - name: limit
        in: query
        description: 每页的项目数
    responses:
      '200':
        description: 用户列表
```

### GraphQL Schema

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  role: UserRole!
  createdAt: String!
  updatedAt: String
}

enum UserRole {
  ADMIN
  MODERATOR
  USER
}

input CreateUserInput {
  name: String!
  email: String!
  role: UserRole
}

type Query {
  users(page: Int, limit: Int): [User!]!
  user(id: ID!): User
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: CreateUserInput!): User!
  deleteUser(id: ID!): Boolean!
}
```

**翻译处理：**
- 类型描述和枚举值描述可以翻译
- 字段名称和类型不翻译
- 参数名称和类型不翻译

---

## 代码文档格式

### Python Docstring

#### Google风格

```python
def calculate_metrics(data: List[float]) -> Dict[str, float]:
    """
    Calculate statistical metrics for the given data.
    
    This function computes basic statistical measures including
    mean, median, standard deviation, and variance.
    
    Args:
        data: A list of numerical values
        precision: Number of decimal places (default: 4)
    
    Returns:
        A dictionary containing the calculated metrics
    
    Raises:
        ValueError: If the input data is empty
        TypeError: If the input contains non-numerical values
    """
    pass
```

**翻译后：**

```python
def calculate_metrics(data: List[float]) -> Dict[str, float]:
    """
    计算给定数据的统计指标。
    
    此函数计算基本统计量，包括
    均值、中位数、标准差和方差。
    
    参数:
        data: 数值列表
        precision: 小数位数（默认值: 4）
    
    返回:
        包含计算指标的字典
    
    异常:
        ValueError: 输入数据为空
        TypeError: 输入包含非数值
    """
    pass
```

#### reST风格

```python
class DataProcessor:
    """
    A class for processing and analyzing data.
    
    This class provides methods for data loading, cleaning,
    transformation, and statistical analysis.
    
    :ivar data: The raw input data
    :vartype data: pd.DataFrame
    
    :ivar cleaned_data: The processed data
    :vartype cleaned_data: pd.DataFrame
    """
    
    def process(self, method: str = 'standard'):
        """
        Process the data using the specified method.
        
        :param method: The processing method to use
        :type method: str
        :return: Processed data
        :rtype: pd.DataFrame
        """
        pass
```

### JavaScript JSDoc

```javascript
/**
 * Represents a user in the system.
 * @class
 */
class User {
  /**
   * Create a new user instance.
   * @param {string} id - The unique identifier
   * @param {string} name - The user's full name
   * @param {string} email - The user's email address
   * @param {string} [role='user'] - The user's role
   */
  constructor(id, name, email, role = 'user') {
    this.id = id;
    this.name = name;
    this.email = email;
    this.role = role;
  }
  
  /**
   * Update the user's profile information.
   * @param {Object} updates - The profile updates
   * @param {string} [updates.name] - New name
   * @param {string} [updates.email] - New email
   * @returns {Promise<void>}
   * @throws {Error} If the update fails
   */
  async updateProfile(updates) {
    // Implementation
  }
}
```

### Java JavaDoc

```java
/**
 * Service class for managing user operations.
 * This class provides business logic for user authentication,
 * profile management, and authorization.
 *
 * @author Development Team
 * @version 1.5.0
 * @since 2020-01-01
 */
public class UserService {
    
    /**
     * Authenticates a user with the given credentials.
     * 
     * This method validates the username and password,
     * and returns a JWT token upon successful authentication.
     *
     * @param username the user's username (must not be null or empty)
     * @param password the user's password (must not be null or empty)
     * @return {@link AuthenticationResult} containing the JWT token
     * @throws AuthenticationException if credentials are invalid
     * @throws IllegalArgumentException if parameters are null or empty
     */
    public AuthenticationResult authenticate(String username, String password) {
        // Implementation
    }
    
    /**
     * Retrieves a user by their unique identifier.
     *
     * @param userId the unique user identifier
     * @return {@link User} the user object if found
     * @throws UserNotFoundException if no user exists with the given ID
     */
    public User getUserById(String userId) {
        // Implementation
    }
}
```

---

## 配置文件格式

### 配置文件结构

#### INI格式

```ini
[application]
name = MyApp
version = 1.0.0
description = A sample application

[server]
host = localhost
port = 8080

[database]
host = localhost
port = 5432
name = mydb
user = admin
password = secret
```

**翻译规则：**
- 翻译注释
- 翻译描述性配置值
- 不翻译键名和值（如路径、端口等）

#### TOML格式

```toml
[title]

[owner]
name = "MyApp Team"
organization = "Example Corp"

[database]
server = "192.168.1.1"
ports = [8001, 8001, 8002]
connection_max = 5000
enabled = true

[servers]

[servers.alpha]
ip = "10.0.0.1"
dc = "eqdc10"

[servers.beta]
ip = "10.0.0.2"
dc = "eqdc10"
```

### 环境变量处理

```yaml
# 配置文件
app:
  name: ${APP_NAME}
  api_key: ${API_KEY}
  debug: ${DEBUG:-false}
```

**处理策略：**
- 环境变量引用不翻译
- 保留`${variable}`语法
- 仅翻译纯文本描述

---

## 特殊格式处理

### 保留内容识别

#### 占位符模式

| 模式 | 示例 | 处理方式 |
|-----|------|---------|
| 格式化字符串 | `"Hello, {name}"` | 翻译内部文本，保留占位符 |
| printf格式 | `"Value: %d"` | 翻译外部文本，保留格式符 |
| 模板变量 | `"${variable}"` | 不翻译 |
| 正则表达式 | `"/[a-z]+/"` | 不翻译 |

#### 特殊语法

```python
# SQL语句中的字符串（不翻译）
query = "SELECT * FROM users WHERE name = 'John'"

# 正则表达式（不翻译）
pattern = r"^[a-zA-Z0-9_-]+$"

# 格式字符串（保留占位符）
message = "User {username} logged in at {time}"
```

### 混合内容处理

```markdown
# 用户管理模块

该模块提供用户认证和授权功能。

```python
def authenticate(username, password):
    """
    验证用户凭据
    
    Args:
        username: 用户名
        password: 密码
    
    Returns:
        bool: 认证结果
    """
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return True
    return False
```

See [API Documentation](#api-documentation) for more details.
```

**处理策略：**
- 翻译Markdown文本
- 翻译代码中的注释和文档字符串
- 保留代码语法
- 翻译普通链接文本，保留URL

---

## 格式验证

### Markdown验证规则

```python
def validate_markdown(content: str) -> ValidationResult:
    """
    验证Markdown格式完整性
    """
    result = ValidationResult()
    
    # 检查标题层级
    headers = re.findall(r'^(#+)\s', content, re.MULTILINE)
    if headers:
        max_level = max(len(h) for h in headers)
        if max_level > 6:
            result.add_warning("标题层级超过6级")
    
    # 检查代码块闭合
    code_blocks = re.findall(r'```(\w*)', content)
    close_blocks = re.findall(r'```', content)
    if len(code_blocks) != len(close_blocks):
        result.add_error("代码块未正确闭合")
    
    # 检查链接格式
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    for text, url in links:
        if not url.startswith(('http://', 'https://', '#', '/', 'mailto:')):
            result.add_warning(f"链接URL格式可能不正确: {url}")
    
    return result
```

### YAML验证规则

```python
def validate_yaml(content: str) -> ValidationResult:
    """
    验证YAML格式完整性
    """
    result = ValidationResult()
    
    try:
        data = yaml.safe_load(content)
        
        # 检查必需的字段
        required_fields = ['version', 'name']
        for field in required_fields:
            if field not in data:
                result.add_warning(f"缺少建议的字段: {field}")
        
    except yaml.YAMLError as e:
        result.add_error(f"YAML解析错误: {e}")
    
    return result
```

---

## 格式转换

### 编码处理

```python
def convert_encoding(content: str, from_encoding: str, to_encoding: str) -> str:
    """
    转换文件编码
    
    Args:
        content: 文件内容
        from_encoding: 原始编码
        to_encoding: 目标编码
        
    Returns:
        str: 转换后的内容
    """
    if from_encoding == to_encoding:
        return content
    
    try:
        decoded = content.encode(from_encoding).decode(to_encoding)
        return decoded
    except (UnicodeDecodeError, UnicodeEncodeError) as e:
        logger.warning(f"编码转换失败: {e}")
        return content
```

### 换行符处理

```python
def normalize_line_endings(content: str, line_ending: str = '\n') -> str:
    """
    标准化换行符
    
    Args:
        content: 文件内容
        line_ending: 目标换行符 ('\n', '\r\n', '\r')
        
    Returns:
        str: 标准化后的内容
    """
    # 统一使用\n作为中间格式
    normalized = content.replace('\r\n', '\n').replace('\r', '\n')
    # 转换为目标格式
    if line_ending == '\r\n':
        normalized = normalized.replace('\n', '\r\n')
    elif line_ending == '\r':
        normalized = normalized.replace('\n', '\r')
    
    return normalized
```

---

## 最佳实践

### 文件读取

```python
def read_file_with_encoding(file_path: str) -> Tuple[str, str]:
    """
    智能读取文件，自动检测编码
    
    Args:
        file_path: 文件路径
        
    Returns:
        Tuple[内容, 编码]
    """
    encodings = ['utf-8', 'utf-8-sig', 'gbk', 'gb2312', 'latin-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            return content, encoding
        except UnicodeDecodeError:
            continue
    
    # 最后尝试使用二进制模式
    with open(file_path, 'rb') as f:
        content = f.read()
    return content.decode('utf-8', errors='replace'), 'utf-8'
```

### 文件写入

```python
def write_file_with_encoding(file_path: str, content: str, encoding: str = 'utf-8') -> None:
    """
    写入文件，保留原始编码
    
    Args:
        file_path: 文件路径
        content: 文件内容
        encoding: 文件编码
    """
    # 确保目录存在
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # 写入文件
    with open(file_path, 'w', encoding=encoding, newline='') as f:
        f.write(content)
```

### 备份处理

```python
def backup_file(file_path: str) -> str:
    """
    备份原文件
    
    Args:
        file_path: 文件路径
        
    Returns:
        str: 备份文件路径
    """
    backup_path = f"{file_path}.bak"
    
    # 如果备份已存在，添加时间戳
    if os.path.exists(backup_path):
        timestamp = int(time.time())
        backup_path = f"{file_path}.{timestamp}.bak"
    
    import shutil
    shutil.copy2(file_path, backup_path)
    
    return backup_path
```
