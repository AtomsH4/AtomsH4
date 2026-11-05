# SETUP · GitHub Actions 静态卡片

STATS、TROPHY 和 SNAKE 都由 `.github/workflows/assets.yml` 生成静态 SVG，
统一发布到本仓库的 `output` 分支。主页直接读取这些文件。

## 自动更新

`Generate Assets` 工作流在以下情况运行：

- 每 12 小时一次：UTC 00:00 / 12:00，即北京时间 08:00 / 20:00；定时任务可能排队延迟。
- 推送到 `main` 分支。
- 手动进入 **Actions → Generate Assets → Run workflow**。

工作流使用 GitHub 自动提供的 `GITHUB_TOKEN`，只统计可访问的公开数据，无需配置个人 Token。
仓库的 Actions 必须启用；工作流声明了发布 `output` 分支所需的 `contents: write` 权限。

## STATS 生成与发布

两张卡片由固定版本的
[GitHub Readme Stats Action](https://github.com/stats-organization/github-readme-stats-action)
直接在 Actions runner 中渲染：

| 文件 | 内容 |
| --- | --- |
| `output/stats.svg` | GitHub 统计，保留 `include_all_commits=true` |
| `output/top-langs.svg` | 紧凑语言统计 |
| `output/trophy.svg` | 成就 |
| `output/github-snake.svg` | 浅色贡献图 |
| `output/github-snake-dark.svg` | 深色贡献图 |

这里的 `output/` 表示 Git 分支，不是 `main` 分支里的目录。
README 使用 `https://raw.githubusercontent.com/AtomsH4/AtomsH4/output/<文件名>`。

统计卡片保留白色背景、粉色标题、青色图标和原有的 165 像素显示高度。
生成器启用 `fail_on_error`，阻止 GitHub API 错误被当作正常图片写入。

`scripts/publish-stats.py` 会校验新文件的 SVG 结构、卡片文字及错误提示。
每张卡片单独回退：新图不可用时，使用 `output` 分支里上一张通过校验的图片；
如果新图和旧图都不可用，工作流失败并停止发布，保留线上已有资源。
Actions 运行摘要会列出每张卡片是更新还是沿用旧图。

工作流使用并发锁，避免两次运行同时覆盖 `output` 分支。

## 检查与排错

1. 查看 **Actions → Generate Assets** 的最新运行和 **Stats cards** 摘要。
2. 直接打开 [stats.svg](https://raw.githubusercontent.com/AtomsH4/AtomsH4/output/stats.svg)
   和 [top-langs.svg](https://raw.githubusercontent.com/AtomsH4/AtomsH4/output/top-langs.svg)。
3. 如遇 API 限流，工作流会提示并尝试保留旧图；待额度恢复后手动重跑。
4. 原始 SVG 已更新而主页仍显示旧图时，等待 GitHub 图片代理缓存刷新。

统计卡片已不依赖 `atomsh4-stats.vercel.app`。已有的 Vercel 项目可以自行保留或关闭。
