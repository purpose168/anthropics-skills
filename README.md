> **注意:** 此仓库包含 Anthropic 为 Claude 实现的技能。有关 Agent Skills 标准的信息，请参阅 [agentskills.io](http://agentskills.io)。

# 技能 (Skills)

技能是包含指令、脚本和资源的文件夹，Claude 会动态加载这些内容以提升在专门任务上的性能。技能教会 Claude 如何以可重复的方式完成特定任务，无论是按照您公司的品牌指南创建文档、使用您组织的特定工作流程分析数据，还是自动化个人任务。

欲了解更多信息，请查看：
- [什么是技能？](https://support.claude.com/en/articles/12512176-what-are-skills)
- [在 Claude 中使用技能](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [如何创建自定义技能](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [使用 Agent Skills 为现实世界配备智能体](https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

# 关于此仓库

此仓库包含的技能展示了 Claude 技能系统的可能性。这些技能范围涵盖创意应用（艺术、音乐、设计）到技术任务（测试 Web 应用、MCP 服务器生成）再到企业工作流程（沟通、品牌等）。

每个技能都独立包含在自己的文件夹中，其中包含一个 `SKILL.md` 文件，该文件包含 Claude 使用的指令和元数据。浏览这些技能以获取您自己技能的灵感，或了解不同的模式和方法。

此仓库中的许多技能都是开源的（Apache 2.0）。我们还在 [`skills/docx`](./skills/docx)、[`skills/pdf`](./skills/pdf)、[`skills/pptx`](./skills/pptx) 和 [`skills/xlsx`](./skills/xlsx) 子文件夹中包含了驱动 [Claude 文档功能](https://www.anthropic.com/news/create-files) 的文档创建和编辑技能。这些是源代码可用，而非开源，但我们希望与开发者分享这些技能，作为在生产 AI 应用中主动使用的更复杂技能的参考。

## 免责声明

**这些技能仅供演示和教育目的。** 虽然其中某些功能可能在 Claude 中可用，但您从 Claude 获得的实现和行为可能与这些技能中显示的不同。这些技能旨在说明模式和可能性。在依赖这些技能执行关键任务之前，请务必在自己的环境中彻底测试它们。

# 技能集
- [./skills](./skills)：创意与设计、开发与技术、企业与沟通以及文档技能的技能示例
- [./spec](./spec)：Agent Skills 规范
- [./template](./template)：技能模板

# 在 Claude Code、Claude.ai 和 API 中尝试

## Claude Code

您可以通过在 Claude Code 中运行以下命令将此仓库注册为 Claude Code 插件市场：
```bash
/plugin marketplace add anthropics/skills
```

然后，要安装特定的技能集：
1. 选择 `浏览并安装插件`
2. 选择 `anthropic-agent-skills`
3. 选择 `document-skills` 或 `example-skills`
4. 选择 `立即安装`

或者，直接通过以下方式安装任一插件：
```bash
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

安装插件后，您只需提及它即可使用该技能。例如，如果您从市场安装了 `document-skills` 插件，您可以要求 Claude Code 执行类似以下操作："使用 PDF 技能从 `path/to/some-file.pdf` 中提取表单字段"

## Claude.ai

这些示例技能在 Claude.ai 的付费计划中已经全部可用。

要使用此仓库中的任何技能或上传自定义技能，请按照 [在 Claude 中使用技能](https://support.claude.com/en/articles/12512180-using-skills-in-claude#h_a4222fa77b) 中的说明操作。

## Claude API

您可以通过 Claude API 使用 Anthropic 的预构建技能并上传自定义技能。有关更多信息，请参阅 [技能 API 快速入门](https://docs.claude.com/en/api/skills-guide#creating-a-skill)。

# 创建基本技能

创建技能很简单 - 只需一个包含 YAML 前置数据和指令的 `SKILL.md` 文件的文件夹。您可以使用此仓库中的 **template-skill** 作为起点：

```markdown
---
name: my-skill-name  # 技能的唯一标识符（小写，空格用连字符）
description: 此功能的清晰描述以及何时使用它
---

# 我的技能名称

[在此添加 Claude 在此技能激活时将遵循的指令]

## 示例
- 示例用法 1
- 示例用法 2

## 指南
- 指南 1
- 指南 2
```

前置数据只需要两个字段：
- `name` - 您技能的唯一标识符（小写，空格用连字符）
- `description` - 技能功能的完整描述以及何时使用它

下面的 markdown 内容包含 Claude 将遵循的指令、示例和指南。有关更多详细信息，请参阅 [如何创建自定义技能](https://support.claude.com/en/articles/12512198-creating-custom-skills)。

# 合作伙伴技能

技能是教会 Claude 如何更好地使用特定软件的好方法。当我们看到来自合作伙伴的优秀示例技能时，我们可能会在此处突出显示其中一些：

- **Notion** - [Notion Skills for Claude](https://www.notion.so/notiondevs/Notion-Skills-for-Claude-28da4445d27180c7af1df7d8615723d0)
