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
# print(gsheet)


def df2gsheet(df: pd.DataFrame, college_name=None):
    """
    uploads dataframe to google sheets
    """
    df2gspread.upload(df, gsheet.id, college_name, col_names=True, row_names=False)


def db2df(college=None, years=(None, None)):
    conn = psycopg2.connect("dbname=collegepdf user=postgres")
    cur = conn.cursor()

    if not college:
        cur.execute("SELECT * FROM textract")
        data = cur.fetchall()
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
