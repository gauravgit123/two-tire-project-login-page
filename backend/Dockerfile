# Use MySQL as the base image
FROM mysql:latest

# Set environment variables
ENV MYSQL_ROOT_PASSWORD=admin
ENV MYSQL_DATABASE=admission_db

# Expose the default MySQL port
EXPOSE 3306

# Copy the initialization script
COPY init.sql /docker-entrypoint-initdb.d/
