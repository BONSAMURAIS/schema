# Relational database schemas for BONSAI

A Postgres database schema for storing raw and processed BONSAI data.

![schema graphic](https://github.com/BONSAMURAIS/schema/raw/master/images/raw-schema.png "Current draft schema")

See `bonsai_raw_data_schema.sql` and the issues for now.

## Usage

Install Postgresql with command line tools.

In a terminal, run the following in order:

    psql -a -f create_user.sql
    psql -a -f create_db.sql
    psql -d bonsai -a -f bonsai_raw_data_schema.sql

Installing common metadata:

    psql -d bonsai -a -f common_metadata_licenses.sql
    psql -d bonsai -a -f common_metadata_locations.sql
