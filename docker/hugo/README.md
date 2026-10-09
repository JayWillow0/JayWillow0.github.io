# 本地 Hugo 运行镜像

本目录定义站点本地构建用的 Hugo 镜像（`hugo:0.166.0`）。镜像由 `scratch`
加官方 release 的 linux-arm64 **标准版**静态二进制与 Go 官方 `zoneinfo.zip`
（scratch 无系统 tzdata，站点时区 `Asia/Shanghai` 靠它解析）构成，构建过程
只访问本机缓存目录，不依赖 Docker Hub 或任何镜像加速源。

## 为什么是标准版而不是 extended

- extended 版 Linux 二进制动态链接 glibc，无法在 scratch 镜像中运行；
  标准版是纯静态 Go 二进制。
- 站点与主题没有 SCSS、无 Hugo Modules 远程依赖，标准版可完成全部构建
  （含 webp 图片处理）。若未来引入 SCSS 再重新评估。

## 为什么不用现成镜像

- 第三方镜像（如 klakegg/hugo）需要从 Docker Hub 拉取，本机 daemon 配置的
  镜像加速源对这类仓库返回 403，且每次换机器都要重新走网络。
- 官方 release tarball 下载一次后保存在 `~/.cache/hugo-docker/`，镜像构建
  完全离线，版本与 CI 使用的 `0.166.0` 严格一致。

## 一次性准备（仅新机器需要）

```bash
mkdir -p ~/.cache/hugo-docker
cd ~/.cache/hugo-docker
# 需要代理时先 export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890
curl -fL -o hugo_0.166.0_linux-arm64.tar.gz \
  https://github.com/gohugoio/hugo/releases/download/v0.166.0/hugo_0.166.0_linux-arm64.tar.gz
curl -fL -o zoneinfo.zip \
  https://raw.githubusercontent.com/golang/go/go1.25.4/lib/time/zoneinfo.zip
```

之后正常使用 `./scripts/hugo.sh` 即可：它检测到镜像缺失会自动解压 tarball
并执行 `docker build`，镜像常驻 Docker 本地存储，重启不丢失。

## 说明

- 镜像是 linux/arm64，面向本机 Apple Silicon；x86 机器把 tarball 换成
  `linux-amd64` 版本即可。
- scratch 镜像不含 CA 证书，本地构建不受影响（主题走 git submodule）。

