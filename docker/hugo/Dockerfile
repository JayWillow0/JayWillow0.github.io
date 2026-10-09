# 本地 Hugo 运行镜像：scratch + 官方 release 静态二进制，不依赖外部镜像仓库。
# 构建上下文是 ~/.cache/hugo-docker/image/（内含解压出的 hugo 二进制与
# zoneinfo.zip），由 scripts/hugo.sh 在镜像缺失时自动构建，
# 一次性流程见 docker/hugo/README.md。
FROM scratch
COPY hugo /hugo
COPY zoneinfo.zip /zoneinfo.zip
ENV HUGO_VERSION=0.166.0
ENV ZONEINFO=/zoneinfo.zip
WORKDIR /src
ENTRYPOINT ["/hugo"]
