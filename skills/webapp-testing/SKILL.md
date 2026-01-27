---
name: webapp-testing
description: 使用Playwright与本地Web应用程序进行交互和测试的工具包。支持验证前端功能、调试UI行为、捕获浏览器截图和查看浏览器日志。
license: Complete terms in LICENSE.txt
---

# Web应用程序测试

要测试本地Web应用程序，请编写原生Python Playwright脚本。

**可用的辅助脚本**：
- `scripts/with_server.py` - 管理服务器生命周期（支持多个服务器）

**始终先使用 `--help` 运行脚本以查看用法**。在尝试运行脚本并发现确实需要定制解决方案之前，不要阅读源代码。这些脚本可能非常大，会污染您的上下文窗口。它们存在是为了被直接调用作为黑盒脚本，而不是被摄入到您的上下文窗口中。

## 决策树：选择您的方法

```
用户任务 → 是静态HTML吗？
    ├─ 是 → 直接读取HTML文件以识别选择器
    │         ├─ 成功 → 使用选择器编写Playwright脚本
    │         └─ 失败/不完整 → 按动态方式处理（如下）
    │
    └─ 否（动态Web应用）→ 服务器已经在运行吗？
        ├─ 否 → 运行: python scripts/with_server.py --help
        │        然后使用辅助脚本 + 编写简化的Playwright脚本
        │
        └─ 是 → 侦察后行动模式：
            1. 导航并等待networkidle
            2. 截图或检查DOM
            3. 从渲染状态中识别选择器
            4. 使用发现的选择器执行操作
```

## 示例：使用with_server.py

要启动服务器，请先运行 `--help`，然后使用辅助脚本：

**单个服务器：**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**多个服务器（例如：后端 + 前端）：**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

要创建自动化脚本，只需包含Playwright逻辑（服务器自动管理）：
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # 始终以无头模式启动chromium
    page = browser.new_page()
    page.goto('http://localhost:5173')  # 服务器已运行并就绪
    page.wait_for_load_state('networkidle')  # 关键：等待JS执行完成
    # ... 您的自动化逻辑
    browser.close()
```

## 侦察后行动模式

1. **检查渲染的DOM**：
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **从检查结果中识别选择器**

3. **使用发现的选择器执行操作**

## 常见陷阱

❌ **不要**在动态应用上等待`networkidle`之前检查DOM
✅ **应该**在检查之前等待`page.wait_for_load_state('networkidle')`

## 最佳实践

- **将捆绑脚本用作黑盒** - 要完成任务，考虑是否可以使用`scripts/`中可用的脚本之一。这些脚本可靠地处理常见的复杂工作流程，而不会弄乱上下文窗口。使用`--help`查看用法，然后直接调用。
- 对同步脚本使用`sync_playwright()`
- 完成后始终关闭浏览器
- 使用描述性选择器：`text=`、`role=`、CSS选择器或ID
- 添加适当的等待：`page.wait_for_selector()`或`page.wait_for_timeout()`

## 参考文件

- **examples/** - 显示常见模式的示例：
  - `element_discovery.py` - 发现页面上的按钮、链接和输入框
  - `static_html_automation.py` - 对本地HTML使用file:// URL
  - `console_logging.py` - 在自动化期间捕获控制台日志