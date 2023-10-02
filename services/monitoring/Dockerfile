FROM node

WORKDIR /App
COPY ./services/monitoring/package*.json ./

RUN npm install

COPY ./services/monitoring .
EXPOSE 8080
CMD ["node", "index.js"]