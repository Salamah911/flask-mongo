FROM python:3.6
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install nano && apt-get -y install cron
ENTRYPOINT ["sh", "manage.sh"]
HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost/ || exit 1
