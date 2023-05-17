# react dockerfile
FROM node:18.16.0-alpine

WORKDIR /app

COPY package.json ./package.json

RUN npm install

COPY . .


CMD [ "npm", "start" ]
