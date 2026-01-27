# Python MCP 服务器实现指南

## 概述

本文档提供使用 MCP Python SDK 实现 MCP 服务器的特定于 Python 的最佳实践和示例。它涵盖服务器设置、工具注册模式、使用 Pydantic 进行输入验证、错误处理以及完整的工作示例。

---

## 快速参考

### 关键导入
```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, Dict, Any
from enum import Enum
import httpx
```

### 服务器初始化
```python
mcp = FastMCP("service_mcp")
```

### 工具注册模式
```python
@mcp.tool(name="tool_name", annotations={...})
async def tool_function(params: InputModel) -> str:
    # 实现代码
    pass
```

---

## MCP Python SDK 和 FastMCP

官方 MCP Python SDK 提供了 FastMCP，这是一个用于构建 MCP 服务器的高级框架。它提供：
- 从函数签名和文档字符串自动生成描述和 inputSchema
- 用于输入验证的 Pydantic 模型集成
- 使用 `@mcp.tool` 装饰器的基于装饰器的工具注册

**要获取完整的 SDK 文档，请使用 WebFetch 加载：**
`https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`

## 服务器命名规范

Python MCP 服务器必须遵循此命名模式：
- **格式**：`{service}_mcp`（小写下划线分隔）
- **示例**：`github_mcp`、`jira_mcp`、`stripe_mcp`

名称应该：
- 通用（不绑定到特定功能）
- 描述所集成的服务/API
- 易于从任务描述中推断
- 不包含版本号或日期

## 工具实现

### 工具命名

对工具名称使用 snake_case（例如 "search_users"、"create_project"、"get_channel_info"），使用清晰的、以动作为导向的名称。

**避免命名冲突**：包含服务上下文以防止重叠：
- 使用 "slack_send_message" 而不是仅 "send_message"
- 使用 "github_create_issue" 而不是仅 "create_issue"
- 使用 "asana_list_tasks" 而不是仅 "list_tasks"

### 使用 FastMCP 的工具结构

工具使用 `@mcp.tool` 装饰器定义，并使用 Pydantic 模型进行输入验证：

```python
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务器
mcp = FastMCP("example_lcp")

# 定义用于输入验证的 Pydantic 模型
class ServiceToolInput(BaseModel):
    '''服务工具操作的输入模型。'''
    model_config = ConfigDict(
        str_strip_whitespace=True,  # 自动去除字符串两端的空白
        validate_assignment=True,    # 在赋值时验证
        extra='forbid'              # 禁止额外字段
    )

    param1: str = Field(..., description="第一个参数的描述（例如 'user123'、'project-abc'）", min_length=1, max_length=100)
    param2: Optional[int] = Field(default=None, description="带约束的可选整数参数", ge=0, le=1000)
    tags: Optional[List[str]] = Field(default_factory=list, description="要应用的标签列表", max_items=10)

@mcp.tool(
    name="service_tool_name",
    annotations={
        "title": "人类可读的工具标题",
        "readOnlyHint": True,      # 工具不会修改环境
        "destructiveHint": False,   # 工具不会执行破坏性操作
        "idempotentHint": True,     # 重复调用不会产生额外效果
        "openWorldHint": False      # 工具不会与外部实体交互
    }
)
async def service_tool_name(params: ServiceToolInput) -> str:
    '''工具描述会自动成为 'description' 字段。

    此工具对服务执行特定操作。它在处理之前使用
    ServiceToolInput Pydantic 模型验证所有输入。

    参数：
        params (ServiceToolInput): 包含以下内容的已验证输入参数：
            - param1 (str): 第一个参数描述
            - param2 (Optional[int]): 带默认值的可选参数
            - tags (Optional[List[str]]): 标签列表

    返回：
        str: 包含操作结果的 JSON 格式化响应
    '''
    # 在此实现
    pass
```

## Pydantic v2 关键特性

- 使用 `model_config` 而不是嵌套的 `Config` 类
- 使用 `field_validator` 而不是废弃的 `validator`
- 使用 `model_dump()` 而不是废弃的 `dict()`
- 验证器需要 `@classmethod` 装饰器
- 验证器方法需要类型提示

```python
from pydantic import BaseModel, Field, field_validator, ConfigDict

class CreateUserInput(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    name: str = Field(..., description="用户的全名", min_length=1, max_length=100)
    email: str = Field(..., description="用户的电子邮件地址", pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: int = Field(..., description="用户的年龄", ge=0, le=150)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("电子邮件不能为空")
        return v.lower()
```

## 响应格式选项

支持多种输出格式以提高灵活性：

```python
from enum import Enum

class ResponseFormat(str, Enum):
    '''工具响应的输出格式。'''
    MARKDOWN = "markdown"
    JSON = "json"

class UserSearchInput(BaseModel):
    query: str = Field(..., description="搜索查询")
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="输出格式：'markdown' 表示人类可读，'json' 表示机器可读"
    )
```

**Markdown 格式**：
- 使用标题、列表和格式以提高清晰度
- 将时间戳转换为人类可读格式（例如 "2024-01-15 10:30:00 UTC" 而不是纪元时间）
- 在括号中显示带 ID 的显示名称（例如 "@john.doe (U123456)"）
- 省略冗长的元数据（例如只显示一个头像 URL，而不是所有尺寸）
- 逻辑地分组相关信息

**JSON 格式**：
- 返回适合程序化处理的完整结构化数据
- 包含所有可用字段和元数据
- 使用一致的字段名称和类型

## 分页实现

对于列出资源的工具：

```python
class ListInput(BaseModel):
    limit: Optional[int] = Field(default=20, description="返回的最大结果数量", ge=1, le=100)
    offset: Optional[int] = Field(default=0, description="用于分页的要跳过的结果数量", ge=0)

async def list_items(params: ListInput) -> str:
    # 使用分页进行 API 请求
    data = await api_request(limit=params.limit, offset=params.offset)

    # 返回分页信息
    response = {
        "total": data["total"],
        "count": len(data["items"]),
        "offset": params.offset,
        "items": data["items"],
        "has_more": data["total"] > params.offset + len(data["items"]),
        "next_offset": params.offset + len(data["items"]) if data["total"] > params.offset + len(data["items"]) else None
    }
    return json.dumps(response, indent=2)
```

## 错误处理

提供清晰、可操作的错误消息：

```python
def _handle_api_error(e: Exception) -> str:
    '''所有工具的一致错误格式化。'''
    if isinstance(e, httpx.HTTPStatusError):
        if e.response.status_code == 404:
            return "错误：未找到资源。请检查 ID 是否正确。"
        elif e.response.status_code == 403:
            return "错误：权限被拒绝。你无权访问此资源。"
        elif e.response.status_code == 429:
            return "错误：超过速率限制。请在发出更多请求之前等待。"
        return f"错误：API 请求失败，状态为 {e.response.status_code}"
    elif isinstance(e, httpx.TimeoutException):
        return "错误：请求超时。请重试。"
    return f"错误：发生意外错误：{type(e).__name__}"
```

## 共享工具

将常见功能提取到可重用函数中：

```python
# 共享的 API 请求函数
async def _make_api_request(endpoint: str, method: str = "GET", **kwargs) -> dict:
    '''所有 API 调用的可重用函数。'''
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method,
            f"{API_BASE_URL}/{endpoint}",
            timeout=30.0,
            **kwargs
        )
        response.raise_for_status()
        return response.json()
```

## Async/Await 最佳实践

始终对网络请求和 I/O 操作使用 async/await：

```python
# 好的做法：异步网络请求
async def fetch_data(resource_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/resource/{resource_id}")
        response.raise_for_status()
        return response.json()

# 不好的做法：同步请求
def fetch_data(resource_id: str) -> dict:
    response = requests.get(f"{API_URL}/resource/{resource_id}")  # 阻塞
    return response.json()
```

## 类型提示

在整个代码中使用类型提示：

```python
from typing import Optional, List, Dict, Any

async def get_user(user_id: str) -> Dict[str, Any]:
    data = await fetch_user(user_id)
    return {"id": data["id"], "name": data["name"]}
```

## 工具文档字符串

每个工具必须具有包含显式类型信息的综合文档字符串：

```python
async def search_users(params: UserSearchInput) -> str:
    '''
    按姓名、电子邮件或团队在示例系统中搜索用户。

    此工具搜索示例平台中的所有用户配置文件，支持部分匹配和各种搜索过滤器。它不会创建或修改用户，仅搜索现有用户。

    参数：
        params (UserSearchInput): 包含以下内容的已验证输入参数：
            - query (str): 用于匹配姓名/电子邮件的搜索字符串（例如 "john"、"@example.com"、"team:marketing"）
            - limit (Optional[int]): 返回的最大结果数量，1-100 之间（默认值：20）
            - offset (Optional[int]): 用于分页的要跳过的结果数量（默认值：0）

    返回：
        str: 包含具有以下模式的搜索结果的 JSON 格式化字符串：

        成功响应：
        {
            "total": int,           # 找到的匹配总数
            "count": int,           # 此响应中的结果数量
            "offset": int,          # 当前分页偏移量
            "users": [
                {
                    "id": str,      # 用户 ID（例如 "U123456789"）
                    "name": str,    # 全名（例如 "John Doe"）
                    "email": str,   # 电子邮件地址（例如 "john@example.com"）
                    "team": str     # 团队名称（例如 "Marketing"）- 可选
                }
            ]
        }

        错误响应：
        "Error: <error message>" 或 "No users found matching '<query>'"

    示例：
        - 使用场景："查找所有营销团队成员" -> params 包含 query="team:marketing"
        - 使用场景："搜索 John 的账户" -> params 包含 query="john"
        - 不使用场景：需要创建用户（改用 example_create_user）
        - 不使用场景：有用户 ID 但需要完整详情（改用 example_get_user）

    错误处理：
        - 输入验证错误由 Pydantic 模型处理
        - 如果请求过多（429 状态）返回 "Error: Rate limit exceeded"
        - 如果 API 密钥无效（401 状态）返回 "Error: Invalid API authentication"
        - 返回格式化的结果列表或 "No users found matching 'query'"
    '''
```

## 完整示例

有关完整的 Python MCP 服务器示例，请参见下文：

```python
#!/usr/bin/env python3
'''
示例服务的 MCP 服务器。

此服务器提供与示例 API 交互的工具，包括用户搜索、
项目管理和数据导出功能。
'''

from typing import Optional, List, Dict, Any
from enum import Enum
import httpx
from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务器
mcp = FastMCP("example_lcp")

# 常量
API_BASE_URL = "https://api.example.com/v1"

# 枚举
class ResponseFormat(str, Enum):
    '''工具响应的输出格式。'''
    MARKDOWN = "markdown"
    JSON = "json"

# 用于输入验证的 Pydantic 模型
class UserSearchInput(BaseModel):
    '''用户搜索操作的输入模型。'''
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    query: str = Field(..., description="用于匹配姓名/电子邮件的搜索字符串", min_length=2, max_length=200)
    limit: Optional[int] = Field(default=20, description="返回的最大结果数量", ge=1, le=100)
    offset: Optional[int] = Field(default=0, description="用于分页的要跳过的结果数量", ge=0)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="输出格式")

    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("查询不能为空或仅包含空白字符")
        return v.strip()

# 共享工具函数
async def _make_api_request(endpoint: str, method: str = "GET", **kwargs) -> dict:
    '''所有 API 调用的可重用函数。'''
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method,
            f"{API_BASE_URL}/{endpoint}",
            timeout=30.0,
            **kwargs
        )
        response.raise_for_status()
        return response.json()

def _handle_api_error(e: Exception) -> str:
    '''所有工具的一致错误格式化。'''
    if isinstance(e, httpx.HTTPStatusError):
        if e.response.status_code == 404:
            return "错误：未找到资源。请检查 ID 是否正确。"
        elif e.response.status_code == 403:
            return "错误：权限被拒绝。你无权访问此资源。"
        elif e.response.status_code == 429:
            return "错误：超过速率限制。请在发出更多请求之前等待。"
        return f"错误：API 请求失败，状态为 {e.response.status_code}"
    elif isinstance(e, httpx.TimeoutException):
        return "错误：请求超时。请重试。"
    return f"错误：发生意外错误：{type(e).__name__}"

# 工具定义
@mcp.tool(
    name="example_search_users",
    annotations={
        "title": "搜索示例用户",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def example_search_users(params: UserSearchInput) -> str:
    '''按姓名、电子邮件或团队在示例系统中搜索用户。

    [如上所示的完整文档字符串]
    '''
    try:
        # 使用已验证的参数进行 API 请求
        data = await _make_api_request(
            "users/search",
            params={
                "q": params.query,
                "limit": params.limit,
                "offset": params.offset
            }
        )

        users = data.get("users", [])
        total = data.get("total", 0)

        if not users:
            return f"未找到匹配 '{params.query}' 的用户"

        # 根据请求的格式格式化响应
        if params.response_format == ResponseFormat.MARKDOWN:
            lines = [f"# 用户搜索结果：'{params.query}'", ""]
            lines.append(f"找到 {total} 个用户（显示 {len(users)} 个）")
            lines.append("")

            for user in users:
                lines.append(f"## {user['name']} ({user['id']})")
                lines.append(f"- **电子邮件**: {user['email']}")
                if user.get('team'):
                    lines.append(f"- **团队**: {user['team']}")
                lines.append("")

            return "\n".join(lines)

        else:
            # 机器可读的 JSON 格式
            import json
            response = {
                "total": total,
                "count": len(users),
                "offset": params.offset,
                "users": users
            }
            return json.dumps(response, indent=2)

    except Exception as e:
        return _handle_api_error(e)

if __name__ == "__main__":
    mcp.run()
```

---

## 高级 FastMCP 特性

### 上下文参数注入

FastMCP 可以自动将 `Context` 参数注入到工具中，以实现日志记录、进度报告、资源读取和用户交互等高级功能：

```python
from mcp.server.fastmcp import FastMCP, Context

mcp = FastMCP("example_lcp")

@mcp.tool()
async def advanced_search(query: str, ctx: Context) -> str:
    '''具有上下文访问功能的高级工具，用于日志记录和进度报告。'''

    # 报告长时间操作的进度
    await ctx.report_progress(0.25, "开始搜索...")

    # 记录信息用于调试
    await ctx.log_info("处理查询", {"query": query, "timestamp": datetime.now()})

    # 执行搜索
    results = await search_api(query)
    await ctx.report_progress(0.75, "格式化结果...")

    # 访问服务器配置
    server_name = ctx.fastmcp.name

    return format_results(results)

@mcp.tool()
async def interactive_tool(resource_id: str, ctx: Context) -> str:
    '''可以向用户请求额外输入的工具。'''

    # 在需要时请求敏感信息
    api_key = await ctx.elicit(
        prompt="请提供你的 API 密钥：",
        input_type="password"
    )

    # 使用提供的密钥
    return await api_call(resource_id, api_key)
```

**上下文功能：**
- `ctx.report_progress(progress, message)` - 报告长时间操作的进度
- `ctx.log_info(message, data)` / `ctx.log_error()` / `ctx.log_debug()` - 日志记录
- `ctx.elicit(prompt, input_type)` - 向用户请求输入
- `ctx.fastmcp.name` - 访问服务器配置
- `ctx.read_resource(uri)` - 读取 MCP 资源

### 资源注册

将数据公开为资源以实现高效的、基于模板的访问：

```python
@mcp.resource("file://documents/{name}")
async def get_document(name: str) -> str:
    '''将文档公开为 MCP 资源。

    资源对于不需要复杂参数的静态或半静态数据很有用。
    它们使用 URI 模板进行灵活访问。
    '''
    document_path = f"./docs/{name}"
    with open(document_path, "r") as f:
        return f.read()

@mcp.resource("config://settings/{key}")
async def get_setting(key: str, ctx: Context) -> str:
    '''使用上下文将配置公开为资源。'''
    settings = await load_settings()
    return json.dumps(settings.get(key, {}))
```

**何时使用资源 vs 工具：**
- **资源**：用于带简单参数的数据访问（URI 模板）
- **工具**：用于需要验证和业务逻辑的复杂操作

### 结构化输出类型

FastMCP 支持字符串之外的多种返回类型：

```python
from typing import TypedDict
from dataclasses import dataclass
from pydantic import BaseModel

# 用于结构化返回的 TypedDict
class UserData(TypedDict):
    id: str
    name: str
    email: str

@mcp.tool()
async def get_user_typed(user_id: str) -> UserData:
    '''返回结构化数据 - FastMCP 处理序列化。'''
    return {"id": user_id, "name": "John Doe", "email": "john@example.com"}

# 用于复杂验证的 Pydantic 模型
class DetailedUser(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime
    metadata: Dict[str, Any]

@mcp.tool()
async def get_user_detailed(user_id: str) -> DetailedUser:
    '''返回 Pydantic 模型 - 自动生成模式。'''
    user = await fetch_user(user_id)
    return DetailedUser(**user)
```

### 生命周期管理

初始化跨请求持久化的资源：

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def app_lifespan():
    '''管理服务器生命周期内存在的资源。'''
    # 初始化连接、加载配置等
    db = await connect_to_database()
    config = load_configuration()

    # 让所有工具可用
    yield {"db": db, "config": config}

    # 关闭时清理
    await db.close()

mcp = FastMCP("example_lcp", lifespan=app_lifespan)

@mcp.tool()
async def query_data(query: str, ctx: Context) -> str:
    # 使用生命周期资源
    db = ctx.fastmcp.state["db"]
    config = ctx.fastmcp.state["config"]
    results = await db.execute(query)
    return format_results(results)
```

### 服务器设置和入口点

配置 MCP 服务器的运行方式：

```python
from mcp.server.fastmcp import FastMCP

# 初始化带可选设置的服务器
mcp = FastMCP(
    "example_lcp",
    lifespan=app_lifespan,  # 生命周期管理
    log_level="INFO"         # 日志级别
)

# 运行服务器（自动选择传输方式）
if __name__ == "__main__":
    mcp.run()
```

**运行选项：**
- **自动检测**：在命令行运行时自动选择传输方式
- **手动指定**：使用环境变量或命令行参数指定传输方式

### 命令行参数

FastMCP 服务器支持以下命令行参数：

```bash
# 运行服务器
python server.py

# 指定传输方式
python server.py --transport stdio      # 使用 stdio 传输
python server.py --transport http       # 使用 HTTP 传输

# 指定端口（仅 HTTP）
python server.py --port 8080

# 日志级别
python server.py --log-level DEBUG
```

### 与其他 MCP 服务器的区别

虽然 MCP 协议是标准化的，但不同 SDK 的实现方式有所不同：

| 特性 | FastMCP (Python) | 其他 SDK |
|------|-----------------|----------|
| 工具注册 | 装饰器 (`@mcp.tool()`) | 显式注册方法 |
| 输入验证 | 自动从 Pydantic 模型生成 | 手动定义模式 |
| 上下文注入 | 自动参数注入 | 手动获取 |
| 资源 | 装饰器 (`@mcp.resource()`) | 显式注册 |
| 生命周期 | lifespan 参数 | 自定义初始化 |

### 测试 MCP 服务器

测试 MCP 服务器的最佳实践：

```python
import pytest
from mcp.server.fastmcp import FastMCP
from your_server import mcp  # 导入你的服务器实例

@pytest.fixture
async def client():
    """创建测试客户端。"""
    transport = TestTransport()  # 使用测试传输
    async with mcp.connect(transport) as session:
        yield session

@pytest.mark.asyncio
async def test_search_users(client):
    """测试用户搜索功能。"""
    result = await client.call_tool(
        "example_search_users",
        {"query": "john", "limit": 10}
    )
    assert result is not None
    # 验证结果格式
```

## 进一步阅读

- [MCP 规范](../spec/agent-skills-spec.md)
- [评估指南](evaluation.md)
- [最佳实践](mcp_best_practices.md)
- [Node.js 实现指南](node_mcp_server.md)
- [官方 MCP Python SDK 文档](https://github.com/modelcontextprotocol/python-sdk)
