#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
源代码解析器

该模块提供完整的源代码解析功能，支持多种编程语言的抽象语法树解析、
代码元素提取、模块识别和依赖分析。能够处理Python、JavaScript、Java、
C/C++、Go、Rust等主流编程语言的源代码。

联系：purpose168@outlook.com
"""

import os
import sys
import ast
import re
import json
import logging
import hashlib
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Set
from pathlib import Path
from enum import Enum
from collections import defaultdict
import concurrent.futures

# 配置日志记录器
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class Language(Enum):
    """支持的编程语言枚举"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CPP = "cpp"
    C = "c"
    CSHARP = "csharp"
    GO = "go"
    RUST = "rust"
    PHP = "php"
    RUBY = "ruby"
    SHELL = "shell"
    UNKNOWN = "unknown"


class ElementType(Enum):
    """代码元素类型枚举"""
    CLASS = "class"
    FUNCTION = "function"
    METHOD = "method"
    VARIABLE = "variable"
    CONSTANT = "constant"
    INTERFACE = "interface"
    ENUM = "enum"
    STRUCT = "struct"
    MODULE = "module"
    IMPORT = "import"
    ANNOTATION = "annotation"
    DECORATOR = "decorator"


@dataclass
class CodeElement:
    """代码元素数据类"""
    name: str                          # 元素名称
    element_type: ElementType          # 元素类型
    file_path: str                     # 文件路径
    line_number: int = 0               # 行号
    end_line_number: int = 0           # 结束行号
    content: str = ""                  # 原始内容
    docstring: Optional[str] = None    # 文档字符串
    parameters: List[Dict] = field(default_factory=list)  # 参数列表
    return_type: Optional[str] = None  # 返回类型
    parent: Optional[str] = None       # 父元素名称
    children: List[str] = field(default_factory=list)     # 子元素列表
    attributes: Dict[str, Any] = field(default_factory=dict)  # 其他属性
    visibility: str = "public"         # 可见性（public/protected/private）
    is_static: bool = False            # 是否为静态
    is_abstract: bool = False          # 是否为抽象
    decorators: List[str] = field(default_factory=list)   # 装饰器列表
    base_classes: List[str] = field(default_factory=list)  # 基类列表
    implements: List[str] = field(default_factory=list)   # 实现的接口
    complexity: int = 1                # 圈复杂度


@dataclass
class FileInfo:
    """文件信息数据类"""
    file_path: str                     # 文件路径
    language: Language                 # 编程语言
    relative_path: str = ""            # 相对路径
    size: int = 0                      # 文件大小（字节）
    lines_of_code: int = 0             # 代码行数
    content: Optional[str] = None      # 文件内容
    elements: List[CodeElement] = field(default_factory=list)  # 代码元素列表
    imports: List[Dict] = field(default_factory=list)  # 导入语句
    dependencies: List[str] = field(default_factory=list)  # 依赖列表
    metadata: Dict[str, Any] = field(default_factory=dict)  # 元数据


@dataclass
class ModuleInfo:
    """模块信息数据类"""
    name: str                          # 模块名称
    path: str                          # 模块路径
    file_count: int = 0                # 文件数量
    elements: List[CodeElement] = field(default_factory=list)  # 代码元素
    dependencies: List[str] = field(default_factory=list)  # 依赖列表
    depended_by: List[str] = field(default_factory=list)   # 被依赖列表
    responsibility: str = ""           # 模块职责
    core_features: List[str] = field(default_factory=list)  # 核心功能
    public_interfaces: List[Dict] = field(default_factory=list)  # 公共接口


class ProjectScanner:
    """项目扫描器，用于扫描项目结构和文件列表"""
    
    # 排除的目录列表
    EXCLUDE_DIRS = {
        '__pycache__', '.git', '.svn', '.hg',
        'node_modules', 'venv', '.venv', 'env',
        'build', 'dist', 'out', 'target',
        '.idea', '.vscode', '__tests__', 'test',
        'tests', '.pytest_cache', '.tox',
        'coverage', '.nyc_output', 'typings'
    }
    
    # 文件扩展名到语言的映射
    EXTENSION_MAP = {
        '.py': Language.PYTHON,
        '.pyi': Language.PYTHON,
        '.js': Language.JAVASCRIPT,
        '.jsx': Language.JAVASCRIPT,
        '.ts': Language.TYPESCRIPT,
        '.tsx': Language.TYPESCRIPT,
        '.java': Language.JAVA,
        '.c': Language.C,
        '.cpp': Language.CPP,
        '.cc': Language.CPP,
        '.cxx': Language.CPP,
        '.h': Language.C,
        '.hpp': Language.CPP,
        '.cs': Language.CSHARP,
        '.go': Language.GO,
        '.rs': Language.RUST,
        '.php': Language.PHP,
        '.rb': Language.RUBY,
        '.sh': Language.SHELL,
        '.bash': Language.SHELL
    }
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化项目扫描器
        
        Args:
            config: 配置字典，可包含排除规则等
        """
        self.config = config or {}
        self.exclude_dirs = self.EXCLUDE_DIRS.copy()
        self.exclude_patterns = set()
        self.include_patterns = set()
        
        # 应用配置
        if 'exclude_dirs' in self.config:
            self.exclude_dirs.update(self.config['exclude_dirs'])
        if 'exclude_patterns' in self.config:
            self.exclude_patterns.update(self.config['exclude_patterns'])
        if 'include_patterns' in self.config:
            self.include_patterns.update(self.config['include_patterns'])
    
    def scan(self, project_path: str) -> Dict[str, Any]:
        """
        扫描项目结构
        
        Args:
            project_path: 项目根目录路径
            
        Returns:
            Dict[str, Any]: 扫描结果，包含文件树、源文件列表等
        """
        result = {
            'file_tree': {},
            'source_files': [],
            'config_files': [],
            'test_files': [],
            'documentation_files': [],
            'entry_points': [],
            'statistics': {
                'total_files': 0,
                'total_dirs': 0,
                'total_size': 0
            }
        }
        
        project_path = os.path.abspath(project_path)
        
        for root, dirs, files in os.walk(project_path):
            # 过滤目录
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs]
            
            # 构建相对路径
            rel_path = os.path.relpath(root, project_path)
            if rel_path == '.':
                rel_path = ''
            
            # 处理文件
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                # 检查排除模式
                if self._match_exclude_pattern(file):
                    continue
                
                # 检查包含模式
                if self.include_patterns and not self._match_include_pattern(file):
                    continue
                
                # 获取文件信息
                file_info = self._get_file_info(file_path, project_path, rel_path)
                
                # 分类文件
                if file_ext in self.EXTENSION_MAP:
                    result['source_files'].append(file_info)
                elif file in ['package.json', 'pom.xml', 'build.gradle', 'go.mod']:
                    result['config_files'].append(file_info)
                elif file.startswith('test_') or file.endswith('_test.py') or file.endswith('.test.js'):
                    result['test_files'].append(file_info)
                elif file.endswith(('.md', '.txt', '.rst', '.doc')):
                    result['documentation_files'].append(file_info)
                
                result['statistics']['total_files'] += 1
                result['statistics']['total_size'] += file_info['size']
            
            result['statistics']['total_dirs'] += len(dirs)
        
        # 构建文件树
        result['file_tree'] = self._build_file_tree(result['source_files'])
        
        # 识别入口点
        result['entry_points'] = self._identify_entry_points(result['source_files'])
        
        logger.info(f"扫描完成：发现 {result['statistics']['total_files']} 个文件")
        
        return result
    
    def _match_exclude_pattern(self, file_name: str) -> bool:
        """检查文件是否匹配排除模式"""
        for pattern in self.exclude_patterns:
            if re.match(pattern, file_name):
                return True
        return False
    
    def _match_include_pattern(self, file_name: str) -> bool:
        """检查文件是否匹配包含模式"""
        for pattern in self.include_patterns:
            if re.match(pattern, file_name):
                return True
        return False
    
    def _get_file_info(self, file_path: str, project_path: str, rel_path: str) -> Dict[str, Any]:
        """
        获取文件信息
        
        Args:
            file_path: 文件完整路径
            project_path: 项目根路径
            rel_path: 相对路径
            
        Returns:
            Dict[str, Any]: 文件信息字典
        """
        file_ext = os.path.splitext(file_path)[1].lower()
        stat = os.stat(file_path)
        
        return {
            'path': file_path,
            'relative_path': os.path.join(rel_path, os.path.basename(file_path)) if rel_path else os.path.basename(file_path),
            'name': os.path.basename(file_path),
            'extension': file_ext,
            'language': self.EXTENSION_MAP.get(file_ext, Language.UNKNOWN).value,
            'size': stat.st_size,
            'mtime': stat.st_mtime
        }
    
    def _build_file_tree(self, source_files: List[Dict]) -> Dict[str, Any]:
        """
        构建文件树结构
        
        Args:
            source_files: 源文件列表
            
        Returns:
            Dict[str, Any]: 文件树结构
        """
        file_tree = {}
        
        for file_info in source_files:
            path_parts = file_info['relative_path'].split(os.sep)
            current = file_tree
            
            for part in path_parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            
            # 添加文件节点
            file_name = path_parts[-1]
            current[file_name] = {
                '_file_info': file_info
            }
        
        return file_tree
    
    def _identify_entry_points(self, source_files: List[Dict]) -> List[Dict]:
        """
        识别项目入口点
        
        Args:
            source_files: 源文件列表
            
        Returns:
            List[Dict]: 入口点列表
        """
        entry_points = []
        
        for file_info in source_files:
            file_name = file_info['name'].lower()
            
            # 检测常见的入口文件命名模式
            if file_name in ['main.py', 'app.py', 'index.js', 'main.js', 'App.tsx', 'main.ts']:
                entry_points.append({
                    'file': file_info['relative_path'],
                    'type': 'entry_point',
                    'confidence': 0.9
                })
            elif file_name == '__init__.py':
                entry_points.append({
                    'file': file_info['relative_path'],
                    'type': 'package_initializer',
                    'confidence': 0.7
                })
            elif file_name == 'server.js' or file_name == 'server.ts':
                entry_points.append({
                    'file': file_info['relative_path'],
                    'type': 'server_entry',
                    'confidence': 0.8
                })
        
        return entry_points


class ASTParser:
    """抽象语法树解析器，支持多种编程语言"""
    
    def __init__(self):
        """初始化AST解析器"""
        self.parsers = {}
        self._init_parsers()
    
    def _init_parsers(self):
        """初始化各语言解析器"""
        self.parsers = {
            Language.PYTHON: PythonASTParser(),
            Language.JAVASCRIPT: JavaScriptASTParser(),
            Language.TYPESCRIPT: TypeScriptASTParser(),
            Language.JAVA: JavaASTParser(),
            Language.CPP: CppASTParser(),
            Language.GO: GoASTParser(),
            Language.RUST: RustASTParser(),
        }
    
    def parse(self, file_path: str, content: str, language: Language) -> Optional[Dict]:
        """
        解析源代码为AST
        
        Args:
            file_path: 文件路径
            content: 文件内容
            language: 编程语言
            
        Returns:
            Optional[Dict]: 解析结果，包含各类元素列表
        """
        parser = self.parsers.get(language)
        if not parser:
            logger.warning(f"不支持的语言: {language.value}")
            return None
        
        try:
            result = parser.parse(content, file_path)
            
            # 添加文件元数据
            if result:
                lines = content.splitlines()
                result['metadata'] = {
                    'file_path': file_path,
                    'language': language.value,
                    'total_lines': len(lines),
                    'code_lines': self._count_code_lines(content),
                    'comment_lines': self._count_comment_lines(content, language),
                    'blank_lines': self._count_blank_lines(content)
                }
            
            return result
            
        except Exception as e:
            logger.error(f"解析失败 {file_path}: {e}")
            return None
    
    def _count_code_lines(self, content: str) -> int:
        """统计代码行数"""
        lines = content.splitlines()
        return sum(1 for line in lines if line.strip() and not self._is_comment_line(line))
    
    def _count_comment_lines(self, content: str, language: Language) -> int:
        """统计注释行数"""
        lines = content.splitlines()
        return sum(1 for line in lines if self._is_comment_line(line, language))
    
    def _count_blank_lines(self, content: str) -> int:
        """统计空行数"""
        lines = content.splitlines()
        return sum(1 for line in lines if not line.strip())
    
    def _is_comment_line(self, line: str, language: Language = Language.PYTHON) -> bool:
        """检查行是否为注释"""
        line = line.strip()
        
        if not line:
            return False
        
        comment_prefixes = {
            Language.PYTHON: ('#', '"""', "'''"),
            Language.JAVASCRIPT: ('//', '/*', '*'),
            Language.TYPESCRIPT: ('//', '/*', '*'),
            Language.JAVA: ('//', '/*', '*'),
            Language.CPP: ('//', '/*', '*'),
            Language.C: ('//', '/*', '*'),
            Language.GO: ('//', '/*'),
            Language.RUST: ('//', '/*', '///'),
            Language.PHP: ('//', '/*', '#'),
            Language.RUBY: ('#', '=begin'),
            Language.CSHARP: ('//', '/*', '///')
        }
        
        prefixes = comment_prefixes.get(language, ('#',))
        
        for prefix in prefixes:
            if line.startswith(prefix):
                return True
        
        return False


class PythonASTParser:
    """Python语言AST解析器"""
    
    def parse(self, content: str, file_path: str) -> Dict[str, Any]:
        """
        解析Python源代码
        
        Args:
            content: 文件内容
            file_path: 文件路径
            
        Returns:
            Dict[str, Any]: 解析结果
        """
        result = {
            'classes': [],
            'functions': [],
            'variables': [],
            'constants': [],
            'imports': [],
            'decorators': [],
            'comments': []
        }
        
        try:
            tree = ast.parse(content)
            
            # 提取导入语句
            self._extract_imports(tree, result)
            
            # 提取类定义
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_info = self._extract_class(node, file_path)
                    result['classes'].append(class_info)
            
            # 提取函数定义
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if not self._is_method(node):
                        func_info = self._extract_function(node, file_path)
                        result['functions'].append(func_info)
            
            # 提取变量和常量
            self._extract_variables(tree, result)
            
            # 提取注释
            result['comments'] = self._extract_comments(content)
            
        except SyntaxError as e:
            logger.error(f"Python语法错误 {file_path}: {e}")
        
        return result
    
    def _extract_imports(self, tree, result):
        """提取导入语句"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    result['imports'].append({
                        'type': 'import',
                        'module': alias.name,
                        'alias': alias.asname,
                        'line': node.lineno
                    })
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    result['imports'].append({
                        'type': 'from_import',
                        'module': module,
                        'name': alias.name,
                        'alias': alias.asname,
                        'line': node.lineno
                    })
    
    def _extract_class(self, node: ast.ClassDef, file_path: str) -> Dict[str, Any]:
        """提取类定义信息"""
        methods = []
        attributes = []
        decorators = []
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_info = self._extract_method(item, file_path)
                methods.append(method_info)
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        attributes.append({
                            'name': target.id,
                            'line': item.lineno
                        })
            elif isinstance(item, ast.AnnAssign):
                if isinstance(target := item.target, ast.Name):
                    attributes.append({
                        'name': target.id,
                        'annotation': self._get_type_string(item.annotation),
                        'line': item.lineno
                    })
        
        # 提取装饰器
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name):
                decorators.append(decorator.id)
            elif isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name):
                decorators.append(decorator.func.id)
        
        return {
            'name': node.name,
            'line_number': node.lineno,
            'end_line_number': node.end_lineno,
            'docstring': ast.get_docstring(node),
            'base_classes': [self._get_base_class_name(base) for base in node.bases],
            'methods': methods,
            'attributes': attributes,
            'decorators': decorators,
            'file_path': file_path
        }
    
    def _extract_function(self, node: ast.FunctionDef, file_path: str) -> Dict[str, Any]:
        """提取函数定义信息"""
        return {
            'name': node.name,
            'line_number': node.lineno,
            'end_line_number': node.end_lineno,
            'docstring': ast.get_docstring(node),
            'parameters': self._extract_parameters(node.args),
            'return_type': self._get_type_string(node.returns) if node.returns else None,
            'decorators': self._extract_decorators(node.decorator_list),
            'complexity': self._calculate_complexity(node),
            'file_path': file_path,
            'is_async': isinstance(node, ast.AsyncFunctionDef)
        }
    
    def _extract_method(self, node: ast.FunctionDef, file_path: str) -> Dict[str, Any]:
        """提取方法定义信息"""
        func_info = self._extract_function(node, file_path)
        
        # 判断可见性
        if node.name.startswith('__') and node.name.endswith('__'):
            func_info['visibility'] = 'special'
        elif node.name.startswith('_'):
            func_info['visibility'] = 'private'
        else:
            func_info['visibility'] = 'public'
        
        return func_info
    
    def _extract_parameters(self, args: ast.arguments) -> List[Dict]:
        """提取函数参数列表"""
        parameters = []
        
        for arg in args.args:
            param_info = {
                'name': arg.arg,
                'type': self._get_type_string(arg.annotation) if arg.annotation else None,
                'default': self._get_default_value(args.defaults, args.args.index(arg)) if args.defaults else None
            }
            parameters.append(param_info)
        
        return parameters
    
    def _extract_variables(self, tree, result):
        """提取变量和常量定义"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        # 检查是否为常量（大写命名）
                        if target.id.isupper() and len(target.id) > 1:
                            result['constants'].append({
                                'name': target.id,
                                'value': self._get_value(node.value),
                                'line': node.lineno
                            })
                        else:
                            result['variables'].append({
                                'name': target.id,
                                'value': self._get_value(node.value),
                                'line': node.lineno
                            })
    
    def _extract_decorators(self, decorator_list: List) -> List[str]:
        """提取装饰器列表"""
        decorators = []
        for decorator in decorator_list:
            if isinstance(decorator, ast.Name):
                decorators.append(decorator.id)
            elif isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name):
                decorators.append(f"{decorator.func.id}()")
        return decorators
    
    def _extract_comments(self, content: str) -> List[Dict]:
        """提取注释"""
        comments = []
        lines = content.splitlines()
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('#'):
                comments.append({
                    'line': i,
                    'content': stripped[1:].strip()
                })
        
        return comments
    
    def _get_base_class_name(self, base) -> str:
        """获取基类名称"""
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Attribute):
            return self._get_attribute_name(base)
        return ''
    
    def _get_type_string(self, annotation) -> Optional[str]:
        """获取类型注解字符串"""
        if annotation is None:
            return None
        
        if isinstance(annotation, ast.Name):
            return annotation.id
        elif isinstance(annotation, ast.Attribute):
            return self._get_attribute_name(annotation)
        elif isinstance(annotation, ast.Subscript):
            return f"{self._get_type_string(annotation.value)}[{self._get_type_string(annotation.slice)}]"
        elif isinstance(annotation, ast.Constant):
            return str(annotation.value)
        elif isinstance(annotation, ast.BinOp):
            return f"Union[{self._get_type_string(annotation.left)}, {self._get_type_string(annotation.right)}]"
        
        return None
    
    def _get_attribute_name(self, node: ast.Attribute) -> str:
        """获取属性访问链名称"""
        parts = []
        current = node
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
        return '.'.join(reversed(parts))
    
    def _get_value(self, node) -> Any:
        """获取节点的值"""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Name):
            return f"'{node.id}'"
        elif isinstance(node, ast.Dict):
            return {}
        elif isinstance(node, ast.List):
            return []
        elif isinstance(node, ast.Tuple):
            return ()
        return None
    
    def _get_default_value(self, defaults: List, param_index: int) -> Any:
        """获取参数默认值"""
        if not defaults:
            return None
        
        # defaults列表只包含有默认值的参数
        # 位置从后往前计算
        num_with_default = len(defaults)
        num_params = len(defaults) + sum(1 for arg in defaults if arg is not None)
        
        return None
    
    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """计算圈复杂度"""
        complexity = 1
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Assert,
                                 ast.With, ast.Try, ast.ExceptHandler)):
                complexity += 1
        
        return complexity
    
    def _is_method(self, node: ast.FunctionDef) -> bool:
        """检查函数是否在类内部"""
        # Python AST中，方法会在ClassDef的body中
        # 但这里使用ast.walk，所以需要通过检查父节点来判断
        # 简化处理：如果函数名以下划线开头，认为是内部方法
        return False


class JavaScriptASTParser:
    """JavaScript语言AST解析器"""
    
    def parse(self, content: str, file_path: str) -> Dict[str, Any]:
        """
        解析JavaScript源代码
        
        Args:
            content: 文件内容
            file_path: 文件路径
            
        Returns:
            Dict[str, Any]: 解析结果
        """
        # 由于JavaScript没有标准AST库，这里使用简化解析
        result = {
            'classes': [],
            'functions': [],
            'variables': [],
            'constants': [],
            'imports': [],
            'comments': []
        }
        
        # 提取注释
        result['comments'] = self._extract_comments(content)
        
        # 提取导入语句
        result['imports'] = self._extract_imports(content)
        
        # 提取函数
        result['functions'] = self._extract_functions(content, file_path)
        
        # 提取类
        result['classes'] = self._extract_classes(content, file_path)
        
        # 提取变量
        result['variables'] = self._extract_variables(content)
        
        return result
    
    def _extract_comments(self, content: str) -> List[Dict]:
        """提取注释"""
        comments = []
        lines = content.splitlines()
        
        in_multiline = False
        current_multiline = []
        
        for i, line in enumerate(lines, 1):
            # 单行注释
            if '//' in line and not in_multiline:
                comment_text = line.split('//')[1].strip()
                if comment_text:
                    comments.append({
                        'line': i,
                        'type': 'single',
                        'content': comment_text
                    })
            
            # 多行注释开始
            if '/*' in line:
                in_multiline = True
                start = line.find('/*') + 2
                current_multiline = [line[start:].strip()]
            
            # 多行注释内容
            if in_multiline:
                if '*/' in line:
                    end = line.find('*/')
                    current_multiline.append(line[:end].strip())
                    comments.append({
                        'line': i,
                        'type': 'multi',
                        'content': ' '.join(current_multiline)
                    })
                    in_multiline = False
                    current_multiline = []
                else:
                    current_multiline.append(line.strip())
        
        return comments
    
    def _extract_imports(self, content: str) -> List[Dict]:
        """提取导入语句"""
        imports = []
        
        # ES6 import
        import_pattern = r'import\s+(?:\{[^}]+\}|\* as \w+|\w+)\s+from\s+[\'"]([^\'"]+)[\'"]'
        for match in re.finditer(import_pattern, content):
            imports.append({
                'type': 'import',
                'module': match.group(1),
                'line': content[:match.start()].count('\n') + 1
            })
        
        # require语句
        require_pattern = r'require\([\'"]([^\'"]+)[\'"]\)'
        for match in re.finditer(require_pattern, content):
            imports.append({
                'type': 'require',
                'module': match.group(1),
                'line': content[:match.start()].count('\n') + 1
            })
        
        return imports
    
    def _extract_functions(self, content: str, file_path: str) -> List[Dict]:
        """提取函数定义"""
        functions = []
        
        # 函数声明
        func_pattern = r'function\s+(\w+)\s*\(([^)]*)\)'
        for match in re.finditer(func_pattern, content):
            func_name = match.group(1)
            params = self._parse_params(match.group(2))
            line = content[:match.start()].count('\n') + 1
            
            functions.append({
                'name': func_name,
                'line_number': line,
                'parameters': params,
                'type': 'function_declaration',
                'file_path': file_path
            })
        
        # 箭头函数
        arrow_pattern = r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\(([^)]*)\)\s*=>'
        for match in re.finditer(arrow_pattern, content):
            func_name = match.group(1)
            params = self._parse_params(match.group(2))
            line = content[:match.start()].count('\n') + 1
            
            functions.append({
                'name': func_name,
                'line_number': line,
                'parameters': params,
                'type': 'arrow_function',
                'file_path': file_path
            })
        
        return functions
    
    def _extract_classes(self, content: str, file_path: str) -> List[Dict]:
        """提取类定义"""
        classes = []
        
        class_pattern = r'class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([^{]+))?\{'
        for match in re.finditer(class_pattern, content):
            class_info = {
                'name': match.group(1),
                'line_number': content[:match.start()].count('\n') + 1,
                'base_classes': [match.group(2)] if match.group(2) else [],
                'implements': [c.strip() for c in match.group(3).split(',')] if match.group(3) else [],
                'methods': [],
                'file_path': file_path
            }
            classes.append(class_info)
        
        return classes
    
    def _extract_variables(self, content: str) -> List[Dict]:
        """提取变量定义"""
        variables = []
        
        # const/let/var声明
        var_pattern = r'(?:const|let|var)\s+(\w+)(?:\s*=\s*([^;]+))?'
        for match in re.finditer(var_pattern, content):
            var_name = match.group(1)
            # 排除函数名
            if not var_name in ['function', 'class', 'if', 'for', 'while', 'switch']:
                variables.append({
                    'name': var_name,
                    'value': match.group(2).strip() if match.group(2) else None,
                    'line': content[:match.start()].count('\n') + 1
                })
        
        return variables
    
    def _parse_params(self, params_str: str) -> List[Dict]:
        """解析参数列表"""
        params = []
        if params_str.strip():
            for param in params_str.split(','):
                param = param.strip()
                if param:
                    parts = param.split('=')
                    params.append({
                        'name': parts[0].strip(),
                        'default': parts[1].strip() if len(parts) > 1 else None
                    })
        return params


class TypeScriptASTParser:
    """TypeScript语言AST解析器"""
    
    def __init__(self):
        """初始化TypeScript解析器"""
        self.js_parser = JavaScriptASTParser()
    
    def parse(self, content: str, file_path: str) -> Dict[str, Any]:
        """
        解析TypeScript源代码
        
        Args:
            content: 文件内容
            file_path: 文件路径
            
        Returns:
            Dict[str, Any]: 解析结果
        """
        result = self.js_parser.parse(content, file_path)
        
        # 提取TypeScript特有结构
        result['interfaces'] = self._extract_interfaces(content, file_path)
        result['type_aliases'] = self._extract_type_aliases(content, file_path)
        result['generics'] = self._extract_generics(content)
        
        return result
    
    def _extract_interfaces(self, content: str, file_path: str) -> List[Dict]:
        """提取接口定义"""
        interfaces = []
        
        interface_pattern = r'interface\s+(\w+)(?:<[^>]+>)?\s*\{([^}]+)\}'
        for match in re.finditer(interface_pattern, content):
            interface_info = {
                'name': match.group(1),
                'line_number': content[:match.start()].count('\n') + 1,
                'properties': self._parse_interface_body(match.group(2)),
                'file_path': file_path
            }
            interfaces.append(interface_info)
        
        return interfaces
    
    def _extract_type_aliases(self, content: str, file_path: str) -> List[Dict]:
        """提取类型别名"""
        type_aliases = []
        
        type_pattern = r'type\s+(\w+)\s*=\s*([^{;]+)'
        for match in re.finditer(type_pattern, content):
            type_aliases.append({
                'name': match.group(1),
                'definition': match.group(2).strip(),
                'line_number': content[:match.start()].count('\n') + 1,
                'file_path': file_path
            })
        
        return type_aliases
    
    def _extract_generics(self, content: str) -> List[Dict]:
        """提取泛型定义"""
        generics = []
        
        generic_pattern = r'(?:class|interface|type|function)\s+(\w+)\s*<([^>]+)>'
        for match in re.finditer(generic_pattern, content):
            generics.append({
                'name': match.group(1),
                'type_params': [p.strip() for p in match.group(2).split(',')]
            })
        
        return generics
    
    def _parse_interface_body(self, body: str) -> List[Dict]:
        """解析接口体"""
        properties = []
        
        prop_pattern = r'(\w+)(\??)\s*:\s*([^;]+)'
        for match in re.finditer(prop_pattern, body):
            properties.append({
                'name': match.group(1),
                'optional': bool(match.group(2)),
                'type': match.group(3).strip()
            })
        
        return properties


class JavaASTParser:
    """Java语言AST解析器"""
    
    def parse(self, content: str, file_path: str) -> Dict[str, Any]:
        """
        解析Java源代码
        
        Args:
            content: 文件内容
            file_path: 文件路径
            
        Returns:
            Dict[str, Any]: 解析结果
        """
        result = {
            'classes': [],
            'interfaces': [],
            'enums': [],
            'methods': [],
            'fields': [],
            'imports': [],
            'annotations': [],
            'comments': []
        }
        
        # 提取注释
        result['comments'] = self._extract_comments(content)
        
        # 提取导入语句
        result['imports'] = self._extract_imports(content)
        
        # 提取类
        result['classes'] = self._extract_classes(content, file_path)
        
        # 提取接口
        result['interfaces'] = self._extract_interfaces(content, file_path)
        
        # 提取枚举
        result['enums'] = self._extract_enums(content, file_path)
        
        # 提取字段
        result['fields'] = self._extract_fields(content)
        
        return result
    
    def _extract_comments(self, content: str) -> List[Dict]:
        """提取注释"""
        comments = []
        lines = content.splitlines()
        
        in_javadoc = False
        current_javadoc = []
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if stripped.startswith('/**') and '*' in stripped[3:]:
                in_javadoc = True
                start = stripped.find('*') + 1
                current_javadoc = [line[start:].strip()]
            elif in_javadoc:
                if stripped.startswith('*/'):
                    comments.append({
                        'line': i,
                        'type': 'javadoc',
                        'content': '\n'.join(current_javadoc)
                    })
                    in_javadoc = False
                    current_javadoc = []
                elif stripped.startswith('*'):
                    current_javadoc.append(stripped[1:].strip())
            elif stripped.startswith('//'):
                if stripped.startswith('///'):
                    comments.append({
                        'line': i,
                        'type': 'doc_comment',
                        'content': stripped[3:].strip()
                    })
                else:
                    comments.append({
                        'line': i,
                        'type': 'single',
                        'content': stripped[2:].strip()
                    })
        
        return comments
    
    def _extract_imports(self, content: str) -> List[Dict]:
        """提取导入语句"""
        imports = []
        
        import_pattern = r'import\s+([\w.]+(?:\.\*)?)\s*;'
        for match in re.finditer(import_pattern, content):
            imports.append({
                'type': 'import',
                'module': match.group(1),
                'line': content[:match.start()].count('\n') + 1
            })
        
        return imports
    
    def _extract_classes(self, content: str, file_path: str) -> List[Dict]:
        """提取类定义"""
        classes = []
        
        class_pattern = r'(?:public\s+)?(?:abstract\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([^{]+))?\{'
        for match in re.finditer(class_pattern, content):
            classes.append({
                'name': match.group(1),
                'line_number': content[:match.start()].count('\n') + 1,
                'base_class': match.group(2),
                'interfaces': [i.strip() for i in match.group(3).split(',')] if match.group(3) else [],
                'methods': [],
                'fields': [],
                'file_path': file_path
            })
        
        return classes
    
    def _extract_interfaces(self, content: str, file_path: str) -> List[Dict]:
        """提取接口定义"""
        interfaces = []
        
        interface_pattern = r'(?:public\s+)?interface\s+(\w+)(?:\s+extends\s+([^{]+))?\{'
        for match in re.finditer(interface_pattern, content):
            interfaces.append({
                'name': match.group(1),
                'line_number': content[:match.start()].count('\n') + 1,
                'extends': [e.strip() for e in match.group(2).split(',')] if match.group(2) else [],
                'methods': [],
                'file_path': file_path
            })
        
        return interfaces
    
    def _extract_enums(self, content: str, file_path: str) -> List[Dict]:
        """提取枚举定义"""
        enums = []
        
        enum_pattern = r'(?:public\s+)?enum\s+(\w+)(?:\s+implements\s+([^{]+))?\{'
        for match in re.finditer(enum_pattern, content):
            enums.append({
                'name': match.group(1),
                'line_number': content[:match.start()].count('\n') + 1,
                'interfaces': [i.strip() for i in match.group(2).split(',')] if match.group(2) else [],
                'values': self._extract_enum_values(match.group(0)),
                'file_path': file_path
            })
        
        return enums
    
    def _extract_enum_values(self, enum_body: str) -> List[str]:
        """提取枚举值"""
        values = []
        value_pattern = r'(\w+)(?:\([^)]*\))?(?:,|\s*\}'
        for match in re.finditer(value_pattern, enum_body):
            val = match.group(1)
            if val not in ['enum', '{', '}']:
                values.append(val)
        return values
    
    def _extract_fields(self, content: str) -> List[Dict]:
        """提取字段定义"""
        fields = []
        
        field_pattern = r'(?:public|private|protected)(?:\s+(?:static|final|transient|volatile))*\s+([\w.<>]+)\s+(\w+)(?:\s*=\s*([^;]+))?\s*;'
        for match in re.finditer(field_pattern, content):
            fields.append({
                'type': match.group(1),
                'name': match.group(2),
                'default': match.group(3).strip() if match.group(3) else None,
                'line': content[:match.start()].count('\n') + 1
            })
        
        return fields


class CppASTParser:
    """C++语言AST解析器"""
    
    def parse(self, content: str, file_path: str) -> Dict[str, Any]:
        """
        解析C++源代码
        
        Args:
            content: 文件内容
            file_path: 文件路径
            
        Returns:
            Dict[str, Any]: 解析结果
        """
        result = {
            'classes': [],
            'structs': [],
            'functions': [],
            'namespaces': [],
            'templates': [],
            'includes': [],
            'comments': []
        }
        
        # 提取注释
        result['comments'] = self._extract_comments(content)
        
        # 提取头文件包含
        result['includes'] = self._extract_includes(content)
        
        # 提取命名空间
        result['namespaces'] = self._extract_namespaces(content, file_path)
        
        # 提取类
        result['classes'] = self._extract_classes(content, file_path)
        
        # 提取结构体
        result['structs'] = self._extract_structs(content, file_path)
        
        # 提取函数
        result['functions'] = self._extract_functions(content, file_path)
        
        # 提取模板
        result['templates'] = self._extract_templates(content)
        
        return result
    
    def _extract_comments(self, content: str) -> List[Dict]:
        """提取注释"""
        comments = []
        lines = content.splitlines()
        
        in_multiline = False
        current_comment = []
        start_line = 0
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if stripped.startswith('//'):
                if stripped.startswith('///'):
                    comments.append({
                        'line': i,
                        'type': 'doc_comment',
                        'content': stripped[3:].strip()
                    })
                else:
                    comments.append({
                        'line': i,
                        'type': 'single',
                        'content': stripped[2:].strip()
                    })
            
            if '/*' in stripped:
                in_multiline = True
                start_line = i
                start = stripped.find('/*') + 2
                current_comment = [stripped[start:].strip()]
            
            if in_multiline:
                if '*/' in stripped:
                    end = stripped.find('*/')
                    current_comment.append(stripped[:end].strip())
                    comments.append({
                        'line': start_line,
                        'type': 'multi',
                        'content': ' '.join(current_comment)
                    })
                    in_multiline = False
                    current_comment = []
                else:
                    current_comment.append(stripped)
        
        return comments
    
    def _extract_includes(self, content: str) -> List[Dict]:
        """提取头文件包含"""
        includes = []
        
        include_pattern = r'#include\s+[<"]([^>"]+)[">]'
        for match in re.finditer(include_pattern, content):
            is_system = match.group(1).startswith('<')
            includes.append({
                'header': match.group(1),
                'type': 'system' if is_system else 'local',
                'line': content[:match.start()].count('\n') + 1
            })
        
        return includes
    
    def _extract_namespaces(self, content: str, file_path: str) -> List[Dict]:
        """提取命名空间"""
        namespaces = []
        
        ns_pattern = r'namespace\s+(\w+)\s*\{'
        for match in re.finditer(ns_pattern, content):
            namespaces.append({
                'name': match.group(1),
                'line_number': content[:match.start()].count('\n') + 1,
                'file_path': file_path
            })
        
        return namespaces
    
    def _extract_classes(self, content: str, file_path: str) -> List[Dict]:
        """提取类定义"""
        classes = []
        
        class_pattern = r'(?:public\s+)?(?:abstract\s+)?class\s+(\w+)(?:\s+:\s*([^{]+))?\{'
        for match in re.finditer(class_pattern, content):
            classes.append({
                'name': match.group(1),
                'line_number': content[:match.start()].count('\n') + 1,
                'base_classes': [b.strip() for b in match.group(2).split(',')] if match.group(2) else [],
                'methods': [],
                'file_path': file_path
            })
        
        return classes
    
    def _extract_structs(self, content: str, file_path: str) -> List[Dict]:
        """提取结构体定义"""
        structs = []
        
        struct_pattern = r'struct\s+(\w+)(?:\s*:\s*([^{]+))?\{'
        for match in re.finditer(struct_pattern, content):
            structs.append({
                'name': match.group(1),
                'line_number': content[:match.start()].count('\n') + 1,
                'base_classes': [b.strip() for b in match.group(2).split(',')] if match.group(2) else [],
                'file_path': file_path
            })
        
        return structs
    
    def _extract_functions(self, content: str, file_path: str) -> List[Dict]:
        """提取函数定义"""
        functions = []
        
        # 普通函数声明
        func_pattern = r'(?:void|int|bool|double|float|char|auto|auto|template\s+<[^>]+>\s+)?(\w+)\s*\(([^)]*)\)\s*(?:const)?\s*\{'
        for match in re.finditer(func_pattern, content):
            func_name = match.group(1)
            # 排除类名和结构体名
            if not func_name in ['if', 'while', 'for', 'switch', 'class', 'struct']:
                functions.append({
                    'name': func_name,
                    'line_number': content[:match.start()].count('\n') + 1,
                    'parameters': self._parse_cpp_params(match.group(2)),
                    'file_path': file_path
                })
        
        return functions
    
    def _extract_templates(self, content: str) -> List[Dict]:
        """提取模板定义"""
        templates = []
        
        template_pattern = r'template\s*<([^>]+)>\s*(?:class|struct|function)\s+(\w+)'
        for match in re.finditer(template_pattern, content):
            templates.append({
                'parameters': [p.strip() for p in match.group(1).split(',')],
                'name': match.group(2)
            })
        
        return templates
    
    def _parse_cpp_params(self, params_str: str) -> List[Dict]:
        """解析C++参数列表"""
        params = []
        if params_str.strip():
            for param in params_str.split(','):
                param = param.strip()
                parts = param.split()
                if len(parts) >= 2:
                    params.append({
                        'type': ' '.join(parts[:-1]),
                        'name': parts[-1]
                    })
                elif len(parts) == 1:
                    params.append({
                        'type': parts[0],
                        'name': None
                    })
        return params


class GoASTParser:
    """Go语言AST解析器"""
    
    def parse(self, content: str, file_path: str) -> Dict[str, Any]:
        """
        解析Go源代码
        
        Args:
            content: 文件内容
            file_path: 文件路径
            
        Returns:
            Dict[str, Any]: 解析结果
        """
        result = {
            'packages': [],
            'functions': [],
            'methods': [],
            'structs': [],
            'interfaces': [],
            'imports': [],
            'variables': [],
            'constants': [],
            'comments': []
        }
        
        # 提取包声明
        package_match = re.search(r'^package\s+(\w+)', content, re.MULTILINE)
        if package_match:
            result['packages'].append({
                'name': package_match.group(1),
                'line': 1
            })
        
        # 提取注释
        result['comments'] = self._extract_comments(content)
        
        # 提取导入
        result['imports'] = self._extract_imports(content)
        
        # 提取结构体
        result['structs'] = self._extract_structs(content, file_path)
        
        # 提取接口
        result['interfaces'] = self._extract_interfaces(content, file_path)
        
        # 提取函数
        result['functions'] = self._extract_functions(content, file_path)
        
        # 提取变量和常量
        result['variables'] = self._extract_variables(content)
        result['constants'] = self._extract_constants(content)
        
        return result
    
    def _extract_comments(self, content: str) -> List[Dict]:
        """提取注释"""
        comments = []
        lines = content.splitlines()
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('//'):
                is_doc = stripped.startswith('///')
                comments.append({
                    'line': i,
                    'type': 'doc' if is_doc else 'comment',
                    'content': stripped[2:].strip() if not is_doc else stripped[3:].strip()
                })
        
        return comments
    
    def _extract_imports(self, content: str) -> List[Dict]:
        """提取导入语句"""
        imports = []
        
        # 单行导入
        import_pattern = r'import\s+"([^"]+)"'
        for match in re.finditer(import_pattern, content):
            imports.append({
                'path': match.group(1),
                'line': content[:match.start()].count('\n') + 1
            })
        
        # 导入块
        import_block_pattern = r'import\s*\(\s*([\s\S]*?)\s*\)'
        for match in re.finditer(import_block_pattern, content):
            block = match.group(1)
            for line in block.split('\n'):
                line = line.strip()
                if line.startswith('"') and line.endswith('"'):
                    path = line[1:-1]
                    imports.append({
                        'path': path,
                        'line': content[:match.start()].count('\n') + 1
                    })
        
        return imports
    
    def _extract_structs(self, content: str, file_path: str) -> List[Dict]:
        """提取结构体定义"""
        structs = []
        
        struct_pattern = r'type\s+(\w+)\s+struct\s*\{([^}]+)\}'
        for match in re.finditer(struct_pattern, content):
            fields = []
            for line in match.group(2).split('\n'):
                line = line.strip()
                if line:
                    parts = line.split()
                    if len(parts) >= 2:
                        fields.append({
                            'type': parts[0],
                            'name': parts[1] if len(parts) > 1 else None
                        })
            
            structs.append({
                'name': match.group(1),
                'line_number': content[:match.start()].count('\n') + 1,
                'fields': fields,
                'file_path': file_path
            })
        
        return structs
    
    def _extract_interfaces(self, content: str, file_path: str) -> List[Dict]:
        """提取接口定义"""
        interfaces = []
        
        interface_pattern = r'type\s+(\w+)\s+interface\s*\{([^}]+)\}'
        for match in re.finditer(interface_pattern, content):
            methods = []
            for line in match.group(2).split('\n'):
                line = line.strip()
                if line:
                    methods.append(line)
            
            interfaces.append({
                'name': match.group(1),
                'line_number': content[:match.start()].count('\n') + 1,
                'methods': methods,
                'file_path': file_path
            })
        
        return interfaces
    
    def _extract_functions(self, content: str, file_path: str) -> List[Dict]:
        """提取函数定义"""
        functions = []
        
        func_pattern = r'func\s+(?:\([^)]+\)\s*)?(\w+)\s*\(([^)]*)\)(?:\s*\((\([^)]+\))\s*)?'
        for match in re.finditer(func_pattern, content):
            func_name = match.group(1)
            params = self._parse_go_params(match.group(2))
            return_type = match.group(3)
            
            functions.append({
                'name': func_name,
                'line_number': content[:match.start()].count('\n') + 1,
                'parameters': params,
                'return_type': return_type.strip() if return_type else None,
                'file_path': file_path
            })
        
        return functions
    
    def _parse_go_params(self, params_str: str) -> List[Dict]:
        """解析Go参数列表"""
        params = []
        if params_str.strip():
            for param in params_str.split(','):
                param = param.strip()
                parts = param.split()
                if len(parts) >= 2:
                    params.append({
                        'name': parts[0],
                        'type': ' '.join(parts[1:])
                    })
                elif len(parts) == 1:
                    params.append({
                        'name': None,
                        'type': parts[0]
                    })
        return params
    
    def _extract_variables(self, content: str) -> List[Dict]:
        """提取变量定义"""
        variables = []
        
        var_pattern = r'var\s+(\w+)\s+(?:\[)?(?:[^\s=]+)(?:\])?\s*=\s*([^{;]+)'
        for match in re.finditer(var_pattern, content):
            variables.append({
                'name': match.group(1),
                'value': match.group(2).strip(),
                'line': content[:match.start()].count('\n') + 1
            })
        
        return variables
    
    def _extract_constants(self, content: str) -> List[Dict]:
        """提取常量定义"""
        constants = []
        
        const_pattern = r'const\s+(\w+)\s*=\s*([^{;]+)'
        for match in re.finditer(const_pattern, content):
            constants.append({
                'name': match.group(1),
                'value': match.group(2).strip(),
                'line': content[:match.start()].count('\n') + 1
            })
        
        return constants


class RustASTParser:
    """Rust语言AST解析器"""
    
    def parse(self, content: str, file_path: str) -> Dict[str, Any]:
        """
        解析Rust源代码
        
        Args:
            content: 文件内容
            file_path: 文件路径
            
        Returns:
            Dict[str, Any]: 解析结果
        """
        result = {
            'crates': [],
            'modules': [],
            'structs': [],
            'enums': [],
            'traits': [],
            'functions': [],
            'impls': [],
            'use_declarations': [],
            'comments': []
        }
        
        # 提取crate声明
        crate_match = re.search(r'^mod\s+(\w+)', content, re.MULTILINE)
        if crate_match:
            result['crates'].append({
                'name': crate_match.group(1),
                'line': 1
            })
        
        # 提取注释
        result['comments'] = self._extract_comments(content)
        
        # 提取use声明
        result['use_declarations'] = self._extract_use_declarations(content)
        
        # 提取结构体
        result['structs'] = self._extract_structs(content, file_path)
        
        # 提取枚举
        result['enums'] = self._extract_enums(content, file_path)
        
        # 提取trait
        result['traits'] = self._extract_traits(content, file_path)
        
        # 提取函数
        result['functions'] = self._extract_functions(content, file_path)
        
        # 提取impl块
        result['impls'] = self._extract_impls(content, file_path)
        
        return result
    
    def _extract_comments(self, content: str) -> List[Dict]:
        """提取注释"""
        comments = []
        lines = content.splitlines()
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if stripped.startswith('//'):
                if stripped.startswith('///'):
                    comments.append({
                        'line': i,
                        'type': 'doc_comment',
                        'content': stripped[3:].strip()
                    })
                elif stripped.startswith('//!') or stripped.startswith('/*!'):
                    comments.append({
                        'line': i,
                        'type': 'inner_doc',
                        'content': stripped[3:].strip()
                    })
                else:
                    comments.append({
                        'line': i,
                        'type': 'comment',
                        'content': stripped[2:].strip()
                    })
            
            if stripped.startswith('/*') and '*/' in stripped:
                if stripped.startswith('/**') or stripped.startswith('/*!'):
                    start = stripped.find('*') + 1
                    end = stripped.rfind('*/')
                    comments.append({
                        'line': i,
                        'type': 'doc_comment',
                        'content': stripped[start:end].strip()
                    })
        
        return comments
    
    def _extract_use_declarations(self, content: str) -> List[Dict]:
        """提取use声明"""
        use_decls = []
        
        use_pattern = r'use\s+([^;]+);'
        for match in re.finditer(use_pattern, content):
            use_decls.append({
                'path': match.group(1).strip(),
                'line': content[:match.start()].count('\n') + 1
            })
        
        return use_decls
    
    def _extract_structs(self, content: str, file_path: str) -> List[Dict]:
        """提取结构体定义"""
        structs = []
        
        struct_pattern = r'(?:pub\s+)?struct\s+(\w+)(?:\s*<[^>]+>)?(?:\s*\(([^)]*)\))?(?:\s*\{([^}]*)\})?'
        for match in re.finditer(struct_pattern, content):
            fields = []
            if match.group(3):
                for line in match.group(3).split('\n'):
                    line = line.strip()
                    if line:
                        parts = line.split(':')
                        if len(parts) >= 2:
                            fields.append({
                                'name': parts[0].strip(),
                                'type': ':'.join(parts[1:]).strip()
                            })
            
            structs.append({
                'name': match.group(1),
                'line_number': content[:match.start()].count('\n') + 1,
                'fields': fields,
                'file_path': file_path
            })
        
        return structs
    
    def _extract_enums(self, content: str, file_path: str) -> List[Dict]:
        """提取枚举定义"""
        enums = []
        
        enum_pattern = r'(?:pub\s+)?enum\s+(\w+)(?:\s*<[^>]+>)?\s*\{([^}]*)\}'
        for match in re.finditer(enum_pattern, content):
            variants = []
            for line in match.group(2).split('\n'):
                line = line.strip()
                if line and not line.startswith('//'):
                    variant = line.split(',')[0].strip()
                    if variant:
                        variants.append(variant)
            
            enums.append({
                'name': match.group(1),
                'line_number': content[:match.start()].count('\n') + 1,
                'variants': variants,
                'file_path': file_path
            })
        
        return enums
    
    def _extract_traits(self, content: str, file_path: str) -> List[Dict]:
        """提取trait定义"""
        traits = []
        
        trait_pattern = r'(?:pub\s+)?trait\s+(\w+)(?:\s*:\s*([^{]+))?\s*\{'
        for match in re.finditer(trait_pattern, content):
            traits.append({
                'name': match.group(1),
                'line_number': content[:match.start()].count('\n') + 1,
                'bounds': [b.strip() for b in match.group(2).split(',')] if match.group(2) else [],
                'file_path': file_path
            })
        
        return traits
    
    def _extract_functions(self, content: str, file_path: str) -> List[Dict]:
        """提取函数定义"""
        functions = []
        
        func_pattern = r'(?:pub\s+)?fn\s+(\w+)(?:\s*<[^>]+>)?\s*\(([^)]*)\)(?:\s*->\s*([^ \{]+))?\s*\{'
        for match in re.finditer(func_pattern, content):
            functions.append({
                'name': match.group(1),
                'line_number': content[:match.start()].count('\n') + 1,
                'parameters': self._parse_rust_params(match.group(2)),
                'return_type': match.group(3).strip() if match.group(3) else None,
                'file_path': file_path
            })
        
        return functions
    
    def _extract_impls(self, content: str, file_path: str) -> List[Dict]:
        """提取impl块"""
        impls = []
        
        impl_pattern = r'(?:pub\s+)?impl(?:\s+<[^>]+>)?\s+(?:\w+\s+for\s+)?(\w+)\s*\{'
        for match in re.finditer(impl_pattern, content):
            impls.append({
                'target': match.group(1),
                'line_number': content[:match.start()].count('\n') + 1,
                'file_path': file_path
            })
        
        return impls
    
    def _parse_rust_params(self, params_str: str) -> List[Dict]:
        """解析Rust参数列表"""
        params = []
        if params_str.strip():
            for param in params_str.split(','):
                param = param.strip()
                parts = param.split(':')
                if len(parts) >= 2:
                    params.append({
                        'name': parts[0].strip(),
                        'type': ':'.join(parts[1:]).strip()
                    })
        return params


class ModuleDetector:
    """模块边界检测器"""
    
    def __init__(self, project_root: str):
        """
        初始化模块检测器
        
        Args:
            project_root: 项目根目录
        """
        self.project_root = os.path.abspath(project_root)
        self.modules = {}
    
    def detect_modules(self, file_analysis_results: List[Dict]) -> Dict[str, ModuleInfo]:
        """
        检测模块边界
        
        Args:
            file_analysis_results: 文件分析结果列表
            
        Returns:
            Dict[str, ModuleInfo]: 模块信息字典
        """
        # 按目录分组文件
        dir_to_files = defaultdict(list)
        
        for file_info in file_analysis_results:
            rel_path = file_info.get('relative_path', '')
            dir_path = os.path.dirname(rel_path) if os.path.dirname(rel_path) else ''
            
            # 识别包/模块标识
            module_name = self._identify_module_name(file_info, dir_path)
            
            if module_name not in self.modules:
                self.modules[module_name] = ModuleInfo(
                    name=module_name,
                    path=os.path.join(self.project_root, dir_path) if dir_path else self.project_root,
                    file_count=0
                )
            
            self.modules[module_name].file_count += 1
            self.modules[module_name].elements.extend(file_info.get('elements', []))
        
        # 分析模块依赖
        self._analyze_dependencies(file_analysis_results)
        
        # 标注模块功能
        self._annotate_modules()
        
        return self.modules
    
    def _identify_module_name(self, file_info: Dict, dir_path: str) -> str:
        """
        识别模块名称
        
        Args:
            file_info: 文件信息
            dir_path: 目录路径
            
        Returns:
            str: 模块名称
        """
        file_name = file_info.get('name', '')
        
        # 检查包标识文件
        if file_name == '__init__.py':
            return dir_path.split(os.sep)[-1] if dir_path else 'root'
        
        # 检查JavaScript包标识
        if file_name == 'package.json':
            return dir_path.split(os.sep)[-1] if dir_path else 'root'
        
        # 检查Java模块标识
        if file_name.endswith('.java'):
            # 从导入语句推断模块
            imports = file_info.get('imports', [])
            for imp in imports:
                module = imp.get('module', '')
                if module:
                    parts = module.split('.')
                    return parts[0] if parts else 'root'
        
        # 默认使用目录名
        return dir_path.split(os.sep)[-1] if dir_path else 'root'
    
    def _analyze_dependencies(self, file_analysis_results: List[Dict]):
        """
        分析模块间依赖
        
        Args:
            file_analysis_results: 文件分析结果列表
        """
        for file_info in file_analysis_results:
            imports = file_info.get('imports', [])
            
            for imp in imports:
                module = imp.get('module', '')
                if module:
                    # 提取模块名
                    parts = module.split('/')
                    dep_module = parts[0] if parts else None
                    
                    if dep_module and dep_module in self.modules:
                        current_module = self._get_file_module(file_info)
                        if current_module != dep_module:
                            if dep_module not in self.modules[current_module].dependencies:
                                self.modules[current_module].dependencies.append(dep_module)
                            if current_module not in self.modules[dep_module].depended_by:
                                self.modules[dep_module].depended_by.append(current_module)
    
    def _get_file_module(self, file_info: Dict) -> str:
        """获取文件所属模块"""
        rel_path = file_info.get('relative_path', '')
        dir_path = os.path.dirname(rel_path)
        return dir_path.split(os.sep)[-1] if dir_path else 'root'
    
    def _annotate_modules(self):
        """标注模块功能"""
        for module_name, module in self.modules.items():
            # 收集所有类名和函数名
            class_names = []
            function_names = []
            
            for element in module.elements:
                if hasattr(element, 'name'):
                    name = element.name if isinstance(element, CodeElement) else element.get('name', '')
                    if isinstance(element, CodeElement):
                        if element.element_type == ElementType.CLASS:
                            class_names.append(name.lower())
                        elif element.element_type in [ElementType.FUNCTION, ElementType.METHOD]:
                            function_names.append(name.lower())
            
            # 分析模块职责
            module.responsibility = self._analyze_responsibility(class_names, function_names)
            
            # 提取核心功能
            module.core_features = self._extract_core_features(function_names, class_names)
            
            # 提取公共接口
            module.public_interfaces = self._extract_public_interfaces(module.elements)
    
    def _analyze_responsibility(self, class_names: List[str], function_names: List[str]) -> str:
        """
        分析模块职责
        
        Args:
            class_names: 类名列表
            function_names: 函数名列表
            
        Returns:
            str: 模块职责描述
        """
        keywords = []
        
        patterns = {
            'controller': '处理HTTP请求和响应',
            'service': '提供业务逻辑服务',
            'repository': '数据访问和存储',
            'manager': '管理和协调功能',
            'util': '提供工具函数',
            'handler': '处理特定事件或请求',
            'processor': '处理数据或任务',
            'builder': '构建复杂对象',
            'factory': '创建对象实例',
            'adapter': '适配不同接口',
            'strategy': '实现策略模式',
            'observer': '实现观察者模式',
            'api': '提供API接口',
            'router': '路由处理',
            'model': '数据模型',
            'view': '视图渲染',
            'middleware': '中间件处理',
            'config': '配置管理',
            'logger': '日志记录',
            'cache': '缓存管理'
        }
        
        all_names = class_names + function_names
        
        for name in all_names:
            name_lower = name.lower()
            for pattern, desc in patterns.items():
                if pattern in name_lower:
                    if desc not in keywords:
                        keywords.append(desc)
        
        if keywords:
            return '、'.join(keywords)
        
        return '通用功能模块'
    
    def _extract_core_features(self, function_names: List[str], class_names: List[str]) -> List[str]:
        """
        提取核心功能列表
        
        Args:
            function_names: 函数名列表
            class_names: 类名列表
            
        Returns:
            List[str]: 核心功能列表
        """
        features = []
        
        # 基于命名推断功能
        feature_patterns = {
            'create': '创建功能',
            'get': '查询功能',
            'update': '更新功能',
            'delete': '删除功能',
            'list': '列表功能',
            'add': '添加功能',
            'remove': '移除功能',
            'validate': '验证功能',
            'parse': '解析功能',
            'serialize': '序列化功能',
            'deserialize': '反序列化功能',
            'transform': '转换功能',
            'convert': '转换功能',
            'send': '发送功能',
            'receive': '接收功能',
            'process': '处理功能',
            'calculate': '计算功能',
            'generate': '生成功能'
        }
        
        all_names = function_names + class_names
        
        for name in all_names:
            name_lower = name.lower()
            for pattern, feature in feature_patterns.items():
                if pattern in name_lower and feature not in features:
                    features.append(feature)
        
        return features[:10]  # 限制最多10个核心功能
    
    def _extract_public_interfaces(self, elements: List[CodeElement]) -> List[Dict]:
        """
        提取公共接口
        
        Args:
            elements: 代码元素列表
            
        Returns:
            List[Dict]: 公共接口列表
        """
        interfaces = []
        
        for element in elements:
            if isinstance(element, CodeElement):
                if element.visibility == 'public' or not element.name.startswith('_'):
                    interfaces.append({
                        'name': element.name,
                        'type': element.element_type.value,
                        'parameters': element.parameters,
                        'return_type': element.return_type,
                        'docstring': element.docstring
                    })
        
        return interfaces


class SourceCodeAnalyzer:
    """源代码分析器主类，整合所有解析功能"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化源代码分析器
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
        self.scanner = ProjectScanner(self.config.get('scan', {}))
        self.ast_parser = ASTParser()
        self.module_detector = None
    
    def analyze(self, project_path: str) -> Dict[str, Any]:
        """
        分析项目源代码
        
        Args:
            project_path: 项目根目录路径
            
        Returns:
            Dict[str, Any]: 分析结果
        """
        result = {
            'project_info': {},
            'file_analysis': [],
            'modules': {},
            'statistics': {},
            'dependencies': {}
        }
        
        logger.info(f"开始分析项目: {project_path}")
        
        # 第一阶段：扫描项目
        logger.info("阶段1：扫描项目结构")
        scan_result = self.scanner.scan(project_path)
        result['project_info'] = {
            'path': project_path,
            'name': os.path.basename(project_path),
            'statistics': scan_result['statistics'],
            'entry_points': scan_result['entry_points']
        }
        
        # 第二阶段：解析源代码
        logger.info("阶段2：解析源代码文件")
        file_analysis_results = []
        
        for file_info in scan_result['source_files']:
            file_path = file_info['path']
            language = Language(file_info['language'])
            
            # 读取文件内容
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 解析AST
                ast_result = self.ast_parser.parse(file_path, content, language)
                
                if ast_result:
                    file_analysis_results.append({
                        'file_info': file_info,
                        'analysis': ast_result
                    })
                
            except Exception as e:
                logger.error(f"解析文件失败 {file_path}: {e}")
        
        result['file_analysis'] = file_analysis_results
        
        # 第三阶段：检测模块
        logger.info("阶段3：检测模块边界")
        self.module_detector = ModuleDetector(project_path)
        modules = self.module_detector.detect_modules([
            {
                'relative_path': fa['file_info']['relative_path'],
                'imports': fa['analysis'].get('imports', []),
                'elements': self._convert_to_elements(fa['analysis'])
            }
            for fa in file_analysis_results
        ])
        result['modules'] = modules
        
        # 第四阶段：统计信息
        logger.info("阶段4：计算统计信息")
        result['statistics'] = self._calculate_statistics(file_analysis_results, modules)
        
        logger.info("分析完成！")
        
        return result
    
    def _convert_to_elements(self, analysis: Dict) -> List[CodeElement]:
        """将分析结果转换为代码元素列表"""
        elements = []
        
        # 转换类
        for cls in analysis.get('classes', []):
            element = CodeElement(
                name=cls['name'],
                element_type=ElementType.CLASS,
                file_path=cls.get('file_path', ''),
                line_number=cls.get('line_number', 0),
                docstring=cls.get('docstring'),
                base_classes=cls.get('base_classes', []),
                visibility='public'
            )
            elements.append(element)
        
        # 转换函数
        for func in analysis.get('functions', []):
            element = CodeElement(
                name=func['name'],
                element_type=ElementType.FUNCTION,
                file_path=func.get('file_path', ''),
                line_number=func.get('line_number', 0),
                docstring=func.get('docstring'),
                parameters=func.get('parameters', []),
                return_type=func.get('return_type'),
                complexity=func.get('complexity', 1)
            )
            elements.append(element)
        
        return elements
    
    def _calculate_statistics(self, file_analysis_results: List, modules: Dict) -> Dict:
        """计算统计信息"""
        stats = {
            'total_files': len(file_analysis_results),
            'total_lines': 0,
            'total_classes': 0,
            'total_functions': 0,
            'total_interfaces': 0,
            'total_modules': len(modules),
            'language_distribution': {},
            'complexity_distribution': {}
        }
        
        for fa in file_analysis_results:
            analysis = fa['analysis']
            metadata = analysis.get('metadata', {})
            
            stats['total_lines'] += metadata.get('code_lines', 0)
            stats['total_classes'] += len(analysis.get('classes', []))
            stats['total_functions'] += len(analysis.get('functions', []))
            stats['total_interfaces'] += len(analysis.get('interfaces', []))
            
            # 语言分布
            lang = fa['file_info'].get('language', 'unknown')
            stats['language_distribution'][lang] = \
                stats['language_distribution'].get(lang, 0) + 1
        
        return stats


def main():
    """
    主函数，命令行入口点
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description='源代码结构分析器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 基本分析
  python source_parser.py ./project -o result.json
  
  # 详细分析
  python source_parser.py ./project --detailed
  
  # 只分析特定语言
  python source_parser.py ./project --languages python,java
  
  # 排除特定目录
  python source_parser.py ./project --exclude-dirs test,temp
        """
    )
    
    parser.add_argument('project', help='项目路径')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('--format', choices=['json', 'yaml'], default='json',
                       help='输出格式（默认: json）')
    parser.add_argument('--exclude-dirs', default='',
                       help='排除的目录（逗号分隔）')
    parser.add_argument('--languages', default='',
                       help='只分析特定语言（逗号分隔）')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='显示详细输出')
    
    args = parser.parse_args()
    
    # 配置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 创建分析器
    config = {}
    if args.exclude_dirs:
        config['exclude_dirs'] = args.exclude_dirs.split(',')
    
    analyzer = SourceCodeAnalyzer(config)
    
    # 执行分析
    result = analyzer.analyze(args.project)
    
    # 输出结果
    if args.output:
        if args.format == 'json':
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
        else:
            import yaml
            with open(args.output, 'w', encoding='utf-8') as f:
                yaml.dump(result, f, allow_unicode=True)
        print(f"分析结果已保存到: {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
