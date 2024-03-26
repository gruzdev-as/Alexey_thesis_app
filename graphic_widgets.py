from matplotlib.figure import Figure # for import figure into the app
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MplCanvas(FigureCanvas):
    ''' The class describe a figure for import them into the apps widget '''

    def __init__(self):
        ''' Executed when the class is instantiated '''
        fig = Figure() # Create a figure
        self.axes = fig.add_subplot(111)
        self.axes.grid()
        fig.subplots_adjust(hspace = 0.5, # hspace = height space
                            left = 0.08,
                            right = 0.98, # 1 - 0.98 = 0.2
                            top = 0.95, # 1 - 0.95 = 0.5
                            bottom = 0.1)
        super().__init__(fig)