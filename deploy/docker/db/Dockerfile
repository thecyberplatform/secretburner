FROM postgres:15

# Set environment variables for automatic error handling and the PostgreSQL version
ENV DEBIAN_FRONTEND=noninteractive
ENV PG_VERSION=15

# Update the package list and install pg_cron
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-$PG_VERSION-cron && \
    rm -rf /var/lib/apt/lists/*

# Add pg_cron to the shared_preload_libraries
RUN echo "shared_preload_libraries = 'pg_cron'" >> /usr/share/postgresql/postgresql.conf.sample
RUN echo "cron.database_name='secretburner'" >> /usr/share/postgresql/postgresql.conf.sample
