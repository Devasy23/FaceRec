# Use the official MongoDB image as the base
FROM mongo:latest

# Set environment variables for MongoDB
ENV MONGO_INITDB_ROOT_USERNAME=admin
ENV MONGO_INITDB_ROOT_PASSWORD=password

# Optional: Copy initialization script to the container
COPY init-mongo.js /docker-entrypoint-initdb.d/
