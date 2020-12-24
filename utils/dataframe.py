from string import ascii_uppercase

import pandas as pd

import gspread
from df2gspread import df2gspread
from df2gspread import gspread2df as g2d

import psycopg2
from psycopg2.extensions import register_adapter
from psycopg2.extras import Json

register_adapter(dict, Json)

gdrive_sheets = gspread.oauth()
gsheet = gdrive_sheets.open("college_catalogs_data")


def insert_value_in_mapping_gsheet(value, college, filename, column='status'):
    try:
        sheet = gsheet.worksheet('Mapping')
        college_records = sheet.findall(college)
        college_rows = [cr.row for cr in college_records]
        college_files = sheet.range(f"E{min(college_rows)}:E{max(college_rows)}")
        file_row = [cell for cell in college_files 
                    if cell.value == filename][0].row
        status_col = ascii_uppercase[sheet.find(column).col-1]
        sheet.update(f'{status_col}{file_row}', value)
    except:
        print(value, college, filename, column)
        print(sheet)
        print(college_records)
        print(college_rows)
        print(file_row)
        print(status_col)

def df2gsheet(df: pd.DataFrame, sheet_name=None):
    """
    uploads dataframe to google sheets
    """
    CELL_MAX_CHAR_LIMIT = 50000
    if 'course' in df.columns:
        aint_gonna_fit = df[df.course.str.len() >= CELL_MAX_CHAR_LIMIT]
        if not aint_gonna_fit.empty:
            print('WARNING ~ {filename} - row are too long'.format(filename=sheet_name))
            print(aint_gonna_fit)
            df['course'] = df['course'].str[:CELL_MAX_CHAR_LIMIT - 1]
    df2gspread.upload(df, gsheet.id, sheet_name, col_names=True, row_names=False, clean=False, new_sheet_dimensions=df.shape)


def get_db_items():
    conn = psycopg2.connect("dbname=collegepdf user=postgres")
    cur = conn.cursor()
    cur.execute('select filename,college from textract')
    return cur.fetchall()
    

def db2df(college=None, filename=None, years=(None, None)):
    conn = psycopg2.connect("dbname=collegepdf user=postgres")
    cur = conn.cursor()

    if not college:
        cur.execute("SELECT * FROM textract")    
    else:
        if filename:
            cur.execute(f"SELECT * FROM textract WHERE college='{college}' AND filename='{filename}'")           
        else:
            cur.execute(f"SELECT * FROM textract WHERE college='{college}'")

    data = cur.fetchall()
    
    return pd.DataFrame(
        data,
        columns=[
            "db_id",
            "filepath",
            "filename",
            "college",
            "pdfminer",
            "pdfminer_detailed",
            "fonts",
            "pypdf2",
            "pypdf2_detailed",
        ],
    )


def gsheet2df():
    return


def get_mapping():
    return g2d.download(gsheet.id, "Mapping", col_names=True, row_names=False)
