# 文档模板参考指南

本文档提供技术文档生成器使用的各类模板参考，包括封面、目录、模块说明、API文档、类文档等模板的定义和使用方法。

---

## 目录

1. [模板系统概述](#模板系统概述)
2. [封面模板](#封面模板)
3. [目录模板](#目录模板)
4. [项目概述模板](#项目概述模板)
5. [架构设计模板](#架构设计模板)
6. [模块说明模板](#模块说明模板)
7. [API接口模板](#api接口模板)
8. [类文档模板](#类文档模板)
9. [函数文档模板](#函数文档模板)
10. [数据字典模板](#数据字典模板)
11. [部署指南模板](#部署指南模板)
12. [代码示例模板](#代码示例模板)
13. [模板变量参考](#模板变量参考)

---

## 模板系统概述

### 模板语法

文档生成器使用简单的模板语法，支持以下功能：

| 语法 | 说明 | 示例 |
|-----|------|------|
| `{{variable}}` | 变量替换 | `{{title}}` 替换为标题 |
| `{{#if condition}}...{{/if}}` | 条件渲染 | `{{#if include_toc}}...{{/if}}` |
| `{{list}}` | 列表展开 | `{{modules}}` 展开为列表项 |

### 模板变量类型

```python
TEMPLATE_VARIABLES = {
    # 字符串变量
    'title': '技术设计文档',  # 标题
    'author': '开发团队',     # 作者
    'version': '1.0.0',       # 版本
    'date': '2024-01-01',    # 日期
    
    # 数字变量
    'total_files': 100,       # 文件总数
    'total_lines': 10000,     # 代码行数
    'total_classes': 50,      # 类数量
    
    # 布尔变量
    'include_toc': True,      # 包含目录
    'include_index': True,    # 包含索引
    'generate_diagrams': True, # 生成图表
    
    # 列表变量
    'modules': ['user', 'order', 'payment'],  # 模块列表
    'tech_stack': ['Python', 'React', 'MySQL'],  # 技术栈
    
    # 对象变量
    'project_info': {
        'name': '项目名',
        'path': '/path/to/project',
        'statistics': {}
    }
}
```

### 模板加载机制

```python
class TemplateEngine:
    """模板引擎"""
    
    def __init__(self, template_dir: Optional[str] = None):
        self.templates = {}
        self.template_dir = template_dir
        self._load_templates()
    
    def _load_templates(self):
        """加载模板文件"""
        if self.template_dir and os.path.exists(self.template_dir):
            for template_file in os.listdir(self.template_dir):
                if template_file.endswith('.tmpl'):
                    template_name = template_file[:-5]
                    template_path = os.path.join(self.template_dir, template_file)
                    with open(template_path, 'r', encoding='utf-8') as f:
                        self.templates[template_name] = f.read()
    
    def get_template(self, name: str) -> str:
        """获取模板"""
        return self.templates.get(name, '')
    
    def render(self, template_name: str, context: Dict) -> str:
        """渲染模板"""
        template = self.get_template(template_name)
        return self._render_template(template, context)
```

---

## 封面模板

### 标准封面模板

```markdown
# {{title}}

{{#if subtitle}}
## {{subtitle}}
{{/if}}

---

**版本**: {{version}}  
**作者**: {{author}}  
**日期**: {{date}}  
**状态**: {{status}}

---

{{#if logo}}
![Logo]({{logo}})
{{/if}}

### 文档说明

{{description}}

---

*本文档由源代码自动生成，最后更新于{{generated_date}}*
```

### 详细封面模板

```markdown
# {{title}}

## {{subtitle}}

---

<div align="center">

![项目Logo]({{logo_url}})

**{{project_name}}**

{{project_slogan}}

---

**版本信息**

| 项目 | 版本 |
|------|------|
| 文档版本 | {{doc_version}} |
| 项目版本 | {{project_version}} |
| 发布日期 | {{release_date}} |

**作者信息**

| 姓名 | 角色 | 联系方式 |
|------|------|---------|
| {{author_name}} | 架构师 | {{author_email}} |
{{#if contributors}}
| {{contributor_name}} | 开发者 | {{contributor_email}} |
{{/if}}

</div>

---

## 文档历史

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|--------|---------|
| {{version}} | {{date}} | {{author}} | 初始版本 |
{{#if revision_history}}
| {{rev_version}} | {{rev_date}} | {{rev_author}} | {{rev_description}} |
{{/if}}

---

{{#if confidential}}
> **保密声明**: 本文档包含保密信息，仅限授权人员查阅。
{{/if}}
```

### 封面变量

| 变量名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| `title` | 字符串 | 是 | 文档标题 |
| `subtitle` | 字符串 | 否 | 副标题 |
| `version` | 字符串 | 是 | 版本号 |
| `author` | 字符串 | 是 | 作者 |
| `date` | 字符串 | 是 | 日期 |
| `logo` | 字符串 | 否 | Logo图片路径 |
| `description` | 字符串 | 否 | 文档描述 |
| `status` | 字符串 | 否 | 文档状态（草稿/正式） |

---

## 目录模板

### 标准目录模板

```markdown
# 目录

{{toc_content}}
```

### 详细目录模板

```markdown
# 目录

## 快速导航

- [1. 项目概述](#1-项目概述)
- [2. 架构设计](#2-架构设计)
- [3. 模块说明](#3-模块说明)
- [4. 接口文档](#4-接口文档)
- [5. 数据字典](#5-数据字典)
- [6. 部署指南](#6-部署指南)
- [附录](#附录)

## 详细目录

### 1. 项目概述
- [1.1 项目背景](#11-项目背景)
- [1.2 技术栈](#12-技术栈)
- [1.3 项目统计](#13-项目统计)
- [1.4 入口点](#14-入口点)

### 2. 架构设计
- [2.1 整体架构](#21-整体架构)
- [2.2 设计模式](#22-设计模式)
- [2.3 核心组件](#23-核心组件)
- [2.4 依赖关系](#24-依赖关系)

### 3. 模块说明
- [3.1 模块列表](#31-模块列表)
{{#if modules}}
{{#each modules}}
- [3.{{@index}} {{name}}](#3{{@index}}-{{name}})
{{/each}}
{{/if}}

### 4. 接口文档
- [4.1 接口概述](#41-接口概述)
{{#if apis}}
{{#each apis}}
- [4.{{@index}} {{name}}](#4{{@index}}-{{name}})
{{/each}}
{{/if}}

### 5. 数据字典
- [5.1 数据模型](#51-数据模型)
- [5.2 枚举值](#52-枚举值)
- [5.3 常量定义](#53-常量定义)

### 6. 部署指南
- [6.1 环境要求](#61-环境要求)
- [6.2 配置说明](#62-配置说明)
- [6.3 部署步骤](#63-部署步骤)

### 附录
- [A. 术语表](#a-术语表)
- [B. 索引](#b-索引)
- [C. 参考资料](#c-参考资料)
```

---

## 项目概述模板

### 标准概述模板

```markdown
## 1. 项目概述

### 1.1 项目背景

{{project_background}}

### 1.2 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
{{#each tech_stack}}
| {{name}} | {{version}} | {{purpose}} |
{{/each}}

### 1.3 项目统计

| 指标 | 数值 |
|------|------|
| 源代码文件数 | {{total_files}} |
| 代码总行数 | {{total_lines}} |
| 类定义数 | {{total_classes}} |
| 函数定义数 | {{total_functions}} |
| 模块数 | {{total_modules}} |
| 注释覆盖率 | {{comment_coverage}}% |

### 1.4 项目结构

```
project/
├── src/                    # 源代码目录
├── tests/                  # 测试目录
├── docs/                   # 文档目录
├── config/                 # 配置文件
├── scripts/                # 脚本文件
└── README.md              # 项目说明
```

### 1.5 入口点

{{entry_points}}
```

### 详细概述模板

```markdown
## 1. 项目概述

### 1.1 项目简介

**项目名称**: {{project_name}}  
**项目代号**: {{project_code}}  
**项目类型**: {{project_type}}  
**开发周期**: {{development_cycle}}

{{project_description}}

### 1.2 业务背景

{{business_background}}

### 1.3 目标用户

{{target_users}}

### 1.4 主要功能

{{#each features}}
- **{{name}}**: {{description}}
{{/each}}

### 1.5 技术选型

#### 前端技术

| 技术 | 版本 | 用途 |
|------|------|------|
{{#each frontend_tech}}
| {{name}} | {{version}} | {{purpose}} |
{{/each}}

#### 后端技术

| 技术 | 版本 | 用途 |
|------|------|------|
{{#each backend_tech}}
| {{name}} | {{version}} | {{purpose}} |
{{/each}}

#### 基础设施

| 技术 | 版本 | 用途 |
|------|------|------|
{{#each infra_tech}}
| {{name}} | {{version}} | {{purpose}} |
{{/each}}

### 1.6 开发团队

| 角色 | 姓名 | 职责 |
|------|------|------|
{{#each team_members}}
| {{role}} | {{name}} | {{responsibility}} |
{{/each}}
```

---

## 架构设计模板

### 标准架构模板

```markdown
## 2. 架构设计

### 2.1 整体架构

{{architecture_diagram}}

### 2.2 架构说明

{{architecture_description}}

### 2.3 设计模式

{{#each design_patterns}}
#### {{name}}

- **类型**: {{type}}
- **应用场景**: {{scenario}}
- **实现方式**: {{implementation}}
{{/each}}

### 2.4 核心组件

| 组件 | 职责 | 依赖 |
|------|------|------|
{{#each components}}
| {{name}} | {{responsibility}} | {{dependencies}} |
{{/each}}

### 2.5 层次结构

```
{{layer_structure}}
```

### 2.6 依赖关系

{{dependency_graph}}
```

### 微服务架构模板

```markdown
## 2. 架构设计

### 2.1 架构概览

```
{{service_architecture_diagram}}
```

### 2.2 服务列表

| 服务名称 | 端口 | 职责 | 状态 |
|---------|------|------|------|
{{#each services}}
| {{name}} | {{port}} | {{responsibility}} | {{status}} |
{{/each}}

### 2.3 服务通信

#### 同步通信

| 调用方 | 被调用方 | 协议 | 接口 |
|--------|---------|------|------|
{{#each sync_communications}}
| {{caller}} | {{callee}} | {{protocol}} | {{endpoint}} |
{{/each}}

#### 异步通信

| 消息队列 | 生产者 | 消费者 | 消息类型 |
|---------|--------|--------|---------|
{{#each async_communications}}
| {{queue}} | {{producer}} | {{consumer}} | {{message_type}} |
{{/each}}

### 2.4 数据流

{{data_flow_diagram}}

### 2.5 容错设计

{{fault_tolerance_design}}
```

---

## 模块说明模板

### 标准模块模板

```markdown
## 3. 模块说明

### 3.1 模块列表

| 模块名 | 职责 | 文件数 | 复杂度 |
|--------|------|--------|--------|
{{#each modules}}
| {{name}} | {{responsibility}} | {{file_count}} | {{complexity}} |
{{/each}}

### 3.2 模块详情

{{#each modules}}
#### 3.{{@index}} {{name}}

**模块路径**: `{{path}}`  
**职责描述**: {{description}}

**核心类**:

| 类名 | 职责 | 方法数 |
|------|------|--------|
{{#each classes}}
| {{class_name}} | {{responsibility}} | {{method_count}} |
{{/each}}

**对外接口**:

{{#each public_interfaces}}
- `{{signature}}` - {{description}}
{{/each}}

**依赖关系**:

- 依赖: {{dependencies}}
- 被依赖: {{dependents}}

**文件列表**:

{{#each files}}
- `{{path}}`
{{/each}}

---
{{/each}}
```

### 详细模块模板

```markdown
## 3. 模块说明

### 3.1 模块概览

本项目共包含 {{total_modules}} 个业务模块，按功能划分为：

{{#each module_groups}}
#### {{group_name}}

{{group_description}}

| 模块名 | 职责 | 依赖 |
|--------|------|------|
{{#each modules}}
| [{{name}}](#3{{@index}}-{{name}}) | {{responsibility}} | {{dependencies}} |
{{/each}}

{{/each}}

### 3.2 模块详解

{{#each modules}}
#### 3.{{@index}} {{name}}

<div id="{{name}}"></div>

##### 基本信息

| 属性 | 值 |
|------|-----|
| 模块名 | {{name}} |
| 路径 | `{{path}}` |
| 职责 | {{responsibility}} |
| 复杂度 | {{complexity}}/10 |
| 状态 | {{status}} |

##### 模块描述

{{description}}

##### 核心类

```{{language}}
{{core_class_code}}
```

**类说明**:

| 类名 | 类型 | 职责 | 关键方法 |
|------|------|------|---------|
{{#each classes}}
| {{name}} | {{type}} | {{responsibility}} | {{key_methods}} |
{{/each}}

##### 对外接口

{{#each interfaces}}
###### {{name}}

- **描述**: {{description}}
- **路径**: `{{path}}`
- **方法**: {{method}}
- **参数**: {{parameters}}

**请求示例**:
```json
{{request_example}}
```

**响应示例**:
```json
{{response_example}}
```
{{/each}}

##### 内部结构

```
{{internal_structure}}
```

##### 依赖关系

**模块依赖图**:
{{dependency_diagram}}

**入向依赖**（被依赖）:

| 依赖模块 | 依赖类型 | 说明 |
|---------|---------|------|
{{#each inbound_dependencies}}
| {{module}} | {{type}} | {{description}} |
{{/each}}

**出向依赖**（依赖其他）:

| 依赖模块 | 依赖类型 | 说明 |
|---------|---------|------|
{{#each outbound_dependencies}}
| {{module}} | {{type}} | {{description}} |
{{/each}}

##### 数据流

{{data_flow_description}}

##### 配置项

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
{{#each configurations}}
| {{name}} | {{type}} | {{default}} | {{description}} |
{{/each}}

##### 扩展点

{{extension_points}}

##### 使用示例

```{{language}}
{{usage_example}}
```

##### 注意事项

{{cautions}}

---
{{/each}}
```

---

## API接口模板

### REST API模板

```markdown
## 4. 接口文档

### 4.1 接口概述

本项目提供以下RESTful API接口：

| 接口组 | 基础路径 | 描述 |
|--------|---------|------|
{{#each api_groups}}
| {{name}} | `{{base_path}}` | {{description}} |
{{/each}}

### 4.2 通用说明

#### 认证方式

所有API请求需要携带认证令牌：

```
Authorization: Bearer <token>
```

#### 错误响应

所有接口返回统一的错误格式：

```json
{
    "code": "ERROR_CODE",
    "message": "错误描述",
    "details": {}
}
```

### 4.3 接口详情

{{#each apis}}
#### {{method}} {{path}}

{{description}}

**请求头**:

| 头部 | 必填 | 描述 |
|------|------|------|
{{#each request_headers}}
| {{name}} | {{required}} | {{description}} |
{{/each}}

**请求参数**:

| 参数名 | 位置 | 类型 | 必填 | 描述 |
|--------|------|------|------|------|
{{#each request_params}}
| {{name}} | {{location}} | {{type}} | {{required}} | {{description}} |
{{/each}}

**请求体**:

```json
{{request_body}}
```

**响应体**:

```json
{{response_body}}
```

**状态码**:

| 状态码 | 描述 |
|--------|------|
{{#each status_codes}}
| {{code}} | {{description}} |
{{/each}}

**示例**:

```bash
curl -X {{method}} "{{base_url}}{{path}}" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{{request_body_json}}'
```

---
{{/each}}
```

### GraphQL API模板

```markdown
## 4. 接口文档

### 4.1 GraphQL端点

- **URL**: `{{endpoint}}`
- **方法**: POST

### 4.2 查询示例

```graphql
{{query_example}}
```

### 4.3 变更示例

```graphql
{{mutation_example}}
```

### 4.4 类型定义

```graphql
{{type_definitions}}
```

### 4.5 接口详情

{{#each fields}}
#### {{name}}

- **类型**: `{{type}}`
- **描述**: {{description}}
- **参数**:

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
{{#each args}}
| {{name}} | {{type}} | {{required}} | {{description}} |
{{/each}}

- **返回值**: `{{return_type}}`

{{/each}}
```

---

## 类文档模板

### 标准类模板

```markdown
### {{class_name}}

```{{language}}
{{class_code}}
```

**职责**: {{responsibility}}

**继承关系**: {{inheritance}}

**实现接口**: {{interfaces}}

{{#if attributes}}
#### 属性

| 属性名 | 类型 | 可见性 | 描述 |
|--------|------|--------|------|
{{#each attributes}}
| {{name}} | {{type}} | {{visibility}} | {{description}} |
{{/each}}
{{/if}}

{{#if methods}}
#### 方法

| 方法名 | 返回类型 | 描述 |
|--------|----------|------|
{{#each methods}}
| {{name}} | {{return_type}} | {{description}} |
{{/each}}
{{/if}}

{{#if examples}}
#### 使用示例

```{{language}}
{{examples}}
```
{{/if}}
```

### 详细类模板

```markdown
### {{class_name}}

<div class="class-info">

**完整类名**: `{{full_name}}`  
**所在文件**: `{{file_path}}`  
**行号**: {{line_number}}  
**职责**: {{responsibility}}

</div>

```{{language}}
{{class_code}}
```

#### 类说明

{{description}}

#### 类特性

{{#each features}}
- **{{name}}**: {{description}}
{{/each}}

#### 继承层次

```
{{inheritance_hierarchy}}
```

#### 实现接口

{{#each interfaces}}
- `{{name}}`{{#if description}}: {{description}}{{/if}}
{{/each}}

#### 属性详细说明

{{#each attributes}}
##### {{name}}

- **类型**: `{{type}}`
- **可见性**: `{{visibility}}`
- **默认值**: `{{default_value}}`
- **说明**: {{description}}

{{#if getter}}
- **Getter**: `{{getter}}`
{{/if}}
{{#if setter}}
- **Setter**: `{{setter}}`
{{/if}}
{{#if validation}}
- **验证规则**: {{validation}}
{{/if}}

{{/each}}

#### 方法详细说明

{{#each methods}}
##### {{name}}

```{{language}}
{{method_signature}}
```

{{description}}

**参数**:

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
|--------|------|------|--------|------|
{{#each params}}
| {{name}} | {{type}} | {{required}} | {{default}} | {{description}} |
{{/each}}

**返回值**:

- **类型**: `{{return_type}}`
- **说明**: {{return_description}}

**可能异常**:

| 异常类型 | 触发条件 |
|---------|---------|
{{#each exceptions}}
| {{type}} | {{condition}} |
{{/each}}

**使用示例**:

```{{language}}
{{example}}
```

**注意事项**:

{{notes}}

{{/each}}

#### 内部类

{{#each inner_classes}}
- `{{name}}`{{#if description}}: {{description}}{{/if}}
{{/each}}

#### 事件

{{#each events}}
- **{{name}}**: {{description}}
{{/each}}
```

---

## 函数文档模板

### 标准函数模板

```markdown
### {{function_name}}

```{{language}}
{{function_signature}}
```

{{docstring}}

**参数**:

{{#each parameters}}
- `{{name}}` (`{{type}}`): {{description}}
{{/each}}

**返回值**:

`{{return_type}}`: {{return_description}}

**示例**:

```{{language}}
{{example}}
```
```

### 详细函数模板

```markdown
### {{function_name}}

<div class="function-info">

**函数名**: `{{name}}`  
**签名**: `{{signature}}`  
**文件**: `{{file_path}}`  
**行号**: {{line_number}}  
**可见性**: {{visibility}}

</div>

```{{language}}
{{full_code}}
```

#### 函数描述

{{description}}

#### 前置条件

{{preconditions}}

#### 后置条件

{{postconditions}}

#### 参数详细说明

{{#each parameters}}
##### {{name}}

- **类型**: `{{type}}`
- **必填**: {{required}}
- **默认值**: {{default_value}}
- **说明**: {{description}}
- **约束**: {{constraints}}
- **示例值**: `{{example_value}}`

{{#if validation}}
**验证规则**:

```{{language}}
{{validation}}
```
{{/if}}

{{/each}}

#### 返回值详细说明

- **类型**: `{{return_type}}`
- **说明**: {{return_description}}
- **可能值**:

| 值 | 说明 |
|---|------|
{{#each possible_returns}}
| `{{value}}` | {{description}} |
{{/each}}

#### 异常说明

| 异常类型 | 抛出条件 | 处理建议 |
|---------|---------|---------|
{{#each exceptions}}
| {{type}} | {{condition}} | {{suggestion}} |
{{/each}}

#### 性能考虑

{{performance_notes}}

#### 线程安全性

{{thread_safety}}

#### 使用示例

##### 基础示例

```{{language}}
{{basic_example}}
```

##### 高级示例

```{{language}}
{{advanced_example}}
```

##### 错误处理示例

```{{language}}
{{error_handling_example}}
```

#### 相关函数

{{#each related_functions}}
- `{{name}}`{{#if description}}: {{description}}{{/if}}
{{/each}}

#### 注意事项

{{cautions}}
```

---

## 数据字典模板

### 标准数据字典模板

```markdown
## 5. 数据字典

### 5.1 数据模型

| 类名 | 表名 | 说明 |
|------|------|------|
{{#each models}}
| {{class_name}} | {{table_name}} | {{description}} |
{{/each}}

### 5.2 字段定义

#### {{table_name}}

| 字段名 | 类型 | 约束 | 默认值 | 说明 |
|--------|------|------|--------|------|
{{#each fields}}
| {{name}} | {{type}} | {{constraints}} | {{default}} | {{description}} |
{{/each}}

### 5.3 枚举值

| 枚举名 | 值 | 说明 |
|--------|------|------|
{{#each enums}}
| {{name}} | {{value}} | {{description}} |
{{/each}}

### 5.4 常量定义

| 常量名 | 值 | 类型 | 说明 |
|--------|------|------|------|
{{#each constants}}
| {{name}} | {{value}} | {{type}} | {{description}} |
{{/each}}
```

### 详细数据字典模板

```markdown
## 5. 数据字典

### 5.1 实体关系图

{{er_diagram}}

### 5.2 数据模型详解

{{#each models}}
#### {{name}}

**对应类**: `{{class_name}}`  
**对应表**: `{{table_name}}`  
**说明**: {{description}}

**字段列表**:

| 字段名 | 类型 | 约束 | 默认值 | 说明 |
|--------|------|------|--------|------|
{{#each fields}}
| {{name}} | {{type}} | {{constraints}} | {{default}} | {{description}} |
{{/each}}

**索引**:

| 索引名 | 类型 | 字段 | 唯一 |
|--------|------|------|------|
{{#each indexes}}
| {{name}} | {{type}} | {{fields}} | {{unique}} |
{{/each}}

**外键**:

| 字段 | 引用表 | 引用字段 | 行为 |
|------|--------|---------|------|
{{#each foreign_keys}}
| {{field}} | {{ref_table}} | {{ref_field}} | {{on_delete}} |
{{/each}}

{{#if relationships}}
**关系**:
{{#each relationships}}
- {{type}}: {{related_entity}}
{{/each}}
{{/if}}

---
{{/each}}

### 5.3 枚举定义

{{#each enums}}
#### {{name}}

| 值 | 键 | 说明 |
|------|------|------|
{{#each values}}
| {{value}} | {{key}} | {{description}} |
{{/each}}

{{/each}}

### 5.4 常量定义

| 常量组 | 常量名 | 值 | 类型 | 说明 |
|--------|--------|------|------|------|
{{#each constants}}
| {{group}} | {{name}} | `{{value}}` | {{type}} | {{description}} |
{{/each}}

### 5.5 数据类型映射

| 编程语言类型 | 数据库类型 | 说明 |
|-------------|-----------|------|
{{#each type_mappings}}
| {{code_type}} | {{db_type}} | {{description}} |
{{/each}}
```

---

## 部署指南模板

### 标准部署模板

```markdown
## 6. 部署指南

### 6.1 环境要求

| 组件 | 最低版本 | 推荐版本 |
|------|---------|---------|
{{#each requirements}}
| {{component}} | {{min_version}} | {{rec_version}} |
{{/each}}

### 6.2 环境变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
{{#each environment_variables}}
| {{name}} | {{required}} | {{default}} | {{description}} |
{{/each}}

### 6.3 配置文件

| 配置文件 | 说明 |
|---------|------|
{{#each config_files}}
| `{{path}}` | {{description}} |
{{/each}}

### 6.4 部署步骤

```bash
# 步骤1: 克隆代码
git clone {{repository_url}}
cd {{project_name}}

# 步骤2: 安装依赖
{{install_command}}

# 步骤3: 配置环境
cp config.example.yml config.yml
# 编辑配置文件

# 步骤4: 构建项目
{{build_command}}

# 步骤5: 运行测试
{{test_command}}

# 步骤6: 启动服务
{{start_command}}
```

### 6.5 验证部署

```bash
# 检查服务状态
{{status_command}}

# 检查日志
{{log_command}}

# 测试接口
curl {{test_endpoint}}
```

### 6.6 回滚步骤

```bash
{{rollback_command}}
```
```

### 详细部署模板

```markdown
## 6. 部署指南

### 6.1 概述

{{deployment_overview}}

### 6.2 环境准备

#### 硬件要求

| 资源 | 最低配置 | 推荐配置 |
|------|---------|---------|
| CPU | 2核 | 4核 |
| 内存 | 4GB | 8GB |
| 磁盘 | 50GB | 100GB SSD |
| 网络 | 10Mbps | 100Mbps |

#### 软件要求

| 软件 | 版本 | 用途 |
|------|------|------|
{{#each software_requirements}}
| {{name}} | {{version}} | {{purpose}} |
{{/each}}

### 6.3 环境配置

#### 系统配置

```bash
# 系统参数优化
{{system_optimization}}
```

#### 数据库配置

```sql
-- 创建数据库
{{database_creation}}

-- 创建用户
{{user_creation}}

-- 授权
{{grant_permissions}}
```

#### 中间件配置

{{middleware_configuration}}

### 6.4 应用配置

#### 配置文件结构

```
config/
├── default.yml      # 默认配置
├── production.yml   # 生产环境
├── staging.yml      # 预发布环境
└── local.yml        # 本地环境（不提交版本控制）
```

#### 关键配置项

| 配置项 | 环境变量 | 说明 |
|--------|---------|------|
{{#each key_configurations}}
| {{config_key}} | {{env_var}} | {{description}} |
{{/each}}

### 6.5 部署流程

#### 准备阶段

1. **代码获取**
   ```bash
   git clone {{repository_url}}
   git checkout {{version_tag}}
   ```

2. **依赖安装**
   ```bash
   {{install_dependencies_command}}
   ```

3. **配置检查**
   ```bash
   {{config_check_command}}
   ```

#### 构建阶段

1. **编译代码**
   ```bash
   {{build_command}}
   ```

2. **运行测试**
   ```bash
   {{test_command}}
   ```

3. **安全扫描**
   ```bash
   {{security_scan_command}}
   ```

#### 部署阶段

1. **停止服务**
   ```bash
   {{stop_service_command}}
   ```

2. **备份数据**
   ```bash
   {{backup_command}}
   ```

3. **更新代码**
   ```bash
   {{deploy_command}}
   ```

4. **启动服务**
   ```bash
   {{start_service_command}}
   ```

5. **验证部署**
   ```bash
   {{verify_command}}
   ```

### 6.6 容器化部署

#### Dockerfile

```dockerfile
{{dockerfile_content}}
```

#### docker-compose.yml

```yaml
{{docker_compose_content}}
```

#### 部署命令

```bash
# 构建镜像
docker build -t {{image_name}} .

# 运行容器
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 6.7 Kubernetes部署

#### Deployment

```yaml
{{kubernetes_deployment}}
```

#### Service

```yaml
{{kubernetes_service}}
```

#### Ingress

```yaml
{{kubernetes_ingress}}
```

### 6.8 监控配置

#### 监控指标

| 指标 | 阈值 | 告警级别 |
|------|------|---------|
{{#each monitoring_metrics}}
| {{metric}} | {{threshold}} | {{level}} |
{{/each}}

#### 日志配置

{{log_configuration}}

### 6.9 故障排查

#### 常见问题

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
{{#each troubleshooting}}
| {{problem}} | {{cause}} | {{solution}} |
{{/each}}

#### 诊断命令

```bash
{{diagnostic_commands}}
```
```

---

## 代码示例模板

### 代码示例模板

````markdown
### {{example_title}}

**语言**: `{{language}}`  
**文件**: `{{file_path}}`  
**行号**: {{line_number}}-{{end_line}}  
**描述**: {{description}}

```{{language}}
{{code}}
```

**说明**:

{{explanation}}
````

### 完整示例模板

````markdown
### {{example_title}}

**用途**: {{purpose}}  
**语言**: `{{language}}`  
**难度**: {{difficulty}}  
**相关类**: {{related_classes}}

#### 场景描述

{{scenario_description}}

#### 代码实现

```{{language}}
{{code}}
```

#### 代码说明

{{code_explanation}}

#### 运行结果

```{{output}}
{{expected_output}}
```

#### 扩展阅读

{{related_resources}}
````

---

## 模板变量参考

### 通用变量

| 变量名 | 类型 | 说明 |
|-------|------|------|
| `title` | 字符串 | 文档标题 |
| `subtitle` | 字符串 | 副标题 |
| `author` | 字符串 | 作者 |
| `version` | 字符串 | 版本号 |
| `date` | 字符串 | 日期 |
| `description` | 字符串 | 描述文本 |
| `language` | 字符串 | 编程语言 |

### 项目变量

| 变量名 | 类型 | 说明 |
|-------|------|------|
| `project_name` | 字符串 | 项目名称 |
| `project_path` | 字符串 | 项目路径 |
| `total_files` | 数字 | 文件总数 |
| `total_lines` | 数字 | 代码行数 |
| `total_classes` | 数字 | 类数量 |
| `total_functions` | 数字 | 函数数量 |
| `total_modules` | 数字 | 模块数量 |

### 模块变量

| 变量名 | 类型 | 说明 |
|-------|------|------|
| `modules` | 列表 | 模块列表 |
| `module_name` | 字符串 | 模块名称 |
| `module_path` | 字符串 | 模块路径 |
| `responsibility` | 字符串 | 模块职责 |
| `dependencies` | 列表 | 依赖列表 |
| `dependents` | 列表 | 被依赖列表 |

### 代码元素变量

| 变量名 | 类型 | 说明 |
|-------|------|------|
| `classes` | 列表 | 类列表 |
| `functions` | 列表 | 函数列表 |
| `interfaces` | 列表 | 接口列表 |
| `variables` | 列表 | 变量列表 |
| `constants` | 列表 | 常量列表 |
| `enums` | 列表 | 枚举列表 |
`attributes` | 列表 | 属性列表 |
| `methods` | 列表 | 方法列表 |
| `parameters` | 列表 | 参数列表 |

### 文档结构变量

| 变量名 | 类型 | 说明 |
|-------|------|------|
| `toc_content` | 字符串 | 目录内容 |
| `table_of_contents` | 列表 | 目录列表 |
| `examples` | 列表 | 示例列表 |
| `diagrams` | 列表 | 图表列表 |
| `figures` | 列表 | 图片列表 |
| `tables` | 列表 | 表格列表 |
| `appendices` | 列表 | 附录列表 |
| `index_entries` | 列表 | 索引条目 |
