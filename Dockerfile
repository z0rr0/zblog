# zblog docker file
# https://github.com/z0rr0/zblog/
# Version z0rr0/zblog:0.0.1
# It is an Alpine based containter for python3 django applications.

FROM alpine:3.10
MAINTAINER Alexander Zaitsev "admin@zorro.website"

RUN apk update && apk upgrade
RUN apk add tzdata ca-certificates gcc build-base python3 python3-dev uwsgi-python3 \
    mariadb-client mariadb-connector-c mariadb-connector-c-dev

ADD requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
ADD blog /var/blog
RUN rm -rf /var/blog/media
VOLUME ["/data/conf", "/var/blog/media"]

RUN rm -f /var/blog/blog/local_settings.py && \
    ln -s /data/conf/local_settings.py /var/blog/blog/local_settings.py

EXPOSE 32123
WORKDIR /var/blog
ENTRYPOINT ["/usr/sbin/uwsgi"]
CMD ["--ini", "/data/conf/uwsgi_blog.ini"]

# docker compose example
# blog:
#   restart: always
#   image: "z0rr0/zblog:latest"
#   ports:
#     - "32123:32123"
#   volumes:
#     - "/data/blog/conf:/data/conf:ro"
#     - "/data/blog/media:/var/media"
#   links:
#     - "mariadb:mariadb"
#   log_driver: "json-file"
#   log_opt:
#     max-size: "16m"
#     max-file: "5"
