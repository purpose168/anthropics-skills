---
name: web-artifacts-builder
description: 一套用于创建精美的多组件大型语言模型.ai HTML工件的工具体系，使用现代前端Web技术（React、Tailwind CSS、shadcn/ui）。适用于需要状态管理、路由或shadcn/ui组件的复杂工件，不适用于简单的单文件HTML/JSX工件。
license: Complete terms in LICENSE.txt
---

# Web工件构建器

要构建功能强大的前端大型语言模型.ai工件，请按以下步骤操作：
1. 使用 `scripts/init-artifact.sh` 初始化前端仓库
2. 通过编辑生成的代码来开发您的工件
3. 使用 `scripts/bundle-artifact.sh` 将所有代码打包成单个HTML文件
4. 向用户展示工件
5. （可选）测试工件

**技术栈**：React 18 + TypeScript + Vite + Parcel（打包）+ Tailwind CSS + shadcn/ui

## 设计与样式指南

非常重要：为避免所谓的"AI垃圾"，请避免使用过多的居中布局、紫色渐变、统一圆角和Inter字体。

## 快速开始

### 步骤1：初始化项目

运行初始化脚本创建新的React项目：
```bash
bash scripts/init-artifact.sh <项目名称>
cd <项目名称>
```

这将创建一个完整配置的项目，包含：
- ✅ React + TypeScript（通过Vite）
- ✅ Tailwind CSS 3.4.1（带shadcn/ui主题系统）
- ✅ 配置的路径别名（`@/`）
- ✅ 预安装的40+个shadcn/ui组件
- ✅ 包含所有Radix UI依赖项
- ✅ 配置的Parcel打包（通过.parcelrc）
- ✅ Node 18+兼容性（自动检测并固定Vite版本）

### 步骤2：开发您的工件

要构建工件，请编辑生成的文件。请参阅下面的"常见开发任务"以获取指导。

### 步骤3：打包成单个HTML文件

要将React应用打包成单个HTML工件：
```bash
bash scripts/bundle-artifact.sh
```

这将创建 `bundle.html` - 一个自包含的工件，所有JavaScript、CSS和依赖项都内联其中。该文件可以在大型语言模型对话中直接作为工件分享。

**要求**：您的项目必须在根目录中有一个 `index.html`。

**脚本执行的操作**：
- 安装打包依赖项（parcel、@parcel/config-default、parcel-resolver-tspaths、html-inline）
- 创建带路径别名支持的 `.parcelrc` 配置
- 使用Parcel构建（无源映射）
- 使用html-inline将所有资源内联到单个HTML中

### 步骤4：与用户分享工件

最后，在对话中与用户分享打包的HTML文件，以便他们可以将其作为工件查看。

### 步骤5：测试/可视化工件（可选）

注意：这是一个完全可选的步骤。仅在必要时或应要求才执行。

要测试/可视化工件，请使用可用工具（包括其他技能或内置工具如Playwright或Puppeteer）。通常，应避免提前测试工件，因为这会增加请求与查看完成工件之间的延迟。在展示工件之后，如果被要求或出现问题，再进行测试。

## 参考资料

- **shadcn/ui组件**：https://ui.shadcn.com/docs/components