import backoff
import gspread
import pandas as pd

from fuzzywuzzy import fuzz
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from gspread_formatting import set_column_widths, set_frozen, set_data_validation_for_cell_range, DataValidationRule,BooleanCondition
from oauth2client.service_account import ServiceAccountCredentials


def add_to_sheet(target, data):
    print('Add sheet processing: {}'.format(target))

    # key name order
    key_order = ['Proposed Title', 'Type', 'Current URL', 'Proposed URL', 'Primary Keywords', 'Monthly Searches',
                 'Proposed Word Count', 'Secondary Keywords']

    if data == []:
        empty_dict = {}
        for k in key_order:
            empty_dict[k] = ''

        data.append(empty_dict)

    df = pd.DataFrame(data)
    df = df[key_order]
    secondary = df['Secondary Keywords'].apply(pd.Series)
    secondary = secondary.rename(columns=lambda x: ''.format(x))

    df.drop('Secondary Keywords', axis=1, inplace=True)
    secondary.columns.values[0] = 'Secondary Keywords'
    df = pd.concat([df[:], secondary[:]], axis=1)

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'content-map-id.json', scope)

    gc = gspread.authorize(credentials)

    # Checking if exists
    list_sheet = gc.openall(title=target)
    ids = [sheet.id for sheet in list_sheet]
    if len(ids) > 0:
        for id in ids:
            gc.del_spreadsheet(id)

    gc.create(target, "sheet file id")
    ws = gc.open(target).worksheet("Sheet1")
    set_with_dataframe(ws, df)
    get_as_dataframe(ws)

    ws.format("A1:H1", {
        "horizontalAlignment": "CENTER",
        "textFormat": {
            "fontSize": 10,
            "bold": True
        }
    })

    set_column_widths(ws, [('A', 500), ('B', 100), ('C', 300), ('D', 300), ('E', 300), ('F', 200), ('G', 200),
                           ('H:AZ', 300)])
    set_frozen(ws, rows=1, cols=1)

    count_row = df.shape[0] + 2
    validation_rule = DataValidationRule(
        BooleanCondition('ONE_OF_LIST', ['Home Page', 'Blog Category', 'Blog Home', 'Blog Post', 'Page', 'Product']),
        showCustomUi=True
    )
    set_data_validation_for_cell_range(ws, 'B2:B{}'.format(count_row), validation_rule)

    print('Add sheet finished: {}'.format(target))



list_data = []
add_to_sheet('file sheet name', list_data)