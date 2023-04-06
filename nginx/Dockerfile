# syntax=docker/dockerfile:1
FROM nginx:latest

COPY . /usr/share/nginx/html

RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/.
# RUN rm /etc/nginx/conf.d/default.conf
COPY board.conf /etc/nginx/conf.d