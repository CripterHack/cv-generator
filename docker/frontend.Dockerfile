FROM node:18-alpine

WORKDIR /app

COPY web/frontend/package*.json ./
RUN npm install

COPY web/frontend/ .

CMD ["npm", "start"] 