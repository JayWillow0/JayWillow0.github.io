#!/usr/bin/env bash
# 固定版本 Hugo 的本地构建入口：封装本地 docker 镜像 hugo:0.166.0。
# 用标准版静态二进制（extended 版动态链接 glibc，无法进 scratch 镜像）；
# 站点无 SCSS，标准版即可完成全部构建。镜像常驻 Docker 本地存储；缺失时用
# ~/.cache/hugo-docker 下的官方 tarball 现场构建（一次性下载流程见
# docker/hugo/README.md），全程不访问镜像仓库。
set -euo pipefail

HUGO_VERSION="0.166.0"
IMAGE="hugo:${HUGO_VERSION}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CACHE_DIR="$HOME/.cache/hugo-docker"
TARBALL="$CACHE_DIR/hugo_${HUGO_VERSION}_linux-arm64.tar.gz"

if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  if [ ! -f "$TARBALL" ] || [ ! -f "$CACHE_DIR/zoneinfo.zip" ]; then
    echo "缺少 $TARBALL 或 $CACHE_DIR/zoneinfo.zip，先按 docker/hugo/README.md 一次性准备（需代理下载）。" >&2
    exit 1
  fi
  mkdir -p "$CACHE_DIR/image"
  tar -xzf "$TARBALL" -C "$CACHE_DIR/image" hugo
  cp "$CACHE_DIR/zoneinfo.zip" "$CACHE_DIR/image/zoneinfo.zip"
  docker build -q -t "$IMAGE" -f "$ROOT/docker/hugo/Dockerfile" "$CACHE_DIR/image" >/dev/null
fi

if [ "${1:-}" = "server" ] || [ "${1:-}" = "serve" ]; then
  exec docker run --rm --tmpfs /tmp -p 1313:1313 -v "$ROOT":/src "$IMAGE" "$@"
fi
exec docker run --rm --tmpfs /tmp -v "$ROOT":/src "$IMAGE" "$@"
