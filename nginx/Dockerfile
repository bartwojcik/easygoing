FROM nginx:1.13
RUN apt-get update && apt-get install -y certbot cron supervisor &&\
 mkdir -p /var/log/supervisor &&\
 rm -f /etc/nginx/sites-available/* &&\
 rm -f /etc/nginx/sites-enabled/*
COPY crontab /etc/cron.d/crontab
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord"]
