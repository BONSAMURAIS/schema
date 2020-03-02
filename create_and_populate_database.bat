echo "Creating user"
psql -a -c "CREATE USER bonsai WITH CREATEDB;"
echo "Creating database"
psql -a -f sql/reset_db.sql
echo "Creating schema"
psql -U bonsai -d bonsai -a -f sql/bonsai_raw_data_schema.sql
echo "Populating metadata: licenses"
psql -U bonsai -d bonsai -a -f sql/common_metadata_licenses.sql
echo "Populating metadata: locations"
psql -U bonsai -d bonsai -a -f sql/common_metadata_locations.sql
echo "Populating metadata: biosphere flows"
psql -U bonsai -d bonsai -a -f sql/common_metadata_biosphere.sql
