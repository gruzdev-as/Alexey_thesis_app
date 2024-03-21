from PyQt6 import QtCore, QtWidgets
import ui_files.additional_window as additional_window_ui 

class Additional_window(QtWidgets.QMainWindow, additional_window_ui.Ui_MainWindow):
    
    submitClicked = QtCore.pyqtSignal(list)

    def __init__(
        self,            
        penetrability,
        viscosity,
        density,
        preassure_start,
        preassure_end,
        capnum,
        sur_tension,
    ):
        
        super().__init__()
        self.setupUi(self)

        # Constant_values
        self.penetrability = penetrability
        self.viscosity = viscosity
        self.density = density
        self.preassure_start = preassure_start
        self.preassure_end = preassure_end
        self.capnum = capnum
        self.sur_tension = sur_tension
        # Set_text
        self.penetrability_edit.setText(str(self.penetrability))
        self.viscosity_edit.setText(str(self.viscosity))
        self.density_edit.setText(str( self.density))
        self.preassure_start_edit.setText(str(self.preassure_start))
        self.preassure_end_edit.setText(str( self.preassure_end))
        self.capnum_edit.setText(str(self.capnum))
        self.sur_tension_edit.setText(str(self.sur_tension))

        # Events 

        self.save_button.clicked.connect(self.save)
        self.exit_button.clicked.connect(self.close)

    def save(self):
            
        self.submitClicked.emit(
            [
            self.penetrability_edit.text(),
            self.viscosity_edit.text(),
            self.density_edit.text(),
            self.preassure_start_edit.text(),
            self.preassure_end_edit.text(),
            self.capnum_edit.text(),
            self.sur_tension_edit.text(),
            ]
        )
        self.close()