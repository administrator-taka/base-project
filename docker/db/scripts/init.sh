#!/bin/bash

# Wait for PostgreSQL server to be ready
until psql --username postgres --dbname postgres -c '\q'; do
  sleep 1
done

# Execute the SQL script
psql --username postgres --dbname postgres -f /sql/test.sql
