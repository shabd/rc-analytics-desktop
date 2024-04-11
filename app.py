from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication,QMainWindow, QMessageBox, QTableWidgetItem,QLCDNumber,QTableWidget
from PyQt6.QtGui import QPalette,QDoubleValidator,QIcon

from rc_ui import Ui_MainWindow
from Chrome_conentrate_and_ore_cal import ChromeOreAnalysis
from FeroChrome_calculation import FeroChromeAnalysis
from Iron_calculation import IronAnalysis

import sys
import time
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph
from reportlab.lib.styles import ParagraphStyle, TA_LEFT

from reportlab.pdfgen import canvas


class LabSystem(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.setWindowTitle("RCI Analytical Services")
        icon = QIcon("Pics/logo.ico")
        self.setWindowIcon(icon)

        self.KnownValue.currentChanged.connect(self.on_tab_changed)

        self.analysis=[] # put the three analysis here 
        self.init_analysis()
        self.current_sample_index = [0,0,0]
        self.currentSampleValues = [{},{},{}]

        self.calculated =[False,False,False]

        self.table_widgets=[]
        self.init_table_widgets()

        self.values = {}
        self.labels = {}
        self.init_values_labels()

        self.sample_values = {}
        self.sample_labels = {}
        self.sample_cal_labels = [self.cr_SampleCalculations,self.feSampletabletext,self.SampleCalculations]
        self.splitters =[self.splitter_7,self.splitter_2,self.splitter_5]
        self.init_sample_values_labels()
        self.init_edit()

        self.sample_info_labels = [self.cr_sample_info,self.FeSampleInfo,self.label]

        self.factor_next_buttons = [self.cr_factor_next_button,self.fe_factor_next_button,self.iron_factor_next_button]

        self.sample_table_widgets = [self.cr_sample_tableWidget,self.fe_tableWidget,self.IronSampleTable]
        for table in self.sample_table_widgets:
            table.cellChanged.connect(self.sample_item_changed)

        # self.sample_save_buttons = [self.cr_save_button,self.fe_save_button,self.IronSaveButton]

        self.sample_next_buttons = [self.cr_sample_next_button,self.fe_sample_next_button,self.iron_sample_next_button]

        self.factor_displays = [self.cr_factor_display,self.fe_factor_display,self.factor_display]
        for display in self.factor_displays:
            display.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
            display.setStyleSheet("QLCDNumber { color: white;background-color:red }")



        self.index = 0
        self.init_tab()

        self.connect_next_buttons()
        self.save_button.clicked.connect(self.saveAllTables)

        # self.connect_save_buttons()
        
        self.set_on_text_changed()


    def on_tab_changed(self,index):
        self.index = index
        if self.current_sample_index[self.index] ==0:
            self.init_tab()
        # if  self.calculated[self.index] == False: # need to add condition of not cleared
        #     self.init_tab() 


    def init_tab(self):
        self.current_sample_index[self.index] = 0
        self.currentSampleValues[self.index] = {}
        self.populate_known_samples_table()
        self.update_sample_info_label()
        self.hide_sample_calculations()
        self.hide_edit()



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
        # self.values['know'] = [ self.cr_factor_know_value,self.fe_factor_know_value,self.factor_know_value]

        self.labels['grams'] =[self.cr_factor_grams_text,self.fe_factor_grams_text,self.iron_factor_grams_text]
        self.labels['ml']=[self.cr_factor_ml_text,self.fe_factor_ml_text,self.iron_factor_ml_text]
        # self.labels['know'] = [self.cr_factor_know_value_text,self.fe_factor_know_value_text,self.iron_factor_know_value_text]


    def init_sample_values_labels(self):
        self.sample_values['ref_id']=[self.cr_sample_ref_id_value,self.fe_sample_ref_id,self.sample_ref_id]
        self.sample_values['grams']=[self.cr_sample_grams_value,self.fe_sample_grams_value,self.sample_grams]
        self.sample_values['ml']=[self.cr_sample_ml_value,self.fe_sample_ml_value,self.sample_ml]


        # Are these needed ? or should be deleted?
        self.sample_labels['ref_id']=[self.cr_sample_ref_id_text,self.fe_sample_ref_id_text,self.sample_ref_id_text]
        self.sample_labels['grams']=[self.cr_sample_grams_text,self.fe_sample_grams_text,self.sample_grams_text]
        self.sample_labels['ml']=[self.cr_sample_ml_text,self.fe_sample_ml_text,self.sample_ml_text]
    

    def init_edit(self):
        self.edit_labels = [self.cr_edit_label,self.fe_edit_label,self.iron_edit_label]
        self.sample_comboboxes = [self.cr_sample_combobox,self.fe_sample_combobox,self.iron_sample_combobox]
        self.input_comboboxes = [self.cr_input_combobox,self.fe_input_combobox,self.iron_input_combobox]
        self.edit_inputs = [self.cr_edit_input,self.fe_edit_input,self.iron_edit_input]
        self.edit_buttons = [self.ce_edit_button,self.fe_edit_button,self.iron_edit_button]


    def connect_next_buttons(self):
        self.cr_factor_next_button.clicked.connect(self.factor_results)
        self.cr_sample_next_button.clicked.connect(self.sample_results) 
        self.fe_factor_next_button.clicked.connect(self.factor_results)
        self.fe_sample_next_button.clicked.connect(self.sample_results)
        self.iron_factor_next_button.clicked.connect(self.factor_results)
        self.iron_sample_next_button.clicked.connect(self.sample_results)


    # def connect_save_buttons(self):
    #     self.cr_save_button.clicked.connect(lambda: self.saveTablesToPDF("table_data_cr"))
    #     self.fe_save_button.clicked.connect(lambda: self.saveTablesToPDF("table_data_fe"))
    #     self.IronSaveButton.clicked.connect(lambda: self.saveTablesToPDF("table_data_iron"))

    def set_on_text_changed(self):
        self.cr_factor_grams_value.textChanged.connect(self.update_grams_field)
        self.fe_factor_grams_value.textChanged.connect(self.update_grams_field)
        self.factor_grams_value.textChanged.connect(self.update_grams_field)

        self.cr_factor_ml_value.textChanged.connect(self.update_ml_field)
        self.fe_factor_ml_value.textChanged.connect(self.update_ml_field)
        self.factor_ml_value.textChanged.connect(self.update_ml_field)

        # self.cr_factor_know_value.textChanged.connect(self.update_know_field)
        # self.fe_factor_know_value.textChanged.connect(self.update_know_field)
        # self.factor_know_value.textChanged.connect(self.update_know_field)

    def sample_item_changed(self,row,col):
        if col in (0, 1, 2):  # Check if edited column is 1 (grams) or 2 (ml) # add 0 also to edit ref id in 
            self.update_row_values(row)

    def update_row_values(self,row):
        try:
            try:
                sample_id = self.sample_table_widgets[self.index].item(row, 0).text()
                grams_text = self.sample_table_widgets[self.index].item(row, 1).text()
                ml_text = self.sample_table_widgets[self.index].item(row, 2).text()
            except: # means table is not populated yet so no need to go through this function..
                return

            grams_float = float(grams_text)
            ml_float = float(ml_text)
            edit = True
            
            updated_samples = self.analysis[self.index].add_and_calculate_sample(sample_id, grams_float, ml_float,edit,row)
            last_entry = updated_samples[row]

            self.sample_table_widgets[self.index].setItem(row, 3, QTableWidgetItem(str(last_entry[3])))  # cal_percent_cr
            # Make columns 3 and 4 non-editable
            # self.sample_table_widgets[self.index].item(row, 3).setFlags(Qt.ItemFlag.ItemIsEnabled)

            if self.index != 1:
                self.sample_table_widgets[self.index].setItem(row, 4, QTableWidgetItem(str(last_entry[4])))  


        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers for grams and ml.")


        
        
    def showError(self, message):
        QMessageBox.critical(self, "Error", message)
        
        
    def populate_known_samples_table(self):
        self.table_widgets[self.index].setRowCount(len(self.analysis[self.index].known_samples))
        for row, sample_name in enumerate(self.analysis[self.index].known_samples.keys()):
            self.table_widgets[self.index].setItem(row, 0, QTableWidgetItem(sample_name))
            self.table_widgets[self.index].item(row, 0).setFlags(Qt.ItemFlag.ItemIsEnabled)
            value = self.analysis[self.index].known_values[row]
            self.table_widgets[self.index].setItem(row, 5, QTableWidgetItem(str(value)))
            self.table_widgets[self.index].item(row, 5).setFlags(Qt.ItemFlag.ItemIsEnabled)

    
    
    def change_next_into_clear_button(self):
        self.factor_next_buttons[self.index].setText("Clear")
        try:
            self.factor_next_buttons[self.index].clicked.disconnect()
        except TypeError:
            # No connections exist yet, so ignore
            pass
        # Connect the clear functionality
        self.factor_next_buttons[self.index].clicked.connect(self.clear_all_data)

                
    def update_sample_info_label(self):
        if self.current_sample_index[self.index] < len(self.analysis[self.index].known_samples):
            sample_name = list(self.analysis[self.index].known_samples.keys())[self.current_sample_index[self.index]]
            self.sample_info_labels[self.index].setText(f"Current Sample: {sample_name}")
        else:
            self.sample_info_labels[self.index].setText("All samples processed.")
            
    def factor_results(self): 
        # self.check_not_empty() # check texts are not empty first
        try:
            grams = float(self.values['grams'][self.index].text())
            ml = float(self.values['ml'][self.index].text())
            # known_value = float(self.values['know'][self.index].text())
        except:

            # Validate input before proceeding
            # if not grams or not ml or not known_value:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields with valid values.")
            return

        sample_name = list(self.analysis[self.index].known_samples.keys())[self.current_sample_index[self.index]]
        self.currentSampleValues[self.index][sample_name] = (grams, ml)#, known_value)

        # Prepare for the next sample or finish
        self.current_sample_index[self.index] += 1
        if self.current_sample_index[self.index] >= len(self.analysis[self.index].known_samples):
            # Since calculate_factors expects a dictionary, now we pass self.currentSampleValues directly
            chrom_calculated_values = self.analysis[self.index].calculate_factors(self.currentSampleValues[self.index])
            self.display_results_in_table(chrom_calculated_values)
            
            bias_violation = False
            for result in chrom_calculated_values:
            # Assuming the bias is the last element in the result list
                if abs(result[6]) > 0.5:
                    QMessageBox.warning(self, "Bias Violation", f"Sample '{result[0]}' exceeded the bias tolerance with a bias of {result[-1]}.")
                    bias_violation = True
                    break
            if not bias_violation:
                self.calculated[self.index]= True
                self.show_sample_calculations() # show the second step table
                self.update_factor_display()
            
            self.hide_inputs_and_calculate()
            self.change_next_into_clear_button()
            # self.show_edit()

        else:
            self.update_sample_info_label()

        # Reset fields for the next sample
        self.values['grams'][self.index].clear()
        self.values['ml'][self.index].clear()
        # self.values['know'][self.index].clear()
    
    def display_results_in_table(self, results):
        self.table_widgets[self.index].setRowCount(len(results))  # Assuming resultsTable is your QTableWidget
        for row, sample in enumerate(results):
            for col, data in enumerate(sample):
                self.table_widgets[self.index].setItem(row, col, QTableWidgetItem(str(data)))
                self.table_widgets[self.index].item(row, col).setFlags(Qt.ItemFlag.ItemIsEnabled)


    def update_factor_display(self):
        factor_average = self.analysis[self.index].factor_average
        self.factor_displays[self.index].display(factor_average)

    def clear_display(self):
        self.factor_displays[self.index].display(0)

            
    def hide_inputs_and_calculate(self):
        # Hide UI elements
        self.labels['grams'][self.index].hide()
        self.values['grams'][self.index].hide()
        self.labels['ml'][self.index].hide()
        self.values['ml'][self.index].hide()
        # self.labels['know'][self.index].hide()
        # self.values['know'][self.index].hide()
    
    def reset_current_state(self):
        self.init_analysis()
        self.currentSampleValues[self.index] = {}
        self.current_sample_index[self.index] = 0




    
    def show_all_factor_text_value(self):
        self.labels['grams'][self.index].show()
        self.values['grams'][self.index].show()
        self.labels['ml'][self.index].show()
        self.values['ml'][self.index].show()
        # self.labels['know'][self.index].show()
        # self.values['know'][self.index].show()
        
    def clear_all_data(self):
   
        self.reset_current_state()
        self.show_all_factor_text_value()
  
        self.factor_next_buttons[self.index].setText("Next")
        self.factor_next_buttons[self.index].clicked.disconnect()
        self.factor_next_buttons[self.index].clicked.connect(self.factor_results)
        # Optionally, clear any displayed results in your table
        self.table_widgets[self.index].clearContents() 
        self.table_widgets[self.index].setRowCount(0)
        # Reset the UI to its initial state if needed
        
        self.sample_table_widgets[self.index].clearContents()
        self.sample_table_widgets[self.index].setRowCount(0)
        
        self.populate_known_samples_table()
        self.update_sample_info_label()
        self.hide_sample_calculations()

        self.clear_display()
        self.calculated[self.index ] = False
    
    def sample_results(self):
        # Collect the input data
        sample_id = self.sample_values['ref_id'][self.index].text()  # Assumes sampleIdLineEdit is your QLineEdit for sample ID
        grams = self.sample_values['grams'][self.index].text()  # Assumes gramsLineEdit is for grams input
        ml = self.sample_values['ml'][self.index].text()  # Assumes mlLineEdit is for ml input

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
        rowPosition = self.sample_table_widgets[self.index].rowCount()
        self.sample_table_widgets[self.index].insertRow(rowPosition)
        for col, item in enumerate(last_entry):
            self.sample_table_widgets[self.index].setItem(rowPosition, col, QTableWidgetItem(str(item)))
        # make them not editable
        self.sample_table_widgets[self.index].item(rowPosition, 3).setFlags(Qt.ItemFlag.ItemIsEnabled)
        if self.index != 1:
            self.sample_table_widgets[self.index].item(rowPosition, 4).setFlags(Qt.ItemFlag.ItemIsEnabled)  # Column 4 (calc_cr2o3)




        # Optionally, clear the input fields after adding the data to the table
        self.sample_values['ref_id'][self.index].clear()
        self.sample_values['grams'][self.index].clear()
        self.sample_values['ml'][self.index].clear()
        


    def hide_edit(self):
        self.edit_labels[self.index].setVisible(False)
        self.sample_comboboxes[self.index].setVisible(False)
        self.input_comboboxes[self.index].setVisible(False)
        self.edit_inputs[self.index].setVisible(False)
        self.edit_buttons[self.index].setVisible(False)

    

    def show_edit(self):
        self.edit_labels[self.index].setVisible(True)
        self.sample_comboboxes[self.index].setVisible(True)
        self.input_comboboxes[self.index].setVisible(True)
        self.edit_inputs[self.index].setVisible(True)
        self.edit_buttons[self.index].setVisible(True)

    def hide_sample_calculations(self):
        self.sample_cal_labels[self.index].setVisible(False)
        self.sample_table_widgets[self.index].setVisible(False)
        # self.sample_save_buttons[self.index].setVisible(False)
        self.splitters[self.index].setVisible(False)

        self.save_button.setVisible(False)


    def show_sample_calculations(self):
        self.sample_cal_labels[self.index].setVisible(True)
        self.sample_table_widgets[self.index].setVisible(True)
        # self.sample_save_buttons[self.index].setVisible(True)
        self.splitters[self.index].setVisible(True)

        # show save buttons if all 3 tables are calculated!!! TODO

    def update_grams_field(self):
        text = self.values['grams'][self.index].text()
        self.table_widgets[self.index].setItem(self.current_sample_index[self.index], 1, QTableWidgetItem(text))
        try:
            self.table_widgets[self.index].item(self.current_sample_index[self.index], 1).setFlags(Qt.ItemFlag.ItemIsEnabled)
        except:
            pass


        

    def update_ml_field(self):
        text = self.values['ml'][self.index].text()
        self.table_widgets[self.index].setItem(self.current_sample_index[self.index], 2, QTableWidgetItem(text))
        try:
            self.table_widgets[self.index].item(self.current_sample_index[self.index], 2).setFlags(Qt.ItemFlag.ItemIsEnabled)
        except:
            pass



    # def update_know_field(self):
    #     text = self.values['know'][self.index].text()
    #     self.table_widgets[self.index].setItem(self.current_sample_index[self.index], 5, QTableWidgetItem(text))
    #     try:
    #         self.table_widgets[self.index].item(self.current_sample_index[self.index], 5).setFlags(Qt.ItemFlag.ItemIsEnabled)
    #     except:
    #         pass


    def saveAllTables(self):
        pass


    def saveTablesToPDF(self, filename):
        try:
            current_time = time.strftime("Date_%d-%m-%Y_Time_%H-%M-%S")
            ext=".pdf"
            final_name = f"{filename}_{current_time}{ext}"

            doc = SimpleDocTemplate(final_name, pagesize=letter, leftMargin=50)
            elements = []

            # Prepare data for the Factors Table
            factors_data = [[["Sample Name", "Grams", "Ml", "Factor", "%CR", "Known %", "Bias"]],
                            [["Sample Name", "Grams", "Ml", "Factor", "%CR", "Known %", "Bias"]],
                            [["Sample Name", "Grams", "Ml", "Known %", "Factor", "%Fe", "Bias", "%FeO"]]]

            for row in range(self.table_widgets[self.index].rowCount()):
                # names_of_samples = list(self.analysis[self.index].known_samples.keys())
                # row_data = [names_of_samples[row]]  # Start each row with the sample name
                row_data=[]
                for col in range(self.table_widgets[self.index].columnCount()):
                    item = self.table_widgets[self.index].item(row, col)
                    row_data.append(item.text() if item else "")
                factors_data[self.index].append(row_data)

            # Add the Factors Table to the elements
            factors_table = Table(factors_data[self.index], hAlign='LEFT')
            factors_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('GRID', (0,0), (-1,-1), 1, colors.black),
                ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke)
            ]))

            
            elements.append(Paragraph(f"<b>Factor Calculation Table</b>", style=ParagraphStyle(
                            alignment=TA_LEFT,  
                            fontSize=24,   
                            fontName="Helvetica-Bold",
                            name='FactorCalculationTable'
                        )))
            elements.append(Table([[""]], colWidths=[doc.width]))

            elements.append(factors_table)
            
            # Adding a space between tables
            elements.append(Table([[""]], colWidths=[doc.width]))

            factor_average = self.analysis[self.index].factor_average
            elements.append(Paragraph(f"<b>Factor Average: {factor_average:.6f}</b>", style=ParagraphStyle(
                alignment=TA_LEFT,  
                fontSize=10,   
                fontName="Helvetica-Bold",
                name='FactorAverage'
            )))


            # standard_deviation = self.analysis[self.index].standard_deviation
            # elements.append(Paragraph(f"<b>Factor Standard Deviation: {standard_deviation:.6f}</b>", style=ParagraphStyle(
            #     alignment=TA_LEFT,  
            #     fontSize=10,   
            #     fontName="Helvetica-Bold",
            #     name='StandardDeviation'
            # )))

            # coefficient_of_variation = self.analysis[self.index].coefficient_of_variation
            # elements.append(Paragraph(f"<b>Factor Standard Deviation Percentage: {coefficient_of_variation:.2f}</b>", style=ParagraphStyle(
            #     alignment=TA_LEFT,  
            #     fontSize=10,   
            #     fontName="Helvetica-Bold",
            #     name= 'StandardDeviationPercentage'
            # )))

            elements.append(Table([[""]], colWidths=[doc.width]))

            elements.append(Paragraph(f"<b>Sample Calculation Table</b>", style=ParagraphStyle(
                            alignment=TA_LEFT,  
                            fontSize=24,   
                            fontName="Helvetica-Bold",
                            name='SampleCalculationTable'
                        )))
            
            elements.append(Table([[""]], colWidths=[doc.width]))



            
            # Prepare data for the Sample Table
            sample_data = [[["Ref ID", "Grams", "Ml", "Cal % CR","% Calc Cr2O3"]],
                        [["Ref ID", "Grams", "Ml", "Cal % CR"]],
                        [["Ref ID", "Grams", "Ml", "%Fe", "%FeO"]]]
            for row in range(self.sample_table_widgets[self.index].rowCount()):
                row_data = []
                for col in range(self.sample_table_widgets[self.index].columnCount()):
                    item = self.sample_table_widgets[self.index].item(row, col)
                    row_data.append(item.text() if item else "")
                sample_data[self.index].append(row_data)

            # Add the Sample Table to the elements
            sample_table = Table(sample_data[self.index], hAlign='LEFT')
            sample_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('GRID', (0,0), (-1,-1), 1, colors.black),
                ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke)
            ]))
            elements.append(sample_table)
            # Build the PDF
            doc.build(elements)
            QMessageBox.information(self, "Success", f"Data saved successfully to {final_name}!")
        except:
            QMessageBox.warning(self, "Error in Saving PDF", "An Error Occured during Saving the file , please try again later")





                        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LabSystem()
    window.show()
    sys.exit(app.exec())