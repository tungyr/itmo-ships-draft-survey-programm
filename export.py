from openpyxl import Workbook
from datetime import datetime


def export_xls(data):
    workbook = Workbook()
    sheet = workbook.active
    sheet["A1"] = 'Draft-survey calculation of m/v'
    sheet["A2"] = str(datetime.today())
    sheet["A3"] = 'Results:'
    print(datetime.today())
    row = 4
    for item in data:
        sheet["A" + str(row)] = str(item)
        row += 1
    workbook.save(filename="export.xlsx")
    print(data)
    return data
