# Use an official Node.js runtime as a parent image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /usr/sql-assistant-using-genai

# Copy the frontend directory contents into the container
COPY ./src ./src
COPY ./public ./public
COPY ./package.json ./
COPY ./package-lock.json ./


# Install the frontend dependencies
RUN npm install

# Expose the port the app runs on
EXPOSE 3000

# Start the React application
CMD ["npm", "start"]
