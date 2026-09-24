# LiuYang Lab

储能电化学、多物理场仿真与智能算法个人博客。站点由 Hugo、Solitude 和 GitHub Pages 构建，生产地址为 <https://jaywillow0.github.io/>。

## 本地预览

需要 Hugo `0.166.0` 和 Git。首次克隆后初始化主题：

```bash
git submodule update --init --recursive
hugo server --disableFastRender
```

访问 <http://localhost:1313/>。不要直接修改 `themes/solitude/`。

## 更新数据

```bash
python3 scripts/fetch_github_repos.py
```

网络不可用时验证现有快照：

```bash
python3 scripts/fetch_github_repos.py --offline
```

## 发布前验证

```bash
python3 -m unittest discover -s tests
hugo --gc --minify --panicOnWarning
python3 scripts/check_site.py public
```

内容维护方法见 [docs/CONTENT_GUIDE.md](docs/CONTENT_GUIDE.md)，视觉规则见 [docs/DESIGN_SYSTEM.md](docs/DESIGN_SYSTEM.md)。

## 自动部署

`.github/workflows/pages.yaml` 在 pull request 中执行测试和生产构建；`main` 分支推送、手动触发和每周定时任务会继续部署到 GitHub Pages。定时任务只刷新当次构建使用的 GitHub 仓库数据，不向源码分支提交快照。
