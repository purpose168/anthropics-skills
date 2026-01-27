---
name: docx
description: "全面的文档创建、编辑和分析功能，支持修订跟踪、批注、格式保留和文本提取。当大型语言模型需要处理专业文档（.docx文件）时使用，包括：(1) 创建新文档，(2) 修改或编辑内容，(3) 处理修订跟踪，(4) 添加批注，或任何其他文档任务"
license: Proprietary. LICENSE.txt has complete terms
---

# DOCX 创建、编辑和分析

## 概述

用户可能要求你创建、编辑或分析 .docx 文件的内容。.docx 文件本质上是一个包含 XML 文件和其他资源的 ZIP 存档，你可以读取或编辑它们。针对不同的任务，有不同的工具和工作流程可用。

## 工作流程决策树

### 读取/分析内容
使用下面的"文本提取"或"原始 XML 访问"部分

### 创建新文档
使用"创建新的 Word 文档"工作流程

### 编辑现有文档
- **你自己的文档 + 简单更改**
  使用"基本 OOXML 编辑"工作流程

- **他人的文档**
  使用**"修订标记工作流程"**（推荐默认）

- **法律、学术、商业或政府文档**
  使用**"修订标记工作流程"**（必需）

## 读取和分析内容

### 文本提取
如果你只需要读取文档的文本内容，应该使用 pandoc 将文档转换为 markdown。Pandoc 提供了出色的文档结构保留支持，并可以显示修订跟踪：

```bash
# 将文档转换为带修订跟踪的 markdown
pandoc --track-changes=all 文档路径.docx -o 输出.md
# 选项：--track-changes=accept/reject/all
```

### 原始 XML 访问
你需要原始 XML 访问权限的情况包括：批注、复杂格式、文档结构、嵌入媒体和元数据。对于这些功能中的任何一个，你需要解包文档并读取其原始 XML 内容。

#### 解包文件
`python ooxml/scripts/unpack.py <office_file> <output_directory>`

#### 关键文件结构
* `word/document.xml` - 主文档内容
* `word/comments.xml` - 文档中引用的批注
* `word/media/` - 嵌入的图片和媒体文件
* 修订跟踪使用 `<w:ins>`（插入）和 `<w:del>`（删除）标签

## 创建新的 Word 文档

从头开始创建新的 Word 文档时，使用 **docx-js**，它允许你使用 JavaScript/TypeScript 创建 Word 文档。

### 工作流程
1. **必须 - 阅读整个文件**：从头到尾完整阅读 [`docx-js.md`](docx-js.md)（约500行）。**阅读此文件时切勿设置范围限制。** 在继续创建文档之前，请阅读完整的文件内容以了解详细语法、关键格式规则和最佳实践。
2. 使用 Document、Paragraph、TextRun 组件创建 JavaScript/TypeScript 文件（你可以假设所有依赖项都已安装，但如果不存在，请参阅下面的依赖项部分）
3. 使用 Packer.toBuffer() 导出为 .docx

## 编辑现有的 Word 文档

编辑现有的 Word 文档时，使用 **Document 库**（用于 OOXML 操作的 Python 库）。该库自动处理基础设施设置并提供文档操作方法。对于复杂场景，你可以通过该库直接访问底层 DOM。

### 工作流程
1. **必须 - 阅读整个文件**：从头到尾完整阅读 [`ooxml.md`](ooxml.md)（约600行）。**阅读此文件时切勿设置范围限制。** 阅读完整的文件内容以了解 Document 库 API 和直接编辑文档文件的 XML 模式。
2. 解包文档：`python ooxml/scripts/unpack.py <office_file> <output_directory>`
3. 创建并运行使用 Document 库的 Python 脚本（参见 ooxml.md 中的"Document 库"部分）
4. 打包最终文档：`python ooxml/scripts/pack.py <input_directory> <office_file>`

Document 库同时提供了用于常见操作的高级方法和用于复杂场景的直接 DOM 访问。

## 用于文档审阅的修订标记工作流程

此工作流程允许你在 OOXML 中实现修订跟踪之前，使用 markdown 规划全面的修订跟踪。**关键要点**：要实现完整的修订跟踪，你必须系统地实现所有更改。

**批处理策略**：将相关更改分组为 3-10 个更改的批次。这使调试易于管理，同时保持效率。在进行下一批之前测试每一批。

**原则：最小化、精确的编辑**
在实现修订跟踪时，只标记实际更改的文本。重复未更改的文本会使编辑更难审阅，且显得不专业。将替换分解为：[未更改的文本] + [删除] + [插入] + [未更改的文本]。通过从原始文本中提取 `<w:r>` 元素并重用它来保留原始 run 的 RSID。

示例 - 将句子中的"30 days"改为"60 days"：
```python
# 不良做法 - 替换整个句子
'<w:del><w:r><w:delText>The term is 30 days.</w:delText></w:r></w:del><w:ins><w:r><w:t>The term is 60 days.</w:t></w:r></w:ins>'

# 良好做法 - 只标记更改的部分，为未更改的文本保留原始 <w:r>
'<w:r w:rsidR="00AB12CD"><w:t>The term is </w:t></w:r><w:del><w:r><w:delText>30</w:delText></w:r></w:del><w:ins><w:r><w:t>60</w:t></w:r></w:ins><w:r w:rsidR="00AB12CD"><w:t> days.</w:t></w:r>'
```

### 修订跟踪工作流程

1. **获取 markdown 表示形式**：将文档转换为保留修订跟踪的 markdown：
   ```bash
   pandoc --track-changes=all 文档路径.docx -o 当前.md
   ```

2. **识别并分组更改**：审阅文档并识别所有需要的更改，将其组织成逻辑批次：

   **定位方法**（用于在 XML 中查找更改）：
   - 部分/标题编号（例如，"第3.2节"、"第四条"）
   - 如果已编号的段落标识符
   - 带唯一周围文本的 Grep 模式
   - 文档结构（例如，"第一段"、"签名块"）
   - **不要使用 markdown 行号** - 它们与 XML 结构不对应

   **批次组织**（每批分组 3-10 个相关更改）：
   - 按部分："批次1：第2节修订"、"批次2：第5节更新"
   - 按类型："批次1：日期更正"、"批次2：当事方名称更改"
   - 按复杂性：从简单的文本替换开始，然后处理复杂的结构更改
   - 顺序："批次1：第1-3页"、"批次2：第4-6页"

3. **阅读文档并解包**：
   - **必须 - 阅读整个文件**：从头到尾完整阅读 [`ooxml.md`](ooxml.md)（约600行）。**阅读此文件时切勿设置范围限制。** 特别关注"Document 库"和"修订跟踪模式"部分。
   - **解包文档**：`python ooxml/scripts/unpack.py <文件.docx> <目录>`
   - **注意建议的 RSID**：解包脚本将建议一个用于你的修订跟踪的 RSID。复制此 RSID 以在步骤 4b 中使用。

4. **分批实现更改**：逻辑上分组更改（按部分、按类型或按接近程度）并在单个脚本中一起实现。这种方法：
   - 使调试更容易（较小的批次 = 更容易隔离错误）
   - 允许增量进度
   - 保持效率（3-10 个更改的批次效果很好）

   **建议的批次分组**：
   - 按文档部分（例如，"第3节更改"、"定义"、"终止条款"）
   - 按更改类型（例如，"日期更改"、"当事方名称更新"、"法律术语替换"）
   - 按接近程度（例如，"第1-3页的更改"、"文档前半部分的更改"）

   对于每一批相关更改：

   **a. 将文本映射到 XML**：在 `word/document.xml` 中 grep 文本，以验证文本如何跨 `<w:r>` 元素拆分。

   **b. 创建并运行脚本**：使用 `get_node` 查找节点，实现更改，然后使用 `doc.save()`。参见 ooxml.md 中的 **"Document 库"** 部分获取模式。

   **注意**：在编写脚本之前，立即 grep `word/document.xml` 以获取当前行号并验证文本内容。每次脚本运行后行号都会更改。

5. **打包文档**：所有批次完成后，将解包的目录转换回 .docx：
   ```bash
   python ooxml/scripts/pack.py 解包的目录 审阅后的文档.docx
   ```

6. **最终验证**：对完整文档进行全面检查：
   - 将最终文档转换为 markdown：
     ```bash
     pandoc --track-changes=all 审阅后的文档.docx -o 验证.md
     ```
   - 验证所有更改是否正确应用：
     ```bash
     grep "原始短语" 验证.md  # 应该找不到
     grep "替换短语" 验证.md  # 应该找到
     ```
   - 检查是否引入了任何意外的更改

## 将文档转换为图像

要直观地分析 Word 文档，请使用两步过程将其转换为图像：

1. **将 DOCX 转换为 PDF**：
   ```bash
   soffice --headless --convert-to pdf 文档.docx
   ```

2. **将 PDF 页面转换为 JPEG 图像**：
   ```bash
   pdftoppm -jpeg -r 150 文档.pdf 页面
   ```
   这将创建 `page-1.jpg`、`page-2.jpg` 等文件。

选项：
- `-r 150`：设置分辨率为 150 DPI（根据质量/大小平衡进行调整）
- `-jpeg`：输出 JPEG 格式（如果需要 PNG，使用 `-png`）
- `-f N`：要转换的第一页（例如，`-f 2` 从第2页开始）
- `-l N`：要转换的最后一页（例如，`-l 5` 在第5页停止）
- `page`：输出文件的前缀

特定范围的示例：
```bash
pdftoppm -jpeg -r 150 -f 2 -l 5 文档.pdf 页面  # 只转换第2-5页
```

## 代码风格指南
**重要提示**：生成 DOCX 操作的代码时：
- 编写简洁的代码
- 避免冗长的变量名和冗余操作
- 避免不必要的打印语句

## 依赖项

所需的依赖项（如果不可用则安装）：

- **pandoc**：`sudo apt-get install pandoc`（用于文本提取）
- **docx**：`npm install -g docx`（用于创建新文档）
- **LibreOffice**：`sudo apt-get install libreoffice`（用于 PDF 转换）
- **Poppler**：`sudo apt-get install poppler-utils`（用于 pdftoppm 将 PDF 转换为图像）
- **defusedxml**：`pip install defusedxml`（用于安全的 XML 解析）
