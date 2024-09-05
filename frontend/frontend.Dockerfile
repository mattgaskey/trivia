# Stage 1: Build the React app
FROM node:14-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Create a lightweight production image
FROM node:14-alpine

WORKDIR /app

COPY --from=build /app/build ./build
COPY package*.json ./
COPY public ./public
COPY src ./src
RUN npm install --only=production

EXPOSE 3000

CMD ["npm", "start"]