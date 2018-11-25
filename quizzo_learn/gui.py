import sys

from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel

def center(window):
    """ centers window """
    qr = window.frameGeometry()
    qr.moveCenter(QDesktopWidget().availableGeometry().center())
    window.move(qr.topLeft())
"""
class WelcomeWindow(QWidget):
    """ Optional welcome page """
    def __init__(self):
        super().__init__()
        # self.setWindowIcon(QIcon())
        self.setWindowTitle("QUIZZO LEARN - WITAJ !!!")
        self.resize(900,650)
        center(self)

        next_button = QPushButton("START")
        next_button.clicked.connect(self.next)
        vbox = QVBoxLayout()
        vbox.addWidget(next_button)

        self.setLayout(vbox)
        self.show()

    def next(self):
        self.close()
        menu_window.init_ui()
"""
class MenuWindow(QWidget):
    """main menu"""
    def __init__(self):
        super().__init__()
        # self.setWindowIcon(QIcon())
        self.setWindowTitle("QUIZZO LEARN")
        self.resize(900,650)
        center(self)

        self.init_ui()
    def init_ui(self):
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # welcome_window = WelcomeWindow()
    menu_window = MenuWindow()
    sys.exit(app.exec_())
