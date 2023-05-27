FROM node:16-alpine3.17 AS builder

WORKDIR /app

COPY package* .

RUN npm install

COPY . .

RUN npm run build

FROM nginx:1.23-alpine3.17

RUN apk add gettext

COPY --from=builder /app/dist /usr/share/nginx/html

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf.template /

CMD envsubst '$APP_HOST' < /nginx.conf.template > /etc/nginx/conf.d/nginx.conf && \
    exec nginx -g 'daemon off;'
