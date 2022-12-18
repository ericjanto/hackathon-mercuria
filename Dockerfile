# This file is a template, and might need editing before it works on your project.
FROM node:8.11

WORKDIR /pythonapp/mock_api

ARG NODE_ENV
USER nobody
ENV NODE_ENV $NODE_ENV

COPY package.json /usr/src/app/
RUN npm install

COPY . /usr/src/app

# replace this with your application's default port
USER root
EXPOSE 8000
CMD [ "npm", "start", "gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "mock_api.wsgi"]
