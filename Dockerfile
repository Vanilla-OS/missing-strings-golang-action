FROM python:alpine

COPY entrypoint.sh /
COPY missing_translations.py /

RUN pip install --no-cache-dir PyYAML

ENTRYPOINT ["/entrypoint.sh"]
