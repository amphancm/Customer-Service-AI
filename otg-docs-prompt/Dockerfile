# Dockerfile (in otg-docs-prompt folder)
#FROM node:16-alpine as build-stage
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 5173
#RUN npm run build
#RUN npm run dev


# FROM nginx:stable-alpine
# COPY nginx.conf /etc/nginx/conf.d/default.conf
# COPY --from=build-stage /app/dist /usr/share/nginx/html
# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]