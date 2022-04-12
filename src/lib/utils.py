import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SHEETS_DIR= os.path.join(BASE_DIR,"sheets")
OUTPUT_DIR= os.path.join(BASE_DIR,"output")
TABLE_SOURCE_DIR= os.path.join(OUTPUT_DIR,"tables_source")
TABLE_FORMATTED_DIR= os.path.join(OUTPUT_DIR,"tables_formatted")

