FROM python:3.9.15-slim
ENV PYTHONUNBUFFERED 1
WORKDIR /opt/cocktail-searcher

COPY requirements.txt /tmp/requirements.txt
RUN buildDeps="gcc python3-dev" \
&& apt-get update \
&& apt-get install -y --no-install-recommends $buildDeps \
&& apt-get install -y --no-install-recommends libpq-dev gettext \
&& pip install -r /tmp/requirements.txt \
&& rm /tmp/requirements.txt \
&& apt-get purge -y --auto-remove $buildDeps \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

COPY cocktail_searcher .
COPY docker-entrypoint.sh /

EXPOSE 8000

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["gunicorn", "cocktail_searcher.wsgi"]