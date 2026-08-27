FROM node:22-alpine AS build
WORKDIR /app
COPY frontend/web/package.json ./
RUN npm install
COPY frontend/web ./
RUN npm run build
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
