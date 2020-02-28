from pathlib import Path
from psycopg2.extensions import adapt
import io
import requests
import shapefile
import zipfile

URL = "https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_countries.zip"
DIRPATH = Path(__file__).resolve().parent.parent
URL_TEMPLATE = """https://www.geonames.org/countries/{}/"""

r = requests.get(URL, allow_redirects=True)
zf = zipfile.ZipFile(io.BytesIO(r.content), 'r')
sf = shapefile.Reader(
    shp=io.BytesIO(zf.read("ne_10m_admin_0_countries.shp")),
    dbf=io.BytesIO(zf.read("ne_10m_admin_0_countries.dbf"))
)
mapping = {x[0]: i for i, x in enumerate(sf.fields[1:])}


###
# "Countries" from Natural Earth that we chose not to import for now
# (as they are not relevant in our project aims):
# Akrotiri
# Ashmore and Cartier Is.
# Baikonur
# Bajo Nuevo Bank
# Clipperton I.
# Coral Sea Is.
# Cyprus U.N. Buffer Zone
# Dhekelia
# Indian Ocean Ter.
# N. Cyprus
# Scarborough Reef
# Serranilla Bank
# Siachen Glacier
# Somaliland
# Spratly Is.
# USNB Guantanamo Bay
###


def prepare_statement(template, values):
    """Correctly escape things and keep as unicode.

    pyscopg2 has a default encoding of `latin-1`: https://github.com/psycopg/psycopg2/issues/331"""
    new_values = []
    for value in values:
        adapted = adapt(value)
        adapted.encoding = 'utf-8'
        new_values.append(adapted.getquoted().decode())

    return template.format(*new_values)


def get_value(rec, key):
    return rec.record[mapping[key]]


TEMPLATE = """INSERT INTO "location" ("label", "identifier", "uri") VALUES ({}, {}, {});\n"""

CODE_MAPPING = {
    'Norway': 'NO',
    "France": 'FR'
}

with open(DIRPATH / "common_metadata_locations.sql", "w", encoding='utf-8') as f:
    f.write("BEGIN;\n")
    for obj in sf:
        code = get_value(obj, 'ISO_A2')
        name = get_value(obj, 'NAME')
        code = CODE_MAPPING.get(name, code)
        if code == "-99":
            continue
        f.write(prepare_statement(
            TEMPLATE,
            (
                adapt(name),
                adapt(code),
                adapt(URL_TEMPLATE.format(code)),)
        ))
    f.write("COMMIT;\n")


# Fields in Natural Earth:
# [('DeletionFlag', 'C', 1, 0),
#  ['featurecla', 'C', 15, 0],
#  ['scalerank', 'N', 1, 0],
#  ['LABELRANK', 'N', 2, 0],
#  ['SOVEREIGNT', 'C', 32, 0],
#  ['SOV_A3', 'C', 3, 0],
#  ['ADM0_DIF', 'N', 1, 0],
#  ['LEVEL', 'N', 1, 0],
#  ['TYPE', 'C', 17, 0],
#  ['ADMIN', 'C', 36, 0],
#  ['ADM0_A3', 'C', 3, 0],
#  ['GEOU_DIF', 'N', 1, 0],
#  ['GEOUNIT', 'C', 36, 0],
#  ['GU_A3', 'C', 3, 0],
#  ['SU_DIF', 'N', 1, 0],
#  ['SUBUNIT', 'C', 36, 0],
#  ['SU_A3', 'C', 3, 0],
#  ['BRK_DIFF', 'N', 1, 0],
#  ['NAME', 'C', 25, 0],
#  ['NAME_LONG', 'C', 36, 0],
#  ['BRK_A3', 'C', 3, 0],
#  ['BRK_NAME', 'C', 32, 0],
#  ['BRK_GROUP', 'C', 17, 0],
#  ['ABBREV', 'C', 13, 0],
#  ['POSTAL', 'C', 4, 0],
#  ['FORMAL_EN', 'C', 52, 0],
#  ['FORMAL_FR', 'C', 35, 0],
#  ['NAME_CIAWF', 'C', 45, 0],
#  ['NOTE_ADM0', 'C', 22, 0],
#  ['NOTE_BRK', 'C', 63, 0],
#  ['NAME_SORT', 'C', 36, 0],
#  ['NAME_ALT', 'C', 19, 0],
#  ['MAPCOLOR7', 'N', 1, 0],
#  ['MAPCOLOR8', 'N', 1, 0],
#  ['MAPCOLOR9', 'N', 1, 0],
#  ['MAPCOLOR13', 'N', 3, 0],
#  ['POP_EST', 'N', 10, 0],
#  ['POP_RANK', 'N', 2, 0],
#  ['GDP_MD_EST', 'N', 11, 2],
#  ['POP_YEAR', 'N', 4, 0],
#  ['LASTCENSUS', 'N', 4, 0],
#  ['GDP_YEAR', 'N', 4, 0],
#  ['ECONOMY', 'C', 26, 0],
#  ['INCOME_GRP', 'C', 23, 0],
#  ['WIKIPEDIA', 'N', 3, 0],
#  ['FIPS_10_', 'C', 3, 0],
#  ['ISO_A2', 'C', 3, 0],
#  ['ISO_A3', 'C', 3, 0],
#  ['ISO_A3_EH', 'C', 3, 0],
#  ['ISO_N3', 'C', 3, 0],
#  ['UN_A3', 'C', 4, 0],
#  ['WB_A2', 'C', 3, 0],
#  ['WB_A3', 'C', 3, 0],
#  ['WOE_ID', 'N', 8, 0],
#  ['WOE_ID_EH', 'N', 8, 0],
#  ['WOE_NOTE', 'C', 167, 0],
#  ['ADM0_A3_IS', 'C', 3, 0],
#  ['ADM0_A3_US', 'C', 3, 0],
#  ['ADM0_A3_UN', 'N', 3, 0],
#  ['ADM0_A3_WB', 'N', 3, 0],
#  ['CONTINENT', 'C', 23, 0],
#  ['REGION_UN', 'C', 23, 0],
#  ['SUBREGION', 'C', 25, 0],
#  ['REGION_WB', 'C', 26, 0],
#  ['NAME_LEN', 'N', 2, 0],
#  ['LONG_LEN', 'N', 2, 0],
#  ['ABBREV_LEN', 'N', 2, 0],
#  ['TINY', 'N', 3, 0],
#  ['HOMEPART', 'N', 3, 0],
#  ['MIN_ZOOM', 'N', 3, 1],
#  ['MIN_LABEL', 'N', 3, 1],
#  ['MAX_LABEL', 'N', 4, 1],
#  ['NE_ID', 'N', 10, 0],
#  ['WIKIDATAID', 'C', 8, 0],
# Plus country names in many languages
