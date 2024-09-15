FROM python:3.12-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create and set the working directory
WORKDIR /app

COPY ./app/api/config/requirements /requirements

RUN apk update \
    && apk add --no-cache \
        build-base \
        gcc \
        musl-dev \
    && apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev \
    && pip install --no-cache-dir -r /requirements/production.txt \
    && apk del .build-deps

# Copy requirements and install local one
RUN rm -rf /requirements

COPY ./deploy/docker/api/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./deploy/docker/api/start-server.sh /start-server.sh
RUN sed -i 's/\r//' /start-server.sh
RUN chmod +x /start-server.sh

COPY ./app/api /app

# Ensure proper permissions and ownership
RUN chown -R nobody:nogroup /app
RUN chown nobody:nogroup /entrypoint.sh
RUN chown nobody:nogroup /start-server.sh

# Switch to a non-root user
USER nobody

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/start-server.sh"]