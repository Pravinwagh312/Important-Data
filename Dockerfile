FROM node:18.12.1-alpine as node
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build --omit=dev


FROM nginx:alpine
COPY --from=node /app/dist/webapp /usr/share/nginx/html
