CREATE TABLE "location" (
  "id" SERIAL PRIMARY KEY,
  "name" text,
  "uri" text
);

CREATE TABLE "temporal_extent" (
  "id" SERIAL PRIMARY KEY,
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
  "numerical_value" float,
  "input_of_id" int REFERENCES "activity" ("id"),
  "output_of_id" int REFERENCES "activity" ("id"),
  "unit_id" int REFERENCES "unit" ("id"),
  "object_type_id" int REFERENCES "flow_object" ("id")
);

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
