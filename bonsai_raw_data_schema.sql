-- SQL table definitions for the BONSAI project: https://bonsai.uno/
-- Original source is at https://github.com/BONSAMURAIS/schema
-- Based on BONSAI ontology: https://github.com/BONSAMURAIS/BONSAI-ontology-RDF-framework
-- BONSAI mailing list: https://bonsai.groups.io/g/main/

-- After initial release, please make all changes following the pull request
-- workflow to allow for community review. Large changes will probably require
-- a BEP: https://github.com/BONSAMURAIS/enhancements

CREATE TABLE "location" (
  "id" SERIAL PRIMARY KEY,
  -- Ontology uses schema:Place (https://schema.org/Place), which wants the
  -- field "name", but we use "label" to be consistent with other tables
  "label" text,
  -- Normally a URL from geonames.org
  "uri" text
);

CREATE TABLE "temporal_extent" (
  "id" SERIAL PRIMARY KEY,
  -- White the data type is "date", it is expected that these values will
  -- always be first/last days of a year. See:
  -- https://github.com/BONSAMURAIS/bonsai/wiki/Data-Storage
  -- Labels adapted from OWL time ontology:
  -- https://www.w3.org/TR/owl-time/#time:ProperInterval
  "starts" date,
  "finishes" date
);

CREATE TABLE "agent" (
  "id" SERIAL PRIMARY KEY,
  "label" text,
  "location_id" int NOT NULL REFERENCES "location" ("id")
);

CREATE TABLE "activity" (
  "id" SERIAL PRIMARY KEY,
  "performed_by_id" int REFERENCES "agent" ("id"),
  "temporal_extent_id" int NOT NULL REFERENCES "temporal_extent" ("id"),
  "location_id" int NOT NULL REFERENCES "location" ("id"),
  "determining_flow_id" int REFERENCES "flow" ("id"),
  "activity_type_id" int NOT NULL REFERENCES "activity_type" ("id")
);

CREATE TABLE "activity_type" (
  "id" SERIAL PRIMARY KEY,
  "label" text
);

CREATE TABLE "flow" (
  "id" SERIAL PRIMARY KEY,
  -- Field label from ontology of units of measure
  "numerical_value" float,
  -- Neither are required, but see constraint below
  "input_of_id" int REFERENCES "activity" ("id"),
  "output_of_id" int REFERENCES "activity" ("id"),
  "unit_id" int REFERENCES "unit" ("id"),
  "object_type_id" int REFERENCES "flow_object" ("id")
);

ALTER TABLE "flow"
  ADD CONSTRAINT flow_has_activity
  ("input_of_id" IS NOT NULL or "output_of_id" IS NOT NULL);

CREATE TABLE "flow_object" (
  "id" SERIAL PRIMARY KEY,
  "label" text
);

CREATE TABLE "unit" (
  "id" SERIAL PRIMARY KEY,
  "label" text,
  "uri" text
);

CREATE TABLE "balancable_property" (
  "id" SERIAL PRIMARY KEY,
  "label" text,
  "flow_id" int REFERENCES "flow" ("id")
);
