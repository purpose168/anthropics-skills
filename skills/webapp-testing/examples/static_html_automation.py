from playwright.sync_api import sync_playwright
import os

# 示例：使用file:// URL对静态HTML文件进行自动化交互

html_file_path = os.path.abspath('path/to/your/file.html')
file_url = f'file://{html_file_path}'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})

    # 导航到本地HTML文件
    page.goto(file_url)

    # 截图
    page.screenshot(path='/mnt/user-data/outputs/static_page.png', full_page=True)

    # 与元素交互
    page.click('text=Click Me')
    page.fill('#name', 'John Doe')
    page.fill('#email', 'john@example.com')

    # 提交表单
    page.click('button[type="submit"]')
    page.wait_for_timeout(500)

    # 截图最终结果
    page.screenshot(path='/mnt/user-data/outputs/after_submit.png', full_page=True)

    browser.close()

print("静态HTML自动化完成！")