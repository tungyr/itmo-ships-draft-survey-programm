from openpyxl import Workbook
from datetime import datetime

labels = ["Fwd mean draft, m: ",
            "Middle mean draft, m: ",
            "Aft mean draft, m: ",
            "Fwd mark misplacement, m: ",
            "Mid mark misplacement, m: ",
            "Aft mark misplacement, m: ",
            "Apparent trim, m: ",
            "Fwd draft correction, m: ",
            "Mid draft correction, m: ",
            "Aft draft correction, m: ",
            "Fwd corrected draft, m: ",
            "Mid corrected draft, m: ",
            "Aft corrected draft, m: ",
            "True trim, m: ",
            "Deflection: ",
            "Mean of means corrected, m:",
            "Displacement by MOMC, mt: ",
            "TPC, mt: ",
            "LCF, m: ",
            "First trim correction, mt:",
            "MTC by MOMC: ",
            "MTC +: ",
            "MTC -: ",
            "MTC difference: ",
            "Second trim correction, mt:",
            "Disp. corrected by trim, mt: ",
            "Constant, mt: ",
            "Displacement corrected, mt: "]


def export_xls(data):
    workbook = Workbook()
    sheet = workbook.active
    sheet["A1"] = 'Draft-survey calculation of m/v'
    sheet["A2"] = str(datetime.today())
    sheet["A3"] = 'Results:'
    print(datetime.today())

    row = 4
    for label in labels:
        sheet["A" + str(row)] = label
        row += 1
        print(label)

    row = 4
    for item in data:
        sheet["B" + str(row)] = str(item)
        row += 1

    workbook.save(filename="export.xlsx")
    return data
