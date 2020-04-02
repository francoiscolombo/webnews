# STEP 1 build static website
FROM node:alpine as builder

ARG FRONTEND_APP_TOKEN
ARG FRONTEND_APP_NAME
ARG WEBNEWS_API_BASE_URL

RUN apk update && apk add --no-cache curl git libc6-compat gettext tzdata

# Create app directory
WORKDIR /app

# Copy project files into the docker image
COPY webnews  /app
COPY environment.prod.ts /

RUN cd /app && \
    envsubst < /environment.prod.ts > /app/src/environments/environment.prod.ts && \
    rm -f /environment.prod.ts && \
    npm install && \
    npm install -g @angular/cli@v6-lts && \
    ng lint && \
    ng build --prod

# STEP 2 build a small nginx image with static website
FROM nginx:stable-alpine

LABEL maintainer  "Francois Colombo <francois_colombo@yahoo.fr>"
LABEL application "webnews_frontend"

# Additional packages
RUN apk update && \
    apk add --no-cache tzdata && \
    rm -rf /var/cache/apk/*

## Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

## From 'builder' copy website to default nginx public folder
COPY --from=builder --chown=nginx:nginx /app/dist/webnews/ /usr/share/nginx/html

RUN ls -l /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]