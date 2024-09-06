FROM node:20

WORKDIR /app/

RUN apt-get -y update && apt-get -y install bzip2 git g++ build-essential && apt-get -y dist-upgrade
RUN npm install -g @quasar/cli

COPY ./deploy/docker/ui/start-server.sh /start-server.sh
RUN sed -i 's/\r//' /start-server.sh
RUN chmod +x /start-server.sh

# Remove the app directory for now if it exists. If running locally, this will be overriden by the bind mount anyway.
RUN rm -rf /app/*
COPY ./app/ui/ /app/