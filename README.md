# agy-session-namer

一个用于 **Google Antigravity (AGY)** 的轻量级半自动会话命名插件。

通过 Antigravity 的 `SessionStart` 生命周期 Hook，在每个新会话启动时自动注入一次命名规则，让模型在**首轮任务完成后**，于回复末尾附带一行规范化的建议会话标题，后续追问不再打扰。

> **说明**：由于 Antigravity 目前暂未向 Agent 或 Hook 开放类似 Codex `set_thread_title` 的自动改名接口，本插件采用「首轮自动生成规范标题 + 手动一键粘贴改名」的半自动方案；待官方开放改标题 API 后可直接升级为全自动版本。

## 标题规范

* **固定格式**：`模块名|持续目标`
* **长度上限**：不超过 **24 个字**（含竖线 `|`）
* **模块名**：看得懂的功能、项目或业务名称
* **持续目标**：写清整个会话从头到尾要做成的事，不写当前这一步，不用“优化”“处理问题”等空话
* **无打扰**：只在第 1 轮回复末尾输出一行 `建议标题：模块名|持续目标`，不解释命名理由，后续追问不再重复输出

**示例对比**

| 类型 | 示例 |
| :--- | :--- |
| 推荐 | `支付回调|接入微信异步验签与对账` |
| 推荐 | `用户导出器|支持按时间段分页导出CSV` |
| 避免 | `支付|优化回调逻辑`（空话） |
| 避免 | `导出|先看下报错日志`（只写了当前这一步） |

## 目录结构

```text
agy-session-namer/
├── plugin.json                     # Antigravity 插件清单
├── hooks.json                      # SessionStart 生命周期 Hook 配置
├── scripts/
│   └── session_start_namer.py      # UTF-8 Python 脚本（按 conversationId 去重）
├── install.ps1                     # Windows 一键本地安装脚本
├── LICENSE
└── README.md
```

## 安装方法（Windows）

### 方式一：运行安装脚本

```powershell
.\install.ps1
```

脚本会将插件文件同步到 `%USERPROFILE%\.gemini\config\plugins\agy-session-namer\`。

### 方式二：手动复制

将本仓库中的 `plugin.json`、`hooks.json` 和 `scripts/` 复制到：

```text
C:\Users\<你的用户名>\.gemini\config\plugins\agy-session-namer\
```

安装完成后无需重启 Antigravity，下次**新建会话**时即会自动生效。你也可以在 Antigravity 的 **Customizations / Plugins** 页面随时开关本插件。

## 使用方法

1. 在 Antigravity 中开启一个**新会话**并发送你的第一个任务；
2. 模型会正常完成任务，并在首轮回复最末尾附带一行：
   ```text
   建议标题：模块名|持续目标
   ```
3. 复制标题后：
   * **桌面端**：点击侧边栏该会话右侧 `...` → **Rename**（或点击顶部标题栏）粘贴回车；
   * **CLI**：执行 `/rename 模块名|持续目标`。

## 环境要求

* Python 3.9+（命令使用 `python -X utf8`，脚本内部同时强制 `stdin/stdout` 为 UTF-8，避免 Windows 中文乱码）
* Google Antigravity 2.0+ / Antigravity CLI

## License

MIT
