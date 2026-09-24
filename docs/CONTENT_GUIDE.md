# 内容维护指南

## 修改个人介绍

直接编辑 `content/about/index.md` 的 Markdown 正文。头像或个人图片放在同一目录后，用相对路径引用。

## 新增研究札记

```bash
hugo new content posts/article-slug/index.md
```

补全标题、日期、摘要、分类和标签，将 `draft` 改为 `false`。文章图片放在同一页面包内，例如 `content/posts/article-slug/model-result.webp`，正文使用 `![说明](model-result.webp)`。

## 新增公众号文章

当前公众号 ID 为“半导铁盒-硅迹”，由 `content/wechat/_index.md` 的 `wechat_account` 字段统一维护。

```bash
hugo new content wechat/article-slug/index.md
```

填写 `external_url`，并把 `wechat_account` 设置为“半导铁盒-硅迹”。正文只写摘要，不抓取或复制公众号全文。没有文章链接时保留空集合，不创建虚构条目。

## 维护项目画廊

GitHub 仓库基础信息由 `scripts/fetch_github_repos.py` 获取。人工策展信息放在 `data/project_overrides.yaml`：

- `slug` 必须与 GitHub 仓库名完全一致。
- `category` 使用既有四个分类之一。
- `featured` 控制是否出现在首页。
- `order` 数字越小越靠前。
- `curator_summary` 说明问题、方法和价值，不重复 GitHub 描述。
- `methods` 是方法标签列表。
- `cover` 是 `assets/` 下的相对路径。
- `accent` 使用十六进制颜色。

新增原创仓库会自动进入“待策展”区域。补齐覆盖数据和封面后，它会进入正式分类。

## 新增页面

页面内容放在 `content/`，站点级模板放在 `layouts/`，样式只写入 `assets/css/custom.css`。新增页面需要同步检查明暗模式、移动端、键盘焦点和减少动画模式。

## 升级主题

主题升级只能在独立分支进行。更新 submodule 后执行完整测试、生产构建和浏览器截图对比，确认无回归再合并。
