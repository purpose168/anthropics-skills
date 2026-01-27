# MCP 服务器最佳实践

## 快速参考

### 服务器命名
- **Python**：`{service}_mcp`（例如 `slack_mcp`）
- **Node/TypeScript**：`{service}-mcp-server`（例如 `slack-mcp-server`）

### 工具命名
- 使用 snake_case 格式并包含服务前缀
- 格式：`{service}_{action}_{resource}`
- 示例：`slack_send_message`、`github_create_issue`

### 响应格式
- 支持 JSON 和 Markdown 两种格式
- JSON 适用于程序化处理
- Markdown 适用于人工阅读

### 分页
- 始终遵守 `limit` 参数
- 返回 `has_more`、`next_offset`、`total_count`
- 默认返回 20-50 条数据

### 传输方式
- **可流式 HTTP**：适用于远程服务器、多客户端场景
- **stdio**：适用于本地集成、命令行工具
- 避免使用 SSE（已被可流式 HTTP 取代）

---

## 服务器命名规范

遵循以下标准化命名模式：

**Python**：使用 `{service}_mcp` 格式（小写下划线分隔）
- 示例：`slack_mcp`、`github_mcp`、`jira_mcp`

**Node/TypeScript**：使用 `{service}-mcp-server` 格式（小写连字符分隔）
- 示例：`slack-mcp-server`、`github-mcp-server`、`jira-mcp-server`

名称应该通用、描述性强、易于从任务描述中推断，且不包含版本号。

---

## 工具命名与设计

### 工具命名

1. **使用 snake_case**：`search_users`、`create_project`、`get_channel_info`
2. **包含服务前缀**：预见到你的 MCP 服务器可能与其他 MCP 服务器一起使用
   - 使用 `slack_send_message` 而不是仅 `send_message`
   - 使用 `github_create_issue` 而不是仅 `create_issue`
3. **以动作为导向**：使用动词开头（get、list、search、create 等）
4. **具体明确**：避免可能与其他服务器冲突的通用名称

### 工具设计

- 工具描述必须狭义且明确地描述功能
- 描述必须与实际功能精确匹配
- 提供工具注解（readOnlyHint、destructiveHint、idempotentHint、openWorldHint）
- 保持工具操作专注且原子化

---

## 响应格式

所有返回数据的工具应支持多种格式：

### JSON 格式（`response_format="json"`）
- 机器可读的结构化数据
- 包含所有可用字段和元数据
- 一致的字段名称和类型
- 适用于程序化处理

### Markdown 格式（`response_format="markdown"`，通常为默认）
- 人类可读的格式化文本
- 使用标题、列表和格式以提高清晰度
- 将时间戳转换为人类可读格式
- 在括号中显示带 ID 的显示名称
- 省略冗长的元数据

---

## 分页

对于列出资源的工具：

- **始终遵守 `limit` 参数**
- **实现分页**：使用 `offset` 或基于游标的分页
- **返回分页元数据**：包含 `has_more`、`next_offset`/`next_cursor`、`total_count`
- **永远不要将所有结果加载到内存中**：对于大型数据集尤为重要
- **使用合理的默认限制**：20-50 条是典型值

分页响应示例：
```json
{
  "total": 150,
  "count": 20,
  "offset": 0,
  "items": [...],
  "has_more": true,
  "next_offset": 20
}
```

---

## 传输选项

### 可流式 HTTP

**最佳适用场景**：远程服务器、Web 服务、多客户端场景

**特性**：
- 通过 HTTP 进行双向通信
- 支持多个同时连接的客户端
- 可以部署为 Web 服务
- 支持服务器到客户端通知

**使用场景**：
- 同时为多个客户端服务
- 部署为云服务
- 与 Web 应用程序集成

### stdio

**最佳适用场景**：本地集成、命令行工具

**特性**：
- 标准输入/输出流通信
- 简单设置，无需网络配置
- 作为客户端的子进程运行

**使用场景**：
- 为本地开发环境构建工具
- 与桌面应用程序集成
- 单用户、单会话场景

**注意**：stdio 服务器不应向 stdout 记录日志（使用 stderr 进行日志记录）

### 传输选择

| 标准 | stdio | 可流式 HTTP |
|------|-------|-------------|
| **部署方式** | 本地 | 远程 |
| **客户端数量** | 单个 | 多个 |
| **复杂度** | 低 | 中等 |
| **实时性** | 否 | 是 |

---

## 安全最佳实践

### 身份验证和授权

**OAuth 2.1**：
- 使用来自公认机构的证书进行安全的 OAuth 2.1 认证
- 在处理请求之前验证访问令牌
- 只接受专门为你的服务器颁发的令牌

**API 密钥**：
- 将 API 密钥存储在环境变量中，绝不写在代码中
- 在服务器启动时验证密钥
- 身份验证失败时提供清晰的错误消息

### 输入验证

- 清理文件路径以防止目录遍历攻击
- 验证 URL 和外部标识符
- 检查参数大小和范围
- 防止系统调用中的命令注入
- 对所有输入使用模式验证（Pydantic/Zod）

### 错误处理

- 不要向客户端暴露内部错误
- 在服务器端记录安全相关错误
- 提供有帮助但不泄露信息的错误消息
- 错误后清理资源

### DNS 重新绑定防护

对于本地运行的可流式 HTTP 服务器：
- 启用 DNS 重新绑定防护
- 验证所有传入连接的 `Origin` 头
- 绑定到 `127.0.0.1` 而不是 `0.0.0.0`

---

## 工具注解

提供注解以帮助客户端理解工具行为：

| 注解 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `readOnlyHint` | 布尔值 | false | 工具不会修改其环境 |
| `destructiveHint` | 布尔值 | true | 工具可能执行破坏性更新 |
| `idempotentHint` | 布尔值 | false | 相同参数的重复调用不会产生额外效果 |
| `openWorldHint` | 布尔值 | true | 工具与外部实体交互 |

**重要提示**：注解是提示，不是安全保证。客户端不应仅根据注解做出安全关键决策。

---

## 错误处理

- 使用标准的 JSON-RPC 错误代码
- 在结果对象内报告工具错误（而不是协议级错误）
- 提供有帮助的、具体的错误消息以及建议的下一步操作
- 不要暴露内部实现细节
- 错误时正确清理资源

错误处理示例：
```typescript
try {
  const result = performOperation();
  return { content: [{ type: "text", text: result }] };
} catch (error) {
  return {
    isError: true,
    content: [{
      type: "text",
      text: `Error: ${error.message}. Try using filter='active_only' to reduce results.`
    }]
  };
}
```

---

## 测试要求

全面的测试应涵盖：

- **功能测试**：使用有效/无效输入验证正确执行
- **集成测试**：测试与外部系统的交互
- **安全测试**：验证身份验证、输入清理、速率限制
- **性能测试**：检查负载下的行为、超时情况
- **错误处理**：确保正确的错误报告和清理

---

## 文档要求

- 提供所有工具和功能的清晰文档
- 包含可工作的示例（每个主要功能至少 3 个）
- 记录安全注意事项
- 指定所需的权限和访问级别
- 记录速率限制和性能特征
