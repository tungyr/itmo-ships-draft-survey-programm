import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from openpyxl import Workbook
from openpyxl import load_workbook
from datetime import date, datetime, time

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


class App(QWidget):

    def __init__(self, data, vessel_name):
        super().__init__()
        self.title = 'PyQt5 file save dialog'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.data = data
        self.filename = ''
        self.vessel_name = vessel_name
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # self.openFileNameDialog()
        # self.openFileNamesDialog()
        self.saveFileDialog()
        self.save_xls()

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        time_stamp = str(datetime.today())
        time_stamp = f'{time_stamp[:13]}-{time_stamp[14:16]}'
        self.filename, _ = QFileDialog.getSaveFileName(self, "Save File", f"{time_stamp} - "
                                                        f"{self.vessel_name} draft calculation" + ".xlsx",
                                                  "Excel Files (*.xlsx);;All Files (*)", options=options)

        if '.xlsx' not in self.filename:
            self.filename = self.filename + ".xlsx"
            print(self.filename)

        return self.filename

    def save_xls(self):

        workbook = Workbook()
        sheet = workbook.active
        sheet["A1"] = f'Draft-survey calculation of m/v "{self.vessel_name}"'
        sheet["A2"] = str(datetime.today())[:16]
        sheet["A3"] = 'Results:'

        row = 4
        for label in labels:
            sheet["A" + str(row)] = label
            row += 1

        row = 4
        for item in self.data:
            sheet["B" + str(row)] = str(item)
            row += 1

        workbook.save(filename=self.filename)
        self.close()
        return



if __name__ == "__main__":

    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    ex.close()



