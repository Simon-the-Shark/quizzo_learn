import sys

from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QSizePolicy
def center(window):
    """ centers window """
    qr = window.frameGeometry()
    qr.moveCenter(QDesktopWidget().availableGeometry().center())
    window.move(qr.topLeft())
"""
class WelcomeWindow(QWidget):
    """""" Optional welcome page """"""
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
        self.load_ui()
        self.init_ui()
    def init_ui(self):
        self.show()
    def load_ui(self):
        mytests_button = QPushButton("MOJE TESTY")
        newtest_button = QPushButton("DODAJ TEST")
        bigtest_button = QPushButton("ZBUDUJ SPRAWDZIAN")

        mytests_button.setSizePolicy(QSizePolicy.Expanding,
                                     QSizePolicy.Preferred)
        newtest_button.setSizePolicy(QSizePolicy.Expanding,
                                     QSizePolicy.Preferred)
        bigtest_button.setSizePolicy(QSizePolicy.Expanding,
                                     QSizePolicy.Preferred)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(mytests_button,2)
        vbox.addStretch(1)
        vbox.addWidget(newtest_button,2)
        vbox.addStretch(1)
        vbox.addWidget(bigtest_button,2)
        vbox.addStretch(1)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox,3)
        hbox.addStretch(1)
        self.setLayout(hbox)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # welcome_window = WelcomeWindow()
    menu_window = MenuWindow()
    sys.exit(app.exec_())
