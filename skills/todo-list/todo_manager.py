#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
待办列表管理器

这是待办列表技能的核心实现文件，包含以下功能：
1. 数据持久化存储
2. 添加待办事项
3. 查看所有待办事项
4. 标记待办事项为已完成
5. 删除待办事项
6. 修改现有待办事项
7. 自然语言指令处理
"""

import json
import os
import re
from datetime import datetime

class TodoManager:
    """待办列表管理器类"""
    
    def __init__(self, data_file="todo_data.json"):
        """
        初始化待办列表管理器
        
        Args:
            data_file (str): 数据存储文件路径
        """
        self.data_file = data_file
        self.todos = self.load_todos()
    
    def load_todos(self):
        """
        加载待办事项数据
        
        Returns:
            list: 待办事项列表
        """
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def save_todos(self):
        """
        保存待办事项数据到文件
        """
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.todos, f, ensure_ascii=False, indent=2)
            return True
        except IOError:
            return False
    
    def add_todo(self, content):
        """
        添加新的待办事项
        
        Args:
            content (str): 待办事项内容
            
        Returns:
            dict: 添加的待办事项
        """
        todo = {
            "id": len(self.todos) + 1,
            "content": content,
            "completed": False,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self.todos.append(todo)
        self.save_todos()
        return todo
    
    def get_all_todos(self):
        """
        获取所有待办事项
        
        Returns:
            list: 待办事项列表
        """
        return self.todos
    
    def mark_completed(self, todo_id):
        """
        标记待办事项为已完成
        
        Args:
            todo_id (int): 待办事项ID
            
        Returns:
            dict or None: 标记后的待办事项，找不到则返回None
        """
        for todo in self.todos:
            if todo["id"] == todo_id:
                todo["completed"] = True
                todo["updated_at"] = datetime.now().isoformat()
                self.save_todos()
                return todo
        return None
    
    def delete_todo(self, todo_id):
        """
        删除待办事项
        
        Args:
            todo_id (int): 待办事项ID
            
        Returns:
            bool: 删除是否成功
        """
        new_todos = [todo for todo in self.todos if todo["id"] != todo_id]
        if len(new_todos) < len(self.todos):
            self.todos = new_todos
            # 重新编号
            for i, todo in enumerate(self.todos, 1):
                todo["id"] = i
            self.save_todos()
            return True
        return False
    
    def update_todo(self, todo_id, new_content):
        """
        修改现有待办事项
        
        Args:
            todo_id (int): 待办事项ID
            new_content (str): 新的待办事项内容
            
        Returns:
            dict or None: 修改后的待办事项，找不到则返回None
        """
        for todo in self.todos:
            if todo["id"] == todo_id:
                todo["content"] = new_content
                todo["updated_at"] = datetime.now().isoformat()
                self.save_todos()
                return todo
        return None
    
    def process_natural_language(self, text):
        """
        处理自然语言指令
        
        Args:
            text (str): 用户输入的自然语言指令
            
        Returns:
            tuple: (操作类型, 操作结果, 消息)
        """
        original_text = text
        text_lower = text.lower().strip()
        
        # 汉字数字映射
        chinese_numbers = {
            '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
            '六': 6, '七': 7, '八': 8, '九': 9, '十': 10
        }
        
        # 1. 处理查看待办事项的指令
        view_keywords = ['查看', '显示', '列出', '我的']
        todo_keywords = ['待办', '任务', '列表']
        
        if any(keyword in text_lower for keyword in view_keywords) and any(keyword in text_lower for keyword in todo_keywords):
            todos = self.get_all_todos()
            return "view", todos, self.format_todos(todos)
        
        # 2. 处理添加待办事项的指令
        if '添加' in text or '新建' in text or '创建' in text or '我需要' in text or '我要' in text or '提醒我' in text:
            if '待办' in text or '任务' in text:
                # 提取冒号后的内容
                parts = re.split(r'[:：]', text, maxsplit=1)
                if len(parts) > 1:
                    content = parts[1].strip()
                    if content:
                        todo = self.add_todo(content)
                        return "add", todo, f"已添加待办事项：{content}"
            # 直接添加任务
            elif '任务' in text:
                parts = re.split(r'[:：]', text, maxsplit=1)
                if len(parts) > 1:
                    content = parts[1].strip()
                    if content:
                        todo = self.add_todo(content)
                        return "add", todo, f"已添加待办事项：{content}"
        
        # 3. 处理标记待办事项为已完成的指令
        if '完成' in text_lower or '标记' in text_lower:
            if '待办' in text_lower or '任务' in text_lower:
                # 查找数字（阿拉伯数字）
                match = re.search(r'第(\d+)个', text)
                if match:
                    todo_id = int(match.group(1))
                    todo = self.mark_completed(todo_id)
                    if todo:
                        return "complete", todo, f"已标记待办事项为已完成：{todo['content']}"
                    else:
                        return "error", None, f"找不到ID为{todo_id}的待办事项"
                # 查找数字（汉字数字）
                for chinese_num, num in chinese_numbers.items():
                    if f'第{chinese_num}个' in text:
                        todo_id = num
                        todo = self.mark_completed(todo_id)
                        if todo:
                            return "complete", todo, f"已标记待办事项为已完成：{todo['content']}"
                        else:
                            return "error", None, f"找不到ID为{todo_id}的待办事项"
                # 尝试通过内容查找
                if '完成' in text_lower:
                    # 提取任务内容
                    content = text_lower.replace('完成', '').replace('任务', '').strip()
                    if content:
                        for todo in self.todos:
                            if content in todo['content'].lower():
                                updated_todo = self.mark_completed(todo['id'])
                                return "complete", updated_todo, f"已标记待办事项为已完成：{updated_todo['content']}"
        
        # 4. 处理删除待办事项的指令
        if '删除' in text or '移除' in text:
            if '待办' in text or '任务' in text:
                # 查找数字（阿拉伯数字）
                match = re.search(r'第(\d+)个', text)
                if match:
                    todo_id = int(match.group(1))
                    success = self.delete_todo(todo_id)
                    if success:
                        return "delete", todo_id, f"已删除ID为{todo_id}的待办事项"
                    else:
                        return "error", None, f"找不到ID为{todo_id}的待办事项"
                # 查找数字（汉字数字）
                for chinese_num, num in chinese_numbers.items():
                    if f'第{chinese_num}个' in text:
                        todo_id = num
                        success = self.delete_todo(todo_id)
                        if success:
                            return "delete", todo_id, f"已删除ID为{todo_id}的待办事项"
                        else:
                            return "error", None, f"找不到ID为{todo_id}的待办事项"
                # 尝试通过内容查找
                else:
                    content = text.replace('删除', '').replace('移除', '').replace('待办事项', '').replace('任务', '').strip()
                    if content:
                        for todo in self.todos:
                            if content in todo['content']:
                                success = self.delete_todo(todo['id'])
                                if success:
                                    return "delete", todo['id'], f"已删除待办事项：{todo['content']}"
        
        # 5. 处理修改待办事项的指令
        if '修改' in text or '更新' in text:
            if '待办' in text or '任务' in text:
                # 查找数字（阿拉伯数字）和新内容
                match = re.search(r'第(\d+)个.*为[:：]?(.*)', text)
                if match and len(match.groups()) == 2:
                    todo_id = int(match.group(1))
                    new_content = match.group(2).strip()
                    if new_content:
                        todo = self.update_todo(todo_id, new_content)
                        if todo:
                            return "update", todo, f"已修改待办事项为：{new_content}"
                        else:
                            return "error", None, f"找不到ID为{todo_id}的待办事项"
                # 查找数字（汉字数字）和新内容
                for chinese_num, num in chinese_numbers.items():
                    if f'第{chinese_num}个' in text:
                        # 提取新内容
                        parts = re.split(r'为[:：]', text, maxsplit=1)
                        if len(parts) > 1:
                            new_content = parts[1].strip()
                            if new_content:
                                todo_id = num
                                todo = self.update_todo(todo_id, new_content)
                                if todo:
                                    return "update", todo, f"已修改待办事项为：{new_content}"
                                else:
                                    return "error", None, f"找不到ID为{todo_id}的待办事项"
        
        return "error", None, "抱歉，我没有理解您的指令。请尝试使用更明确的表达方式，例如：'添加待办事项：明天开会'或'查看所有待办事项'"
    
    def format_todos(self, todos):
        """
        格式化待办事项列表为可读字符串
        
        Args:
            todos (list): 待办事项列表
            
        Returns:
            str: 格式化后的字符串
        """
        if not todos:
            return "您的待办事项列表为空"
        
        result = "您的待办事项列表：\n"
        for i, todo in enumerate(todos, 1):
            status = "✓" if todo["completed"] else "✗"
            result += f"{i}. [{status}] {todo['content']}\n"
        return result

# 测试代码
if __name__ == "__main__":
    """测试待办列表管理器的功能"""
    manager = TodoManager()
    
    # 测试添加待办事项
    print("测试添加待办事项：")
    manager.add_todo("明天早上开会")
    manager.add_todo("去超市买东西")
    manager.add_todo("完成项目报告")
    
    # 测试查看待办事项
    print("\n测试查看待办事项：")
    todos = manager.get_all_todos()
    print(manager.format_todos(todos))
    
    # 测试标记待办事项为已完成
    print("\n测试标记待办事项为已完成：")
    manager.mark_completed(1)
    print(manager.format_todos(manager.get_all_todos()))
    
    # 测试修改待办事项
    print("\n测试修改待办事项：")
    manager.update_todo(2, "去超市买牛奶和鸡蛋")
    print(manager.format_todos(manager.get_all_todos()))
    
    # 测试删除待办事项
    print("\n测试删除待办事项：")
    manager.delete_todo(3)
    print(manager.format_todos(manager.get_all_todos()))
    
    # 测试自然语言处理
    print("\n测试自然语言处理：")
    test_commands = [
        "添加一个待办事项：后天去健身房",
        "查看所有待办事项",
        "完成第二个任务",
        "删除第一个待办事项",
        "修改第一个待办事项为：明天下午去健身房"
    ]
    
    for command in test_commands:
        print(f"\n输入：{command}")
        action, result, message = manager.process_natural_language(command)
        print(f"输出：{message}")
    
    # 清理测试数据
    if os.path.exists("todo_data.json"):
        os.remove("todo_data.json")
    print("\n测试完成，已清理测试数据")