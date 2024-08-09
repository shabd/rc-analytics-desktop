from PyQt6.QtWidgets import QDialog
from names import Ui_Dialog
class NamesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        
