# SETUP · 让 STATS 卡片上线

`README.md` 里的 **STATS（数据面板）** 卡片指向你自己的 Vercel 自托管实例
（`atomsh4-stats`），需要你部署一次（约 5 分钟）。部署完成前这块会显示为裂图，其余部分
（标题、打字机、徽章、贪吃蛇、奖杯、联系方式）发布后即可用。

> 为什么要自托管：公共的 `github-readme-stats.vercel.app` 实例长期被限流甚至暂停
> （发布时正处于 `DEPLOYMENT_PAUSED`）。自托管后永不限流，且卡片样式完全一致。
>
> **TROPHY（成就）** 已改为由 GitHub Action 直接渲染成静态 SVG（和贪吃蛇一样推到
> `output` 分支），**无需任何部署**。

---

## 0. 准备一个 GitHub Token（两个实例共用）

1. 打开 https://github.com/settings/tokens → **Generate new token (classic)**。
2. 名称随意，**无需勾选任何 scope**（只读公开数据即可）；如果以后想统计私有仓库，再勾选 `repo`。
3. 生成后复制 token（形如 `ghp_xxx`），下面两步都会用到。

---

## 1. 部署 STATS 实例（github-readme-stats）

1. 打开 https://vercel.com/new ，用 GitHub 登录。
2. Import 仓库：先 Fork 一份 https://github.com/anuraghazra/github-readme-stats 到自己名下，
   再在 Vercel 里 Import 这个 fork（或直接用仓库 README 里的 **Deploy** 按钮）。
3. **Project Name 必须设为 `atomsh4-stats`**（这样域名才是 `https://atomsh4-stats.vercel.app`，
   与 README 中的链接一致）。
4. 展开 **Environment Variables**，添加：
   - Name: `PAT_1`
   - Value: 第 0 步的 token
5. 点 **Deploy**，等待完成。
6. 打开 `https://atomsh4-stats.vercel.app/api?username=AtomsH4` 验证能出图。

---

## 2. 完成

实例上线后，刷新 https://github.com/AtomsH4 ，STATS 卡片会自动出现，无需改动 `README.md`。

> 如果你用了**别的 Project Name**，只需把 `README.md` 里的域名
> `atomsh4-stats.vercel.app` 替换成你的实际域名即可。

---

## 关于贪吃蛇 🐍 和奖杯 🏆（全自动，无需部署）

`.github/workflows/assets.yml` 会在每次 push、每 12 小时、以及手动触发时：

- 用 `Platane/snk` 把贡献图生成贪吃蛇 SVG；
- 用 `github-profile-trophy` 的 `render_svg.ts` 渲染奖杯静态 SVG；

并把 `github-snake.svg` / `github-snake-dark.svg` / `trophy.svg` 一起推到 `output` 分支。
首次发布后会自动跑一次；也可在 **Actions 标签页 → Generate Assets → Run workflow** 手动触发。
