#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模块依赖分析器

该模块提供完整的模块依赖关系分析功能，包括依赖图构建、依赖类型分类、
循环依赖检测、耦合度计算和依赖关系报告生成。支持多种编程语言的依赖提取。

联系：purpose168@outlook.com
"""

import os
import sys
import json
import re
import logging
import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set, Any
from pathlib import Path
from enum import Enum
from collections import defaultdict, deque
import graphviz

# 配置日志记录器
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class DependencyType(Enum):
    """依赖类型枚举"""
    IMPORT = "import"           # 导入依赖
    INHERIT = "inherit"         # 继承依赖
    COMPOSITION = "composition"  # 组合依赖
    AGGREGATION = "aggregation"  # 聚合依赖
    ASSOCIATION = "association"  # 关联依赖
    CALL = "call"               # 调用依赖
    DATA_FLOW = "data_flow"     # 数据流依赖
    CONFIG = "config"           # 配置依赖
    DATABASE = "database"       # 数据库依赖
    EXTERNAL = "external"       # 外部依赖


class CouplingMetric(Enum):
    """耦合度指标枚举"""
    AFFERENT_COUPLING = "ca"     # 入向耦合（被依赖数）
    EFFERENT_COUPLING = "ce"     # 出向耦合（依赖数）
    INSTABILITY = "I"            # 不稳定性
    ABSTRACTION = "A"            # 抽象度
    DISTANCE = "D"               # 距离主序列


@dataclass
class Dependency:
    """依赖关系数据类"""
    source_module: str           # 源模块
    target_module: str           # 目标模块
    dependency_type: DependencyType  # 依赖类型
    strength: float = 1.0        # 依赖强度（0-1）
    file_path: str = ""          # 依赖所在文件
    line_number: int = 0         # 依赖所在行号
    element_name: str = ""       # 依赖的元素名称
    description: str = ""        # 依赖描述


@dataclass
class ModuleDependencyInfo:
    """模块依赖信息数据类"""
    module_name: str             # 模块名称
    module_path: str             # 模块路径
    afferent_coupling: int = 0   # 入向耦合度（被其他模块依赖的数量）
    efferent_coupling: int = 0   # 出向耦合度（依赖其他模块的数量）
    instability: float = 0.0     # 不稳定性
    abstraction: float = 0.0     # 抽象度
    distance: float = 0.0        # 到主序列的距离
    dependencies: List[Dependency] = field(default_factory=list)  # 出向依赖
    dependents: List[Dependency] = field(default_factory=list)    # 入向依赖
    core_classes: List[str] = field(default_factory=list)         # 核心类
    public_interfaces: List[str] = field(default_factory=list)    # 公共接口
    metrics: Dict[str, Any] = field(default_factory=dict)         # 其他指标


@dataclass
class DependencyGraph:
    """依赖图数据类"""
    nodes: Dict[str, ModuleDependencyInfo] = field(default_factory=dict)  # 节点
    edges: List[Dependency] = field(default_factory=list)                  # 边
    metadata: Dict[str, Any] = field(default_factory=dict)                # 元数据


class DependencyExtractor:
    """依赖提取器，从源代码中提取依赖关系"""
    
    def __init__(self):
        """初始化依赖提取器"""
        self.import_patterns = {}
        self._init_patterns()
    
    def _init_patterns(self):
        """初始化各语言的导入模式"""
        self.import_patterns = {
            'python': [
                r'import\s+(\w+(?:\.\w+)*)',
                r'from\s+(\w+(?:\.\w+)*)\s+import',
                r'import\s+\w+\s+as\s+\w+',
            ],
            'javascript': [
                r'(?:require|import)\s*\(?\s*[\'"]([^\'"]+)[\'"]',
                r'import\s+(?:\{[^}]+\}|\*|\w+)\s+from\s+[\'"]([^\'"]+)[\'"]',
            ],
            'java': [
                r'import\s+([\w.]+(?:\.\*)?)\s*;',
                r'import\s+static\s+([\w.]+)\s*;',
            ],
            'cpp': [
                r'#include\s+[<"]([^>"]+)[">]',
            ],
            'go': [
                r'import\s*\(\s*([^\)]+)\s*\)',
                r'import\s+"([^"]+)"',
            ],
            'rust': [
                r'use\s+([^;]+)\s*;',
                r'extern\s+crate\s+(\w+)',
                r'use\s+\w+\s*::\s*\{([^}]+)\}',
            ],
            'typescript': [
                r'(?:require|import)\s*\(?\s*[\'"]([^\'"]+)[\'"]',
                r'import\s+(?:\{[^}]+\}|\*|\w+)\s+from\s+[\'"]([^\'"]+)[\'"]',
                r'import\s+=?\s*require\([\'"]([^\'"]+)[\'"]',
            ],
        }
    
    def extract_dependencies(self, file_path: str, content: str, language: str) -> List[Dependency]:
        """
        从源代码中提取依赖关系
        
        Args:
            file_path: 文件路径
            content: 文件内容
            language: 编程语言
            
        Returns:
            List[Dependency]: 依赖关系列表
        """
        dependencies = []
        
        patterns = self.import_patterns.get(language.lower(), [])
        
        for pattern in patterns:
            for match in re.finditer(pattern, content):
                module_name = self._extract_module_name(match, pattern, language)
                if module_name:
                    dependency = Dependency(
                        source_module=os.path.dirname(file_path),
                        target_module=module_name,
                        dependency_type=DependencyType.IMPORT,
                        file_path=file_path,
                        line_number=content[:match.start()].count('\n') + 1,
                        element_name=module_name.split('.')[-1] if '.' in module_name else module_name
                    )
                    dependencies.append(dependency)
        
        return dependencies
    
    def _extract_module_name(self, match, pattern: str, language: str) -> Optional[str]:
        """
        从正则匹配中提取模块名称
        
        Args:
            match: 正则匹配对象
            pattern: 正则模式
            language: 编程语言
            
        Returns:
            Optional[str]: 模块名称
        """
        if language == 'python':
            if 'from' in pattern:
                return match.group(1) if match.lastindex == 1 else None
            else:
                return match.group(1) if match.lastindex == 1 else None
        
        elif language in ['javascript', 'typescript']:
            # 多个匹配组，取最后一个非空组
            for i in range(match.lastindex, 0, -1):
                if match.group(i):
                    return match.group(i)
        
        elif language == 'java':
            return match.group(1)
        
        elif language == 'cpp':
            header = match.group(1)
            # 排除标准库头文件
            if not header.startswith('<'):
                return header
        
        elif language == 'go':
            # 处理多行导入块
            line = match.group(1)
            if line.strip().startswith('"') and line.strip().endswith('"'):
                return line.strip()[1:-1]
        
        elif language == 'rust':
            return match.group(1).split('::')[0] if '::' in match.group(1) else match.group(1)
        
        return None


class DependencyGraphBuilder:
    """依赖图构建器"""
    
    def __init__(self, project_root: str):
        """
        初始化依赖图构建器
        
        Args:
            project_root: 项目根目录
        """
        self.project_root = os.path.abspath(project_root)
        self.extractor = DependencyExtractor()
        self.modules = {}
        self.graph = DependencyGraph()
    
    def build_graph(self, file_analyses: List[Dict]) -> DependencyGraph:
        """
        构建模块依赖图
        
        Args:
            file_analyses: 文件分析结果列表
            
        Returns:
            DependencyGraph: 依赖图
        """
        logger.info("开始构建依赖图")
        
        # 收集所有模块
        for fa in file_analyses:
            file_info = fa.get('file_info', {})
            rel_path = file_info.get('relative_path', '')
            module_name = self._get_module_name(rel_path)
            
            if module_name not in self.modules:
                self.modules[module_name] = ModuleDependencyInfo(
                    module_name=module_name,
                    module_path=os.path.dirname(file_info.get('path', ''))
                )
            
            # 提取并记录依赖
            content = fa.get('content', '')
            language = file_info.get('language', '')
            
            if content:
                dependencies = self.extractor.extract_dependencies(
                    file_info.get('path', ''),
                    content,
                    language
                )
                
                for dep in dependencies:
                    self._add_dependency(dep)
        
        # 计算耦合度指标
        self._calculate_metrics()
        
        # 构建图结构
        self._build_graph_structure()
        
        logger.info(f"依赖图构建完成：{len(self.graph.nodes)} 个模块，{len(self.graph.edges)} 条依赖")
        
        return self.graph
    
    def _get_module_name(self, rel_path: str) -> str:
        """
        从相对路径获取模块名称
        
        Args:
            rel_path: 相对路径
            
        Returns:
            str: 模块名称
        """
        if not rel_path:
            return 'root'
        
        parts = rel_path.split(os.sep)
        
        # 检查是否是包标识文件
        if parts[-1] == '__init__.py':
            return parts[-2] if len(parts) > 1 else 'root'
        
        # 使用第一层目录作为模块名
        return parts[0] if parts else 'root'
    
    def _add_dependency(self, dependency: Dependency):
        """
        添加依赖关系
        
        Args:
            dependency: 依赖关系
        """
        source = dependency.source_module
        target = dependency.target_module
        
        # 规范化模块名
        source = self._normalize_module_name(source)
        target = self._normalize_module_name(target)
        
        if source == target:
            return
        
        # 更新源模块的出向依赖
        if source not in self.modules:
            self.modules[source] = ModuleDependencyInfo(
                module_name=source,
                module_path=''
            )
        
        if target not in self.modules:
            self.modules[target] = ModuleDependencyInfo(
                module_name=target,
                module_path=''
            )
        
        # 检查依赖是否已存在
        existing = [d for d in self.modules[source].dependencies
                   if d.target_module == target and d.dependency_type == dependency.dependency_type]
        
        if not existing:
            dependency.source_module = source
            dependency.target_module = target
            self.modules[source].dependencies.append(dependency)
        
        # 更新目标模块的入向依赖
        reverse_dep = Dependency(
            source_module=target,
            target_module=source,
            dependency_type=dependency.dependency_type,
            strength=dependency.strength,
            file_path=dependency.file_path,
            line_number=dependency.line_number,
            element_name=dependency.element_name
        )
        
        existing_rev = [d for d in self.modules[target].dependents
                       if d.target_module == source]
        
        if not existing_rev:
            self.modules[target].dependents.append(reverse_dep)
    
    def _normalize_module_name(self, module_name: str) -> str:
        """
        规范化模块名称
        
        Args:
            module_name: 原始模块名
            
        Returns:
            str: 规范化后的模块名
        """
        if not module_name:
            return 'root'
        
        # 移除文件扩展名
        if '.' in module_name:
            module_name = module_name.split('.')[0]
        
        # 移除常见前缀
        prefixes = ['src.', 'lib.', 'core.', 'app.']
        for prefix in prefixes:
            if module_name.startswith(prefix):
                module_name = module_name[len(prefix):]
        
        return module_name.split('/')[0] if '/' in module_name else module_name
    
    def _calculate_metrics(self):
        """计算各模块的耦合度指标"""
        # 计算入向和出向耦合度
        for module_name, module in self.modules.items():
            module.efferent_coupling = len(module.dependencies)
            module.afferent_coupling = len(module.dependents)
            
            # 计算不稳定性 I = Ce / (Ca + Ce)
            total = module.afferent_coupling + module.efferent_coupling
            if total > 0:
                module.instability = module.efferent_coupling / total
            else:
                module.instability = 0.0
        
        # 计算抽象度 A = Na / Nc
        self._calculate_abstraction()
        
        # 计算到主序列的距离 D = |A + I - 1|
        self._calculate_distance()
    
    def _calculate_abstraction(self):
        """计算模块抽象度"""
        for module_name, module in self.modules.items():
            # 统计抽象元素数量（接口、抽象类）
            abstract_count = 0
            total_count = len(module.core_classes) + len(module.public_interfaces)
            
            for cls in module.core_classes:
                if 'interface' in cls.lower() or 'abstract' in cls.lower():
                    abstract_count += 1
            
            if total_count > 0:
                module.abstraction = abstract_count / total_count
            else:
                module.abstraction = 0.0
    
    def _calculate_distance(self):
        """计算到主序列的距离"""
        for module_name, module in self.modules.items():
            # 主序列公式：D = |A + I - 1|
            module.distance = abs(module.abstraction + module.instability - 1)
            
            # 记录指标
            module.metrics = {
                'afferent_coupling': module.afferent_coupling,
                'efferent_coupling': module.efferent_coupling,
                'instability': round(module.instability, 3),
                'abstraction': round(module.abstraction, 3),
                'distance': round(module.distance, 3)
            }
    
    def _build_graph_structure(self):
        """构建图结构"""
        # 添加节点
        for module_name, module in self.modules.items():
            self.graph.nodes[module_name] = module
        
        # 收集边
        for module_name, module in self.modules.items():
            for dep in module.dependencies:
                self.graph.edges.append(dep)
        
        # 添加元数据
        self.graph.metadata = {
            'total_nodes': len(self.graph.nodes),
            'total_edges': len(self.graph.edges),
            'average_coupling': self._calculate_average_coupling(),
            'max_coupling': self._find_max_coupling_module(),
            'core_modules': self._identify_core_modules(5),
        }
    
    def _calculate_average_coupling(self) -> float:
        """计算平均耦合度"""
        if not self.graph.nodes:
            return 0.0
        
        total_coupling = sum(
            m.afferent_coupling + m.efferent_coupling
            for m in self.graph.nodes.values()
        )
        
        return round(total_coupling / len(self.graph.nodes), 2)
    
    def _find_max_coupling_module(self) -> Optional[str]:
        """找出耦合度最高的模块"""
        max_coupling = -1
        max_module = None
        
        for module_name, module in self.modules.items():
            coupling = module.afferent_coupling + module.efferent_coupling
            if coupling > max_coupling:
                max_coupling = coupling
                max_module = module_name
        
        return max_module
    
    def _identify_core_modules(self, count: int = 5) -> List[Dict]:
        """
        识别核心模块
        
        Args:
            count: 返回数量
            
        Returns:
            List[Dict]: 核心模块列表
        """
        # 根据度数（入度+出度）排序
        module_scores = []
        
        for module_name, module in self.modules.items():
            score = module.afferent_coupling + module.efferent_coupling
            module_scores.append({
                'name': module_name,
                'score': score,
                'afferent': module.afferent_coupling,
                'efferent': module.efferent_coupling,
                'instability': module.instability
            })
        
        # 按分数降序排序
        module_scores.sort(key=lambda x: x['score'], reverse=True)
        
        return module_scores[:count]


class CycleDetector:
    """循环依赖检测器"""
    
    def __init__(self, graph: DependencyGraph):
        """
        初始化循环依赖检测器
        
        Args:
            graph: 依赖图
        """
        self.graph = graph
    
    def detect_cycles(self) -> List[List[str]]:
        """
        检测循环依赖
        
        使用深度优先搜索算法检测图中的环
        
        Returns:
            List[List[str]]: 循环依赖列表，每个循环是一个模块名列表
        """
        cycles = []
        visited = set()
        rec_stack = set()
        path = []
        
        def dfs(node: str):
            """深度优先搜索"""
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            # 获取当前节点的邻居
            node_info = self.graph.nodes.get(node)
            if node_info:
                for dep in node_info.dependencies:
                    neighbor = dep.target_module
                    
                    if neighbor not in visited:
                        if dfs(neighbor):
                            return True
                    elif neighbor in rec_stack:
                        # 发现循环
                        cycle_start = path.index(neighbor)
                        cycle = path[cycle_start:] + [neighbor]
                        cycles.append(cycle)
                        return True
            
            path.pop()
            rec_stack.remove(node)
            return False
        
        # 对每个未访问的节点进行DFS
        for node in self.graph.nodes:
            if node not in visited:
                dfs(node)
        
        # 移除重复或嵌套的循环
        unique_cycles = self._unique_cycles(cycles)
        
        return unique_cycles
    
    def _unique_cycles(self, cycles: List[List[str]]) -> List[List[str]]:
        """
        获取唯一的循环依赖
        
        Args:
            cycles: 所有检测到的循环
            
        Returns:
            List[List[str]]: 去重后的循环列表
        """
        unique = []
        
        for cycle in cycles:
            # 规范化循环（旋转到最小元素开始）
            normalized = self._normalize_cycle(cycle)
            
            # 检查是否已存在
            is_duplicate = False
            for existing in unique:
                if set(normalized) == set(existing):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique.append(normalized)
        
        return unique
    
    def _normalize_cycle(self, cycle: List[str]) -> List[str]:
        """
        规范化循环
        
        将循环旋转到字典序最小的起点
        
        Args:
            cycle: 循环列表
            
        Returns:
            List[str]: 规范化后的循环
        """
        if len(cycle) <= 2:
            return cycle
        
        # 找到字典序最小的元素位置
        min_idx = 0
        for i in range(1, len(cycle) - 1):
            if cycle[i] < cycle[min_idx]:
                min_idx = i
        
        # 旋转循环
        normalized = cycle[min_idx:-1] + cycle[:min_idx] + [cycle[min_idx]]
        
        return normalized
    
    def get_cycle_details(self, cycles: List[List[str]]) -> List[Dict]:
        """
        获取循环依赖详情
        
        Args:
            cycles: 循环列表
            
        Returns:
            List[Dict]: 循环详情列表
        """
        details = []
        
        for i, cycle in enumerate(cycles):
            detail = {
                'cycle_id': i + 1,
                'modules': cycle,
                'length': len(cycle) - 1,
                'severity': self._assess_severity(cycle),
                'breaking_suggestions': self._suggest_breaking(cycle)
            }
            details.append(detail)
        
        return details
    
    def _assess_severity(self, cycle: List[str]) -> str:
        """
        评估循环依赖严重程度
        
        Args:
            cycle: 循环列表
            
        Returns:
            str: 严重程度描述
        """
        length = len(cycle) - 1
        
        if length == 2:
            return "严重（双向直接依赖）"
        elif length <= 3:
            return "高（短循环依赖）"
        elif length <= 5:
            return "中（中等长度循环）"
        else:
            return "低（长循环链）"
    
    def _suggest_breaking(self, cycle: List[str]) -> List[str]:
        """
        提供打破循环的建议
        
        Args:
            cycle: 循环列表
            
        Returns:
            List[str]: 建议列表
        """
        suggestions = []
        
        # 建议1：使用依赖注入
        suggestions.append("使用依赖注入/接口隔离打破直接依赖")
        
        # 建议2：提取公共模块
        suggestions.append(f"提取公共模块，将 cycle[0] 和 cycle[-1] 的共同依赖分离")
        
        # 建议3：改变调用方向
        suggestions.append("考虑改变调用方向，使用回调或事件机制")
        
        # 建议4：引入中间层
        suggestions.append("引入中间层或协调者模式")
        
        return suggestions


class CouplingAnalyzer:
    """耦合度分析器"""
    
    def __init__(self, graph: DependencyGraph):
        """
        初始化耦合度分析器
        
        Args:
            graph: 依赖图
        """
        self.graph = graph
    
    def analyze_coupling(self) -> Dict[str, Any]:
        """
        分析模块耦合度
        
        Returns:
            Dict[str, Any]: 耦合度分析结果
        """
        result = {
            'summary': {},
            'high_coupling': [],
            'violations': [],
            'recommendations': []
        }
        
        # 计算汇总信息
        result['summary'] = self._calculate_summary()
        
        # 识别高耦合模块
        result['high_coupling'] = self._identify_high_coupling_modules()
        
        # 检测架构违规
        result['violations'] = self._detect_architecture_violations()
        
        # 生成优化建议
        result['recommendations'] = self._generate_recommendations()
        
        return result
    
    def _calculate_summary(self) -> Dict[str, Any]:
        """计算耦合度汇总信息"""
        if not self.graph.nodes:
            return {}
        
        modules = list(self.graph.nodes.values())
        
        # 计算平均指标
        avg_instability = sum(m.instability for m in modules) / len(modules)
        avg_abstraction = sum(m.abstraction for m in modules) / len(modules)
        
        # 统计分布
        instability_distribution = {
            'stable': sum(1 for m in modules if m.instability < 0.3),
            'moderate': sum(1 for m in modules if 0.3 <= m.instability <= 0.7),
            'unstable': sum(1 for m in modules if m.instability > 0.7)
        }
        
        return {
            'total_modules': len(modules),
            'total_dependencies': len(self.graph.edges),
            'average_instability': round(avg_instability, 3),
            'average_abstraction': round(avg_abstraction, 3),
            'instability_distribution': instability_distribution
        }
    
    def _identify_high_coupling_modules(self, threshold: int = 10) -> List[Dict]:
        """
        识别高耦合模块
        
        Args:
            threshold: 耦合度阈值
            
        Returns:
            List[Dict]: 高耦合模块列表
        """
        high_coupling = []
        
        for module_name, module in self.graph.nodes.items():
            total_coupling = module.afferent_coupling + module.efferent_coupling
            
            if total_coupling >= threshold:
                high_coupling.append({
                    'module': module_name,
                    'total_coupling': total_coupling,
                    'afferent': module.afferent_coupling,
                    'efferent': module.efferent_coupling,
                    'instability': module.instability,
                    'risk_level': 'high' if total_coupling > threshold * 2 else 'medium'
                })
        
        # 按耦合度降序排序
        high_coupling.sort(key=lambda x: x['total_coupling'], reverse=True)
        
        return high_coupling
    
    def _detect_architecture_violations(self) -> List[Dict]:
        """
        检测架构违规
        
        检测常见的架构设计问题：
        - 依赖环
        - 跨越层次的依赖
        - 核心模块的高耦合
        
        Returns:
            List[Dict]: 违规列表
        """
        violations = []
        
        # 检测循环依赖
        cycle_detector = CycleDetector(self.graph)
        cycles = cycle_detector.detect_cycles()
        
        for cycle in cycles:
            violations.append({
                'type': 'cyclic_dependency',
                'severity': 'high',
                'modules': cycle,
                'description': f"发现循环依赖: {' -> '.join(cycle[:-1])}"
            })
        
        # 检测不稳定依赖不稳定（依赖于不稳定模块）
        for module_name, module in self.graph.nodes.items():
            if module.instability > 0.7:  # 不稳定模块
                for dep in module.dependencies:
                    target = self.graph.nodes.get(dep.target_module)
                    if target and target.instability > 0.7:
                        violations.append({
                            'type': 'unstable_to_unstable',
                            'severity': 'medium',
                            'from': module_name,
                            'to': dep.target_module,
                            'description': f"不稳定模块 {module_name} 依赖不稳定模块 {dep.target_module}"
                        })
        
        return violations
    
    def _generate_recommendations(self) -> List[Dict]:
        """
        生成优化建议
        
        Returns:
            List[Dict]: 建议列表
        """
        recommendations = []
        
        # 建议1：降低高耦合模块复杂度
        high_coupling = self._identify_high_coupling_modules()
        if high_coupling:
            recommendations.append({
                'category': 'reduce_coupling',
                'priority': 'high',
                'modules': [m['module'] for m in high_coupling[:3]],
                'suggestion': "考虑将高耦合模块拆分为更小的模块，降低单一职责"
            })
        
        # 建议2：遵循依赖倒置原则
        recommendations.append({
            'category': 'dependency_inversion',
            'priority': 'medium',
            'suggestion': "高层模块不应依赖低层模块，应依赖抽象接口"
        })
        
        # 建议3：提高抽象度
        low_abstraction = [
            m for m in self.graph.nodes.values()
            if m.abstraction < 0.2 and m.instability > 0.5
        ]
        if low_abstraction:
            recommendations.append({
                'category': 'increase_abstraction',
                'priority': 'medium',
                'modules': [m.module_name for m in low_abstraction],
                'suggestion': "这些模块不稳定且抽象度低，考虑提取接口或抽象类"
            })
        
        return recommendations


class DependencyVisualizer:
    """依赖关系可视化器"""
    
    def __init__(self, graph: DependencyGraph):
        """
        初始化可视化器
        
        Args:
            graph: 依赖图
        """
        self.graph = graph
    
    def generate_graph_image(self, output_path: str, format: str = 'png',
                            include_external: bool = False) -> str:
        """
        生成依赖图图片
        
        Args:
            output_path: 输出路径（不含扩展名）
            format: 图片格式（png, svg, pdf等）
            include_external: 是否包含外部依赖
            
        Returns:
            str: 输出文件路径
        """
        dot = graphviz.Digraph(comment='Dependency Graph')
        
        # 设置图形属性
        dot.attr('node', style='filled', fontsize='10')
        dot.attr('edge', arrowsize='0.5')
        
        # 添加节点
        for module_name, module in self.graph.nodes.items():
            # 根据不稳定性设置颜色
            if module.instability > 0.7:
                color = '#ffcccc'  # 红色 - 不稳定
            elif module.instability < 0.3:
                color = '#ccffcc'  # 绿色 - 稳定
            else:
                color = '#ffffcc'  # 黄色 - 中等
            
            # 根据抽象度设置形状
            if module.abstraction > 0.5:
                shape = 'box'
            else:
                shape = 'ellipse'
            
            label = f"{module_name}\n(I={module.instability:.2f})"
            dot.node(module_name, label=label, shape=shape, fillcolor=color)
        
        # 添加边
        for dep in self.graph.edges:
            if not include_external and dep.target_module not in self.graph.nodes:
                continue
            
            # 根据依赖类型设置边的样式
            style = 'solid'
            if dep.dependency_type == DependencyType.INHERIT:
                style = 'dashed'
                color = 'blue'
            elif dep.dependency_type == DependencyType.CALL:
                color = 'green'
            else:
                color = 'black'
            
            dot.edge(dep.source_module, dep.target_module,
                    style=style, color=color)
        
        # 渲染图片
        output_file = f"{output_path}.{format}"
        dot.render(output_file, format=format, cleanup=True)
        
        logger.info(f"依赖图已生成: {output_file}")
        
        return output_file
    
    def generate_mermaid_chart(self) -> str:
        """
        生成Mermaid格式的依赖图
        
        Returns:
            str: Mermaid格式的图表定义
        """
        lines = ["```mermaid", "graph TD"]
        
        # 添加节点
        for module_name in self.graph.nodes:
            lines.append(f"    {module_name}[{module_name}]")
        
        # 添加边
        seen_edges = set()
        for dep in self.graph.edges:
            edge_key = (dep.source_module, dep.target_module)
            if edge_key not in seen_edges:
                seen_edges.add(edge_key)
                
                # 根据依赖类型设置箭头样式
                if dep.dependency_type == DependencyType.INHERIT:
                    lines.append(f"    {dep.source_module} --|> {dep.target_module}")
                else:
                    lines.append(f"    {dep.source_module} --> {dep.target_module}")
        
        lines.append("```")
        
        return '\n'.join(lines)
    
    def generate_dot_code(self) -> str:
        """
        生成Graphviz DOT格式的依赖图
        
        Returns:
            str: DOT格式的图定义
        """
        lines = ["digraph DependencyGraph {"]
        lines.append('    rankdir=LR;')
        lines.append('    node [shape=box, style=filled, fontsize=10];')
        lines.append('    edge [arrowsize=0.5];')
        
        # 添加节点
        for module_name, module in self.graph.nodes.items():
            # 根据不稳定性设置颜色
            if module.instability > 0.7:
                color = 'lightcoral'
            elif module.instability < 0.3:
                color = 'lightgreen'
            else:
                color = 'lightyellow'
            
            lines.append(f'    {module_name} [label="{module_name}\\n(I={module.instability:.2f})"'
                        f', fillcolor={color}];')
        
        # 添加边
        seen_edges = set()
        for dep in self.graph.edges:
            edge_key = (dep.source_module, dep.target_module)
            if edge_key not in seen_edges:
                seen_edges.add(edge_key)
                
                if dep.dependency_type == DependencyType.INHERIT:
                    lines.append(f'    {dep.source_module} -> {dep.target_module} [style=dashed, color=blue];')
                else:
                    lines.append(f'    {dep.source_module} -> {dep.target_module};')
        
        lines.append("}")
        
        return '\n'.join(lines)


class DependencyReportGenerator:
    """依赖分析报告生成器"""
    
    def __init__(self, graph: DependencyGraph):
        """
        初始化报告生成器
        
        Args:
            graph: 依赖图
        """
        self.graph = graph
        self.coupling_analyzer = CouplingAnalyzer(graph)
        self.cycle_detector = CycleDetector(graph)
    
    def generate_report(self, output_format: str = 'markdown') -> str:
        """
        生成依赖分析报告
        
        Args:
            output_format: 输出格式（markdown, html, json）
            
        Returns:
            str: 报告内容
        """
        if output_format == 'json':
            return self._generate_json_report()
        elif output_format == 'html':
            return self._generate_html_report()
        else:
            return self._generate_markdown_report()
    
    def _generate_markdown_report(self) -> str:
        """生成Markdown格式报告"""
        lines = []
        
        # 标题
        lines.append("# 模块依赖分析报告\n")
        
        # 汇总信息
        lines.append("## 1. 汇总信息\n")
        lines.append(f"- **模块总数**: {self.graph.metadata.get('total_nodes', 0)}")
        lines.append(f"- **依赖关系总数**: {self.graph.metadata.get('total_edges', 0)}")
        lines.append(f"- **平均耦合度**: {self.graph.metadata.get('average_coupling', 0)}")
        lines.append(f"- **最高耦合模块**: {self.graph.metadata.get('max_coupling', 'N/A')}")
        lines.append("")
        
        # 核心模块
        lines.append("## 2. 核心模块\n")
        lines.append("| 模块 | 分数 | 入向耦合 | 出向耦合 | 不稳定性 |")
        lines.append("|------|------|---------|---------|----------|")
        
        core_modules = self.graph.metadata.get('core_modules', [])
        for module in core_modules:
            lines.append(f"| {module['name']} | {module['score']} | "
                        f"{module['afferent']} | {module['efferent']} | "
                        f"{module['instability']:.2f} |")
        lines.append("")
        
        # 循环依赖检测
        lines.append("## 3. 循环依赖分析\n")
        cycles = self.cycle_detector.detect_cycles()
        
        if not cycles:
            lines.append("✅ 未检测到循环依赖\n")
        else:
            cycle_details = self.cycle_detector.get_cycle_details(cycles)
            for detail in cycle_details:
                lines.append(f"### 循环 {detail['cycle_id']}\n")
                lines.append(f"- **严重程度**: {detail['severity']}")
                lines.append(f"- **涉及模块**: {' → '.join(detail['modules'][:-1])}")
                lines.append("- **优化建议**:")
                for suggestion in detail['breaking_suggestions']:
                    lines.append(f"  - {suggestion}")
                lines.append("")
        
        # 耦合度分析
        lines.append("## 4. 耦合度分析\n")
        coupling_analysis = self.coupling_analyzer.analyze_coupling()
        
        lines.append("### 4.1 汇总\n")
        summary = coupling_analysis['summary']
        lines.append(f"- 平均不稳定性: {summary.get('average_instability', 0)}")
        lines.append(f"- 平均抽象度: {summary.get('average_abstraction', 0)}")
        
        dist = summary.get('instability_distribution', {})
        lines.append(f"- 稳定模块数: {dist.get('stable', 0)}")
        lines.append(f"- 中等模块数: {dist.get('moderate', 0)}")
        lines.append(f"- 不稳定模块数: {dist.get('unstable', 0)}")
        lines.append("")
        
        lines.append("### 4.2 高耦合模块\n")
        high_coupling = coupling_analysis['high_coupling']
        if high_coupling:
            lines.append("| 模块 | 总耦合度 | 入向 | 出向 | 风险级别 |")
            lines.append("|------|---------|------|------|----------|")
            for module in high_coupling:
                lines.append(f"| {module['module']} | {module['total_coupling']} | "
                            f"{module['afferent']} | {module['efferent']} | "
                            f"{module['risk_level']} |")
        else:
            lines.append("✅ 未发现高耦合模块\n")
        lines.append("")
        
        # 架构违规
        lines.append("## 5. 架构违规检测\n")
        violations = coupling_analysis['violations']
        if violations:
            for violation in violations:
                lines.append(f"- **{violation['type']}** ({violation['severity']})")
                lines.append(f"  - {violation['description']}")
        else:
            lines.append("✅ 未检测到架构违规\n")
        lines.append("")
        
        # 优化建议
        lines.append("## 6. 优化建议\n")
        recommendations = coupling_analysis['recommendations']
        for rec in recommendations:
            lines.append(f"### {rec['category']}\n")
            lines.append(f"- **优先级**: {rec['priority']}")
            if 'modules' in rec:
                lines.append(f"- **涉及模块**: {', '.join(rec['modules'])}")
            lines.append(f"- **建议**: {rec['suggestion']}")
            lines.append("")
        
        # 依赖图
        lines.append("## 7. 依赖图\n")
        visualizer = DependencyVisualizer(self.graph)
        lines.append(visualizer.generate_mermaid_chart())
        
        return '\n'.join(lines)
    
    def _generate_json_report(self) -> str:
        """生成JSON格式报告"""
        coupling_analysis = self.coupling_analyzer.analyze_coupling()
        cycles = self.cycle_detector.detect_cycles()
        
        report = {
            'metadata': self.graph.metadata,
            'modules': {},
            'coupling_analysis': coupling_analysis,
            'cycles': {
                'detected': len(cycles),
                'details': self.cycle_detector.get_cycle_details(cycles)
            }
        }
        
        for module_name, module in self.graph.nodes.items():
            report['modules'][module_name] = {
                'name': module.module_name,
                'path': module.module_path,
                'coupling': {
                    'afferent': module.afferent_coupling,
                    'efferent': module.efferent_coupling,
                    'instability': module.instability,
                    'abstraction': module.abstraction,
                    'distance': module.distance
                },
                'dependencies': [
                    {
                        'target': dep.target_module,
                        'type': dep.dependency_type.value,
                        'strength': dep.strength
                    }
                    for dep in module.dependencies
                ]
            }
        
        return json.dumps(report, ensure_ascii=False, indent=2)
    
    def _generate_html_report(self) -> str:
        """生成HTML格式报告"""
        markdown_report = self._generate_markdown_report()
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>模块依赖分析报告</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #555;
            margin-top: 30px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #007bff;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .warning {{
            background-color: #fff3cd;
            border: 1px solid #ffc107;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
        }}
        .success {{
            background-color: #d4edda;
            border: 1px solid #28a745;
            padding: 10px;
            border-radius: 4px;
        }}
        .high-risk {{
            background-color: #f8d7da;
            border: 1px solid #dc3545;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>模块依赖分析报告</h1>
        <p>生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <!-- Markdown内容 -->
        {self._markdown_to_html(markdown_report)}
    </div>
</body>
</html>
"""
        
        return html
    
    def _markdown_to_html(self, markdown: str) -> str:
        """简单的Markdown转HTML"""
        # 简化实现
        html = markdown.replace('\n', '<br>')
        html = re.sub(r'# (.*?)<br>', r'<h1>\1</h1>', html)
        html = re.sub(r'## (.*?)<br>', r'<h2>\1</h2>', html)
        html = re.sub(r'### (.*?)<br>', r'<h3>\1</h3>', html)
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        html = re.sub(r'```mermaid\n(.*?)\n```', r'<div class="mermaid">\1</div>', html, flags=re.DOTALL)
        
        return html


class DependencyAnalyzer:
    """依赖分析器主类"""
    
    def __init__(self, project_root: str):
        """
        初始化依赖分析器
        
        Args:
            project_root: 项目根目录
        """
        self.project_root = project_root
        self.graph = None
    
    def analyze(self, file_analyses: List[Dict]) -> Dict[str, Any]:
        """
        执行依赖分析
        
        Args:
            file_analyses: 文件分析结果列表
            
        Returns:
            Dict[str, Any]: 分析结果
        """
        logger.info("开始依赖分析")
        
        # 构建依赖图
        builder = DependencyGraphBuilder(self.project_root)
        self.graph = builder.build_graph(file_analyses)
        
        # 生成报告
        report_generator = DependencyReportGenerator(self.graph)
        report = report_generator.generate_report('markdown')
        
        # 循环依赖检测
        cycle_detector = CycleDetector(self.graph)
        cycles = cycle_detector.detect_cycles()
        
        # 耦合度分析
        coupling_analyzer = CouplingAnalyzer(self.graph)
        coupling_analysis = coupling_analyzer.analyze_coupling()
        
        result = {
            'graph': self.graph,
            'report': report,
            'cycles': {
                'detected': len(cycles),
                'list': [c[:-1] for c in cycles],
                'details': cycle_detector.get_cycle_details(cycles)
            },
            'coupling': coupling_analysis,
            'metrics': {
                'total_modules': len(self.graph.nodes),
                'total_dependencies': len(self.graph.edges),
                'core_modules': self.graph.metadata.get('core_modules', []),
                'average_coupling': self.graph.metadata.get('average_coupling', 0)
            }
        }
        
        logger.info("依赖分析完成")
        
        return result
    
    def export_graph(self, output_path: str, format: str = 'png'):
        """
        导出依赖图
        
        Args:
            output_path: 输出路径
            format: 输出格式
        """
        if not self.graph:
            raise ValueError("请先执行分析")
        
        visualizer = DependencyVisualizer(self.graph)
        visualizer.generate_graph_image(output_path, format)


def main():
    """
    主函数，命令行入口点
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description='模块依赖分析器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 从JSON文件加载分析结果
  python dependency_analyzer.py --input analysis.json --output report.md
  
  # 生成依赖图
  python dependency_analyzer.py --input analysis.json --graph output.png
  
  # 只检测循环依赖
  python dependency_analyzer.py --input analysis.json --detect-cycles
        """
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入文件路径（JSON格式）')
    parser.add_argument('--output', '-o', help='输出报告路径')
    parser.add_argument('--graph', '-g', help='输出图形文件路径')
    parser.add_argument('--format', choices=['png', 'svg', 'pdf'], default='png',
                       help='图形格式（默认: png）')
    parser.add_argument('--detect-cycles', action='store_true',
                       help='只检测循环依赖')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='显示详细输出')
    
    args = parser.parse_args()
    
    # 配置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 加载分析结果
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 初始化分析器
    project_root = data.get('project_info', {}).get('path', '.')
    analyzer = DependencyAnalyzer(project_root)
    
    # 执行分析
    file_analyses = data.get('file_analysis', [])
    result = analyzer.analyze(file_analyses)
    
    if args.detect_cycles:
        print(f"检测到 {result['cycles']['detected']} 个循环依赖:")
        for i, cycle in enumerate(result['cycles']['list'], 1):
            print(f"  {i}. {' -> '.join(cycle)}")
    else:
        # 输出报告
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result['report'])
            print(f"报告已保存到: {args.output}")
        else:
            print(result['report'])
        
        # 生成依赖图
        if args.graph:
            analyzer.export_graph(args.graph, args.format)
            print(f"依赖图已保存到: {args.graph}")


if __name__ == '__main__':
    main()
