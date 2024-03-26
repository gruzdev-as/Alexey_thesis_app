import numpy as np
from PyQt6 import QtCore
from sympy import S, symbols, lambdify
from scipy.integrate import quad
import math

class Calculation_Thread(QtCore.QThread):

    # GUI updated
    process_complete = QtCore.pyqtSignal(object, object)
    bar_changed = QtCore.pyqtSignal(float)

    def __init__(self, parameters):
        super(Calculation_Thread, self).__init__()
        
        # TODO how to unpack/use it better? 
        self.penetrability = parameters['penetrability']
        self.viscosity = parameters['viscosity']
        self.pressure_end = parameters['pressure_end']
        self.pressure_start = parameters['pressure_start']
        self.density = parameters['density']
        self.X_data = parameters['X_data']
        self.polynom = parameters['polynom']
        self.formula = parameters['formula']
        self.v_cap = parameters['v_cap']
    
    def run(self):
        
        def calculate_length(a, b):
            
            def calc_derr(x_):

                x = symbols('x')
                derrivative = self.formula.diff(x)
                return lambdify(x, derrivative)(x_)
            
            length, _ = quad(lambda x: math.sqrt(1+(calc_derr(x)**2)), a, b)
            return length
        
        def calc_velocity(l0:float, h0:float, l1:float, h1:float) -> float:
            return - (self.penetrability / self.viscosity) * (((self.pressure_end - self.pressure_start) / (l1 - l0)) - (self.density * 9.81 *(h1 - h0)))
            
        def search(left, l0, h0):

            right = max(self.X_data)
            max_l = calculate_length(0, right)

            while left <= right:
                
                # Выбираем точку на прямой 
                mid_point = (left + right) / 2

                # Определяем параметры в этой точке
                l_mid_point = calculate_length(0, mid_point)
                h_mid_point = self.polynom(mid_point)
                vf = calc_velocity(l0, h0, l_mid_point, h_mid_point)
                if round(l_mid_point, 3) == round(max_l, 3):
                    print('Дошел до конца прямой')
                    return(self.X_data.max(), h_mid_point, vf, l_mid_point)

                if round(vf, 4) == round(self.v_cap, 4):
                    print(f'Получено равенство скоростей Vk = {round(self.v_cap, 4)}, Vf = {round(vf, 4)}')
                    print(f'Получил нужное соотношение на точке {mid_point, h_mid_point}, на длине {l_mid_point}')
                    print('#'*50)
                    return(mid_point, h_mid_point, vf, l_mid_point)
                elif round(vf, 4) > round(self.v_cap, 4):
                    left = mid_point - 0.0002
                else:
                    right = mid_point + 0.0002

            return 0, 0, 0, 0
    
        h0, l0 = 0, 0
        points = []
        lengths  = []
        left = 0

        while round(left, 3) < round(max(self.X_data), 3):

            X_mid, y_mid, vf, l = search(left, l0, h0)
            points.append((round(X_mid, 4), round(y_mid, 4)))
            lengths.append(round(calculate_length(left, X_mid), 4))
            l0 = l
            h0 = y_mid
            left = X_mid

            self.bar_changed.emit(round(left / max(self.X_data), 2))    

        self.process_complete.emit(points, lengths)
