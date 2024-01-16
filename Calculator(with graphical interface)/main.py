import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from Calculator import Ui_MainWindow
from PySide6.QtGui import QFontDatabase
from sympy import solve, parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
import operator

default_font_size = 17
default_entry_font_size = 45


class Calculator(QMainWindow):
    def __init__(self):
        super(Calculator, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        QFontDatabase.addApplicationFont("fonts/Helvetica-Regular.ttf") # font

        self.ui.btn_0.clicked.connect(lambda: self.add_or_replace('0'))
        self.ui.btn_1.clicked.connect(lambda: self.add_or_replace('1'))
        self.ui.btn_2.clicked.connect(lambda: self.add_or_replace('2'))
        self.ui.btn_3.clicked.connect(lambda: self.add_or_replace('3'))
        self.ui.btn_4.clicked.connect(lambda: self.add_or_replace('4'))
        self.ui.btn_5.clicked.connect(lambda: self.add_or_replace('5'))
        self.ui.btn_6.clicked.connect(lambda: self.add_or_replace('6'))
        self.ui.btn_7.clicked.connect(lambda: self.add_or_replace('7'))
        self.ui.btn_8.clicked.connect(lambda: self.add_or_replace('8'))
        self.ui.btn_9.clicked.connect(lambda: self.add_or_replace('9'))
        self.ui.btn_clear.clicked.connect(lambda: self.clear_all())  # CA
        self.ui.btn_cdot.clicked.connect(lambda: self.add_symbol('.'))  # .
        self.ui.btn_plus.clicked.connect(lambda: self.add_or_replace('+'))  # +
        self.ui.btn_minus.clicked.connect(lambda: self.add_or_replace('-'))  # -
        self.ui.btn_mult.clicked.connect(lambda: self.add_symbol('*'))  # *
        self.ui.btn_div.clicked.connect(lambda: self.add_symbol('/'))  # /
        self.ui.btn_degree.clicked.connect(lambda: self.add_symbol('^'))  # degree
        self.ui.btn_eq.clicked.connect(lambda: self.add_symbol('='))  # =
        self.ui.btn_sqrt.clicked.connect(lambda: self.add_symbol('^0.5'))  # square root
        self.ui.btn_x.clicked.connect(lambda: self.add_or_replace('x'))  # x
        self.ui.btn_left.clicked.connect(lambda: self.add_or_replace('('))  # (
        self.ui.btn_right.clicked.connect(lambda: self.add_symbol(')'))  # )
        self.ui.btn_qe.clicked.connect(lambda: self.add_symbol('>'))  # >
        self.ui.btn_le.clicked.connect(lambda: self.add_symbol('<'))  # <
        self.ui.btn_pi.clicked.connect(lambda: self.add_or_replace('pi')) # pi
        self.ui.btn_abs.clicked.connect(lambda: self.add_or_replace('abs(')) # module
        self.ui.btn_delete.clicked.connect(lambda: self.backspace())  # backspace

        self.ui.btn_solve.clicked.connect(lambda: self.main()) # solution

    def add_or_replace(self, btn_text: str) -> None:
        replaceable = ['0', 'ZeroDivisionError', 'SyntaxError', 'ValueError', 'TokenError', 'NameError',
                       'TypeError', 'class', 'NotImplementedError', 'Error']
        # False and True should be put in as well, but what could be better than True/3=0.33333333333
        if self.ui.lineEdit.text() in replaceable:
            self.ui.lineEdit.setText(str(btn_text))
            # If lineEdit = 0, Error, ZeroDivisionError, etc. Then lineEdit = text of the pressed button
        else:
            current_text = self.ui.lineEdit.text()
            self.ui.lineEdit.setText(current_text + str(btn_text))
            # Simply add the text of the pressed button to lineEdit
        self.adjust_entry_font_size()
        # this function is responsible for adjusting the text size. It will be present in every LineEdit change.
        self.disable_btn(False)

    def clear_all(self) -> None: # clearing lineEdit and label
        self.ui.lineEdit.setText('0') # lineEdit becomes 0
        self.ui.label.clear() # label is completely cleared
        self.adjust_entry_font_size()
        self.adjust_temp_font_size()
        self.disable_btn(False)

    def add_symbol(self, btn_text) -> None: # simply adds a character to lineEdit
        current_text = self.ui.lineEdit.text()
        self.ui.lineEdit.setText(current_text + str(btn_text))
        self.adjust_entry_font_size()

    def backspace(self) -> None:
        expression = self.ui.lineEdit.text()
        if len(expression) != 1:
            self.ui.lineEdit.setText(expression[:-1])
        else:
            self.ui.lineEdit.setText('0')
        # If the length of lineEdit is not 1, remove one character. Else we set it to 0
        self.adjust_entry_font_size()
        self.disable_btn(False)

    def get_entry_text_wight(self) -> int:
        return self.ui.lineEdit.fontMetrics().boundingRect(self.ui.lineEdit.text()).width()

    def get_temp_text_wight(self) -> int:
        return self.ui.label.fontMetrics().boundingRect(self.ui.label.text()).width()

    def adjust_entry_font_size(self) -> None:
        font_size = default_entry_font_size
        while self.get_entry_text_wight() > self.ui.lineEdit.width() - 15:
            font_size -= 1
            self.ui.lineEdit.setStyleSheet('font-size: ' + str(font_size) + 'pt; border: none;')

        font_size = 1
        while self.get_entry_text_wight() < self.ui.lineEdit.width() - 60:
            font_size += 1
            if font_size > default_entry_font_size:
                break
            self.ui.lineEdit.setStyleSheet('font-size: ' + str(font_size) + 'pt; border: none;')

    def resizeEvent(self, event) -> None:
        # If the window resolution changes
        self.adjust_entry_font_size()
        self.adjust_temp_font_size()

    def adjust_temp_font_size(self) -> None:
        font_size = default_font_size
        while self.get_temp_text_wight() > self.ui.label.width() - 10:
            font_size -= 1
            self.ui.label.setStyleSheet('font-size: ' + str(font_size) + 'pt; color: #888;')

        font_size = 1
        while self.get_temp_text_wight() < self.ui.label.width() - 60:
            font_size += 1
            if font_size > default_font_size:
                break
            self.ui.label.setStyleSheet('font-size: ' + str(font_size) + 'pt; color: #888;')

    def disable_btn(self, disable: bool) -> None:
        self.ui.btn_sqrt.setDisabled(disable)
        self.ui.btn_degree.setDisabled(disable)
        self.ui.btn_eq.setDisabled(disable)
        self.ui.btn_le.setDisabled(disable)
        self.ui.btn_qe.setDisabled(disable)
        self.ui.btn_div.setDisabled(disable)
        self.ui.btn_mult.setDisabled(disable)
        self.ui.btn_cdot.setDisabled(disable)
        self.ui.btn_right.setDisabled(disable)

        color = 'color: #888;' if disable else 'color: white;'
        self.change_btn_cl(color)

    def change_btn_cl(self, css_color: str) -> None:
        self.ui.btn_sqrt.setStyleSheet(css_color)
        self.ui.btn_degree.setStyleSheet(css_color)
        self.ui.btn_eq.setStyleSheet(css_color)
        self.ui.btn_le.setStyleSheet(css_color)
        self.ui.btn_qe.setStyleSheet(css_color)
        self.ui.btn_div.setStyleSheet(css_color)
        self.ui.btn_mult.setStyleSheet(css_color)
        self.ui.btn_cdot.setStyleSheet(css_color)
        self.ui.btn_right.setStyleSheet(css_color)




    def main(self) -> None: # start calculating
        try:
            self.ui.label.setText(self.ui.lineEdit.text()) # move text from lineEdit to label
            self.adjust_temp_font_size()
            expression = (self.ui.lineEdit.text().replace('^', '**').replace("pi", "3.14159265358979323846"))
            for i in range(10):
                expression = expression.replace(f'{i}(', f'{i}*(').replace(')(', ')*(').replace('///', '%')
            # if the equation
            if expression.find('x') > -1 and expression.find('Error') == -1:
                transformations = (standard_transformations + (implicit_multiplication_application,))
                if ">" not in expression and "<" not in expression:
                    op = "x = "
                else:
                    op = "x ∈ "
                f = parse_expr(expression.replace("=", "-"), transformations=transformations)
                answer = str(solve(f)).replace('&', '∪').replace('oo', '∞').replace('((', '(').replace('))', ')')
                if answer[0] == '[' and answer[len(answer) - 1] == ']' and answer != '[]':
                    self.ui.lineEdit.setText(op + answer[1:len(answer) - 1])
                elif answer == '[]':
                    self.ui.lineEdit.setText('x ∈ R')
                else:
                    self.ui.lineEdit.setText('x ∈ ' + answer.replace(' < x) ∪ (x < ', '; ').replace('|', '∪'))
            # if x is of degree zero
            elif expression.find('x') == -1 and expression.find('Error') == -1:
                expression = expression.replace('=', '==')
                ops = {
                    ">=": operator.ge,
                    "<=": operator.le,
                    ">": operator.gt,
                    "<": operator.lt,
                    "==": operator.eq
                }
                for op in ops:
                    if op in expression:
                        before, after = expression.split(op)
                        self.ui.lineEdit.setText(str(ops[op](eval(before), eval(after))))
                    elif op not in expression:
                        self.ui.lineEdit.setText(str(eval(expression)))
            else:
                self.ui.lineEdit.setText('Error')
        # error output
        except Exception as e:
            error_name = type(e).__name__
            self.ui.lineEdit.setText(error_name)
            self.disable_btn(True)
        self.adjust_entry_font_size()
        # I originally had self.adjust_entry_font_size() after every LineEdit change in this function.
        # But since LineEdit is only changed once in this function, you can move self.adjust_entry_font_size()
        # to the very end of the function




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec())
