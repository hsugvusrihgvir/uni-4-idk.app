FROM node:20-slim

WORKDIR /app

COPY package*.json ./
RUN npm install
RUN npm install --save-dev @rollup/rollup-linux-x64-gnu@4.60.2

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]
