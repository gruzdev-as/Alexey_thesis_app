import sys
from PyQt6 import QtWidgets

from application import MainApplication

def main():
        
    app = QtWidgets.QApplication(sys.argv)

    window = MainApplication()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()                                          