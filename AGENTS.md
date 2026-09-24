# LiuYang Lab 工程规范

## 项目目标

本仓库是 `JayWillow0.github.io` 的 Hugo 源码。站点使用 Solitude 主题和 GitHub Pages，面向储能电化学、多物理场仿真与智能算法内容的长期发布。

## 技术边界

- Hugo 固定使用 `0.166.0`，不要改为浮动的 `latest`。
- Solitude 通过 Git submodule 固定版本，禁止直接编辑 `themes/solitude/`。
- 站点必须保持纯静态，不引入服务器、数据库、商业 CMS 或运行时 API 请求。
- 不启用第三方评论、统计、音乐、远程字体或前端 CDN。
- 代码高亮使用 Hugo 内置 Chroma。

## 目录约定

- `content/posts/<slug>/index.md`：原生文章页面包；文章图片与正文同目录。
- `content/wechat/<slug>/index.md`：公众号文章索引；正文可写摘要。
- `content/about/index.md`：个人介绍，保持可直接用 Markdown 修改。
- `data/project_overrides.yaml`：原创仓库的人工策展信息。
- `data/generated/`：脚本生成或刷新的数据，只能由脚本维护。
- `assets/images/projects/<repo-slug>.*`：项目封面与科研示意图。
- `assets/images/wechat/<article-slug>.*`：公众号文章封面；从原文获取后自托管，不运行时引用微信图片。
- `assets/css/custom.css`：站点级视觉覆盖。
- `layouts/`：站点级模板覆盖；不得复制并长期维护整套主题。
- `scripts/`：无第三方依赖的维护与验证脚本。
- `tests/`：脚本和数据契约测试。
- `.github/workflows/`：GitHub Pages 构建、验证与部署流程；固定工具版本，不在工作流中回写源码分支。
- `public/`、`resources/`：构建产物，不提交。

## 内容契约

原生文章 front matter 使用：`title`、`date`、`lastmod`、`description`、`cover`、`categories`、`tags`、`draft`、`toc`。

公众号条目 front matter 使用：`title`、`date`、`external_url`、`wechat_account`、`description`、`cover`、`categories`、`tags`、`draft`。

公众号条目只保存公开元数据、人工摘要与原文链接，不复制公众号全文；`external_url` 必须是 `https://mp.weixin.qq.com/` 原文地址。

项目人工覆盖字段固定为：`slug`、`category`、`featured`、`order`、`curator_summary`、`methods`、`cover`、`accent`。

## 实现纪律

- 站点正文、标签、配置与生成页面不得出现特定商业多物理场软件的品牌名，统一写作“电化学仿真”“电化学与热仿真”或“多物理场仿真”。
- 新页面必须同时检查桌面端、平板、390px 移动端、键盘焦点、明暗模式和 `prefers-reduced-motion`。
- 新原创仓库即使没有人工策展信息，也必须出现在“待策展”区域。
- GitHub API 不可用时必须回退到已提交的数据快照，不能阻断部署。
- 所有外部链接使用 HTTPS；新标签页链接必须包含 `rel="noopener noreferrer"`。
- 不提交密钥、token、密码、个人隐私数据或本地绝对路径。
- 调整目录或内容契约时，先更新本文件和维护文档，再修改实现。

## 验证命令

```bash
python3 -m unittest discover -s tests
python3 scripts/fetch_github_repos.py --offline
hugo --gc --minify --panicOnWarning
python3 scripts/check_site.py public
```

视觉改动还必须用浏览器检查 `/`、`/projects/`、`/posts/`、`/wechat/`、`/about/` 和 `/404.html`。

## Git 与发布

- 默认分支使用 `main`。
- 不提交 `public/`。
- 主题升级必须在独立分支完成，并重新执行全部验证与视觉检查。
- 未获得用户当次明确授权，不执行 `git push`、公开仓库创建或 GitHub Pages 发布。
