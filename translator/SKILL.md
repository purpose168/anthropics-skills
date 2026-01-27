---
name: tech-doc-translator
description: 专业的技术文档与多语言代码英文翻译技能。将各类技术文档（API文档、用户手册、技术规范、注释说明等）及多种编程语言代码（Python、Java、JavaScript、C++等）中的英文内容准确翻译成简体中文。严格保持原文档或代码的语法规范、格式结构和技术术语一致性，具备识别代码与自然语言文本边界的能力，支持直接修改原文件和调用智能体进行翻译处理。
---

# 技术文档与多语言代码翻译技能

## 概述

本技能用于将技术文档和多语言代码中的英文内容准确翻译成简体中文，同时严格保持：
- 技术文档的格式完整性和专业术语一致性
- 代码的可执行性和语法正确性
- 原始文件结构不被破坏

---

# 核心功能

## 文档翻译能力

### 支持的文档类型

| 文档类型 | 文件扩展名 | 翻译特点 |
|---------|-----------|---------|
| API文档 | .md, .yaml, .json, .yml | 保持API端点格式、参数说明、响应结构 |
| 用户手册 | .md, .txt, .rst | 保持教程结构、步骤说明、注意事项 |
| 技术规范 | .md, .txt, .pdf | 保持技术术语、规格参数、引用标注 |
| 代码注释 | .py, .js, .ts, .java, .cpp, .c, .go, .rs | 保持注释格式、文档字符串、类型注解 |
| 配置文件 | .json, .yaml, .yml, .toml, .ini | 保持配置结构、注释说明、键值格式 |
| 数据库文档 | .sql, .md | 保持DDL语句、注释说明、示例代码 |

### 翻译质量保障

- **术语一致性**：建立技术术语库，确保相同术语在整个文档中翻译一致
- **格式保留**：保持Markdown、YAML、JSON等格式的完整性
- **链接处理**：保持文档内部链接和外部链接的有效性
- **代码块保护**：正确识别和处理代码块，防止误翻译

## 代码翻译能力

### 支持的编程语言

| 编程语言 | 文件扩展名 | 翻译范围 |
|---------|-----------|---------|
| Python | .py, .pyi | 字符串、注释、文档字符串、类型注解 |
| JavaScript/TypeScript | .js, .jsx, .ts, .tsx | 字符串、注释、JSDoc |
| Java | .java | 字符串、注释、Javadoc |
| C/C++ | .c, .cpp, .h, .hpp | 字符串、注释、Doxygen |
| C# | .cs | 字符串、注释、XML文档注释 |
| Go | .go | 字符串、注释、Godoc |
| Rust | .rs | 字符串、注释、文档注释 |
| PHP | .php | 字符串、注释、PHPDoc |
| Ruby | .rb | 字符串、注释、RDoc |
| Shell | .sh, .bash | 字符串、注释 |

### 代码元素处理策略

#### 可翻译元素

- **字符串字面量**：用户可见的文本内容
- **注释**：单行注释（//, #, --）、多行注释（/* */, ''' ''', """ """）
- **文档字符串**：函数、类、模块的文档说明
- **类型注解**：类型说明文字
- **错误消息**：异常信息、错误提示

#### 不可翻译元素

- **关键字**：if, for, while, class, function等语言关键字
- **变量名**：变量、函数、类、接口的名称
- **标识符**：API端点路径、路由配置
- **配置键名**：JSON/YAML配置项名称
- **文件路径**：文件系统路径、URL地址
- **正则表达式**：模式匹配表达式
- **SQL语句**：数据库查询语句关键字

---

# 使用场景

## 场景1：翻译整个项目文档

当用户请求翻译项目中的所有文档时：

```markdown
请将整个项目的英文文档翻译成中文，包括：
- README.md 主文档
- docs/ 目录下的所有文档
- API接口文档
```

**处理流程**：
1. 扫描项目目录，识别所有需要翻译的文件
2. 按文件类型分类，确定翻译策略
3. 批量处理文档，保持术语一致性
4. 生成翻译报告，记录处理结果

## 场景2：翻译特定代码文件

当用户请求翻译特定代码文件时：

```markdown
请将 src/utils/helper.py 文件中的注释和文档字符串翻译成中文
```

**处理流程**：
1. 分析文件类型和结构
2. 识别可翻译的字符串和注释
3. 保持代码语法正确性
4. 直接修改原文件或生成新文件

## 场景3：翻译API文档

当用户请求翻译API文档时：

```markdown
请将 openapi.yaml 中的英文描述翻译成中文
```

**处理流程**：
1. 解析OpenAPI/Swagger文档结构
2. 翻译描述性字段（summary, description）
3. 保持参数定义、响应结构不变
4. 验证翻译后的文档格式正确

## 场景4：混合内容翻译

当用户请求翻译包含代码和文档的混合内容时：

```markdown
请将包含Python代码和Markdown说明的技术文章翻译成中文
```

**处理流程**：
1. 识别文档中的代码块和自然语言部分
2. 对不同类型内容应用不同翻译策略
3. 保持整体文档结构完整

---

# 工作流程

## 翻译处理流程

### 第一阶段：文件分析

#### 1.1 文件类型识别

```python
def analyze_file(file_path):
    """分析文件类型和结构"""
    file_extension = get_file_extension(file_path)
    encoding = detect_file_encoding(file_path)
    file_size = get_file_size(file_path)
    
    file_type = categorize_file_type(file_extension)
    return {
        'path': file_path,
        'extension': file_extension,
        'encoding': encoding,
        'type': file_type,
        'size': file_size
    }
```

#### 1.2 编码检测

支持的文件编码：
- UTF-8（默认）
- UTF-8 with BOM
- GB2312/GBK/GB18030
- Latin-1
- ASCII

#### 1.3 结构解析

针对不同文件类型进行结构解析：
- **代码文件**：解析语法树，识别注释和字符串
- **Markdown**：解析标题、段落、代码块、列表
- **YAML/JSON**：解析键值对，识别描述字段
- **配置文件**：解析配置结构，识别注释行

### 第二阶段：内容提取

#### 2.1 代码内容提取

```python
def extract_translatable_content(file_content, language):
    """提取可翻译内容"""
    if language == 'python':
        return extract_python_content(file_content)
    elif language == 'javascript':
        return extract_javascript_content(file_content)
    # ... 其他语言
    
def extract_python_content(content):
    """提取Python文件中的可翻译内容"""
    translatable_items = []
    
    # 提取字符串字面量
    strings = extract_strings(content, python_string_patterns)
    translatable_items.extend(strings)
    
    # 提取注释
    comments = extract_comments(content, python_comment_patterns)
    translatable_items.extend(comments)
    
    # 提取文档字符串
    docstrings = extract_docstrings(content)
    translatable_items.extend(docstrings)
    
    return translatable_items
```

#### 2.2 文档内容提取

```python
def extract_markdown_content(content):
    """提取Markdown文档中的可翻译内容"""
    translatable_blocks = []
    
    # 解析代码块（不翻译）
    code_blocks = identify_code_blocks(content)
    
    # 解析标题和段落
    headers = extract_headers(content)
    paragraphs = extract_paragraphs(content)
    
    # 解析列表和表格
    lists = extract_lists(content)
    tables = extract_tables(content)
    
    translatable_blocks.extend(headers)
    translatable_blocks.extend(paragraphs)
    
    return translatable_blocks
```

### 第三阶段：翻译处理

#### 3.1 智能翻译引擎

```python
def translate_content(content, content_type, target_language='zh-CN'):
    """智能翻译内容"""
    if content_type == 'code_string':
        return translate_string(content, preserve_placeholders=True)
    elif content_type == 'code_comment':
        return translate_comment(content, preserve_formatting=True)
    elif content_type == 'documentation':
        return translate_documentation(content, maintain_structure=True)
    elif content_type == 'api_description':
        return translate_api_description(content, preserve_technical_terms=True)
```

#### 3.2 术语管理

```python
class TerminologyManager:
    """术语管理器，确保翻译一致性"""
    
    def __init__(self):
        self.term_base = load_terminology_base()
        self.custom_terms = {}
    
    def translate_term(self, term):
        """翻译术语，优先使用术语库"""
        if term in self.term_base:
            return self.term_base[term]
        if term in self.custom_terms:
            return self.custom_terms[term]
        return None
    
    def add_custom_term(self, source, target):
        """添加自定义术语"""
        self.custom_terms[source] = target
```

### 第四阶段：内容重建

#### 4.1 代码文件重建

```python
def rebuild_code_file(original_content, translations, language):
    """重建代码文件，应用翻译"""
    rebuilt_content = original_content
    
    for translation in translations:
        position = translation['position']
        original_text = translation['original']
        translated_text = translation['translated']
        
        rebuilt_content = replace_text(
            rebuilt_content,
            position,
            original_text,
            translated_text
        )
    
    return rebuilt_content
```

#### 4.2 文档文件重建

```python
def rebuild_document(original_content, translations, doc_type):
    """重建文档，应用翻译"""
    rebuilt_content = original_content
    
    # 保持代码块不变
    code_blocks = identify_code_blocks(original_content)
    
    # 应用翻译到非代码区域
    for translation in translations:
        if not is_in_code_block(translation['position'], code_blocks):
            rebuilt_content = apply_translation(
                rebuilt_content,
                translation
            )
    
    return rebuilt_content
```

### 第五阶段：验证与输出

#### 5.1 语法验证

```python
def validate_translated_code(content, language):
    """验证翻译后的代码语法正确性"""
    if language == 'python':
        return validate_python_syntax(content)
    elif language == 'javascript':
        return validate_javascript_syntax(content)
    # ... 其他语言
    
def validate_python_syntax(content):
    """验证Python代码语法"""
    try:
        ast.parse(content)
        return {'valid': True}
    except SyntaxError as e:
        return {
            'valid': False,
            'error': str(e),
            'line': e.lineno
        }
```

#### 5.2 格式验证

```python
def validate_document_format(content, doc_type):
    """验证文档格式完整性"""
    if doc_type == 'markdown':
        return validate_markdown_format(content)
    elif doc_type == 'yaml':
        return validate_yaml_format(content)
    elif doc_type == 'json':
        return validate_json_format(content)
```

---

# 智能体调用

## 调用翻译智能体

当遇到复杂翻译任务时，可调用专门的翻译智能体：

```python
def call_translation_agent(content, context, requirements):
    """调用翻译智能体处理复杂任务"""
    agent_task = {
        'content': content,
        'context': context,
        'requirements': requirements,
        'target_language': 'zh-CN'
    }
    
    result = Task.execute(
        agent='python-translator',
        task='翻译技术内容',
        query=f"请将以下技术内容翻译成简体中文：{content}",
        response_language='zh-CN'
    )
    
    return result
```

## 智能体任务类型

| 任务类型 | 适用场景 | 说明 |
|---------|---------|------|
| python-translator | Python代码翻译 | 保持语法正确性 |
| chinese-commentator | TypeScript代码翻译 | 添加详细中文注释 |
| vite-chinese-translator | 前端工程文件翻译 | 配置文件和代码翻译 |
| shell-localizer-commenter | Shell脚本翻译 | 脚本和注释翻译 |
| go-translator-commenter | Go代码翻译 | 代码和文档翻译 |
| rust-i18n-translator | Rust代码翻译 | 国际化处理 |

---

# 配置选项

## 翻译模式

### 模式1：保留原文（Preview）

仅识别和标记可翻译内容，不进行实际翻译：
- 生成翻译建议列表
- 标记需要人工审核的内容
- 适合预览翻译工作量

### 模式2：自动翻译（Auto）

使用自动翻译引擎进行翻译：
- 调用翻译API或智能体
- 应用术语库进行一致性处理
- 适合大量内容批量处理

### 模式3：人工审核（Review）

自动翻译后等待人工审核：
- 生成翻译建议
- 提供审核界面
- 确认后应用翻译

### 模式4：混合模式（Hybrid）

根据内容类型自动选择翻译方式：
- 简单内容自动翻译
- 复杂内容调用智能体
- 关键技术术语人工确认

## 术语库配置

### 默认术语库

内置常见技术术语翻译：
- 编程概念：function, class, variable, object...
- 数据结构：array, list, tree, graph...
- 网络术语：endpoint, request, response, API...
- 数据库术语：query, table, index, schema...

### 自定义术语库

支持添加项目特定的术语：
```yaml
custom_terms:
  "ProjectName": "项目名称"
  "CustomConfig": "自定义配置"
  "SpecialAPI": "特殊接口"
```

## 输出选项

### 文件处理

- **原地修改**：直接修改原文件（谨慎使用）
- **备份翻译**：生成翻译后的新文件
- **双语对照**：生成包含原文和译文的对照文件

### 报告生成

- **翻译报告**：记录翻译统计和变更日志
- **术语报告**：列出使用的术语和翻译一致性
- **问题报告**：记录翻译中的问题和需要审核的内容

---

# 最佳实践

## 文件处理建议

### 1. 备份原文件

在执行翻译之前，始终备份原文件：
```bash
# 创建备份
cp original_file.py original_file.py.bak

# 或使用版本控制
git commit -m "翻译前备份"
```

### 2. 分批处理

对于大型项目，建议分批翻译：
- 先翻译核心文档
- 再翻译示例代码
- 最后翻译注释和辅助说明

### 3. 验证测试

翻译代码后，运行测试确保功能正常：
```bash
# Python代码验证
python -m py_compile translated_file.py

# 运行单元测试
pytest tests/

# JavaScript代码验证
node --check translated_file.js
```

## 术语一致性

### 建立术语表

在项目开始时建立术语表：
```markdown
# 项目术语表

| 英文术语 | 中文翻译 | 使用场景 |
|---------|---------|---------|
| Service | 服务 | 业务逻辑层 |
| Repository | 仓储 | 数据访问层 |
| Entity | 实体 | 数据模型 |
```

### 跨文档同步

确保术语在所有文档中一致使用：
- 定期检查翻译一致性
- 使用术语库自动校正
- 建立术语更新流程

## 质量控制

### 翻译审核清单

- [ ] 技术术语翻译准确
- [ ] 代码语法保持正确
- [ ] 文档格式完整无缺
- [ ] 链接和引用有效
- [ ] 术语使用一致

### 常见问题处理

**问题1：代码中的占位符被翻译**
- 解决：使用正则表达式识别占位符模式
- 解决：配置忽略特定格式的字符串

**问题2：术语翻译不一致**
- 解决：使用术语库强制一致性
- 解决：翻译后运行一致性检查

**问题3：翻译后格式错乱**
- 解决：备份原文件格式
- 解决：使用专业的文档解析工具

---

# 集成使用

## 作为独立工具使用

```bash
# 翻译单个文件
python scripts/translator.py --file path/to/file.py --mode auto

# 翻译整个目录
python scripts/translator.py --dir path/to/project --output translated/

# 仅预览翻译内容
python scripts/translator.py --file path/to/file.py --mode preview
```

## 作为智能体调用

```python
from Task import Task

# 调用翻译智能体
result = Task.execute(
    agent='python-translator',
    task='翻译Python代码文件',
    query='请将 src/utils.py 文件中的所有注释和文档字符串翻译成简体中文，保持代码语法正确',
    response_language='zh-CN'
)
```

## 与版本控制系统集成

```bash
# 在Git钩子中使用
# .git/pre-commit
python scripts/translator.py --staged --mode review

# 提交翻译后的文件
git add translated/
git commit -m "docs: 翻译更新"
```

---

# 错误处理

## 常见错误类型

### 文件处理错误

| 错误代码 | 错误描述 | 解决方案 |
|---------|---------|---------|
| F001 | 文件编码不支持 | 转换为UTF-8编码 |
| F002 | 文件格式损坏 | 检查文件完整性 |
| F003 | 权限不足 | 检查文件读写权限 |

### 翻译处理错误

| 错误代码 | 错误描述 | 解决方案 |
|---------|---------|---------|
| T001 | 语法解析失败 | 检查代码语法 |
| T002 | 术语冲突 | 更新术语库配置 |
| T003 | 翻译超时 | 分批处理内容 |

### 智能体调用错误

| 错误代码 | 错误描述 | 解决方案 |
|---------|---------|---------|
| A001 | 智能体不可用 | 检查智能体配置 |
| A002 | 翻译失败 | 手动翻译或重试 |
| A003 | 结果验证失败 | 审核翻译结果 |

## 错误恢复

```python
def handle_translation_error(error, context):
    """处理翻译错误"""
    error_code = error['code']
    
    if error_code in ['F001', 'F002']:
        return handle_file_error(error, context)
    elif error_code in ['T001', 'T002']:
        return handle_translation_error(error, context)
    elif error_code in ['A001', 'A002', 'A003']:
        return handle_agent_error(error, context)
    
    # 记录错误日志
    log_error(error, context)
    
    # 返回错误报告
    return {
        'status': 'failed',
        'error': error,
        'context': context
    }
```

---

# 性能优化

## 大文件处理

### 分块处理

对于大型文件，采用分块处理：
```python
def process_large_file(file_path, chunk_size=10000):
    """分块处理大文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chunks = split_content(content, chunk_size)
    results = []
    
    for i, chunk in enumerate(chunks):
        translated = translate_chunk(chunk)
        results.append(translated)
    
    return combine_results(results)
```

### 并行处理

多线程并行处理多个文件：
```python
from concurrent.futures import ThreadPoolExecutor

def translate_files_parallel(file_list, max_workers=4):
    """并行翻译多个文件"""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(translate_file, file_list))
    return results
```

## 缓存机制

### 翻译缓存

```python
class TranslationCache:
    """翻译结果缓存"""
    
    def __init__(self, cache_dir='.translation_cache'):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_cache_key(self, content, content_type):
        """生成缓存键"""
        import hashlib
        content_hash = hashlib.md5(content.encode()).hexdigest()
        return f"{content_type}_{content_hash}"
    
    def get(self, content, content_type):
        """获取缓存的翻译结果"""
        key = self.get_cache_key(content, content_type)
        cache_path = os.path.join(self.cache_dir, f"{key}.json")
        
        if os.path.exists(cache_path):
            with open(cache_path, 'r') as f:
                return json.load(f)['translated']
        return None
    
    def set(self, content, content_type, translated):
        """缓存翻译结果"""
        key = self.get_cache_key(content, content_type)
        cache_path = os.path.join(self.cache_dir, f"{key}.json")
        
        with open(cache_path, 'w') as f:
            json.dump({
                'original': content,
                'translated': translated,
                'content_type': content_type
            }, f)
```

---

# 术语库管理

## 内置术语库

### 编程语言术语

| 英文 | 中文 | 说明 |
|-----|------|------|
| function | 函数 | 可重用的代码块 |
| class | 类 | 面向对象的基本单位 |
| method | 方法 | 类中定义的函数 |
| variable | 变量 | 存储数据的容器 |
| constant | 常量 | 不可修改的变量 |
| interface | 接口 | 抽象类型定义 |
| inheritance | 继承 | 类之间的父子关系 |
| polymorphism | 多态 | 同名方法的多种实现 |
| encapsulation | 封装 | 隐藏内部实现细节 |
| abstraction | 抽象 | 简化复杂系统 |

### 网络通信术语

| 英文 | 中文 | 说明 |
|-----|------|------|
| endpoint | 端点 | API访问地址 |
| request | 请求 | 客户端发送的数据 |
| response | 响应 | 服务器返回的数据 |
| authentication | 身份验证 | 确认用户身份 |
| authorization | 授权 | 权限控制机制 |
| header | 头信息 | 请求/响应的元数据 |
| payload | 载荷 | 传输的数据内容 |
| latency | 延迟 | 请求响应时间 |
| throughput | 吞吐量 | 单位时间处理量 |

### 数据库术语

| 英文 | 中文 | 说明 |
|-----|------|------|
| query | 查询 | 数据库检索操作 |
| schema | 模式 | 数据库结构定义 |
| index | 索引 | 加速查询的数据结构 |
| transaction | 事务 | 原子性操作序列 |
| constraint | 约束 | 数据有效性规则 |
| primary key | 主键 | 唯一标识字段 |
| foreign key | 外键 | 表间关联字段 |
| normalization | 规范化 | 数据库设计原则 |

## 自定义术语添加

```python
def add_custom_terminology(term_file):
    """从文件加载自定义术语"""
    with open(term_file, 'r', encoding='utf-8') as f:
        terms = yaml.safe_load(f)
    
    terminology_manager = TerminologyManager()
    
    for category, term_list in terms.items():
        for term in term_list:
            terminology_manager.add_custom_term(
                term['source'],
                term['target']
            )
    
    return terminology_manager
```

---

# 扩展开发

## 添加新文件类型支持

```python
class FileTypeRegistry:
    """文件类型注册表"""
    
    def __init__(self):
        self.handlers = {}
    
    def register(self, extension, handler_class):
        """注册新的文件类型处理器"""
        self.handlers[extension] = handler_class
    
    def get_handler(self, file_path):
        """获取文件类型处理器"""
        extension = get_file_extension(file_path)
        
        if extension in self.handlers:
            return self.handlers[extension]()
        
        # 默认处理器
        return DefaultFileHandler()

# 使用示例
registry = FileTypeRegistry()
registry.register('.swift', SwiftFileHandler)
registry.register('.kt', KotlinFileHandler)
```

## 添加新语言支持

```python
class LanguageRegistry:
    """编程语言注册表"""
    
    def __init__(self):
        self.configs = {}
    
    def register(self, language, config):
        """注册新的编程语言"""
        self.configs[language] = config
    
    def get_config(self, language):
        """获取语言配置"""
        return self.configs.get(language, DefaultLanguageConfig())

# 注册新的编程语言
language_registry = LanguageRegistry()
language_registry.register('kotlin', {
    'string_patterns': r'"[^"]*"',
    'comment_patterns': [
        r'//.*$',
        r'/\*[\s\S]*?\*/'
    ],
    'docstring_patterns': [
        r'/\*\*[\s\S]*?\*/'
    ],
    'keywords': [...]  # Kotlin关键字列表
})
```

---

# 快速参考

## 命令行用法

```bash
# 基本用法
python scripts/translator.py -f <file> [-o <output>]

# 批量翻译
python scripts/translator.py -d <directory> --recursive

# 指定翻译模式
python scripts/translator.py -f <file> --mode auto|preview|review

# 生成报告
python scripts/translator.py -f <file> --report

# 使用配置文件
python scripts/translator.py -f <file> --config <config.yaml>
```

## 配置文件示例

```yaml
# translator_config.yaml
translation:
  mode: auto
  target_language: zh-CN
  
terminology:
  use_default: true
  custom_terms_file: terms.yaml
  
output:
  backup_original: true
  generate_report: true
  
processing:
  chunk_size: 10000
  parallel_threads: 4
  cache_enabled: true
```

## API接口

```python
from translator import TechnicalDocumentTranslator

# 初始化翻译器
translator = TechnicalDocumentTranslator(config)

# 翻译单个文件
result = translator.translate_file('path/to/file.py')

# 翻译整个目录
result = translator.translate_directory('path/to/project')

# 获取翻译统计
stats = translator.get_translation_stats()
```

---

# 故障排除

## 常见问题FAQ

**Q: 翻译后代码无法运行怎么办？**
A: 1. 检查是否误翻译了关键字或变量名
   2. 使用语法验证功能检查代码正确性
   3. 查看翻译报告中的错误日志
   4. 必要时使用备份文件恢复

**Q: 术语翻译不一致如何解决？**
A: 1. 更新术语库配置
   2. 使用一致性检查工具
   3. 批量更新已翻译内容
   4. 建立术语审核流程

**Q: 特殊格式文件如何处理？**
A: 1. 检查是否支持该文件类型
   2. 尝试转换为支持格式
   3. 联系开发者添加支持
   4. 手动处理关键内容

**Q: 翻译质量如何保证？**
A: 1. 使用专业翻译智能体
   2. 建立审核流程
   3. 定期检查翻译质量
   4. 收集用户反馈改进

---

# 更新日志

## 版本1.0.0

- 初始版本发布
- 支持主流编程语言翻译
- 支持常见文档格式
- 内置技术术语库
- 智能代码识别功能
- 语法验证能力
