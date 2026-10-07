# 内容维护指南

## 修改个人介绍

直接编辑 `content/about/index.md` 的 Markdown 正文。头像或个人图片放在同一目录后，用相对路径引用。

## 新增研究札记

```bash
hugo new content posts/article-slug/index.md
```

补全标题、日期、摘要、分类和标签，将 `draft` 改为 `false`。文章图片放在同一页面包内，例如 `content/posts/article-slug/model-result.webp`，正文使用 `![说明](model-result.webp)`。

系列文章在 front matter 加 `series: [<系列名>]`（数组形式，同系列各篇必须完全一致），并在正文适当位置（通常是开篇导语之后）插入 `{{< series name="<系列名>" >}}`（name 必须显式传，裸调用与数组参数不兼容），页面会按日期自动列出全系列链接，无需手工维护清单。

正文含 LaTeX 数学公式时，front matter 加 `math: true`，公式用 `$...$`（行内）和 `$$...$$`（独立成段）书写。Goldmark passthrough 会把公式原文交给页面内自托管的 KaTeX 渲染，资源位于 `static/katex/`，不引入外部 CDN。公式里的小于号必须写成 `\lt`，不能写裸 `<`；KaTeX 在页面加载后才运行，浏览器会先把 `<字母` 序列解析成 HTML 标签，公式即被破坏。升级 KaTeX 时从 npm 发行包重新拷贝 `katex.min.css`、`katex.min.js`、`contrib/auto-render.min.js` 和 `fonts/*.woff2`，并回归检查公式渲染。permalink 使用 `:slug`，front matter 需显式写 `slug`（与目录名一致），否则 URL 会回落成中文标题转写。

## 新增公众号文章

当前公众号 ID 为“半导铁盒-硅迹”，由 `content/wechat/_index.md` 的 `wechat_account` 字段统一维护。

```bash
hugo new content wechat/article-slug/index.md
```

填写 `external_url`，并把 `wechat_account` 设置为“半导铁盒-硅迹”。正文只写摘要，不抓取或复制公众号全文。文章封面放入 `assets/images/wechat/<article-slug>.*`，在 `cover` 中填写相对 `assets/` 的路径；原文封面必须下载后自托管，不能在页面运行时引用微信图片。没有文章链接时保留空集合，不创建虚构条目。

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

新增原创仓库会自动进入“待策展”区域。补齐覆盖数据和封面后，它会进入正式分类。本站仓库 `JayWillow0.github.io` 被 `EXCLUDED_REPOS` 按名排除，不进入快照；其余排除需求先改 AGENTS.md 契约再改脚本。

## 新增页面

页面内容放在 `content/`，站点级模板放在 `layouts/`，样式只写入 `assets/css/custom.css`。新增页面需要同步检查明暗模式、移动端、键盘焦点和减少动画模式。

## 升级主题

主题升级只能在独立分支进行。更新 submodule 后执行完整测试、生产构建和浏览器截图对比，确认无回归再合并。
