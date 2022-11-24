# Name the node stage "builderapi"
FROM node:16 AS builderapi
# Set working directory for Backend
WORKDIR /api
COPY . .
# Install Node modules for Backend Express Apllication
RUN npm install
# Open Ports for Container
EXPOSE 5000
# Start the Application
CMD ["npm", "start"]
