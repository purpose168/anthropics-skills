#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技术文档生成器

该模块提供完整的技术文档生成功能，能够从源代码分析结果中生成多种格式
的技术文档，包括Markdown、HTML、PDF和reStructuredText。文档内容包括
目录索引、模块说明、接口定义、实现逻辑流程图及代码关键片段注释。

联系：purpose168@outlook.com
"""

import os
import sys
import json
import re
import logging
import time
import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from enum import Enum
from collections import defaultdict
from datetime import datetime

# 配置日志记录器
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class OutputFormat(Enum):
    """输出格式枚举"""
    MARKDOWN = "markdown"
    HTML = "html"
    PDF = "pdf"
    RESTRUCTURED = "rst"
    DOCX = "docx"


class DocumentationSection(Enum):
    """文档章节枚举"""
    COVER = "cover"
    TABLE_OF_CONTENTS = "toc"
    OVERVIEW = "overview"
    ARCHITECTURE = "architecture"
    MODULES = "modules"
    APIs = "apis"
    DATA_DICTIONARY = "data_dictionary"
    DEPLOYMENT = "deployment"
    APPENDIX = "appendix"
    INDEX = "index"


@dataclass
class DocumentConfig:
    """文档配置数据类"""
    title: str = "技术设计文档"
    subtitle: str = ""
    author: str = ""
    version: str = "1.0.0"
    date: str = ""
    language: str = "zh-CN"
    template: str = "standard"
    include_toc: bool = True
    include_index: bool = True
    include_examples: bool = True
    generate_diagrams: bool = True
    max_line_width: int = 120
    code_theme: str = "github"


@dataclass
class DocumentSection:
    """文档章节数据类"""
    section_id: str              # 章节ID
    title: str                   # 章节标题
    level: int = 1               # 标题级别
    content: str = ""            # 章节内容
    subsections: List['DocumentSection'] = field(default_factory=list)  # 子章节
    order: int = 0               # 排序顺序


@dataclass
class CodeExample:
    """代码示例数据类"""
    language: str                # 编程语言
    code: str                    # 代码内容
    description: str = ""        # 示例描述
    filename: str = ""           # 文件名
    line_range: Tuple[int, int] = (0, 0)  # 行号范围


class TemplateEngine:
    """模板引擎，提供文档模板渲染功能"""
    
    def __init__(self, template_dir: Optional[str] = None):
        """
        初始化模板引擎
        
        Args:
            template_dir: 模板目录路径
        """
        self.templates = {}
        self.template_dir = template_dir
        self._load_default_templates()
    
    def _load_default_templates(self):
        """加载默认模板"""
        self.templates = {
            'cover': self._default_cover_template(),
            'toc': self._default_toc_template(),
            'overview': self._default_overview_template(),
            'architecture': self._default_architecture_template(),
            'module': self._default_module_template(),
            'api': self._default_api_template(),
            'class': self._default_class_template(),
            'function': self._default_function_template(),
            'data_dictionary': self._default_data_dictionary_template(),
            'deployment': self._default_deployment_template(),
            'code_example': self._default_code_example_template(),
        }
    
    def _default_cover_template(self) -> str:
        """默认封面模板"""
        return """# {{title}}

{{#if subtitle}}
## {{subtitle}}
{{/if}}

---

**版本**: {{version}}  
**作者**: {{author}}  
**日期**: {{date}}

---

*本文档由源代码自动生成*
"""
    
    def _default_toc_template(self) -> str:
        """默认目录模板"""
        return """# 目录

{{toc_items}}
"""
    
    def _default_overview_template(self) -> str:
        """默认概述模板"""
        return """## 项目概述

{{project_description}}

### 项目统计

| 指标 | 数值 |
|------|------|
| 总文件数 | {{total_files}} |
| 总代码行数 | {{total_lines}} |
| 类数量 | {{total_classes}} |
| 函数数量 | {{total_functions}} |
| 模块数量 | {{total_modules}} |

### 技术栈

{{tech_stack}}

### 入口点

{{entry_points}}
"""
    
    def _default_architecture_template(self) -> str:
        """默认架构模板"""
        return """## 架构设计

### 整体架构

{{architecture_diagram}}

### 架构说明

{{architecture_description}}

### 技术层次

{{layer_description}}
"""
    
    def _default_module_template(self) -> str:
        """默认模块模板"""
        return """## {{module_name}}

### 模块概述

{{module_description}}

### 核心类

| 类名 | 职责 | 方法数 |
|------|------|--------|
{{class_table}}

### 对外接口

{{public_interfaces}}

### 依赖关系

**依赖的模块**: {{dependencies}}  
**被依赖的模块**: {{dependents}}

### 文件列表

{{file_list}}
"""
    
    def _default_api_template(self) -> str:
        """默认API模板"""
        return """## {{api_name}}

### 接口描述

{{api_description}}

### 请求信息

**URL**: `{{url}}`  
**方法**: `{{method}}`

### 请求参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
{{request_params}}

### 响应格式

```json
{{response_example}}
```

### 错误码

| 错误码 | 描述 |
|--------|------|
{{error_codes}}
"""
    
    def _default_class_template(self) -> str:
        """默认类模板"""
        return """### {{class_name}}

```{{language}}
{{class_code}}
```

**职责**: {{responsibility}}

**继承关系**: {{inheritance}}

#### 属性

| 属性名 | 类型 | 可见性 | 描述 |
|--------|------|--------|------|
{{properties}}

#### 方法

| 方法名 | 返回类型 | 描述 |
|--------|----------|------|
{{methods}}
"""
    
    def _default_function_template(self) -> str:
        """默认函数模板"""
        return """### {{function_name}}

```{{language}}
{{function_signature}}
```

{{docstring}}

**参数说明**:

{{parameters}}

**返回值**:

{{returns}}

**使用示例**:

```{{language}}
{{example}}
```
"""
    
    def _default_data_dictionary_template(self) -> str:
        """默认数据字典模板"""
        return """## 数据字典

### 数据模型

{{data_models}}

### 枚举值

{{enumerations}}

### 常量定义

{{constants}}
"""
    
    def _default_deployment_template(self) -> str:
        """默认部署模板"""
        return """## 部署指南

### 环境要求

{{environment_requirements}}

### 配置说明

{{configuration}}

### 部署步骤

{{deployment_steps}}
"""
    
    def _default_code_example_template(self) -> str:
        """默认代码示例模板"""
        return """```{{language}}
{{code}}
```

{{description}}
"""
    
    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        渲染模板
        
        Args:
            template_name: 模板名称
            context: 上下文数据
            
        Returns:
            str: 渲染后的内容
        """
        template = self.templates.get(template_name, "")
        
        # 简单模板渲染（支持变量替换和基本条件）
        for key, value in context.items():
            if isinstance(value, bool):
                if value:
                    template = re.sub(r'\{\{#if\s+' + key + r'\}\}([\s\S]*?)\{\{/if\}\}',
                                    r'\1', template)
                else:
                    template = re.sub(r'\{\{#if\s+' + key + r'\}\}[\s\S]*?\{\{/if\}\}',
                                    '', template)
            else:
                placeholder = '{{' + key + '}}'
                template = template.replace(placeholder, str(value))
        
        # 处理列表
        for key, values in context.items():
            if isinstance(values, list):
                pattern = r'\{\{' + key + r'\}\}'
                if pattern in template:
                    items_html = '\n'.join(str(v) for v in values)
                    template = template.replace(pattern, items_html)
        
        return template


class MarkdownGenerator:
    """Markdown文档生成器"""
    
    def __init__(self, config: DocumentConfig):
        """
        初始化Markdown生成器
        
        Args:
            config: 文档配置
        """
        self.config = config
        self.template_engine = TemplateEngine()
        self.sections: List[DocumentSection] = []
    
    def generate(self, analysis_result: Dict) -> str:
        """
        生成Markdown文档
        
        Args:
            analysis_result: 源代码分析结果
            
        Returns:
            str: Markdown文档内容
        """
        lines = []
        
        # 生成封面
        lines.append(self._generate_cover())
        
        # 生成目录
        if self.config.include_toc:
            lines.append(self._generate_table_of_contents())
        
        # 生成各章节
        lines.append(self._generate_overview(analysis_result))
        lines.append(self._generate_architecture(analysis_result))
        lines.append(self._generate_modules(analysis_result))
        lines.append(self._generate_apis(analysis_result))
        lines.append(self._generate_data_dictionary(analysis_result))
        lines.append(self._generate_deployment(analysis_result))
        
        # 生成索引
        if self.config.include_index:
            lines.append(self._generate_index(analysis_result))
        
        return '\n'.join(lines)
    
    def _generate_cover(self) -> str:
        """生成封面"""
        context = {
            'title': self.config.title,
            'subtitle': self.config.subtitle,
            'version': self.config.version,
            'author': self.config.author,
            'date': self.config.date or datetime.now().strftime('%Y-%m-%d')
        }
        
        return self.template_engine.render('cover', context)
    
    def _generate_table_of_contents(self) -> str:
        """生成目录"""
        toc_items = []
        
        section_mapping = {
            'overview': '1. 项目概述',
            'architecture': '2. 架构设计',
            'modules': '3. 模块说明',
            'apis': '4. 接口文档',
            'data_dictionary': '5. 数据字典',
            'deployment': '6. 部署指南',
            'index': '附录：索引'
        }
        
        for section_id, title in section_mapping.items():
            toc_items.append(f"- [{title}](#{section_id})")
            
            # 如果有模块，添加子目录
            if section_id == 'modules':
                toc_items.append("  - [模块列表](#_31-模块列表)")
        
        context = {
            'toc_items': '\n'.join(toc_items)
        }
        
        return self.template_engine.render('toc', context)
    
    def _generate_overview(self, analysis_result: Dict) -> str:
        """生成项目概述章节"""
        project_info = analysis_result.get('project_info', {})
        statistics = project_info.get('statistics', {})
        modules = analysis_result.get('modules', {})
        
        # 生成技术栈列表
        file_analyses = analysis_result.get('file_analysis', [])
        language_dist = statistics.get('language_distribution', {})
        tech_stack_items = []
        for lang, count in language_dist.items():
            tech_stack_items.append(f"- **{lang}**: {count} 个文件")
        
        # 生成入口点列表
        entry_points = project_info.get('entry_points', [])
        entry_items = []
        for entry in entry_points[:5]:
            entry_items.append(f"- `{entry.get('file', '')}` ({entry.get('type', '')})")
        
        context = {
            'project_description': f"本项目是一个基于 {len(modules)} 个模块的软件系统，"
                                  f"包含 {statistics.get('total_files', 0)} 个源代码文件，"
                                  f"共计 {statistics.get('total_lines', 0)} 行代码。",
            'total_files': statistics.get('total_files', 0),
            'total_lines': statistics.get('total_lines', 0),
            'total_classes': statistics.get('total_classes', 0),
            'total_functions': statistics.get('total_functions', 0),
            'total_modules': len(modules),
            'tech_stack': '\n'.join(tech_stack_items),
            'entry_points': '\n'.join(entry_items) if entry_items else "无明确的入口点"
        }
        
        return self.template_engine.render('overview', context)
    
    def _generate_architecture(self, analysis_result: Dict) -> str:
        """生成架构设计章节"""
        modules = analysis_result.get('modules', {})
        
        # 生成架构图（Mermaid格式）
        diagram = self._generate_architecture_diagram(modules)
        
        # 描述架构层次
        layer_description = self._describe_architecture_layers(modules)
        
        context = {
            'architecture_diagram': diagram,
            'architecture_description': "本项目采用分层架构设计，包括表现层、应用层、领域层和基础设施层。",
            'layer_description': layer_description
        }
        
        return self.template_engine.render('architecture', context)
    
    def _generate_architecture_diagram(self, modules: Dict) -> str:
        """生成架构图"""
        lines = ["```mermaid", "graph TD"]
        
        # 添加模块节点
        for module_name, module in list(modules.items())[:10]:
            responsibility = module.get('responsibility', '')[:20]
            lines.append(f"    {module_name}[{module_name}]")
        
        # 添加依赖边
        seen_edges = set()
        for module_name, module in modules.items():
            for dep in module.get('dependencies', []):
                target = dep.get('target_module', '')
                if target in modules and target != module_name:
                    edge = (module_name, target)
                    if edge not in seen_edges:
                        seen_edges.add(edge)
                        lines.append(f"    {module_name} --> {target}")
        
        lines.append("```")
        
        return '\n'.join(lines)
    
    def _describe_architecture_layers(self, modules: Dict) -> str:
        """描述架构层次"""
        layers = {
            '表现层': [],
            '应用层': [],
            '领域层': [],
            '基础设施层': [],
            '其他': []
        }
        
        for module_name, module in modules.items():
            responsibility = module.get('responsibility', '')
            
            if any(kw in responsibility for kw in ['控制器', '视图', '页面', 'API']):
                layers['表现层'].append(module_name)
            elif any(kw in responsibility for kw in ['服务', '业务', '用例']):
                layers['应用层'].append(module_name)
            elif any(kw in responsibility for kw in ['实体', '值对象', '聚合']):
                layers['领域层'].append(module_name)
            elif any(kw in responsibility for kw in ['仓储', '数据', '持久化']):
                layers['基础设施层'].append(module_name)
            else:
                layers['其他'].append(module_name)
        
        lines = []
        for layer_name, mods in layers.items():
            if mods:
                lines.append(f"### {layer_name}")
                for mod in mods:
                    lines.append(f"- **{mod}**: {mods[mod] if isinstance(mods[mod], str) else '模块'}")
        
        return '\n'.join(lines)
    
    def _generate_modules(self, analysis_result: Dict) -> str:
        """生成模块说明章节"""
        modules = analysis_result.get('modules', {})
        lines = ["## 3. 模块说明\n"]
        
        lines.append("### 模块列表\n")
        lines.append("| 模块名 | 职责 | 文件数 | 出向依赖 | 入向依赖 |")
        lines.append("|--------|------|--------|---------|---------|")
        
        for module_name, module in modules.items():
            lines.append(f"| **{module_name}** | {module.get('responsibility', '暂无描述')[:30]}... | "
                        f"{module.get('file_count', 0)} | {len(module.get('dependencies', []))} | "
                        f"{len(module.get('dependents', []))} |")
        
        # 生成各模块详细说明
        lines.append("\n### 模块详情\n")
        
        for module_name, module in modules.items():
            lines.append(f"#### 3.{list(modules.keys()).index(module_name)+1} {module_name}\n")
            
            # 模块概述
            lines.append(f"**模块职责**: {module.get('responsibility', '暂无描述')}\n")
            
            # 核心类
            core_classes = module.get('core_classes', [])
            if core_classes:
                lines.append("\n**核心类**:")
                for cls in core_classes[:5]:
                    lines.append(f"- `{cls}`")
                lines.append("")
            
            # 公共接口
            public_interfaces = module.get('public_interfaces', [])
            if public_interfaces:
                lines.append("\n**公共接口**:")
                for interface in public_interfaces[:5]:
                    if isinstance(interface, dict):
                        lines.append(f"- `{interface.get('name', '')}()`")
                    else:
                        lines.append(f"- `{interface}`")
                lines.append("")
            
            # 依赖关系
            dependencies = [d.get('target_module', '') for d in module.get('dependencies', [])]
            dependents = [d.get('source_module', '') for d in module.get('dependents', [])]
            
            if dependencies:
                lines.append(f"\n**依赖**: {', '.join(dependencies[:5])}")
            if dependents:
                lines.append(f"\n**被依赖**: {', '.join(dependents[:5])}")
            
            lines.append("\n---")
        
        return '\n'.join(lines)
    
    def _generate_apis(self, analysis_result: Dict) -> str:
        """生成接口文档章节"""
        file_analyses = analysis_result.get('file_analysis', [])
        apis = []
        
        # 提取API信息
        for fa in file_analyses:
            analysis = fa.get('analysis', {})
            classes = analysis.get('classes', [])
            
            for cls in classes:
                methods = cls.get('methods', [])
                for method in methods:
                    method_name = method.get('name', '')
                    # 识别可能是API的方法
                    if any(kw in method_name.lower() for kw in ['get', 'post', 'put', 'delete', 'handle']):
                        apis.append({
                            'class': cls.get('name', ''),
                            'method': method_name,
                            'description': method.get('docstring', ''),
                            'parameters': method.get('parameters', []),
                            'return_type': method.get('return_type', '')
                        })
        
        lines = ["## 4. 接口文档\n"]
        
        if not apis:
            lines.append("未检测到明确的API接口。\n")
            return '\n'.join(lines)
        
        # 分组显示
        for api in apis[:20]:
            lines.append(f"### {api['class']}.{api['method']}\n")
            
            if api['description']:
                lines.append(f"{api['description']}\n")
            
            # 参数表格
            params = api.get('parameters', [])
            if params:
                lines.append("**参数**:")
                lines.append("| 参数名 | 类型 | 描述 |")
                lines.append("|--------|------|------|")
                for param in params:
                    lines.append(f"| {param.get('name', '')} | {param.get('type', 'any')} | {param.get('description', '-')} |")
                lines.append("")
            
            # 返回类型
            if api['return_type']:
                lines.append(f"**返回类型**: `{api['return_type']}`\n")
            
            lines.append("---\n")
        
        return '\n'.join(lines)
    
    def _generate_data_dictionary(self, analysis_result: Dict) -> str:
        """生成数据字典章节"""
        file_analyses = analysis_result.get('file_analysis', [])
        classes = []
        constants = []
        
        for fa in file_analyses:
            analysis = fa.get('analysis', {})
            classes.extend(analysis.get('classes', []))
            constants.extend(analysis.get('constants', []))
        
        lines = ["## 5. 数据字典\n"]
        
        # 数据模型
        lines.append("### 5.1 数据模型\n")
        lines.append("| 类名 | 职责 | 属性数 | 方法数 |")
        lines.append("|------|------|--------|--------|")
        
        for cls in classes[:20]:
            lines.append(f"| {cls.get('name', '')} | {cls.get('docstring', '')[:30] if cls.get('docstring') else '-'}... | "
                        f"{len(cls.get('attributes', []))} | {len(cls.get('methods', []))} |")
        
        # 常量定义
        lines.append("\n### 5.2 常量定义\n")
        lines.append("| 常量名 | 值 |")
        lines.append("|--------|-----|")
        
        for const in constants[:20]:
            lines.append(f"| {const.get('name', '')} | `{const.get('value', '')}` |")
        
        return '\n'.join(lines)
    
    def _generate_deployment(self, analysis_result: Dict) -> str:
        """生成部署指南章节"""
        file_analyses = analysis_result.get('file_analysis', [])
        
        # 查找配置文件
        config_files = []
        for fa in file_analyses:
            file_info = fa.get('file_info', {})
            if file_info.get('name') in ['package.json', 'requirements.txt', 'pom.xml',
                                         'go.mod', 'Cargo.toml', 'Dockerfile']:
                config_files.append(file_info.get('relative_path', ''))
        
        lines = ["## 6. 部署指南\n"]
        
        # 环境要求
        lines.append("### 6.1 环境要求\n")
        lines.append("基于项目配置文件，部署需要以下环境：\n")
        
        if 'package.json' in config_files:
            lines.append("- Node.js 14+")
            lines.append("- npm 或 yarn\n")
        
        if 'requirements.txt' in config_files:
            lines.append("- Python 3.8+")
            lines.append("- pip\n")
        
        if 'go.mod' in config_files:
            lines.append("- Go 1.16+\n")
        
        if 'Cargo.toml' in config_files:
            lines.append("- Rust 1.56+\n")
        
        # 配置文件
        lines.append("### 6.2 配置文件\n")
        lines.append("项目包含以下配置文件：\n")
        
        for config_file in config_files:
            lines.append(f"- `{config_file}`")
        
        lines.append("\n### 6.3 构建和部署\n")
        lines.append("```bash\n")
        
        if 'package.json' in config_files:
            lines.append("# 安装依赖")
            lines.append("npm install")
            lines.append("")
            lines.append("# 构建项目")
            lines.append("npm run build")
            lines.append("")
        
        if 'requirements.txt' in config_files:
            lines.append("# 安装依赖")
            lines.append("pip install -r requirements.txt")
            lines.append("")
        
        if 'go.mod' in config_files:
            lines.append("# 构建项目")
            lines.append("go build")
            lines.append("")
        
        if 'Cargo.toml' in config_files:
            lines.append("# 构建项目")
            lines.append("cargo build --release")
            lines.append("")
        
        lines.append("```")
        
        return '\n'.join(lines)
    
    def _generate_index(self, analysis_result: Dict) -> str:
        """生成索引章节"""
        file_analyses = analysis_result.get('file_analysis', [])
        modules = analysis_result.get('modules', {})
        
        # 收集所有类名和函数名
        index_entries = {}
        
        for fa in file_analyses:
            analysis = fa.get('analysis', {})
            
            for cls in analysis.get('classes', []):
                cls_name = cls.get('name', '')
                if cls_name and cls_name not in index_entries:
                    index_entries[cls_name] = {
                        'type': '类',
                        'module': self._find_module(cls_name, modules)
                    }
            
            for func in analysis.get('functions', []):
                func_name = func.get('name', '')
                if func_name and func_name not in index_entries:
                    index_entries[func_name] = {
                        'type': '函数',
                        'module': self._find_module(func_name, modules)
                    }
        
        lines = ["## 附录：索引\n"]
        
        # 按字母分组
        grouped = defaultdict(list)
        for name, info in index_entries.items():
            first_letter = name[0].upper() if name else '#'
            grouped[first_letter].append((name, info))
        
        for letter in sorted(grouped.keys()):
            lines.append(f"### {letter}\n")
            for name, info in sorted(grouped[letter], key=lambda x: x[0]):
                module = info['module']
                lines.append(f"- **{name}** ({info['type']}) - {module}")
            lines.append("")
        
        return '\n'.join(lines)
    
    def _find_module(self, element_name: str, modules: Dict) -> str:
        """查找元素所属模块"""
        for module_name, module in modules.items():
            for element in module.get('elements', []):
                if hasattr(element, 'name') and element.name == element_name:
                    return module_name
        return '未知'


class HTMLGenerator:
    """HTML文档生成器"""
    
    def __init__(self, config: DocumentConfig):
        """
        初始化HTML生成器
        
        Args:
            config: 文档配置
        """
        self.config = config
        self.markdown_generator = MarkdownGenerator(config)
    
    def generate(self, analysis_result: Dict) -> str:
        """
        生成HTML文档
        
        Args:
            analysis_result: 源代码分析结果
            
        Returns:
            str: HTML文档内容
        """
        markdown_content = self.markdown_generator.generate(analysis_result)
        
        # 转换为HTML
        html_content = self._markdown_to_html(markdown_content)
        
        # 添加HTML框架
        html = f"""<!DOCTYPE html>
<html lang="{self.config.language}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.config.title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #1a1a1a;
            border-bottom: 3px solid #0066cc;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #2c5282;
            margin-top: 40px;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 8px;
        }}
        h3 {{
            color: #2d3748;
            margin-top: 24px;
        }}
        h4 {{
            color: #4a5568;
            margin-top: 18px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #e2e8f0;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #0066cc;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f7fafc;
        }}
        code {{
            background-color: #edf2f7;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.9em;
        }}
        pre {{
            background-color: #2d3748;
            color: #f7fafc;
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.9em;
        }}
        pre code {{
            background: none;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #0066cc;
            margin: 20px 0;
            padding: 10px 20px;
            background-color: #ebf8ff;
        }}
        ul, ol {{
            padding-left: 24px;
        }}
        li {{
            margin: 8px 0;
        }}
        .cover {{
            text-align: center;
            padding: 60px 0;
        }}
        .cover h1 {{
            border: none;
            font-size: 2.5em;
            margin-bottom: 20px;
        }}
        .cover .subtitle {{
            font-size: 1.5em;
            color: #666;
            margin-bottom: 40px;
        }}
        .cover .meta {{
            color: #888;
        }}
        .toc {{
            background-color: #f7fafc;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .toc ul {{
            list-style-type: none;
            padding-left: 0;
        }}
        .toc li {{
            margin: 8px 0;
        }}
        .toc a {{
            color: #0066cc;
            text-decoration: none;
        }}
        .toc a:hover {{
            text-decoration: underline;
        }}
        .mermaid {{
            text-align: center;
            margin: 20px 0;
        }}
        .warning {{
            background-color: #fffaf0;
            border-left: 4px solid #ed8936;
            padding: 12px 16px;
            margin: 16px 0;
        }}
        .success {{
            background-color: #f0fff4;
            border-left: 4px solid #48bb78;
            padding: 12px 16px;
            margin: 16px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
{self._indent_html(html_content, 4)}
    </div>
</body>
</html>
"""
        
        return html
    
    def _markdown_to_html(self, markdown: str) -> str:
        """Markdown转HTML"""
        lines = markdown.split('\n')
        html_lines = []
        in_code_block = False
        in_list = False
        list_type = None
        
        for line in lines:
            # 代码块
            if line.startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    html_lines.append('<pre><code>')
                else:
                    in_code_block = False
                    html_lines.append('</code></pre>')
                continue
            
            if in_code_block:
                # 转义HTML实体
                escaped = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                html_lines.append(escaped)
                continue
            
            # 标题
            if line.startswith('#'):
                match = re.match(r'^(#+)\s*(.*)', line)
                if match:
                    level = len(match.group(1))
                    text = match.group(2)
                    html_lines.append(f'<h{level} id="{self._slugify(text)}">{text}</h{level}>')
                    continue
            
            # 水平线
            if line.strip() == '---':
                html_lines.append('<hr>')
                continue
            
            # 列表
            if re.match(r'^[\s]*[-*+]\s', line):
                content = re.sub(r'^[\s]*[-*+]\s*', '', line)
                if not in_list or list_type != 'ul':
                    if in_list:
                        html_lines.append('</ul>')
                    in_list = True
                    list_type = 'ul'
                    html_lines.append('<ul>')
                html_lines.append(f'<li>{content}</li>')
                continue
            
            if re.match(r'^[\s]*\d+\.\s', line):
                content = re.sub(r'^[\s]*\d+\.\s*', '', line)
                if not in_list or list_type != 'ol':
                    if in_list:
                        html_lines.append('</ul>')
                    in_list = True
                    list_type = 'ol'
                    html_lines.append('<ol>')
                html_lines.append(f'<li>{content}</li>')
                continue
            
            # 表格
            if line.startswith('|'):
                if not in_list:
                    # 表格开始
                    html_lines.append('<table>')
                html_lines.append('<tr>')
                cells = line.strip('|').split('|')
                for cell in cells:
                    tag = 'th' if line.startswith('|') and not in_list else 'td'
                    html_lines.append(f'<{tag}>{cell.strip()}</{tag}>')
                html_lines.append('</tr>')
                in_list = False
                continue
            
            # 粗体和斜体
            processed = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line)
            processed = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', processed)
            processed = re.sub(r'`([^`]+)`', r'<code>\1</code>', processed)
            
            # 链接
            processed = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', processed)
            
            # 引用
            if line.startswith('>'):
                html_lines.append(f'<blockquote>{line[2:].strip()}</blockquote>')
                continue
            
            # 段落
            if line.strip():
                html_lines.append(f'<p>{processed}</p>')
            
            in_list = False
        
        # 关闭列表
        if in_list:
            html_lines.append('</ul>' if list_type == 'ul' else '</ol>')
        
        return '\n'.join(html_lines)
    
    def _indent_html(self, html: str, spaces: int) -> str:
        """缩进HTML内容"""
        indent = ' ' * spaces
        lines = html.split('\n')
        return '\n'.join(indent + line if line else '' for line in lines)
    
    def _slugify(self, text: str) -> str:
        """生成URL友好的slug"""
        return re.sub(r'[^\w\s-]', '', text.lower()).replace(' ', '-')


class DocumentationGenerator:
    """文档生成器主类"""
    
    def __init__(self, config: Optional[DocumentConfig] = None):
        """
        初始化文档生成器
        
        Args:
            config: 文档配置
        """
        self.config = config or DocumentConfig()
        self.generators = {
            OutputFormat.MARKDOWN: MarkdownGenerator(self.config),
            OutputFormat.HTML: HTMLGenerator(self.config),
        }
    
    def generate(self, analysis_result: Dict, output_format: str = 'markdown') -> str:
        """
        生成技术文档
        
        Args:
            analysis_result: 源代码分析结果
            output_format: 输出格式
            
        Returns:
            str: 生成的文档内容
        """
        format_enum = OutputFormat(output_format)
        generator = self.generators.get(format_enum)
        
        if not generator:
            raise ValueError(f"不支持的输出格式: {output_format}")
        
        return generator.generate(analysis_result)
    
    def generate_multi_format(self, analysis_result: Dict,
                              output_dir: str) -> Dict[str, str]:
        """
        生成多种格式的文档
        
        Args:
            analysis_result: 源代码分析结果
            output_dir: 输出目录
            
        Returns:
            Dict[str, str]: 生成的文档路径
        """
        os.makedirs(output_dir, exist_ok=True)
        outputs = {}
        
        # 生成Markdown
        md_content = self.generate(analysis_result, 'markdown')
        md_path = os.path.join(output_dir, '技术设计文档.md')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        outputs['markdown'] = md_path
        
        # 生成HTML
        html_content = self.generate(analysis_result, 'html')
        html_path = os.path.join(output_dir, '技术设计文档.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        outputs['html'] = html_path
        
        logger.info(f"文档已生成到 {output_dir}")
        logger.info(f"  - Markdown: {md_path}")
        logger.info(f"  - HTML: {html_path}")
        
        return outputs
    
    def save_document(self, content: str, output_path: str) -> None:
        """
        保存文档到文件
        
        Args:
            content: 文档内容
            output_path: 输出文件路径
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"文档已保存到: {output_path}")


def main():
    """
    主函数，命令行入口点
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description='技术文档生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 从分析结果生成Markdown文档
  python documentation_generator.py --input analysis.json --output docs/

  # 生成多种格式的文档
  python documentation_generator.py --input analysis.json --output docs/ --formats markdown,html

  # 指定文档标题和作者
  python documentation_generator.py --input analysis.json --output docs/ \\
      --title "项目技术文档" --author "开发团队" --version "2.0.0"
        """
    )
    
    parser.add_argument('--input', '-i', required=True, help='分析结果文件路径（JSON格式）')
    parser.add_argument('--output', '-o', required=True, help='输出目录路径')
    parser.add_argument('--formats', default='markdown,html',
                       help='输出格式，逗号分隔（默认: markdown,html）')
    parser.add_argument('--title', default='技术设计文档', help='文档标题')
    parser.add_argument('--subtitle', default='', help='文档副标题')
    parser.add_argument('--author', default='', help='作者')
    parser.add_argument('--version', default='1.0.0', help='版本号')
    parser.add_argument('--template', default='standard',
                       help='使用的模板')
    parser.add_argument('--no-toc', action='store_true', help='不生成目录')
    parser.add_argument('--no-index', action='store_true', help='不生成索引')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细输出')
    
    args = parser.parse_args()
    
    # 配置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 加载分析结果
    with open(args.input, 'r', encoding='utf-8') as f:
        analysis_result = json.load(f)
    
    # 创建配置
    config = DocumentConfig(
        title=args.title,
        subtitle=args.subtitle,
        author=args.author,
        version=args.version,
        include_toc=not args.no_toc,
        include_index=not args.no_index,
        template=args.template
    )
    
    # 创建文档生成器
    generator = DocumentationGenerator(config)
    
    # 生成文档
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)
    
    formats = [f.strip() for f in args.formats.split(',')]
    
    for fmt in formats:
        try:
            if fmt == 'markdown':
                content = generator.generate(analysis_result, 'markdown')
                output_path = os.path.join(output_dir, '技术设计文档.md')
                generator.save_document(content, output_path)
            elif fmt == 'html':
                content = generator.generate(analysis_result, 'html')
                output_path = os.path.join(output_dir, '技术设计文档.html')
                generator.save_document(content, output_path)
            else:
                logger.warning(f"不支持的格式: {fmt}")
        except Exception as e:
            logger.error(f"生成{fmt}文档失败: {e}")
    
    logger.info("文档生成完成！")


if __name__ == '__main__':
    main()
