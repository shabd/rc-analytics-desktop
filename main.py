from PyQt6.QtCore import Qt
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt6.QtGui import QPalette

from rc_ui import Ui_MainWindow
from Chrome_conentrate_and_ore_cal import ChromeOreAnalysis

import sys


class LabSystem(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        
        self.chromeAnalysis = ChromeOreAnalysis()
        self.current_sample_index = 0
        self.chromeSampleValues = {}
        self.populate_known_samples_table()
        self.update_sample_info_label()
        self.cr_factor_next_button.clicked.connect(self.factor_results)
        self.cr_sample_next_button.clicked.connect(self.sample_results)  # Assuming addButton is the name of your "Add" button

        
    def showError(self, message):
        QMessageBox.critical(self, "Error", message)
        
        
    def populate_known_samples_table(self):
        self.cr_factor_TableWidget.setRowCount(len(self.chromeAnalysis.known_samples))
        for row, sample_name in enumerate(self.chromeAnalysis.known_samples.keys()):
            self.cr_factor_TableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(sample_name))
    
    
    def change_next_into_clear_button(self):
        self.cr_factor_next_button.setText("Clear")
        try:
            self.cr_factor_next_button.clicked.disconnect()
        except TypeError:
            # No connections exist yet, so ignore
            pass
        # Connect the clear functionality
        self.cr_factor_next_button.clicked.connect(self.clear_all_data)
                
    def update_sample_info_label(self):
        if self.current_sample_index < len(self.chromeAnalysis.known_samples):
            sample_name = list(self.chromeAnalysis.known_samples.keys())[self.current_sample_index]
            self.cr_sample_info.setText(f"Current Sample: {sample_name}")
        else:
            self.cr_sample_info.setText("All samples processed.")
            
    def factor_results(self):
  
        grams = float(self.cr_factor_grams_value.text())
        ml = float(self.cr_factor_ml_value.text())
        known_value = float(self.cr_factor_know_value.text())

        # Validate input before proceeding
        if not grams or not ml or not known_value:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        sample_name = list(self.chromeAnalysis.known_samples.keys())[self.current_sample_index]
        self.chromeSampleValues[sample_name] = (grams, ml, known_value)

        # Prepare for the next sample or finish
        self.current_sample_index += 1
        if self.current_sample_index >= len(self.chromeAnalysis.known_samples):
            # Since calculate_factors expects a dictionary, now we pass self.chromeSampleValues directly
            chrom_calculated_values = self.chromeAnalysis.calculate_factors(self.chromeSampleValues)
            self.display_results_in_table(chrom_calculated_values)
            
            bias_violation = False
            for result in chrom_calculated_values:
            # Assuming the bias is the last element in the result list
                if abs(result[-1]) > 0.5:
                    QMessageBox.warning(self, "Bias Violation", f"Sample '{result[0]}' exceeded the bias tolerance with a bias of {result[-1]}.")
                    self.lock_sample_table()
                    bias_violation = True
                    break
            if not bias_violation:
                self.unlock_sample_table()
            
            self.hide_inputs_and_calculate()
            self.change_next_into_clear_button()
        else:
            # Reset fields for the next sample
            self.cr_factor_grams_value.clear()
            self.cr_factor_ml_value.clear()
            self.cr_factor_know_value.clear()
            self.update_sample_info_label()
    
    def display_results_in_table(self, results):
        self.cr_factor_TableWidget.setRowCount(len(results))  # Assuming resultsTable is your QTableWidget
        for row, sample in enumerate(results):
            for col, data in enumerate(sample):
                self.cr_factor_TableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(str(data)))

    
    def lock_sample_table(self):
        self.cr_sample_tableWidget.setDisabled(True)
        self.cr_sample_next_button.setDisabled(True)

    def unlock_sample_table(self):
        self.cr_sample_tableWidget.setEnabled(True)
        self.cr_sample_next_button.setEnabled(True)

            
    def hide_inputs_and_calculate(self):
        # Hide UI elements
        self.cr_factor_grams_text.hide()
        self.cr_factor_grams_value.hide()
        self.cr_factor_ml_text.hide()
        self.cr_factor_ml_value.hide()
        self.cr_factor_know_value_text.hide()
        self.cr_factor_know_value.hide()
    
    def reset_current_state(self):
        self.chromeAnalysis = ChromeOreAnalysis()
        self.chromeSampleValues = {}
        self.current_sample_index = 0


    
    def show_all_factor_text_value(self):
        self.cr_factor_grams_text.show()
        self.cr_factor_grams_value.show()
        self.cr_factor_ml_text.show()
        self.cr_factor_ml_value.show()
        self.cr_factor_know_value_text.show()
        self.cr_factor_know_value.show()
        
    def clear_all_data(self):
   
        self.reset_current_state()
        self.show_all_factor_text_value()
  
        self.cr_factor_next_button.setText("Next")
        self.cr_factor_next_button.clicked.disconnect()
        self.cr_factor_next_button.clicked.connect(self.factor_results)
        # Optionally, clear any displayed results in your table
        self.cr_factor_TableWidget.clearContents()
        self.cr_factor_TableWidget.setRowCount(0)
        # Reset the UI to its initial state if needed
        
        self.cr_sample_tableWidget.clearContents()
        self.cr_sample_tableWidget.setRowCount(0)
        
        self.populate_known_samples_table()
        self.update_sample_info_label()
    
        self.unlock_sample_table() 
    
    def sample_results(self):
        # Collect the input data
        sample_id = self.cr_sample_ref_id_value.text()  # Assumes sampleIdLineEdit is your QLineEdit for sample ID
        grams = self.cr_sample_grams_value.text()  # Assumes gramsLineEdit is for grams input
        ml = self.cr_sample_ml_value.text()  # Assumes mlLineEdit is for ml input

        # Convert inputs to appropriate types (assuming grams and ml should be floats)
        try:
            grams_float = float(grams)
            ml_float = float(ml)
        except ValueError:
            # Handle invalid input (e.g., show an error message)
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please enter valid numbers for grams and ml.")
            return

        # Call add_and_calculate_sample with the collected data
        try:
            updated_samples = self.chromeAnalysis.add_and_calculate_sample(sample_id, grams_float, ml_float)
        except ValueError as e:
            # Handle the case where factor_average has not been calculated
            QtWidgets.QMessageBox.warning(self, "Calculation Error", str(e))
            return

        # Assuming the last entry in updated_samples is the one we just added
        last_entry = updated_samples[-1]
        # The expected format of last_entry is [ref_id, grams, ml, cal_percent_cr, calc_cr2o3]

        # Add the new entry to the table
        rowPosition = self.cr_sample_tableWidget.rowCount()
        self.cr_sample_tableWidget.insertRow(rowPosition)
        for col, item in enumerate(last_entry):
            self.cr_sample_tableWidget.setItem(rowPosition, col, QtWidgets.QTableWidgetItem(str(item)))

        # Optionally, clear the input fields after adding the data to the table
        self.cr_sample_ref_id_value.clear()
        self.cr_sample_grams_value.clear()
        self.cr_sample_ml_value.clear()

                
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LabSystem()
    window.show()
    sys.exit(app.exec())