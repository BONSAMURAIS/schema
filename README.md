# Relational database schemas for BONSAI

A Postgres database schema for storing raw and processed BONSAI data.

![schema graphic](https://github.com/BONSAMURAIS/schema/raw/master/images/raw-schema.png "Current draft schema")

See `bonsai_raw_data_schema.sql` and the issues for now.

## Usage

Install Postgresql with the associated command line tools.

In a terminal, run the following:

```bash
    create_and_populate_database.sh
```

## Development

Python files (in the `python` directory of this repo) used to define the common metadata require the following dependencies:

- pandas
- psycopg2
- pyarrow
- pyshp
- requests
