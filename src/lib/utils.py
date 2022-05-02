import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SHEETS_DIR= os.path.join(BASE_DIR,"sheets")
DOCS_DIR= os.path.join(BASE_DIR,"docs")
DOCS_OUTCOMES_DIR= os.path.join(DOCS_DIR,"outcomes")
SHEETS_OUTCOMES_DIR= os.path.join(SHEETS_DIR,"outcomes")
SHEETS_GENERAL_DIR= os.path.join(SHEETS_DIR,"general")
OUTPUT_DIR= os.path.join(BASE_DIR,"output")
OUTCOME_TABLE_SOURCE_DIR= os.path.join(SHEETS_DIR,"outcome_tables_source")
TABLE_FORMATTED_DIR= os.path.join(OUTPUT_DIR,"tables")

