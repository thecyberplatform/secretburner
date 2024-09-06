FROM nginx:1.27-alpine

RUN apk add --no-cache sed openssl

RUN rm /etc/nginx/conf.d/*

# Import the correct configuration file for the build.
ARG nginx_conf_file
ADD ./deploy/docker/nginx/conf.d/$nginx_conf_file /etc/nginx/conf.d/app.conf

COPY ./deploy/docker/nginx/build.sh /build.sh

RUN sed -i 's/\r//' /build.sh
RUN chmod +x /build.sh
