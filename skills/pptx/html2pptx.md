# HTML 转 PowerPoint 指南

使用 `html2pptx.js` 库将 HTML 幻灯片转换为具有准确定位的 PowerPoint 演示文稿。

## 目录

1. [创建 HTML 幻灯片](#创建-html-幻灯片)
2. [使用 html2pptx 库](#使用-html2pptx-库)
3. [使用 PptxGenJS](#使用-pptxgenjs)

---

## 创建 HTML 幻灯片

每个 HTML 幻灯片必须包含适当的 body 尺寸：

### 布局尺寸

- **16:9**（默认）：`width: 720pt; height: 405pt`
- **4:3**：`width: 720pt; height: 540pt`
- **16:10**：`width: 720pt; height: 450pt`

### 支持的元素

- `<p>`、`<h1>`-`<h6>` - 带样式的文本
- `<ul>`、`<ol>` - 列表（永远不要使用手动项目符号 •、-、*）
- `<b>`、`<strong>` - 粗体文本（行内格式）
- `<i>`、`<em>` - 斜体文本（行内格式）
- `<u>` - 下划线文本（行内格式）
- `<span>` - 带 CSS 样式的行内格式（粗体、斜体、下划线、颜色）
- `<br>` - 换行
- `<div>` 带 bg/border - 变为形状
- `<img>` - 图片
- `class="placeholder"` - 图表的保留空间（返回 `{ id, x, y, w, h }`）

### 关键文本规则

**所有文本必须位于 `<p>`、`<h1>`-`<h6>`、`<ul>` 或 `<ol>` 标签内：**
- ✅ 正确：`<div><p>此处文本</p></div>`
- ❌ 错误：`<div>此处文本</div>` - **文本不会出现在 PowerPoint 中**
- ❌ 错误：`<span>文本</span>` - **文本不会出现在 PowerPoint 中**
- `<div>` 或 `<span>` 中没有文本标签的文本将被静默忽略

**永远不要使用手动项目符号（•、-、* 等）- 使用 `<ul>` 或 `<ol>` 列表代替**

**只使用普遍可用的网页安全字体：**
- ✅ 网页安全字体：`Arial`、`Helvetica`、`Times New Roman`、`Georgia`、`Courier New`、`Verdana`、`Tahoma`、`Trebuchet MS`、`Impact`、`Comic Sans MS`
- ❌ 错误：`'Segoe UI'`、`'SF Pro'`、`'Roboto'`、自定义字体 - **可能导致渲染问题**

### 样式

- 在 body 上使用 `display: flex` 以防止 margin collapse 破坏溢出验证
- 使用 `margin` 进行间距（padding 包含在尺寸内）
- 行内格式：使用 `<b>`、`<i>`、`<u>` 标签或带 CSS 样式的 `<span>`
  - `<span>` 支持：`font-weight: bold`、`font-style: italic`、`text-decoration: underline`、`color: #rrggbb`
  - `<span>` 不支持：`margin`、`padding`（PowerPoint 文本运行不支持）
  - 示例：`<span style="font-weight: bold; color: #667eea;">粗体蓝色文本</span>`
- Flexbox 有效 - 位置根据渲染布局计算
- 在 CSS 中使用带 `#` 前缀的十六进制颜色
- **文本对齐**：必要时使用 CSS `text-align`（`center`、`right` 等）作为 PptxGenJS 文本格式的提示，以防文本长度略有偏差

### 形状样式（仅限 DIV 元素）

**重要提示：背景、边框和阴影仅在 `<div>` 元素上有效，不在文本元素（`<p>`、`<h1>`-`<h6>`、`<ul>`、`<ol>`）上**

- **背景**：仅 `<div>` 元素上的 CSS `background` 或 `background-color`
  - 示例：`<div style="background: #f0f0f0;">` - 创建带背景的形状
- **边框**：`<div>` 元素上的 CSS `border` 转换为 PowerPoint 形状边框
  - 支持统一边框：`border: 2px solid #333333`
  - 支持部分边框：`border-left`、`border-right`、`border-top`、`border-bottom`（渲染为线条形状）
  - 示例：`<div style="border-left: 8pt solid #E76F51;">`
- **边框圆角**：`<div>` 元素上的 CSS `border-radius` 用于圆角
  - `border-radius: 50%` 或更高创建圆形
  - 小于 50% 的百分比相对于形状的较小尺寸计算
  - 支持 px 和 pt 单位（例如 `border-radius: 8pt;`、`border-radius: 12px;`）
  - 示例：在 100x200px 框上的 `<div style="border-radius: 25%;">` = 100px 的 25% = 25px 半径
- **阴影**：`<div>` 元素上的 CSS `box-shadow` 转换为 PowerPoint 阴影
  - 仅支持外部阴影（忽略内部阴影以防止损坏）
  - 示例：`<div style="box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);">`
  - 注意：PowerPoint 不支持内部/内阴影，将被跳过

### 图标和渐变

**重要提示：永远不要使用 CSS 渐变（`linear-gradient`、`radial-gradient`）- 它们不会转换为 PowerPoint**
**务必先使用 Sharp 创建渐变/图标 PNG，然后在 HTML 中引用**
- 对于渐变：将 SVG 光栅化为 PNG 背景图像
- 对于图标：将 react-icons SVG 光栅化为 PNG 图像
- 所有视觉效果必须在 HTML 渲染之前预先光栅化为栅格图像

**使用 Sharp 光栅化图标：**

```javascript
const React = require('react');
const ReactDOMServer = require('react-dom/server');
const sharp = require('sharp');
const { FaHome } = require('react-icons/fa');

async function rasterizeIconPng(IconComponent, color, size = "256", filename) {
  // 将图标组件渲染为静态 SVG 标记
  const svgString = ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color: `#${color}`, size: size })
  );

  // 使用 Sharp 将 SVG 转换为 PNG
  await sharp(Buffer.from(svgString))
    .png()
    .toFile(filename);

  return filename;
}

// 使用方法：先光栅化图标再用于 HTML
const iconPath = await rasterizeIconPng(FaHome, "4472c4", "256", "home-icon.png");
// 然后在 HTML 中引用：<img src="home-icon.png" style="width: 40pt; height: 40pt;">
```

**使用 Sharp 光栅化渐变：**

```javascript
const sharp = require('sharp');

async function createGradientBackground(filename) {
  // 创建渐变 SVG
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="562.5">
    <defs>
      <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#COLOR1"/>
        <stop offset="100%" style="stop-color:#COLOR2"/>
      </linearGradient>
    </defs>
    <rect width="100%" height="100%" fill="url(#g)"/>
  </svg>`;

  // 使用 Sharp 将 SVG 转换为 PNG
  await sharp(Buffer.from(svg))
    .png()
    .toFile(filename);

  return filename;
}

// 使用方法：先创建渐变背景再用于 HTML
const bgPath = await createGradientBackground("gradient-bg.png");
// 然后在 HTML 中：<body style="background-image: url('gradient-bg.png');">
```

### 示例

```html
<!DOCTYPE html>
<html>
<head>
<style>
html { background: #ffffff; }
body {
  width: 720pt; height: 405pt; margin: 0; padding: 0;
  background: #f5f5f5; font-family: Arial, sans-serif;
  display: flex;
}
.content { margin: 30pt; padding: 40pt; background: #ffffff; border-radius: 8pt; }
h1 { color: #2d3748; font-size: 32pt; }
.box {
  background: #70ad47; padding: 20pt; border: 3px solid #5a8f37;
  border-radius: 12pt; box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.25);
}
</style>
</head>
<body>
<div class="content">
  <h1>食谱标题</h1>
  <ul>
    <li><b>项目：</b>描述</li>
  </ul>
  <p>文本带 <b>粗体</b>、<i>斜体</i>、<u>下划线</u>。</p>
  <div id="chart" class="placeholder" style="width: 350pt; height: 200pt;"></div>

  <!-- 文本必须在 <p> 标签内 -->
  <div class="box">
    <p>5</p>
  </div>
</div>
</body>
</html>
```

## 使用 html2pptx 库

### 依赖项

这些库已全局安装，可以使用：
- `pptxgenjs`
- `playwright`
- `sharp`

### 基本用法

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require('./html2pptx');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';  // 必须与 HTML body 尺寸匹配

const { slide, placeholders } = await html2pptx('slide1.html', pptx);

// 将图表添加到占位符区域
if (placeholders.length > 0) {
    slide.addChart(pptx.charts.LINE, chartData, placeholders[0]);
}

await pptx.writeFile('output.pptx');
```

### API 参考

#### 函数签名
```javascript
await html2pptx(htmlFile, pres, options)
```

#### 参数
- `htmlFile`（字符串）：HTML 文件路径（绝对路径或相对路径）
- `pres`（pptxgen）：PptxGenJS 演示文稿实例，布局已设置
- `options`（对象，可选）：
  - `tmpDir`（字符串）：生成文件的临时目录（默认：`process.env.TMPDIR || '/tmp'`）
  - `slide`（对象）：要重用的现有幻灯片（默认：创建新幻灯片）

#### 返回值
```javascript
{
    slide: pptxgenSlide,           // 创建/更新的幻灯片
    placeholders: [                 // 占位符位置数组
        { id: string, x: number, y: number, w: number, h: number },
        ...
    ]
}
```

### 验证

该库会自动验证并在抛出前收集所有错误：

1. **HTML 尺寸必须匹配演示文稿布局** - 报告尺寸不匹配
2. **内容不得溢出 body** - 报告溢出并给出精确测量值
3. **CSS 渐变** - 报告不支持的渐变使用
4. **文本元素样式** - 报告文本元素上的背景/边框/阴影（仅允许在 div 上）

**所有验证错误会被收集并在一条错误消息中一起报告**，允许您一次性修复所有问题，而不是逐个修复。

### 使用占位符

```javascript
const { slide, placeholders } = await html2pptx('slide.html', pptx);

// 使用第一个占位符
slide.addChart(pptx.charts.BAR, data, placeholders[0]);

// 按 ID 查找
const chartArea = placeholders.find(p => p.id === 'chart-area');
slide.addChart(pptx.charts.LINE, data, chartArea);
```

### 完整示例

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require('./html2pptx');

async function createPresentation() {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = '您的姓名';
    pptx.title = '我的演示文稿';

    // 幻灯片 1：标题
    const { slide: slide1 } = await html2pptx('slides/title.html', pptx);

    // 幻灯片 2：带图表的内容
    const { slide: slide2, placeholders } = await html2pptx('slides/data.html', pptx);

    const chartData = [{
        name: '销售额',
        labels: ['Q1', 'Q2', 'Q3', 'Q4'],
        values: [4500, 5500, 6200, 7100]
    }];

    slide2.addChart(pptx.charts.BAR, chartData, {
        ...placeholders[0],
        showTitle: true,
        title: '季度销售额',
        showCatAxisTitle: true,
        catAxisTitle: '季度',
        showValAxisTitle: true,
        valAxisTitle: '销售额（千美元）'
    });

    // 保存
    await pptx.writeFile({ fileName: 'presentation.pptx' });
    console.log('演示文稿创建成功！');
}

createPresentation().catch(console.error);
```

## 使用 PptxGenJS

使用 `html2pptx` 将 HTML 转换为幻灯片后，您将使用 PptxGenJS 添加动态内容，如图表、图像和其他元素。

### ⚠️ 关键规则

#### 颜色
- **在 PptxGenJS 中永远不要使用 `#` 前缀的十六进制颜色** - 会导致文件损坏
- ✅ 正确：`color: "FF0000"`、`fill: { color: "0066CC" }`
- ❌ 错误：`color: "#FF0000"`（破坏文档）

### 添加图像

始终根据实际图像尺寸计算宽高比：

```javascript
// 获取图像尺寸：identify image.png | grep -o '[0-9]* x [0-9]*'
const imgWidth = 1860, imgHeight = 1519;  // 来自实际文件
const aspectRatio = imgWidth / imgHeight;

const h = 3;  // 最大高度
const w = h * aspectRatio;
const x = (10 - w) / 2;  // 在 16:9 幻灯片上居中

slide.addImage({ path: "chart.png", x, y: 1.5, w, h });
```

### 添加文本

```javascript
// 带格式的富文本
slide.addText([
    { text: "粗体 ", options: { bold: true } },
    { text: "斜体 ", options: { italic: true } },
    { text: "普通文本" }
], {
    x: 1, y: 2, w: 8, h: 1
});
```

### 添加形状

```javascript
// 矩形
slide.addShape(pptx.shapes.RECTANGLE, {
    x: 1, y: 1, w: 3, h: 2,
    fill: { color: "4472C4" },
    line: { color: "000000", width: 2 }
});

// 圆形
slide.addShape(pptx.shapes.OVAL, {
    x: 5, y: 1, w: 2, h: 2,
    fill: { color: "ED7D31" }
});

// 圆角矩形
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 1, y: 4, w: 3, h: 1.5,
    fill: { color: "70AD47" },
    rectRadius: 0.2
});
```

### 添加图表

**大多数图表必需：** 使用 `catAxisTitle`（类别）和 `valAxisTitle`（值）的轴标签。

**图表数据格式：**
- 对于简单的柱状图/折线图，使用**带有所有标签的单个系列**
- 每个系列创建一个单独的图例项
- 标签数组定义 X 轴值

**时间序列数据 - 选择正确的粒度：**
- **< 30 天**：使用每日分组（例如 "10-01"、"10-02"）- 避免创建单点图表的月度聚合
- **30-365 天**：使用月度分组（例如 "2024-01"、"2024-02"）
- **> 365 天**：使用年度分组（例如 "2023"、"2024"）
- **验证**：只有 1 个数据点的图表可能表示该时间段的不正确聚合

```javascript
const { slide, placeholders } = await html2pptx('slide.html', pptx);

// 正确：带有所有标签的单个系列
slide.addChart(pptx.charts.BAR, [{
    name: "2024 年销售额",
    labels: ["Q1", "Q2", "Q3", "Q4"],
    values: [4500, 5500, 6200, 7100]
}], {
    ...placeholders[0],  // 使用占位符位置
    barDir: 'col',       // 'col' = 垂直柱状图，'bar' = 水平条形图
    showTitle: true,
    title: '季度销售额',
    showLegend: false,   // 单系列不需要图例
    // 必需的轴标签
    showCatAxisTitle: true,
    catAxisTitle: '季度',
    showValAxisTitle: true,
    valAxisTitle: '销售额（千美元）',
    // 可选：控制缩放（根据数据范围调整最小值以获得更好的可视化效果）
    valAxisMaxVal: 8000,
    valAxisMinVal: 0,  // 用于计数/金额；对于聚类数据（例如 4500-7100），考虑从接近最小值开始
    valAxisMajorUnit: 2000,  // 控制 y 轴标签间距以防止拥挤
    catAxisLabelRotate: 45,  // 如果拥挤则旋转标签
    dataLabelPosition: 'outEnd',
    dataLabelColor: '000000',
    // 对单系列图表使用单一颜色
    chartColors: ["4472C4"]  // 所有柱状图相同颜色
});
```

#### 散点图

**重要提示**：散点图数据格式不寻常 - 第一个系列包含 X 轴值，后续系列包含 Y 值：

```javascript
// 准备数据
const data1 = [{ x: 10, y: 20 }, { x: 15, y: 25 }, { x: 20, y: 30 }];
const data2 = [{ x: 12, y: 18 }, { x: 18, y: 22 }];

const allXValues = [...data1.map(d => d.x), ...data2.map(d => d.x)];

slide.addChart(pptx.charts.SCATTER, [
    { name: 'X 轴', values: allXValues },  // 第一个系列 = X 值
    { name: '系列 1', values: data1.map(d => d.y) },  // 仅 Y 值
    { name: '系列 2', values: data2.map(d => d.y) }   // 仅 Y 值
], {
    x: 1, y: 1, w: 8, h: 4,
    lineSize: 0,  // 0 = 无连接线
    lineDataSymbol: 'circle',
    lineDataSymbolSize: 6,
    showCatAxisTitle: true,
    catAxisTitle: 'X 轴',
    showValAxisTitle: true,
    valAxisTitle: 'Y 轴',
    chartColors: ["4472C4", "ED7D31"]
});
```

#### 折线图

```javascript
slide.addChart(pptx.charts.LINE, [{
    name: "温度",
    labels: ["1月", "2月", "3月", "4月"],
    values: [32, 35, 42, 55]
}], {
    x: 1, y: 1, w: 8, h: 4,
    lineSize: 4,
    lineSmooth: true,
    // 必需的轴标签
    showCatAxisTitle: true,
    catAxisTitle: '月份',
    showValAxisTitle: true,
    valAxisTitle: '温度（°F）',
    // 可选：Y 轴范围（根据数据范围设置最小值以获得更好的可视化效果）
    valAxisMinVal: 0,     // 用于从 0 开始的范围（计数、百分比等）
    valAxisMaxVal: 60,
    valAxisMajorUnit: 20,  // 控制 y 轴标签间距以防止拥挤（例如 10、20、25）
    // valAxisMinVal: 30,  // 首选：对于聚类在一个范围内的数据（例如 32-55 或评分 3-5），将轴从接近最小值开始以显示变化
    // 可选：图表颜色
    chartColors: ["4472C4", "ED7D31", "A5A5A5"]
});
```

#### 饼图（不需要轴标签）

**重要提示**：饼图需要**单个数据系列**，所有类别在 `labels` 数组中，对应的值在 `values` 数组中。

```javascript
slide.addChart(pptx.charts.PIE, [{
    name: "市场份额",
    labels: ["产品 A", "产品 B", "其他"],  // 所有类别在一个数组中
    values: [35, 45, 20]  // 所有值在一个数组中
}], {
    x: 2, y: 1, w: 6, h: 4,
    showPercent: true,
    showLegend: true,
    legendPos: 'r',  // 右侧
    chartColors: ["4472C4", "ED7D31", "A5A5A5"]
});
```

#### 多个数据系列

```javascript
slide.addChart(pptx.charts.LINE, [
    {
        name: "产品 A",
        labels: ["Q1", "Q2", "Q3", "Q4"],
        values: [10, 20, 30, 40]
    },
    {
        name: "产品 B",
        labels: ["Q1", "Q2", "Q3", "Q4"],
        values: [15, 25, 20, 35]
    }
], {
    x: 1, y: 1, w: 8, h: 4,
    showCatAxisTitle: true,
    catAxisTitle: '季度',  // 共享 X 轴标签
    showLegend: true,
    legendPos: 'b',
    chartColors: ["4472C4", "ED7D31"]
});
```

#### 组合图表

```javascript
// 组合柱状图和折线图
slide.addChart(pptx.charts.BAR, [
    {
        name: "销售额",
        labels: ["1月", "2月", "3月", "4月"],
        values: [30, 45, 50, 65],
    }
], {
    x: 1, y: 1, w: 8, h: 4,
    showTitle: true,
    title: '销售趋势',
    barDir: 'col',
    showCatAxisTitle: true,
    catAxisTitle: '月份',
    showValAxisTitle: true,
    valAxisTitle: '金额（千美元）',
    showValAxisSecondary: true,  // 启用次 Y 轴用于折线图
    valAxisMaxVal: 80000,
    chartColors: ["4472C4"]  // 柱状图使用蓝色
});

// 添加第二个图表到同一位置（折线图将叠加）
slide.addChart(pptx.charts.LINE, [
    {
        name: "目标",
        labels: ["1月", "2月", "3月", "4月"],
        values: [25, 40, 50, 60],
    }
], {
    x: 1, y: 1, w: 8, h: 4,
    lineSize: 2,
    showLegend: true,
    legendPos: 'b',
    chartColors: ["ED7D31"]  // 折线图使用橙色
});
```

### 添加动画

**重要提示**：PptxGenJS 动画支持有限 - 仅支持基本效果。

```javascript
// 添加简单的淡入效果
slide.addAnimation({
    obj: shapeOrTextObject,  // 要应用动画的对象
    effect: 'fadeIn',        // 效果类型
    order: 'after',          // 在之前对象之后
    step: 1000               // 持续时间（毫秒）
});
```

### 添加演讲者备注

```javascript
// 添加演讲者备注
slide.addNotes('演讲者备注内容...');
```

### 完整的多幻灯片示例

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require('./html2pptx');

async function createFullPresentation() {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = 'Claude AI';
    pptx.title = '产品演示';
    pptx.subject = '产品功能介绍';

    // 幻灯片 1：标题页
    const { slide: slide1 } = await html2pptx('slides/title.html', pptx);
    slide1.addNotes('欢迎大家参加本次产品演示。');

    // 幻灯片 2：功能概述
    const { slide: slide2, placeholders: placeholders2 } = await html2pptx('slides/features.html', pptx);

    // 在占位符中添加列表
    if (placeholders2.length > 0) {
        slide2.addText([
            { text: "核心功能", options: { bold: true, fontSize: 14 } },
            { text: "\n• 自动化工作流程\n• 实时协作\n• 高级分析", options: { bullet: true, fontSize: 12 } }
        ], placeholders2[0]);
    }

    // 幻灯片 3：图表页
    const { slide: slide3, placeholders: placeholders3 } = await html2pptx('slides/chart.html', pptx);

    // 添加柱状图
    const chartData = [{
        name: '用户增长',
        labels: ['Q1', 'Q2', 'Q3', 'Q4'],
        values: [1200, 1800, 2400, 3200]
    }];

    if (placeholders3.length > 0) {
        slide3.addChart(pptx.charts.BAR, chartData, {
            ...placeholders3[0],
            showTitle: true,
            title: '用户增长趋势',
            showCatAxisTitle: true,
            catAxisTitle: '季度',
            showValAxisTitle: true,
            valAxisTitle: '用户数',
            barDir: 'col'
        });
    }

    // 幻灯片 4：总结页
    const { slide: slide4 } = await html2pptx('slides/conclusion.html', pptx);

    // 添加联系方式
    slide4.addText([
        { text: "联系我们", options: { bold: true, fontSize: 24 } },
        { text: "\n\n邮箱：contact@example.com\n电话：123-456-7890", options: { fontSize: 14 } }
    ], { x: 1, y: 2, w: 8, h: 2, align: 'center' });

    // 保存文件
    await pptx.writeFile({ fileName: 'product-demo.pptx' });
    console.log('演示文稿已创建：product-demo.pptx');
}

createFullPresentation().catch(console.error);
```

## 常见问题

### 问题：文本未出现在 PowerPoint 中

**原因**：文本不在 `<p>`、`<h1>`-`<h6>`、`<ul>` 或 `<ol>` 标签内

**解决方案**：
```html
<!-- 错误 -->
<div>文本内容</div>

<!-- 正确 -->
<div><p>文本内容</p></div>
```

### 问题：渐变未正确显示

**原因**：CSS 渐变无法转换为 PowerPoint

**解决方案**：使用 Sharp 预先光栅化为 PNG
```javascript
// 预先创建渐变背景
const bgPath = await createGradientBackground("gradient-bg.png");

// 在 HTML 中引用
<body style="background-image: url('gradient-bg.png');">
```

### 问题：图像宽高比不正确

**原因**：未根据实际图像尺寸计算宽高比

**解决方案**：
```javascript
// 获取实际图像尺寸
const imgWidth = 1860, imgHeight = 1519;
const aspectRatio = imgWidth / imgHeight;

// 计算正确的宽度
const h = 3;
const w = h * aspectRatio;
```

### 问题：颜色导致文件损坏

**原因**：在 PptxGenJS 中使用了 `#` 前缀的十六进制颜色

**解决方案**：
```javascript
// 错误
fill: { color: "#0066CC" }

// 正确
fill: { color: "0066CC" }
```

### 问题：图表轴标签缺失

**原因**：未提供 `catAxisTitle` 和 `valAxisTitle`

**解决方案**：
```javascript
slide.addChart(pptx.charts.BAR, data, {
    showCatAxisTitle: true,
    catAxisTitle: '类别',  // X 轴标签
    showValAxisTitle: true,
    valAxisTitle: '数值'   // Y 轴标签
});
```

## 最佳实践

1. **始终验证 HTML 尺寸**：确保 HTML body 尺寸与演示文稿布局匹配
2. **使用占位符**：为动态内容预留空间
3. **预先处理图像**：使用 Sharp 处理图标和渐变
4. **遵循文本规则**：所有文本必须在正确的标签内
5. **测试图表**：确保所有图表都有正确的轴标签
6. **备份文件**：在修改现有演示文稿前创建备份
7. **使用版本控制**：跟踪 HTML 和生成的 PPTX 文件的更改

## 相关资源

- [html2pptx.js 文档](https://github.com/example/html2pptx)
- [PptxGenJS GitHub](https://github.com/gitbrent/PptxGenJS)
- [Sharp 文档](https://sharp.pixelplumbing.com/)
- [Playwright 文档](https://playwright.dev/)
