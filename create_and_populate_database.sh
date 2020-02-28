#!/bin/bash

NOW=$(date +"%F")
LOGFILE="logs/create-script-$NOW.log"

# https://stackoverflow.com/questions/592620/how-can-i-check-if-a-program-exists-from-a-bash-script
command -v psql >/dev/null 2>&1 || { echo >&2 "psql command line tool not found. Aborting."; exit 1; }

if [[ $(psql postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='bonsai'") = "1" ]]; then
        :
    else
        echo "Creating "
        psql -a -c "CREATE USER bonsai WITH CREATEDB;" > $LOGFILE
fi

echo "Creating database"
psql -a -f sql/reset_db.sql > $LOGFILE

echo "Creating schema"
psql -d bonsai -a -f sql/bonsai_raw_data_schema.sql > $LOGFILE

echo "Populating metadata: licenses"
psql -d bonsai -a -f sql/common_metadata_licenses.sql > $LOGFILE

echo "Populating metadata: locations"
psql -d bonsai -a -f sql/common_metadata_locations.sql > $LOGFILE
