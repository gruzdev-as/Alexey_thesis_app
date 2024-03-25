import os
import numpy as np
import pandas as pd


from PyQt6 import QtWidgets, QtCore
from sympy import symbols, S, lambdify
from scipy.integrate import quad
import math

import ui_files.main_design as design
from graphic_widgets import MplCanvas
from additional_window import Additional_window
from thread import Calculation_Thread

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
        self.penetrability = 1.5e-10
        self.viscosity = 0.3
        self.density =  1.1e3
        self.pressure_start = 101325
        self.pressure_end = 15199
        self.capnum = 1000
        self.sur_tension = 4.6e-2
        self.v_cap = 0.0025
        ## Events 
        self.choosedata_button.clicked.connect(self.choose_data_file)
        self.build_poly_button.clicked.connect(self.draw_polynom)
        self.calculate_length_button.clicked.connect(self.show_lentgh)
        self.adjust_coef_button.clicked.connect(self.show_additional_window)
        self.start_search_button.clicked.connect(self.binary_search_points)
    
    def choose_data_file(self):
        
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, 'Open File', '', "System (*.txt)"
        )

        if file_path:
            with open(file_path, 'r') as f:
                data_df = pd.read_csv(file_path, sep=';', decimal='.')
                self.X_data, self.Y_data = data_df.X.to_numpy() / 1000, data_df.Y.to_numpy() / 1000

        else:
            return

        #Draw Point in the graph
        self.graph_first_widget.axes.plot(self.X_data, self.Y_data, '.')
        self.graph_first_widget.draw()
        self.build_poly_button.setEnabled(True)
        self.poly_degree_spinBox.setEnabled(True)
        
    def draw_polynom(self):
        
        polynom_degree = self.poly_degree_spinBox.value()
        coef = np.polyfit(self.X_data, self.Y_data, polynom_degree)
        self.polynom = np.poly1d(coef)
        self.x_poly_values = self.X_data
        self.y_poly_values = self.polynom(self.X_data)
        
        # Draw the line and points 
        self.graph_first_widget.axes.clear()
        self.graph_first_widget.axes.plot(self.X_data, self.Y_data, '.')
        self.graph_first_widget.axes.plot(self.x_poly_values, self.y_poly_values, color='red')
        self.graph_first_widget.draw()

        # Write the equation (not the beauty form)
        x = symbols('x')
        self.formula = sum(S("{:}".format(v))*x**i for i, v in enumerate(coef[::-1]))
        self.poly_display_textbrowser.setText(str(self.formula))

        self.pointA_lineEdit.setEnabled(True)
        self.pointB_lineedit.setEnabled(True)
        self.calculate_length_button.setEnabled(True)
        self.adjust_coef_button.setEnabled(True)
        self.start_search_button.setEnabled(True)

    def show_lentgh(self):
        
        a = float(self.pointA_lineEdit.text())
        b = float(self.pointB_lineedit.text())

        length = self.calculate_length(a, b)

        self.length_label.setText(f'Длина участка от А до B = {length}')

        # Draw the trajectory and points on it in the second view
        self.graph_first_widget.axes.plot(a, self.polynom(a), '.', markersize=10., color='green')
        self.graph_first_widget.axes.plot(b, self.polynom(b), '.', markersize=10., color='green')
        self.graph_first_widget.draw()

    def calculate_length(self, a, b):
        def calc_derr(x_):

            x = symbols('x')
            derrivative = self.formula.diff(x)
            return lambdify(x, derrivative)(x_)
        
        length, _ = quad(lambda x: math.sqrt(1+(calc_derr(x)**2)), a, b)
        
        return length

    def show_additional_window(self):
        '''Show the window with additional hydro_system settigs'''
        
        def aplly_changes(array):
            
            self.penetrability = float(array[0])
            self.viscosity = float(array[1])
            self.density = float(array[2])
            self.pressure_start = float(array[3])
            self.pressure_end = float(array[4])
            self.capnum = float(array[5])
            self.sur_tension = float(array[6])

        self.edit_window = Additional_window(
            self.penetrability,
            self.viscosity,
            self.density,
            self.pressure_start,
            self.pressure_end,
            self.capnum,
            self.sur_tension,
        )
        self.edit_window.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.edit_window.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose, True)   
        self.edit_window.submitClicked.connect(aplly_changes)
        self.edit_window.show()
    
    def binary_search_points(self):
        '''Bin search for points in the trajectory'''
        def visualize(points, lengths):
            self.search_textBrowser.append(f'Рассчет закончен успешно!')
            self.search_textBrowser.append('#'*35)
            self.graph_second_widget.axes.plot(self.x_poly_values, self.y_poly_values, color='red')
            for i in range(len(points[:-1])):
                self.search_textBrowser.append(f'{points[i]} на длине {lengths[i]}')
                self.graph_second_widget.axes.plot(points[i][0], points[i][1], '.', markersize = 15, color='Black')
                
            self.graph_second_widget.axes.grid()
            self.graph_second_widget.draw()

        self.search_textBrowser.append(f'Начинаю расчет точек')
        self.calc_thread = Calculation_Thread(self.__dict__)
        self.calc_thread.start()
        self.calc_thread.process_complete.connect(visualize)