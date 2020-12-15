import pandas as pd
import gspread
from df2gspread import df2gspread

gdrive_sheets = gspread.oauth()
gsheet = gdrive_sheets.open("college_catalogs_data")
print(gsheet)


def df2gsheet(df: pd.DataFrame, college_name=None, departments=False):
    """
    uploads dataframe to google sheets
    """
    sheet_name = college_name if not departments else college_name + "_departments"
    df2gspread.upload(df, gsheet.id, college_name)


def db2df():
    return
