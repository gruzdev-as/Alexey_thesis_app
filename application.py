import os
import numpy as np
import pandas as pd


from PyQt6 import QtWidgets, QtCore
from sympy import symbols, S


import ui_files.main_design as design
from graphic_widgets import MplCanvas

class MainApplication(QtWidgets.QMainWindow, design.Ui_MainWindow):
    '''Main window class'''

    def __init__(self):

        super().__init__()
        self.setupUi(self)

        ## Graphic Widgets
        self.graph_first_widget = MplCanvas()
        self.first_display_widget_lay = QtWidgets.QHBoxLayout(
            self.first_display_widget
            )
        self.first_display_widget_lay.addWidget(self.graph_first_widget) 

        self.graph_second_widget = MplCanvas()
        self.second_display_widget_lay = QtWidgets.QHBoxLayout(
            self.second_display_widget
            )
        self.second_display_widget_lay.addWidget(self.graph_second_widget) 
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
                data_df = pd.read_csv(file_path, sep=';', decimal='.')
                self.X_data, self.Y_data = data_df.X.to_numpy(), data_df.Y.to_numpy()
        else:
            return

        #Draw Point in the graph
        self.graph_first_widget.axes.plot(self.X_data, self.Y_data, '.')
        self.graph_first_widget.draw()
        
    def draw_polynom(self):
        
        polynom_degree = self.poly_degree_spinBox.value()
        coef = np.polyfit(self.X_data, self.Y_data, polynom_degree)
        polynom = np.poly1d(coef)
        self.x_poly_values = self.X_data
        self.y_poly_values = polynom(self.X_data)
        
        # Draw the line 
        self.graph_first_widget.axes.plot(self.x_poly_values, self.y_poly_values, color='red')
        self.graph_first_widget.draw()

        # Write the equation (not the beauty form)
        x = symbols('x')
        formula = sum(S("{:}".format(v))*x**i for i, v in enumerate(coef[::-1]))
        self.poly_display_textbrowser.setText(str(formula))


