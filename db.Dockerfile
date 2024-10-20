FROM postgres:16-alpine

# Create directory to copy initialization files (optional if you want to copy into a new directory)
RUN mkdir -p /docker-entrypoint-initdb.d

# Copy the SQL initialization script into the container
COPY ./docker/postgresql/init.sql /docker-entrypoint-initdb.d/
#COPY ./docker/postgresql/invoiceFakeData.sql /docker-entrypoint-initdb.d/

# Set the correct file permissions for the SQL script
RUN chmod 644 /docker-entrypoint-initdb.d/init.sql
#RUN chmod 644 /docker-entrypoint-initdb.d/invoiceFakeData.sql

# Expose the PostgreSQL port
EXPOSE 5432

# Start the PostgreSQL service
CMD ["postgres"]