from PyQt6.QtCore import Qt
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt6.QtGui import QPalette


import sys
from rc_ui import Ui_MainWindow
from Iron_calculation import IronAnalysis

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfgen import canvas


class LabSystem(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.red)
       
        
        self.analysis = IronAnalysis()
        self.currentFactorIndex = 0
        self.sampleInputs = []
        self.ironsampleNames = ["SARM146", "SARM131", "NIST64C", "SARM144", "AMIS0388"]
        self.IronBiasLimitExceeded = False 
        self.factorTableUpdated = False
        
        self.updateFactorLabel()
        self.factor_next_button.clicked.connect(self.handleNextSample)
        self.sample_next_button.clicked.connect(self.addSampleToTable)
        self.Save.clicked.connect(lambda: self.saveTablesToPDF("table_data.pdf"))


    def showError(self, message):
        QMessageBox.critical(self, "Error", message)
        
    def updateFactorLabel(self):
        if self.currentFactorIndex < len(self.ironsampleNames):
            sampleName = self.ironsampleNames[self.currentFactorIndex]
            self.label.setText(f"Enter Information for {sampleName}")
        else:
            self.calculateAndPopulateTable()

    def handleNextSample(self):
        try:
            grams = float(self.factor_grams_value.text())
            ml = float(self.factor_ml_value.text())
            known_percent = float(self.factor_know_value.text())

            print(f"Adding: Grams={grams}, ML={ml}, Known%={known_percent}")

            self.sampleInputs.append({
                "name": self.ironsampleNames[self.currentFactorIndex],
                "grams": grams,
                "ml": ml,
                "known_percent": known_percent
            })
            print("Current sampleInputs:", self.sampleInputs)
            self.currentFactorIndex += 1
            self.updateFactorLabel()
            
                
            if self.currentFactorIndex >= len(self.ironsampleNames):
                # Hide input fields and labels
                self.factor_grams_text.hide()
                self.factor_know_value_text.hide()
                self.factor_ml_text.hide()
               
                
                self.factor_grams_value.hide()
                self.factor_ml_value.hide()
                self.factor_know_value.hide()
        
                
                # Change the button text and connect it to the new functionality
                self.factor_next_button.setText("Clear")
                self.factor_next_button.disconnect()  # Disconnect previous slot
                self.factor_next_button.clicked.connect(self.clearTables)

        except ValueError as e:
            self.showError("Please enter valid numeric values for grams, ml, and known percent.Use . not ,")
            return  # Return early to stop processing and allow user correction

        self.factor_grams_value.clear()
        self.factor_ml_value.clear()
        self.factor_know_value.clear()
    
    def show_factor_text_and_values(self):
        self.factor_grams_text.show()
        self.factor_know_value_text.show()
        self.factor_ml_text.show()
       
        self.factor_grams_value.show()
        self.factor_ml_value.show()
        self.factor_know_value.show()
        

        
    def clearTables(self):
        self.IronTableWidget.setRowCount(0)  # Clear the table completely
        self.tableWidget.setRowCount(0)  # Clear the table completely
        self.sampleInputs.clear()  


        self.currentFactorIndex = 0
        # Reset the sample inputs to clear previous data
        self.sampleInputs = []
        # Reset the bias limit exceeded flag
        self.IronBiasLimitExceeded = False
        # Re-enable the sample table in case it was disabled
        self.IronSampleTable.setEnabled(True)
        # Reset UI to initial state
        self.show_factor_text_and_values()
        # Optionally, if you have an LCD or display for the average factor, reset it as well
        self.factor_display.display(0)
        # Change the button text back to "Next" and reconnect the original functionality
        self.factor_next_button.setText("Next")
        self.factor_next_button.disconnect()
        self.factor_next_button.clicked.connect(self.handleNextSample)
        # Ensure the label is updated to prompt for the first sample again
        self.updateFactorLabel()
        self.initializeSampleNamesInTable()
      
    def initializeSampleNamesInTable(self):
        self.IronTableWidget.setRowCount(len(self.ironsampleNames))
        for row, name in enumerate(self.ironsampleNames):
            # Set sample names in the first column or as row headers as per your table setup
            self.IronTableWidget.setItem(row, 0, QTableWidgetItem(name))
            # If you're using row headers to display names: self.IronTableWidget.setVerticalHeaderItem(row, QTableWidgetItem(name))

    # Reset any other UI elements or states as necessary
    def show_sample_values_text(self):

        self.sample_grams_text.show()
        self.sample_ml_text.show()
        self.sample_ref_id_text.show()
        
        self.sample_grams.show()
        self.sample_ref_id.show()
        self.sample_ml.show()
    
    
    def hide_sample_values_text_and_values(self):
        self.sample_grams_text.hide()
        self.sample_ml_text.hide()
        self.sample_ref_id_text.hide()
        
        self.sample_grams.hide()
        self.sample_ref_id.hide()
        self.sample_ml.hide()
    
        
    def calculateAndPopulateTable(self):
        try:
            value_dict = {sample['name']: [sample['grams'], sample['ml'], sample['known_percent']]
                    for sample in self.sampleInputs}
            
            print("Value dict before calculation:", value_dict)
            
            results = self.analysis.calculate_factors(value_dict)
            
            if results is None:
                print("No results returned from calculations.")
                return
            if self.analysis.factor_average is not None:
                self.factor_display.display(self.analysis.factor_average)
             
            else:
                # Optional: Clear the display or handle the unset state as desired
                self.factor_display.display("")
         
            for row, result in enumerate(results):
            # result is now a list, so we access each element by index
                for col in range(len(result)):
                    print(f"Populating row {row} with: {result}")
                    item = QTableWidgetItem(str(result[col]))
                    item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                    self.IronTableWidget.setItem(row, col, item)
            
            # Check for bias after table population
            self.IronBiasLimitExceeded = False
            biases_over_limit = []
            for row, result in enumerate(results):
           
                bias_value = result[-1]  
                if abs(bias_value) >= 0.5:
                    self.IronBiasLimitExceeded = True
                    if row < len(self.ironsampleNames):
                        sample_name = self.ironsampleNames[row]
                        biases_over_limit.append(sample_name)

            # If any biases are over the limit, show a warning message
            if biases_over_limit:
                self.biasLimitExceeded = True  # Indicate that the bias limit has been exceeded
                self.IronSampleTable.setEnabled(False)  # Disable the sample table
                
                self.hide_sample_values_text_and_values()
                
                samples_with_issues = ", ".join(biases_over_limit)
                QMessageBox.warning(self, "Warning", f"Bias over 0.5% detected for samples: {samples_with_issues}. Please rerun tests.")
            else:
                self.biasLimitExceeded = False  # No bias issues, allow table interaction
                self.IronSampleTable.setEnabled(True) 

        except Exception as e:
            print(f"PrintError with calculations {e}")
            self.showError(f"An error occurred during calculation: {str(e)}")
    
    def addSampleToTable(self):
        # Get the inputs
        grams = self.sample_grams.text()
        ml = self.sample_ml.text()
        ref_id = self.sample_ref_id.text()

        # Convert inputs to float and validate
        try:
            grams = float(grams)
            ml = float(ml)
        except ValueError:
            self.showError("Please enter valid numeric values for grams and ml.")
            return

        # Add and calculate sample
        try:
            self.analysis.add_and_calculate_sample(ref_id, grams, ml)
        except ValueError as e:
            self.showError(str(e))
            return

        # Assuming the last entry in self.analysis.tested_samples is the current sample
        last_sample_data = self.analysis.tested_samples[-1]

        # Add the input data and calculated results to the table
        rowPosition = self.IronSampleTable.rowCount()
        self.IronSampleTable.insertRow(rowPosition)

        self.IronSampleTable.setItem(rowPosition, 0, QTableWidgetItem(ref_id))
        self.IronSampleTable.setItem(rowPosition, 1, QTableWidgetItem(str(grams)))
        self.IronSampleTable.setItem(rowPosition, 2, QTableWidgetItem(str(ml)))
        # Assuming you want to display other specific data in column 3, adjust as necessary
        # Update with calculated %Fe and %FeO from last_sample_data
        self.IronSampleTable.setItem(rowPosition, 3, QTableWidgetItem(str(last_sample_data[3])))  # %Fe
        self.IronSampleTable.setItem(rowPosition, 4, QTableWidgetItem(str(last_sample_data[4])))  # %FeO

        # Optionally clear the input fields for the next sample
        self.sample_ref_id.clear()
        self.sample_grams.clear()
        self.sample_ml.clear()
        
    def saveTablesToPDF(self, filename="table_data.pdf"):
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []

        # Prepare data for the Factors Table
        factors_data = [["Sample Name", "Grams", "Ml", "Known %", "Factor", "%Fe", "Bias", "%FeO"]]

        for row in range(self.IronTableWidget.rowCount()):
            row_data = [self.ironsampleNames[row]]  # Start each row with the sample name
            for col in range(self.IronTableWidget.columnCount()):
                item = self.IronTableWidget.item(row, col)
                row_data.append(item.text() if item else "")
            factors_data.append(row_data)

        # Add the Factors Table to the elements
        factors_table = Table(factors_data)
        factors_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke)
        ]))
        elements.append(factors_table)
        
        # Adding a space between tables
        elements.append(Table([[""]], colWidths=[doc.width]))
        
        # Prepare data for the Sample Table
        sample_data = [["Ref ID", "Grams", "Ml", "%Fe", "%FeO"]]
        for row in range(self.IronSampleTable.rowCount()):
            row_data = []
            for col in range(self.IronSampleTable.columnCount()):
                item = self.IronSampleTable.item(row, col)
                row_data.append(item.text() if item else "")
            sample_data.append(row_data)

        # Add the Sample Table to the elements
        sample_table = Table(sample_data)
        sample_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke)
        ]))
        elements.append(sample_table)

        # Build the PDF
        doc.build(elements)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LabSystem()
    window.show()
    sys.exit(app.exec())
