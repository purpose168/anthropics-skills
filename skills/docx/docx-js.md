# DOCX 库教程

使用 JavaScript/TypeScript 生成 .docx 文件。

**重要提示：在开始之前请阅读整个文档。** 关键格式规则和常见陷阱贯穿全文——跳过部分可能会导致文件损坏或渲染问题。

## 设置
假设 docx 已经全局安装
如果未安装：`npm install -g docx`

```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun, Media, 
        Header, Footer, AlignmentType, PageOrientation, LevelFormat, ExternalHyperlink, 
        InternalHyperlink, TableOfContents, HeadingLevel, BorderStyle, WidthType, TabStopType, 
        TabStopPosition, UnderlineType, ShadingType, VerticalAlign, SymbolRun, PageNumber,
        FootnoteReferenceRun, Footnote, PageBreak } = require('docx');

// 创建并保存
const doc = new Document({ sections: [{ children: [/* 内容 */] }] });
Packer.toBuffer(doc).then(buffer => fs.writeFileSync("doc.docx", buffer)); // Node.js
Packer.toBlob(doc).then(blob => { /* 下载逻辑 */ }); // 浏览器
```

## 文本与格式
```javascript
// 重要提示：永远不要使用 \n 进行换行 - 始终使用独立的 Paragraph 元素
// ❌ 错误：new TextRun("第一行\n第二行")
// ✅ 正确：new Paragraph({ children: [new TextRun("第一行")] }), new Paragraph({ children: [new TextRun("第二行")] })

// 带所有格式选项的基本文本
new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 200, after: 200 },
  indent: { left: 720, right: 720 },
  children: [
    new TextRun({ text: "Bold", bold: true }),
    new TextRun({ text: "Italic", italics: true }),
    new TextRun({ text: "Underlined", underline: { type: UnderlineType.DOUBLE, color: "FF0000" } }),
    new TextRun({ text: "Colored", color: "FF0000", size: 28, font: "Arial" }), // Arial default
    new TextRun({ text: "Highlighted", highlight: "yellow" }),
    new TextRun({ text: "Strikethrough", strike: true }),
    new TextRun({ text: "x2", superScript: true }),
    new TextRun({ text: "H2O", subScript: true }),
    new TextRun({ text: "SMALL CAPS", smallCaps: true }),
    new SymbolRun({ char: "2022", font: "Symbol" }), // Bullet •
    new SymbolRun({ char: "00A9", font: "Arial" })   // Copyright © - Arial for symbols
  ]
})
```

## 样式与专业格式

```javascript
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } }, // 默认 12pt
    paragraphStyles: [
      // 文档标题样式 - 覆盖内置的 Title 样式
      { id: "Title", name: "Title", basedOn: "Normal",
        run: { size: 56, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 240, after: 120 }, alignment: AlignmentType.CENTER } },
      // 重要提示：通过使用精确的 ID 覆盖内置标题样式
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, color: "000000", font: "Arial" }, // 16pt
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } }, // TOC 需要
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, color: "000000", font: "Arial" }, // 14pt
        paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 } },
      // 自定义样式使用你自己的 ID
      { id: "myStyle", name: "My Style", basedOn: "Normal",
        run: { size: 28, bold: true, color: "000000" },
        paragraph: { spacing: { after: 120 }, alignment: AlignmentType.CENTER } }
    ],
    characterStyles: [{ id: "myCharStyle", name: "My Char Style",
      run: { color: "FF0000", bold: true, underline: { type: UnderlineType.SINGLE } } }]
  },
  sections: [{
    properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    children: [
      new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("Document Title")] }), // Uses overridden Title style
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Heading 1")] }), // Uses overridden Heading1 style
      new Paragraph({ style: "myStyle", children: [new TextRun("Custom paragraph style")] }),
      new Paragraph({ children: [
        new TextRun("Normal with "),
        new TextRun({ text: "custom char style", style: "myCharStyle" })
      ]})
    ]
  }]
});
```

**专业字体组合：**
- **Arial（标题）+ Arial（正文）** - 最通用支持，简洁专业
- **Times New Roman（标题）+ Arial（正文）** - 经典衬线标题配现代无衬线正文
- **Georgia（标题）+ Verdana（正文）** - 优化屏幕阅读，对比优雅

**关键样式原则：**
- **覆盖内置样式**：使用精确 ID 如"Heading1"、"Heading2"、"Heading3"覆盖 Word 的内置标题样式
- **HeadingLevel 常量**：`HeadingLevel.HEADING_1` 使用"Heading1"样式，`HeadingLevel.HEADING_2` 使用"Heading2"样式等
- **包含 outlineLevel**：为 H1 设置 `outlineLevel: 0`，为 H2 设置 `outlineLevel: 1` 等，以确保 TOC 正常工作
- **使用自定义样式**而非内联格式以保持一致性
- **设置默认字体**使用 `styles.default.document.run.font` - Arial 被普遍支持
- **建立视觉层次**使用不同的字体大小（标题 > 标题 > 正文）
- **添加适当的间距**使用 `before` 和 `after` 段落间距
- **谨慎使用颜色**：标题和标题默认使用黑色（000000）和灰色色调（标题 1、标题 2 等）
- **设置一致的边距**（1440 = 1 英寸是标准）


## 列表（始终使用正确的列表 - 永远不要使用 Unicode 项目符号）
```javascript
// 项目符号 - 始终使用编号配置，而不是 unicode 符号
// 关键提示：使用 LevelFormat.BULLET 常量，而不是字符串 "bullet"
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullet-list",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "first-numbered-list",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "second-numbered-list", // 不同的引用 = 重新从 1 开始
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }
    ]
  },
  sections: [{
    children: [
      // 项目符号列表项
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("第一个项目符号点")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("第二个项目符号点")] }),
      // 编号列表项
      new Paragraph({ numbering: { reference: "first-numbered-list", level: 0 },
        children: [new TextRun("第一个编号项")] }),
      new Paragraph({ numbering: { reference: "first-numbered-list", level: 0 },
        children: [new TextRun("第二个编号项")] }),
      // ⚠️ 关键提示：不同的引用 = 独立列表，从 1 重新开始
      // 相同的引用 = 继续之前的编号
      new Paragraph({ numbering: { reference: "second-numbered-list", level: 0 },
        children: [new TextRun("再次从 1 开始（因为引用不同）")] })
    ]
  }]
});

// ⚠️ 关键编号规则：每个引用创建一个独立的编号列表
// - 相同的引用 = 继续编号（1, 2, 3... 然后 4, 5, 6...）
// - 不同的引用 = 从 1 重新开始（1, 2, 3... 然后 1, 2, 3...）
// 对每个独立的编号部分使用唯一的引用名称！

// ⚠️ 关键提示：永远不要使用 unicode 项目符号 - 它们创建无法正常工作的假列表
// new TextRun("• 项目")           // 错误
// new SymbolRun({ char: "2022" }) // 错误
// ✅ 始终使用带有 LevelFormat.BULLET 的编号配置来创建真正的 Word 列表
```

## 表格
```javascript
// 完整表格，包含边距、边框、标题和项目符号
const tableBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const cellBorders = { top: tableBorder, bottom: tableBorder, left: tableBorder, right: tableBorder };

new Table({
  columnWidths: [4680, 4680], // ⚠️ 关键提示：在表格级别设置列宽 - 单位为 DXA（点的二十分之一）
  margins: { top: 100, bottom: 100, left: 180, right: 180 }, // 为所有单元格设置一次
  rows: [
    new TableRow({
      tableHeader: true,
      children: [
        new TableCell({
          borders: cellBorders,
          width: { size: 4680, type: WidthType.DXA }, // 也在每个单元格上设置宽度
          // ⚠️ 关键提示：始终使用 ShadingType.CLEAR 防止 Word 中的黑色背景。
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR }, 
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({ 
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: "标题", bold: true, size: 22 })]
          })]
        }),
        new TableCell({
          borders: cellBorders,
          width: { size: 4680, type: WidthType.DXA }, // 也在每个单元格上设置宽度
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
          children: [new Paragraph({ 
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: "项目符号点", bold: true, size: 22 })]
          })]
        })
      ]
    }),
    new TableRow({
      children: [
        new TableCell({
          borders: cellBorders,
          width: { size: 4680, type: WidthType.DXA }, // 也在每个单元格上设置宽度
          children: [new Paragraph({ children: [new TextRun("常规数据")] })]
        }),
        new TableCell({
          borders: cellBorders,
          width: { size: 4680, type: WidthType.DXA }, // 也在每个单元格上设置宽度
          children: [
            new Paragraph({ 
              numbering: { reference: "bullet-list", level: 0 },
              children: [new TextRun("第一个项目符号点")] 
            }),
            new Paragraph({ 
              numbering: { reference: "bullet-list", level: 0 },
              children: [new TextRun("第二个项目符号点")] 
            })
          ]
        })
      ]
    })
  ]
})
```

**重要提示：表格宽度和边框**
- 同时使用 `columnWidths: [width1, width2, ...]` 数组和在每个单元格上的 `width: { size: X, type: WidthType.DXA }`
- DXA 单位值（1440 = 1 英寸），信纸可用宽度 = 9360 DXA（1 英寸边距）
- 将边框应用到各个 `TableCell` 元素，而不是 `Table` 本身

**预计算列宽（信纸尺寸，1 英寸边距 = 9360 DXA 总宽度）：**
- **2 列：** `columnWidths: [4680, 4680]`（等宽）
- **3 列：** `columnWidths: [3120, 3120, 3120]`（等宽）

## 链接与导航
```javascript
// TOC（需要标题）关键提示：仅使用 HeadingLevel，而非自定义样式
// ❌ 错误：new Paragraph({ heading: HeadingLevel.HEADING_1, style: "customHeader", children: [new TextRun("标题")] })
// ✅ 正确：new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("标题")] })
new TableOfContents("目录", { hyperlink: true, headingStyleRange: "1-3" }),

// 外部链接
new Paragraph({
  children: [new ExternalHyperlink({
    children: [new TextRun({ text: "Google", style: "Hyperlink" })],
    link: "https://www.google.com"
  })]
}),

// 内部链接和书签
new Paragraph({
  children: [new InternalHyperlink({
    children: [new TextRun({ text: "转到章节", style: "Hyperlink" })],
    anchor: "section1"
  })]
}),
new Paragraph({
  children: [new TextRun("章节内容")],
  bookmark: { id: "section1", name: "section1" }
}),
```

## 图片与媒体
```javascript
// 带尺寸和定位的基本图片
// 关键提示：始终指定 'type' 参数 - 这是 ImageRun 必需的
new Paragraph({
  alignment: AlignmentType.CENTER,
  children: [new ImageRun({
    type: "png", // 新要求：必须指定图片类型（png、jpg、jpeg、gif、bmp、svg）
    data: fs.readFileSync("image.png"),
    transformation: { width: 200, height: 150, rotation: 0 }, // rotation 单位为度
    altText: { title: "Logo", description: "公司标志", name: "名称" } // 重要提示：所有三个字段都是必需的
  })]
})
```

## 分页符
```javascript
// 手动分页符
new Paragraph({ children: [new PageBreak()] }),

// 段落前的分页符
new Paragraph({
  pageBreakBefore: true,
  children: [new TextRun("这从新页面开始")]
})

// ⚠️ 关键提示：永远不要单独使用 PageBreak - 它会创建 Word 无法打开的无效 XML
// ❌ 错误：new PageBreak() 
// ✅ 正确：new Paragraph({ children: [new PageBreak()] })
```

## 页眉/页脚与页面设置
```javascript
const doc = new Document({
  sections: [{
    properties: {
      page: {
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }, // 1440 = 1 英寸
        size: { orientation: PageOrientation.LANDSCAPE },
        pageNumbers: { start: 1, formatType: "decimal" } // "upperRoman"、"lowerRoman"、"upperLetter"、"lowerLetter"
      }
    },
    headers: {
      default: new Header({ children: [new Paragraph({ 
        alignment: AlignmentType.RIGHT,
        children: [new TextRun("页眉文本")]
      })] })
    },
    footers: {
      default: new Footer({ children: [new Paragraph({ 
        alignment: AlignmentType.CENTER,
        children: [new TextRun("第 "), new TextRun({ children: [PageNumber.CURRENT] }), new TextRun(" 页，共 "), new TextRun({ children: [PageNumber.TOTAL_PAGES] }), new TextRun(" 页")]
      })] })
    },
    children: [/* 内容 */]
  }]
});
```

## 制表符
```javascript
new Paragraph({
  tabStops: [
    { type: TabStopType.LEFT, position: TabStopPosition.MAX / 4 },
    { type: TabStopType.CENTER, position: TabStopPosition.MAX / 2 },
    { type: TabStopType.RIGHT, position: TabStopPosition.MAX * 3 / 4 }
  ],
  children: [new TextRun("左\t中\t右")]
})
```

## 常量与快速参考
- **下划线：** `SINGLE`、`DOUBLE`、`WAVY`、`DASH`
- **边框：** `SINGLE`、`DOUBLE`、`DASHED`、`DOTTED`  
- **编号：** `DECIMAL`（1,2,3）、`UPPER_ROMAN`（I,II,III）、`LOWER_LETTER`（a,b,c）
- **制表符：** `LEFT`、`CENTER`、`RIGHT`、`DECIMAL`
- **符号：** `"2022"`（•）、`"00A9"`（©）、`"00AE"`（®）、`"2122"`（™）、`"00B0"`（°）、`"F070"`（✓）、`"F0FC"`（✗）

## 关键问题与常见错误
- **关键提示：PageBreak 必须始终在 Paragraph 内部** - 单独的 PageBreak 创建 Word 无法打开的无效 XML
- **始终为表格单元格使用 ShadingType.CLEAR** - 不要使用 ShadingType.SOLID（会导致黑色背景）。
- DXA 单位测量（1440 = 1 英寸）| 每个表格单元格需要至少 1 个段落 | TOC 仅需要 HeadingLevel 样式
- **始终使用带 Arial 字体的自定义样式**以获得专业外观和正确的视觉层次
- **始终使用 `styles.default.document.run.font` 设置默认字体** - 推荐 Arial
- **始终为表格使用 columnWidths 数组** + 单个单元格宽度以保持兼容性
- **永远不要使用 unicode 符号作为项目符号** - 始终使用带有 `LevelFormat.BULLET` 常量（不是字符串 "bullet"）的正确编号配置
- **永远不要在任何地方使用 \n 进行换行** - 始终对每行使用独立的 Paragraph 元素
- **始终在 Paragraph children 中使用 TextRun 对象** - 不要直接在 Paragraph 上使用 text 属性
- **图片关键提示**：ImageRun 需要 `type` 参数 - 始终指定 "png"、"jpg"、"jpeg"、"gif"、"bmp" 或 "svg"
- **项目符号关键提示**：必须使用 `LevelFormat.BULLET` 常量，而不是字符串 "bullet"，并包含 `text: "•"` 作为项目符号字符
- **编号关键提示**：每个编号引用创建一个独立的列表。相同的引用 = 继续编号（1,2,3 然后 4,5,6）。不同的引用 = 从 1 重新开始（1,2,3 然后 1,2,3）。对每个独立的编号部分使用唯一的引用名称！
- **TOC 关键提示**：使用 TableOfContents 时，标题必须仅使用 HeadingLevel - 不要向标题段落添加自定义样式，否则 TOC 将损坏
- **表格**：设置 `columnWidths` 数组 + 单个单元格宽度，将边框应用到单元格而不是表格
- **在 TABLE 级别设置表格边距**以获得一致的单元格填充（避免每个单元格重复）
