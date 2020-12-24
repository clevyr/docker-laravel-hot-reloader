ARG NODE_VERSION=lts
FROM node:$NODE_VERSION-alpine

WORKDIR /app

COPY rootfs/ /

CMD ["/entrypoint"]
