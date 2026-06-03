FROM node:18-alpine

WORKDIR /app

COPY web/frontend/package*.json ./
RUN npm ci --prefer-offline || npm install

COPY web/frontend/ .

CMD ["npm", "start"] 