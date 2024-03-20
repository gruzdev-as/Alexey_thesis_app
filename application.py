import os
import pandas as pd


from PyQt6 import QtWidgets, QtCore


import ui_files.main_design as design

class MainApplication(QtWidgets.QMainWindow, design.Ui_MainWindow):
    '''Main window class'''

    def __init__(self):

        super().__init__()
        self.setupUi(self)

        ## Constants


        ## Events 
        self.choosedata_button.clicked.connect(self.choose_data_file)
        self.build_poly_button.clicked.connect(self.draw_polynom)
    
    def choose_data_file(self):
        
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, 'Open File', '', "System (*.txt)"
        )

        if file_path:
            with open(file_path, 'r') as f:
                data_df = pd.read_csv('DATA.txt', sep=';', decimal='.')
                self.X_data, self.Y_data = data_df.X.to_numpy(), data_df.Y.to_numpy()
        else:
            return
        
    def draw_polynom(self):
        pass

