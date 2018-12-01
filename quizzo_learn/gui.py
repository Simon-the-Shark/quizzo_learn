import sys
import os.path

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QIcon, QFocusEvent
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, \
    QSizePolicy, QListWidget, QListWidgetItem, QInputDialog, QLineEdit, QMessageBox, QTextEdit

import quizzo_learn.files_interactions
from quizzo_learn.QuizControl import QuizControl, give_globals


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


def set_background_colors():
    p = menu_window.palette()
    p.setColor(menu_window.backgroundRole(), Qt.lightGray)
    menu_window.setPalette(p)

    p = new_test_window.palette()
    p.setColor(new_test_window.backgroundRole(), Qt.lightGray)
    new_test_window.setPalette(p)

    p = my_tests_window.palette()
    p.setColor(my_tests_window.backgroundRole(), Qt.lightGray)
    my_tests_window.setPalette(p)

    p = start_window.palette()
    p.setColor(start_window.backgroundRole(), Qt.lightGray)
    start_window.setPalette(p)

    p = quiz_window.palette()
    p.setColor(quiz_window.backgroundRole(), Qt.lightGray)
    quiz_window.setPalette(p)

    p = correct_window.palette()
    p.setColor(correct_window.backgroundRole(), Qt.lightGray)
    correct_window.setPalette(p)

    p = incorrect_window.palette()
    p.setColor(incorrect_window.backgroundRole(), Qt.lightGray)
    incorrect_window.setPalette(p)

    p = rating_window.palette()
    p.setColor(rating_window.backgroundRole(), Qt.lightGray)
    rating_window.setPalette(p)

    p = build_big_test_window.palette()
    p.setColor(build_big_test_window.backgroundRole(), Qt.lightGray)
    build_big_test_window.setPalette(p)


class CorrectWindow(QWidget):
    def __init__(self, practice=False):
        super().__init__()
        self.practice = practice
        self.setWindowIcon(QIcon(os.path.join(os.pardir, "res", "img", "logo.png")))
        self.setWindowTitle("QUIZZO LEARN")
        self.resize(900, 650)
        center(self)

        self.label = QLabel("DOBRZE !!!\nZDOBYWASZ PUNKT !!!")
        self.label.setFont(QFont("serif", 50))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: green ; color:AntiqueWhite;")

        next_button = QPushButton("NASTĘPNE")
        next_button.setDefault(True)
        next_button.setFont(QFont("serif", 30))
        next_button.setSizePolicy(QSizePolicy.Expanding,
                                  QSizePolicy.Preferred)
        next_button.setStyleSheet("background-color: LimeGreen; color:AntiqueWhite")
        next_button.clicked.connect(self.next_button_act)

        box = QVBoxLayout()
        box.addWidget(self.label, 9)
        box.addWidget(next_button, 1)

        self.setLayout(box)

    def init_ui(self):
        self.show()

    def next_button_act(self):
        self.close()
        if self.practice:
            start_window.quizz_control.next_endless_question()
        else:
            start_window.quizz_control.next_question()

    def set_label_if_practice(self):
        if not self.practice:
            self.label.setText("DOBRZE !!!\nZDOBYWASZ PUNKT !!!")
        else:
            self.label.setText("DOBRZE !!!")


class InCorrectWindow(QWidget):
    def __init__(self, practice=False):
        super().__init__()
        self.practice = practice
        self.setWindowIcon(QIcon(os.path.join(os.pardir, "res", "img", "logo.png")))
        self.setWindowTitle("QUIZZO LEARN")
        self.resize(900, 650)
        center(self)

        self.label = QLabel("ŹLE :(\nPOPEŁNIŁEŚ BŁĄD :(")
        self.label.setFont(QFont("serif", 50))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: orangered; color:AntiqueWhite;")

        next_button = QPushButton("NASTĘPNE")
        next_button.setFont(QFont("serif", 30))
        next_button.setDefault(True)
        next_button.setSizePolicy(QSizePolicy.Expanding,
                                  QSizePolicy.Preferred)
        next_button.setStyleSheet("background-color: LimeGreen; color:AntiqueWhite")
        next_button.clicked.connect(self.next_button_act)

        box = QVBoxLayout()
        box.addWidget(self.label, 9)
        box.addWidget(next_button, 1)
        self.setLayout(box)

    def init_ui(self):
        self.show()

    def next_button_act(self):
        self.close()
        if self.practice:
            start_window.quizz_control.next_endless_question()
        else:
            start_window.quizz_control.next_question()

    def set_label_if_practice(self, good_answer=""):
        if self.practice:
            self.label.setText("ŹLE :(\nPOPEŁNIŁEŚ BŁĄD :(\nPOPRAWNA ODPOWIEDZ TO\n{}".format(good_answer))
        else:
            self.label.setText("ŹLE :(\nPOPEŁNIŁEŚ BŁĄD :(")


class RatingWindow(QWidget):
    def __init__(self, points=0, max_points=1):
        super().__init__()
        self.setWindowIcon(QIcon(os.path.join(os.pardir, "res", "img", "logo.png")))
        self.setWindowTitle("QUIZZO LEARN")
        self.resize(900, 650)
        center(self)

        self.points = points
        self.max_points = max_points

        self.load_ui()

    def init_ui(self, points, max_points):
        self.points = points
        self.max_points = max_points

        proc = self.points / self.max_points * 100
        self.label_punkty.setText("ZDOBYŁEŚ\n {} / {} \nPUNKTÓW".format(self.points, self.max_points))
        self.label_procenty.setText("TO {}%".format(str(proc)[:5]))

        self.show()

    def load_ui(self):
        box = QVBoxLayout()

        self.label_procenty = QLabel()
        self.label_punkty = QLabel()

        self.label_punkty.setStyleSheet(
            "background-color: darkorange; color:AntiqueWhite;")
        self.label_punkty.setAlignment(Qt.AlignCenter)
        self.label_punkty.setWordWrap(True)
        self.label_punkty.setFont(QFont("serif", 40))

        self.label_procenty.setStyleSheet(
            "background-color: darkorange; color:AntiqueWhite;")
        self.label_procenty.setAlignment(Qt.AlignCenter)
        self.label_procenty.setWordWrap(True)
        self.label_procenty.setFont(QFont("serif", 40))

        end_button = QPushButton("ZAKOŃCZ TEST")
        end_button.setFont(QFont("serif", 30))
        end_button.setSizePolicy(QSizePolicy.Expanding,
                                 QSizePolicy.Preferred)
        end_button.setStyleSheet("background-color: forestgreen; color:AntiqueWhite")
        end_button.clicked.connect(self.end_button_act)

        box.addWidget(self.label_punkty, 4)
        box.addWidget(self.label_procenty, 4)
        box.addWidget(end_button, 1)

        self.setLayout(box)

    def end_button_act(self):
        del start_window.quizz_control
        self.close()
        menu_window.init_ui()


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
        button.setStyleSheet("background-color:LimeGreen; color:AntiqueWhite")
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

        mytests_button.setStyleSheet("background-color: DarkOrange; color:AntiqueWhite")
        newtest_button.setStyleSheet("background-color: DarkOrange; color:AntiqueWhite")
        bigtest_button.setStyleSheet("background-color: DarkOrange; color:AntiqueWhite")

        font = QFont("Serif", 20)
        mytests_button.setFont(font)
        newtest_button.setFont(font)
        bigtest_button.setFont(font)

        newtest_button.clicked.connect(self.newtest_act)
        mytests_button.clicked.connect(self.mytests_act)
        bigtest_button.clicked.connect(self.bigtest_act)

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

    def bigtest_act(self):
        self.close()
        build_big_test_window.init_ui()


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
        OK_button.setStyleSheet("background-color: LimeGreen; color:AntiqueWhite")
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
        self.QList.setStyleSheet("background-color:PeachPuff ")

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
        if frase1 is None:
            QMessageBox.warning(self, "PUSTE", "Prosze podać jakąś fraze", QMessageBox.Ok)
            return None
        frase2 = text_dialog(self, "FRAZA 2", "  PODAJ PROSZĘ FRAZĘ 2")
        if frase2 is None:
            QMessageBox.warning(self, "PUSTE", "Prosze podać jakąś fraze", QMessageBox.Ok)
            return None

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
        start_window.label.setText(self.test_name)
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
        label.setStyleSheet("color:AntiqueWhite; background-color:darkorange")

        self.QList = QListWidget()
        self.QList.setStyleSheet("background-color:PeachPuff ")

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
        start_window.label.setText(name)
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
        self.label.setStyleSheet("background-color: darkorange; color:AntiqueWhite; text-align: center")
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

        endless_button.setStyleSheet("background-color: darkorange; color:AntiqueWhite")
        quizz_button.setStyleSheet("background-color: darkorange; color:AntiqueWhite")

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
        self.close()

        correct_window.practice = True
        correct_window.set_label_if_practice()
        incorrect_window.practice = True
        incorrect_window.set_label_if_practice()

        self.quizz_control = QuizControl(self.dirs_of_questions, True)

    def quizz_button_act(self):
        self.close()

        correct_window.practice = False
        correct_window.set_label_if_practice()
        incorrect_window.practice = False
        incorrect_window.set_label_if_practice()

        self.quizz_control = QuizControl(self.dirs_of_questions, False)

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
        self.practice = True
        self.load_ui()

    def init_ui(self):
        self.answer.setFocus()
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
        next_button.setStyleSheet("background-color: LimeGreen; color:AntiqueWhite")
        next_button.clicked.connect(self.next_button_act)

        button_box = QHBoxLayout()
        button_box.addWidget(back_button, 5)
        button_box.addStretch(3)
        button_box.addWidget(next_button, 5)

        self.question = QLabel()
        self.question.setStyleSheet(
            "background-color: darkorange; color:AntiqueWhite;")
        self.question.setAlignment(Qt.AlignCenter)
        self.question.setWordWrap(True)

        self.answer = QLineEdit()
        self.answer.setFont(QFont("Serif", 30))
        self.answer.returnPressed.connect(self.next_button_act)
        self.answer.setStyleSheet("background-color:PapayaWhip")
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
        if self.practice:
            are_you_sure = QMessageBox.question(self, "Zakończyć ?", "Jesteś pewien, że chcesz zakończyć trening?",
                                                QMessageBox.Yes, QMessageBox.No)
        else:
            are_you_sure = QMessageBox.warning(self, "Zakończyć?", "Jesteś pewien, że chcesz przerwać w trakcie??",
                                               QMessageBox.Yes, QMessageBox.No)

        if are_you_sure == QMessageBox.Yes:
            dirs_of_questions = [start_window.quizz_control.dir_of_questions,
                                 start_window.quizz_control.reversed_dir_of_questions]
            del start_window.quizz_control
            self.close()
            start_window.init_ui(dirs_of_questions)
        else:
            return None

    def next_button_act(self):
        question_text = self.question.text()
        user_answer = str(self.answer.text())

        self.answer.clear()

        correct, good_answer = start_window.quizz_control.check(question_text, user_answer)
        if correct:
            if not self.practice:
                start_window.quizz_control.current_points += 1
            self.close()
            correct_window.init_ui()
        else:
            if self.practice:
                incorrect_window.set_label_if_practice(good_answer)
            self.close()
            incorrect_window.init_ui()

class BuildBigTest(QWidget):
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
        label = QLabel("Wybierz testy, aby zbudować duży sprawdzian")
        label.setFont(QFont("serif", 30))
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)
        label.setStyleSheet("background-color:darkorange;color:AntiqueWhite")

        back_button = QPushButton("<= WRÓĆ")
        back_button.setStyleSheet("background-color: YellowGreen; color:purple")
        back_button.clicked.connect(self.back_button_act)
        back_box = QHBoxLayout()
        back_box.addWidget(back_button)
        back_box.addStretch(4)

        self.QList = QListWidget()
        self.QList.setStyleSheet("background-color:PeachPuff")

        next_button = QPushButton("ROZPOCZNIJ SPRAWDZIAN =>")
        next_button.setFont(QFont("serif", 30))
        next_button.setSizePolicy(QSizePolicy.Expanding,
                                  QSizePolicy.Preferred)
        next_button.setStyleSheet("background-color: LimeGreen; color:AntiqueWhite")
        next_button.clicked.connect(self.next_button_act)

        box = QVBoxLayout()
        box.addWidget(label, 3)
        box.addLayout(back_box, 1)
        box.addWidget(self.QList, 20)
        box.addWidget(next_button, 3)

        self.setLayout(box)

    def next_button_act(self):
        pass

    def back_button_act(self):
        self.close()
        menu_window.init_ui()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    menu_window = MenuWindow()
    new_test_window = NewTestWindow()
    my_tests_window = MyTest()
    start_window = StartWindow()
    quiz_window = QuizWindow()
    correct_window = CorrectWindow()
    incorrect_window = InCorrectWindow()
    rating_window = RatingWindow()
    build_big_test_window = BuildBigTest()
    give_globals(quiz_window, rating_window)

    set_background_colors()

    sys.exit(app.exec_())
