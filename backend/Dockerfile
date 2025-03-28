# Use MySQL as the base image
FROM mysql:5.7

# Set environment variables
ENV MYSQL_ROOT_PASSWORD=admin
ENV MYSQL_DATABASE=admission_db

# Copy the initialization script
COPY init.sql /docker-entrypoint-initdb.d/
