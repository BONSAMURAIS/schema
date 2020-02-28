#!/usr/bin/env python

import requests
from pathlib import Path
from psycopg2.extensions import adapt

DIRPATH = Path(__file__).resolve().parent.parent
URL = "https://github.com/spdx/license-list-data/raw/master/json/licenses.json"


def prepare_statement(template, values):
    """Correctly escape things and keep as unicode.

    pyscopg2 has a default encoding of `latin-1`: https://github.com/psycopg/psycopg2/issues/331"""
    new_values = []
    for value in values:
        adapted = adapt(value)
        adapted.encoding = 'utf-8'
        new_values.append(adapted.getquoted().decode())

    return template.format(*new_values)


data = requests.get(URL).json()['licenses']

TEMPLATE = """INSERT INTO "license" ("full_name", "identifier", "url") VALUES ({}, {}, {});\n"""

with open(DIRPATH / "common_metadata_licenses.sql", "w", encoding='utf-8') as f:
    f.write("BEGIN;\n")
    for obj in data:
        f.write(prepare_statement(
            TEMPLATE,
            (adapt(obj['name']), adapt(obj['licenseId']), adapt(obj['detailsUrl']))
        ))
    f.write("COMMIT;\n")
