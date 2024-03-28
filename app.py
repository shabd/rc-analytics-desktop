from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication,QMainWindow, QMessageBox, QTableWidgetItem
from PyQt6.QtGui import QPalette,QDoubleValidator

from rc_ui import Ui_MainWindow
from Chrome_conentrate_and_ore_cal import ChromeOreAnalysis
from FeroChrome_calculation import FeroChromeAnalysis
from Iron_calculation import IronAnalysis

import sys


class LabSystem(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()


        self.KnownValue.currentChanged.connect(self.on_tab_changed)

        self.analysis=[] # put the three analysis here 
        self.init_analysis()

        self.table_widgets=[]
        self.init_table_widgets()

        self.values = {}
        self.labels = {}
        self.init_values_labels()

        self.sample_info_labels = [self.cr_sample_info,self.FeSampleInfo,self.label]

        self.index = 0
        self.init_tab()

        self.connect_next_buttons()
        
        

        self.hide_sample_calculations()
        # these shouldnot be like this , they should be like buttons

        self.set_on_text_changed()



    def on_tab_changed(self,index):
        self.index = index
        self.init_tab()


    def init_tab(self):
        self.current_sample_index = 0
        self.currentSampleValues = {}
        self.populate_known_samples_table()
        self.update_sample_info_label()


    def init_analysis(self):
        self.analysis.append(ChromeOreAnalysis())
        self.analysis.append(FeroChromeAnalysis())
        self.analysis.append(IronAnalysis())

    def init_table_widgets(self):
        self.table_widgets.append(self.cr_factor_TableWidget)
        self.table_widgets.append(self.FeFactorTableWidget)
        self.table_widgets.append(self.IronTableWidget)


    def init_values_labels(self):
        self.values['grams']=[self.cr_factor_grams_value, self.fe_factor_grams_value,self.factor_grams_value]  
        self.values['ml'] = [self.cr_factor_ml_value,self.fe_factor_ml_value,self.factor_ml_value]     
        self.values['know'] = [ self.cr_factor_know_value,self.fe_factor_know_value,self.factor_know_value]

        self.labels['grams'] =[self.cr_factor_grams_text,self.fe_factor_grams_text,self.iron_factor_grams_text]
        self.labels['ml']=[self.cr_factor_ml_text,self.fe_factor_ml_text,self.iron_factor_ml_text]
        self.labels['know'] = [self.cr_factor_know_value_text,self.fe_factor_know_value_text,self.iron_factor_know_value_text]

    


    def connect_next_buttons(self):
        self.cr_factor_next_button.clicked.connect(self.factor_results)
        self.cr_sample_next_button.clicked.connect(self.sample_results) 
        self.fe_factor_next_button.clicked.connect(self.factor_results)
        self.fe_sample_next_button.clicked.connect(self.sample_results)
        self.iron_factor_next_button.clicked.connect(self.factor_results)
        self.iron_sample_next_button.clicked.connect(self.sample_results)

    def set_on_text_changed(self):
        self.cr_factor_grams_value.textChanged.connect(self.update_grams_field)
        self.fe_factor_grams_value.textChanged.connect(self.update_grams_field)
        self.factor_grams_value.textChanged.connect(self.update_grams_field)

        self.cr_factor_ml_value.textChanged.connect(self.update_ml_field)
        self.fe_factor_ml_value.textChanged.connect(self.update_ml_field)
        self.factor_ml_value.textChanged.connect(self.update_ml_field)

        self.cr_factor_know_value.textChanged.connect(self.update_know_field)
        self.fe_factor_know_value.textChanged.connect(self.update_know_field)
        self.factor_know_value.textChanged.connect(self.update_know_field)

        
        
    def showError(self, message):
        QMessageBox.critical(self, "Error", message)
        
        
    def populate_known_samples_table(self):
        self.table_widgets[self.index].setRowCount(len(self.analysis[self.index].known_samples))
        for row, sample_name in enumerate(self.analysis[self.index].known_samples.keys()):
            self.table_widgets[self.index].setItem(row, 0, QTableWidgetItem(sample_name))
    
    
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
        if self.current_sample_index < len(self.analysis[self.index].known_samples):
            sample_name = list(self.analysis[self.index].known_samples.keys())[self.current_sample_index]
            self.sample_info_labels[self.index].setText(f"Current Sample: {sample_name}")
        else:
            self.sample_info_labels[self.index].setText("All samples processed.")
            
    def factor_results(self): 
        # self.check_not_empty() # check texts are not empty first
        grams = float(self.values['grams'][self.index].text())
        ml = float(self.values['ml'][self.index].text())
        known_value = float(self.values['know'][self.index].text())

        # Validate input before proceeding
        if not grams or not ml or not known_value:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        sample_name = list(self.analysis[self.index].known_samples.keys())[self.current_sample_index]
        self.currentSampleValues[sample_name] = (grams, ml, known_value)

        # Prepare for the next sample or finish
        self.current_sample_index += 1
        if self.current_sample_index >= len(self.analysis[self.index].known_samples):
            # Since calculate_factors expects a dictionary, now we pass self.currentSampleValues directly
            chrom_calculated_values = self.analysis[self.index].calculate_factors(self.currentSampleValues)
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
                self.show_sample_calculations()
                self.unlock_sample_table()
            
            self.hide_inputs_and_calculate()
            self.change_next_into_clear_button()
        else:
            # Reset fields for the next sample
            self.values['grams'][self.index].clear()
            self.values['ml'][self.index].clear()
            self.values['know'][self.index].clear()
            self.update_sample_info_label()
    
    def display_results_in_table(self, results):
        self.table_widgets[self.index].setRowCount(len(results))  # Assuming resultsTable is your QTableWidget
        for row, sample in enumerate(results):
            for col, data in enumerate(sample):
                self.table_widgets[self.index].setItem(row, col, QTableWidgetItem(str(data)))

    
    def lock_sample_table(self):
        self.cr_sample_tableWidget.setDisabled(True)
        self.cr_sample_next_button.setDisabled(True)

    def unlock_sample_table(self):
        self.cr_sample_tableWidget.setEnabled(True)
        self.cr_sample_next_button.setEnabled(True)

            
    def hide_inputs_and_calculate(self):
        # Hide UI elements
        self.labels['grams'][self.index].hide()
        self.values['grams'][self.index].hide()
        self.labels['ml'][self.index].hide()
        self.values['ml'][self.index].hide()
        self.labels['know'][self.index].hide()
        self.values['know'][self.index].hide()
    
    def reset_current_state(self):
        # self.chromeAnalysis = ChromeOreAnalysis()
        self.init_analysis()
        self.currentSampleValues = {}
        self.current_sample_index = 0


    
    def show_all_factor_text_value(self):
        self.labels['grams'][self.index].show()
        self.values['grams'][self.index].show()
        self.labels['ml'][self.index].show()
        self.values['ml'][self.index].show()
        self.labels['know'][self.index].show()
        self.values['know'][self.index].show()
        
    def clear_all_data(self):
   
        self.reset_current_state()
        self.show_all_factor_text_value()
  
        self.cr_factor_next_button.setText("Next")
        self.cr_factor_next_button.clicked.disconnect()
        self.cr_factor_next_button.clicked.connect(self.factor_results)
        # Optionally, clear any displayed results in your table
        self.table_widgets[self.index].clearContents()
        self.table_widgets[self.index].setRowCount(0)
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
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers for grams and ml.")
            return

        # Call add_and_calculate_sample with the collected data
        try:
            updated_samples = self.analysis[self.index].add_and_calculate_sample(sample_id, grams_float, ml_float)
        except ValueError as e:
            # Handle the case where factor_average has not been calculated
            QMessageBox.warning(self, "Calculation Error", str(e))
            return

        # Assuming the last entry in updated_samples is the one we just added
        last_entry = updated_samples[-1]
        # The expected format of last_entry is [ref_id, grams, ml, cal_percent_cr, calc_cr2o3]

        # Add the new entry to the table
        rowPosition = self.cr_sample_tableWidget.rowCount()
        self.cr_sample_tableWidget.insertRow(rowPosition)
        for col, item in enumerate(last_entry):
            self.cr_sample_tableWidget.setItem(rowPosition, col, QTableWidgetItem(str(item)))

        # Optionally, clear the input fields after adding the data to the table
        self.cr_sample_ref_id_value.clear()
        self.cr_sample_grams_value.clear()
        self.cr_sample_ml_value.clear()


    def hide_sample_calculations(self):
        self.cr_SampleCalculations.setVisible(False)
        self.cr_sample_tableWidget.setVisible(False)
        self.cr_save_button.setVisible(False)
        self.splitter_7.setVisible(False)



    def show_sample_calculations(self):
        self.cr_SampleCalculations.setVisible(True)
        self.cr_sample_tableWidget.setVisible(True)
        self.cr_save_button.setVisible(True)
        self.splitter_7.setVisible(True)

    def update_grams_field(self):
        text = self.values['grams'][self.index].text()
        self.table_widgets[self.index].setItem(self.current_sample_index, 1, QTableWidgetItem(text))

        

    def update_ml_field(self):
        text = self.values['ml'][self.index].text()
        self.table_widgets[self.index].setItem(self.current_sample_index, 2, QTableWidgetItem(text))


    def update_know_field(self):
        text = self.values['know'][self.index].text()
        self.table_widgets[self.index].setItem(self.current_sample_index, 5, QTableWidgetItem(text))

                        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LabSystem()
    window.show()
    sys.exit(app.exec())