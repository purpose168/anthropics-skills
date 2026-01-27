---
name: xlsx
description: "全面的电子表格创建、编辑和分析，支持公式、格式化、数据分析和可视化。当大型语言模型需要处理电子表格（.xlsx、.xlsm、.csv、.tsv等）时：（1）创建带有公式和格式化的新电子表格；（2）读取或分析数据；（3）修改现有电子表格同时保留公式；（4）电子表格中的数据分析和可视化；（5）重新计算公式"
license: Proprietary。LICENSE.txt包含完整条款
---

# 输出要求

## 所有Excel文件

### 零公式错误
- 每个Excel模型必须以零公式错误交付（#REF!、#DIV/0!、#VALUE!、#N/A、#NAME?）

### 保留现有模板（在更新模板时）
- 修改文件时研究和精确匹配现有格式、样式和约定
- 切勿对具有既定模式的文件施加标准化格式
- 现有模板约定始终优先于这些准则

## 财务模型

### 颜色编码标准
除非用户或现有模板另有说明

#### 行业标准颜色约定
- **蓝色文本（RGB: 0,0,255）**：硬编码输入，以及用户将针对场景更改的数字
- **黑色文本（RGB: 0,0,0）**：所有公式和计算
- **绿色文本（RGB: 0,128,0)**: 从同一工作簿的其他工作表中提取的链接
- **红色文本（RGB: 255,0,0)**: 到其他文件的外部链接
- **黄色背景（RGB: 255,255,0)**: 需要注意的关键假设或需要更新的单元格

### 数字格式标准

#### 必需的格式规则
- **年份**：格式化为文本字符串（例如，"2024"而非"2,024"）
- **货币**：使用$#,##0格式；在标题中始终指定单位（"收入（百万美元）"）
- **零**：使用数字格式使所有零显示为"-"，包括百分比（例如，"$#,##0;($#,##0);-"）
- **百分比**：默认使用0.0%格式（一位小数）
- **倍数**：估值倍数格式化为0.0x（EV/EBITDA、市盈率）
- **负数**：使用括号(123)而非减号-123

### 公式构建规则

#### 假设放置
- 将所有假设（增长率、利润率、倍数等）放在单独的假设单元格中
- 在公式中使用单元格引用而非硬编码值
- 示例：使用 =B5*(1+$B$6) 而非 =B5*1.05

#### 公式错误预防
- 验证所有单元格引用正确
- 检查范围中的差一错误
- 确保所有预测期间的公式一致
- 测试边界情况（零值、负数）
- 验证无意外的循环引用

#### 硬编码的文档要求
- 在单元格旁边注释或注明（如果在表格末尾）。格式："来源：[系统/文档]，[日期]，[具体参考]，[URL如果适用]"
- 示例：
  - "来源：公司10-K报告，2024财年，第45页，收入说明，[SEC EDGAR网址]"
  - "来源：公司10-Q报告，2025年第二季度，附件99.1，[SEC EDGAR网址]"
  - "来源：彭博终端，2025年8月15日，AAPL US Equity"
  - "来源：FactSet，2025年8月20日，共识估计屏幕"

# XLSX创建、编辑和分析

## 概述

用户可能要求您创建、编辑或分析.xlsx文件的内容。不同任务有不同的工具和工作流程。

## 重要要求

**公式重算需要LibreOffice**：您可以假设LibreOffice已安装，使用`recalc.py`脚本重新计算公式值。该脚本在首次运行时自动配置LibreOffice

## 读取和分析数据

### 使用pandas进行数据分析
对于数据分析、可视化和基本操作，使用**pandas**，它提供强大的数据处理能力：

```python
import pandas as pd

# 读取Excel
df = pd.read_excel('file.xlsx')  # 默认：第一个工作表
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # 所有工作表作为字典

# 分析
df.head()      # 预览数据
df.info()      # 列信息
df.describe()  # 统计信息

# 写入Excel
df.to_excel('output.xlsx', index=False)
```

## Excel文件工作流程

## 关键：使用公式，而非硬编码值

**始终使用Excel公式而非在Python中计算值并硬编码。** 这确保电子表格保持动态可更新。

### ❌ 错误 - 硬编码计算值
```python
# 错误：在Python中计算并硬编码结果
total = df['销售额'].sum()
sheet['B10'] = total  # 硬编码5000

# 错误：在Python中计算增长率
growth = (df.iloc[-1]['收入'] - df.iloc[0]['收入']) / df.iloc[0]['收入']
sheet['C5'] = growth  # 硬编码0.15

# 错误：Python计算平均值
avg = sum(values) / len(values)
sheet['D20'] = avg  # 硬编码42.5
```

### ✅ 正确 - 使用Excel公式
```python
# 正确：让Excel计算总和
sheet['B10'] = '=SUM(B2:B9)'

# 正确：增长率作为Excel公式
sheet['C5'] = '=(C4-C2)/C2'

# 正确：使用Excel函数计算平均值
sheet['D20'] = '=AVERAGE(D2:D19)'
```

这适用于所有计算 - 总计、百分比、比率、差异等。电子表格应该在源数据更改时能够重新计算。

## 常见工作流程
1. **选择工具**：pandas用于数据，openpyxl用于公式/格式化
2. **创建/加载**：创建新工作簿或加载现有文件
3. **修改**：添加/编辑数据、公式和格式化
4. **保存**：写入文件
5. **重新计算公式（如果使用公式则强制）**：使用recalc.py脚本
   ```bash
   python recalc.py output.xlsx
   ```
6. **验证并修复任何错误**：
   - 脚本返回包含错误详细信息的JSON
   - 如果`status`为`errors_found`，检查`error_summary`获取特定错误类型和位置
   - 修复识别的错误并重新计算
   - 常见错误修复：
     - `#REF!`：无效的单元格引用
     - `#DIV/0!`：除以零
     - `#VALUE!`：公式中的数据类型错误
     - `#NAME?`：无法识别的公式名称

### 创建新的Excel文件

```python
# 使用openpyxl处理公式和格式化
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

# 添加数据
sheet['A1'] = '您好'
sheet['B1'] = '世界'
sheet.append(['行', '的', '数据'])

# 添加公式
sheet['B2'] = '=SUM(A1:A10)'

# 格式化
sheet['A1'].font = Font(bold=True, color='FF0000')
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')
sheet['A1'].alignment = Alignment(horizontal='center')

# 列宽
sheet.column_dimensions['A'].width = 20

wb.save('output.xlsx')
```

### 编辑现有的Excel文件

```python
# 使用openpyxl保留公式和格式化
from openpyxl import load_workbook

# 加载现有文件
wb = load_workbook('existing.xlsx')
sheet = wb.active  # 或使用wb['工作表名称']指定工作表

# 处理多个工作表
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    print(f"工作表: {sheet_name}")

# 修改单元格
sheet['A1'] = '新值'
sheet.insert_rows(2)  # 在位置2插入行
sheet.delete_cols(3)  # 删除第3列

# 添加新工作表
new_sheet = wb.create_sheet('新工作表')
new_sheet['A1'] = '数据'

wb.save('modified.xlsx')
```

## 重新计算公式

由openpyxl创建或修改的Excel文件包含公式字符串但未计算值。使用提供的`recalc.py`脚本重新计算公式：

```bash
python recalc.py <excel_file> [timeout_seconds]
```

示例：
```bash
python recalc.py output.xlsx 30
```

该脚本：
- 首次运行时自动设置LibreOffice宏
- 重新计算所有工作表中的所有公式
- 扫描所有单元格中的Excel错误（#REF!、#DIV/0!等）
- 返回包含详细错误位置和计数的JSON
- 适用于Linux和macOS

## 公式验证清单

确保公式正确工作的快速检查：

### 基本验证
- [ ] **测试2-3个示例引用**：在构建完整模型之前验证它们提取正确的值
- [ ] **列映射**：确认Excel列匹配（例如，第64列=BL，而非BK）
- [ ] **行偏移**：记住Excel行是1索引的（DataFrame第5行=Excel第6行）

### 常见陷阱
- [ ] **NaN处理**：使用`pd.notna()`检查空值
- [ ] **最右边的列**：财务数据通常在第50列之后
- [ ] **多个匹配项**：搜索所有出现位置，而不仅仅是第一个
- [ ] **除以零**：在公式中使用"/"之前检查分母（#DIV/0!）
- [ ] **错误的引用**：验证所有单元格引用指向预期的单元格（#REF!）
- [ ] **跨工作表引用**：使用正确的格式（Sheet1!A1）链接工作表

### 公式测试策略
- [ ] **从小开始**：在广泛应用之前测试2-3个单元格的公式
- [ ] **验证依赖项**：检查公式中引用的所有单元格是否存在
- [ ] **测试边界情况**：包括零、负数和非常大的值

### 解释recalc.py输出
脚本返回包含错误详细信息的JSON：
```json
{
  "status": "success",           // 或 "errors_found"
  "total_errors": 0,              // 错误总数
  "total_formulas": 42,           // 文件中的公式数量
  "error_summary": {              // 仅在发现错误时存在
    "#REF!": {
      "count": 2,
      "locations": ["Sheet1!B5", "Sheet1!C10"]
    }
  }
}
```

## 最佳实践

### 库选择
- **pandas**：最适合数据分析、批量操作和简单的数据导出
- **openpyxl**：最适合复杂格式化、公式和Excel特定功能

### 使用openpyxl
- 单元格索引从1开始（row=1, column=1对应单元格A1）
- 使用`data_only=True`读取计算值：`load_workbook('file.xlsx', data_only=True)`
- **警告**：如果使用`data_only=True`打开并保存，公式将被值替换并永久丢失
- 对于大文件：使用`read_only=True`读取或`write_only=True`写入
- 公式保留但不计算值 - 使用recalc.py更新值

### 使用pandas
- 指定数据类型以避免推断问题：`pd.read_excel('file.xlsx', dtype={'id': str})`
- 对于大文件，读取特定列：`pd.read_excel('file.xlsx', usecols=['A', 'C', 'E'])`
- 正确处理日期：`pd.read_excel('file.xlsx', parse_dates=['date_column'])`

## 代码风格指南
**重要**：生成用于Excel操作的Python代码时：
- 编写简洁的Python代码，无需不必要的注释
- 避免冗长的变量名和冗余操作
- 避免不必要的print语句

**对于Excel文件本身**：
- 为复杂公式或重要假设添加单元格注释
- 记录硬编码值的数据来源
- 包含关键计算和模型部分的说明