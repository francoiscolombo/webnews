# STEP 1 build static website
FROM node:stable-alpine as builder

RUN apk update && apk add --no-cache git libc6-compat

# Create app directory
WORKDIR /app

# Copy project files into the docker image
COPY webnews  /app

RUN cd /app && \
    npm install && \
    npm audit && echo "no issue" || echo "some issues, check the logs"

RUN ng build --prod

# STEP 2 build a small nginx image with static website
FROM nginx:stable-alpine

LABEL maintainer  "Francois Colombo <francois_colombo@yahoo.fr>"
LABEL application "webnews_frontend"

# Additional packages
RUN apk update && \
    apk add --no-cache gettext tzdata bash && \
    rm -rf /var/cache/apk/* && \
    chown root:root /docker-entrypoint.sh && \
    chmod 755 /docker-entrypoint.sh

## Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

## From 'builder' copy website to default nginx public folder
COPY --from=builder --chown=nginx:nginx /app/dist/webnews/ /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]