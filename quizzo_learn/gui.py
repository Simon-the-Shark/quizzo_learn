import sys
import os.path
from random import sample

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, \
    QSizePolicy, QListWidget, QListWidgetItem, QInputDialog, QLineEdit, QMessageBox, QTextEdit

import quizzo_learn.files_interactions


def center(window):
    """ centers window """
    qr = window.frameGeometry()
    qr.moveCenter(QDesktopWidget().availableGeometry().center())
    window.move(qr.topLeft())


def text_dialog(parent, title, question):
    """ gets text """
    text, ok_pressed = QInputDialog.getText(parent, title, question, QLineEdit.Normal)
    if ok_pressed and text:
        return text
    else:
        return None


class QItemTest(QWidget):
    def __init__(self, name):
        super().__init__()
        self.name = name

        delete_button = QPushButton("")
        delete_button.setIcon(QIcon(os.path.join(os.pardir, "res", "img", "delete-icon.png")))
        delete_button.setIconSize(QSize(20, 20))
        delete_button.setStyleSheet("background-color: grey;")
        delete_button.clicked.connect(self.delete_button_act)

        layout = QHBoxLayout()

        label = QLabel(name)

        button = QPushButton("ROZWIĄŻ =>")
        button.setStyleSheet("background-color:LimeGreen; color:azure")
        button.clicked.connect(self.button_act)

        layout.addWidget(label, 20)
        layout.addWidget(delete_button, 1)
        layout.addWidget(button, 3)
        self.setLayout(layout)

    def button_act(self):
        my_tests_window.start_test(self.name)

    def delete_button_act(self):
        alert = QMessageBox.warning(self, "UWAGA !!!",
                                    "JESTEŚ PEWIEN, ŻE CHCESZ USUNĄĆ TEN ({}) TEST ???".format(self.name),
                                    QMessageBox.Yes, QMessageBox.No)
        if alert == QMessageBox.Yes:
            input = text_dialog(self, "USUWANIE",
                                "DLA OCHRONY PRZED POMYŁKAMI PRZEPISZ  NAZWĘ ({}) TESTU".format(self.name))
            if input == self.name:
                my_tests_window.deleting(self.name)


class QItemQuestion(QWidget):
    """ a simple widget for MyQListWidgetItem"""

    def __init__(self, id, frase1, frase2):
        super().__init__()
        self.id = id
        delete_button = QPushButton("")
        delete_button.setIcon(QIcon(os.path.join(os.pardir, "res", "img", "delete-icon.png")))
        delete_button.setIconSize(QSize(40, 40))
        delete_button.setStyleSheet("background-color: grey;")
        delete_button.clicked.connect(self.delete_button_act)

        label1 = QLabel(frase1)
        label2 = QLabel(frase2)

        layout = QHBoxLayout()
        layout.addWidget(label1, 5)
        layout.addWidget(QLabel("="), 1)
        layout.addWidget(label2, 5)
        layout.addWidget(delete_button)

        self.setLayout(layout)

    def delete_button_act(self):
        new_test_window.deleting(self.id)


class MenuWindow(QWidget):
    """main menu"""

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(os.path.join(os.pardir, "res", "img", "logo.png")))
        self.setWindowTitle("QUIZZO LEARN")
        self.resize(900, 650)
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

        mytests_button.setStyleSheet("background-color: DarkOrange; color:Azure")
        newtest_button.setStyleSheet("background-color: DarkOrange; color:Azure")
        bigtest_button.setStyleSheet("background-color: DarkOrange; color:Azure")

        font = QFont("Serif", 20)
        mytests_button.setFont(font)
        newtest_button.setFont(font)
        bigtest_button.setFont(font)

        newtest_button.clicked.connect(self.newtest_act)
        mytests_button.clicked.connect(self.mytests_act)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(mytests_button, 2)
        vbox.addStretch(1)
        vbox.addWidget(newtest_button, 2)
        vbox.addStretch(1)
        vbox.addWidget(bigtest_button, 2)
        vbox.addStretch(1)

        hbox = QHBoxLayout()

        hbox.addStretch(1)
        hbox.addLayout(vbox, 3)
        hbox.addStretch(1)
        self.setLayout(hbox)

    def mytests_act(self):
        self.close()
        my_tests_window.init_ui()

    def newtest_act(self):
        test_name = text_dialog(self, "NAZWIJ SWÓJ TEST", "PODAJ NAZWĘ TESTU")
        if test_name is not None:
            self.close()
            new_test_window.init_ui(test_name)


class NewTestWindow(QWidget):
    """ adding new test"""

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(os.path.join(os.pardir, "res", "img", "logo.png")))
        self.setWindowTitle("QUIZZO LEARN")
        self.resize(900, 650)
        center(self)
        self.load_ui()

    def init_ui(self, test_name):
        self.test_name = test_name
        self.number_of_frases = 0
        self.QList.clear()
        self.show()

    def load_ui(self):
        back_button = QPushButton("<= WRÓĆ")
        back_button.setStyleSheet("background-color: YellowGreen; color:purple")
        back_button.clicked.connect(self.back_button_act)

        add_button = QPushButton()
        add_button.setIcon(QIcon(os.path.join(os.pardir, "res", "img", "add-icon.png")))
        add_button.setIconSize(QSize(100, 100))
        add_button.setSizePolicy(QSizePolicy.Expanding,
                                 QSizePolicy.Preferred)
        add_button.clicked.connect(self.add)

        OK_button = QPushButton("ZAPISZ I \nROZPOCZNIJ \n TEST")
        OK_button.setSizePolicy(QSizePolicy.Expanding,
                                QSizePolicy.Preferred)
        OK_button.setStyleSheet("background-color: LimeGreen; color:Azure")
        font = QFont("Serif", 15)
        OK_button.setFont(font)
        OK_button.clicked.connect(self.save)

        vbox = QVBoxLayout()
        vbox.addStretch(2)
        vbox.addWidget(add_button, 2)
        vbox.addStretch(2)
        vbox.addWidget(OK_button, 3)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(back_button)
        hbox2.addStretch(4)

        self.QList = QListWidget()
        vbox2 = QVBoxLayout()
        vbox2.addLayout(hbox2)
        vbox2.addWidget(self.QList)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox2, 7)
        hbox.addLayout(vbox, 1)

        self.setLayout(hbox)

    def back_button_act(self):
        alert = QMessageBox().warning(self, "JESTEŚ PEWIEN ??",
                                      "UWAGA !!! \n STRACISZ WPROWADZONE SŁOWA \n JESTEŚ PEWIEN ??", QMessageBox.Yes,
                                      QMessageBox.No)
        if alert == QMessageBox.Yes:
            self.close()
            menu_window.show()

    def add(self):
        frase1 = text_dialog(self, "FRAZA 1", "  PODAJ PROSZĘ FRAZĘ 1")
        frase2 = text_dialog(self, "FRAZA 2", "  PODAJ PROSZĘ FRAZĘ 2")

        item = QListWidgetItem()
        item.id = self.number_of_frases
        item.frase1 = frase1
        item.frase2 = frase2
        item.is_empty = False

        widget_item = QItemQuestion(self.number_of_frases, frase1, frase2)
        item.setSizeHint(widget_item.sizeHint())

        self.number_of_frases += 1

        self.QList.addItem(item)
        self.QList.setItemWidget(item, widget_item)

    def save(self):
        dir_of_questions = {}  # yeah it is something like LIST OF GOD
        reversed_dir_of_questions = {}

        i = 0
        i2 = self.QList.count()
        while i < i2:
            item = self.QList.item(i)
            if not item.is_empty:
                dir_of_questions[item.frase1] = item.frase2
                reversed_dir_of_questions[item.frase2] = item.frase1
            i += 1
        if len(dir_of_questions) < 1:
            QMessageBox.warning(self, "PUSTE", "NIE DA RADY STWORZYĆ PUSTEGO TESTU !!!", QMessageBox.Ok)
            return None

        quizzo_learn.files_interactions.save_test(dir_of_questions,
                                                  os.path.join(os.pardir, "res", "my_tests", self.test_name + ".test"))
        self.close()
        start_window.label.setText("    " + self.test_name)
        start_window.init_ui([dir_of_questions, reversed_dir_of_questions])
        my_tests_window.refresh()

    def deleting(self, id):
        i = 0
        i2 = self.QList.count()
        while i < i2:
            item = self.QList.item(i)
            if item.id == id:
                self.QList.removeItemWidget(item)
                item.is_empty = True
            i += 1


class MyTest(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(os.path.join(os.pardir, "res", "img", "logo.png")))
        self.setWindowTitle("QUIZZO LEARN")
        self.resize(900, 650)
        center(self)
        self.load_ui()

    def init_ui(self):
        self.show()

    def load_ui(self):
        box = QVBoxLayout()

        back_button = QPushButton("<= WRÓĆ")
        back_button.setStyleSheet("background-color: YellowGreen; color:purple")
        back_button.clicked.connect(self.back_button_act)

        font = QFont("Serif", 20)
        label = QLabel("MOJE TESTY:")
        label.setFont(font)
        label.setStyleSheet("color:azure; background-color:darkorange")

        self.QList = QListWidget()

        hbox2 = QHBoxLayout()
        hbox2.addWidget(back_button)
        hbox2.addStretch(4)

        box.addWidget(label, 1)
        box.addLayout(hbox2, 1)
        box.addWidget(self.QList, 8)

        self.setLayout(box)

        self.load_tests()

    def back_button_act(self):
        self.close()
        menu_window.show()

    def load_tests(self):
        tests = quizzo_learn.files_interactions.list_of_tests(os.path.join(os.pardir, "res", "my_tests"))
        for test in tests:
            item = QListWidgetItem()
            item.name = test
            test_widget = QItemTest(test)
            item.setSizeHint(test_widget.sizeHint())

            self.QList.addItem(item)
            self.QList.setItemWidget(item, test_widget)

    def refresh(self):
        self.QList.clear()
        self.load_tests()

    def deleting(self, name):
        i = 0
        i2 = self.QList.count()
        while i < i2:
            item = self.QList.item(i)
            if item.name == name:
                self.QList.removeItemWidget(item)
                quizzo_learn.files_interactions.delete_file(
                    os.path.join(os.pardir, "res", "my_tests", name + ".test"))
            i += 1

    def start_test(self, name):
        dirs_of_questions = quizzo_learn.files_interactions.read_test(
            os.path.join(os.pardir, "res", "my_tests", name + ".test"))
        self.close()
        start_window.label.setText("    " + name)
        start_window.init_ui(dirs_of_questions)


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(os.path.join(os.pardir, "res", "img", "logo.png")))
        self.setWindowTitle("QUIZZO LEARN")
        self.resize(900, 650)
        center(self)
        self.load_ui()

    def init_ui(self, dirs_of_questions):
        self.dirs_of_questions = dirs_of_questions
        self.show()

    def load_ui(self):
        box = QVBoxLayout()

        self.label = QLabel()
        self.label.setFont(QFont("Serif", 25))
        self.label.setStyleSheet("background-color: darkorange; color:azure; text-align: center")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        back_button = QPushButton("<= WRÓĆ")
        back_button.setStyleSheet("background-color: YellowGreen; color:purple")
        back_button.clicked.connect(self.back_button_act)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(back_button)
        hbox2.addStretch(4)

        endless_button = QPushButton("ĆWICZ W NIESKOŃCZONOŚĆ")
        quizz_button = QPushButton("SPRAWDŹ SIĘ")

        endless_button.setSizePolicy(QSizePolicy.Expanding,
                                     QSizePolicy.Preferred)
        quizz_button.setSizePolicy(QSizePolicy.Expanding,
                                   QSizePolicy.Preferred)

        endless_button.setStyleSheet("background-color: darkorange; color:Azure")
        quizz_button.setStyleSheet("background-color: darkorange; color:Azure")

        font = QFont("Serif", 20)
        endless_button.setFont(font)
        quizz_button.setFont(font)

        endless_button.clicked.connect(self.endless_button_act)
        quizz_button.clicked.connect(self.quizz_button_act)

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()

        vbox.addWidget(endless_button, 3)
        vbox.addStretch(1)
        vbox.addWidget(quizz_button, 3)

        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        box.addWidget(self.label, 2)
        box.addLayout(hbox2)
        box.addStretch(1)
        box.addLayout(hbox, 5)
        box.addStretch(2)

        self.setLayout(box)

    def endless_button_act(self):
        pass

    def quizz_button_act(self):
        quizz_control = QuizControl(self.dirs_of_questions, False)

    def back_button_act(self):
        self.close()
        menu_window.show()


class QuizWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(os.path.join(os.pardir, "res", "img", "logo.png")))
        self.setWindowTitle("QUIZZO LEARN")
        self.resize(900, 650)
        center(self)
        self.practise = True
        self.load_ui()

    def init_ui(self):
        self.show()

    def load_ui(self):
        back_button = QPushButton("<= ZAKOŃCZ")
        back_button.setFont(QFont("serif", 30))
        back_button.setStyleSheet("background-color: YellowGreen; color:purple")
        back_button.setSizePolicy(QSizePolicy.Expanding,
                                  QSizePolicy.Preferred)
        back_button.clicked.connect(self.back_button_act)

        next_button = QPushButton("DALEJ =>")
        next_button.setFont(QFont("serif", 30))
        next_button.setSizePolicy(QSizePolicy.Expanding,
                                  QSizePolicy.Preferred)
        next_button.setStyleSheet("background-color: LimeGreen; color:Azure")
        next_button.clicked.connect(self.next_button_act)

        button_box = QHBoxLayout()
        button_box.addWidget(back_button, 5)
        button_box.addStretch(3)
        button_box.addWidget(next_button, 5)

        self.question = QLabel()
        self.question.setStyleSheet(
            "background-color: darkorange; color:azure;")
        self.question.setAlignment(Qt.AlignCenter)
        self.question.setWordWrap(True)

        self.answer = QTextEdit()
        self.answer.setFont(QFont("Serif", 30))

        box = QVBoxLayout()

        box.addWidget(self.question, 5)
        box.addWidget(self.answer, 3)
        box.addLayout(button_box, 1)

        self.setLayout(box)

    def set_question(self, new_q):
        if len(new_q) <= 15:
            self.question.setFont(QFont("serif", 55))
        elif len(new_q) <= 30:
            self.question.setFont(QFont("serif", 35))
        else:
            self.question.setFont(QFont("serif", 20))

        self.question.setText(new_q)

    def back_button_act(self):
        pass

    def next_button_act(self):
        pass


class QuizControl(object):
    def __init__(self, dirs_of_questions, practice=True):
        self.dir_of_questions, self.reversed_dir_of_questions = dirs_of_questions
        self.practice = practice

        if self.practice:
            self.start_endless_quiz()
        elif not self.practice:
            self.max_points = len(self.dir_of_questions)
            self.current_points = 0
            self.start_test()

    def set_questions_queue(self):
        keys_list = self.dir_of_questions.keys()
        reversed_keys_list = self.reversed_dir_of_questions.keys()
        mixed_keys_list = sample(keys_list, len(keys_list))
        mixed_reversed_keys_list = sample(reversed_keys_list, len(reversed_keys_list))

        queue = []
        while len(mixed_keys_list) > 0:
            queue.append(mixed_keys_list[0])

            if not self.dir_of_questions[mixed_keys_list[0]] == mixed_reversed_keys_list[0]:
                queue.append(mixed_reversed_keys_list.pop(0))
            elif len(mixed_keys_list) == 1:
                queue.append(mixed_reversed_keys_list.pop(0))
            else:
                queue.append(mixed_reversed_keys_list.pop())
                mixed_reversed_keys_list[len(mixed_reversed_keys_list) - 1] = mixed_reversed_keys_list[0]

            trash = mixed_keys_list.pop(0)
        return queue

    def start_test(self):
        queue = self.set_questions_queue()
        print(queue)

    def start_endless_quiz(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu_window = MenuWindow()
    new_test_window = NewTestWindow()
    my_tests_window = MyTest()
    start_window = StartWindow()
    quiz_window = QuizWindow()
    sys.exit(app.exec_())
