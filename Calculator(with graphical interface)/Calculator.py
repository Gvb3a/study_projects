################################################################################
## Form generated from reading UI file 'Calculator.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QShortcut)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)
import icon_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(380, 550)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(320, 500))
        MainWindow.setSizeIncrement(QSize(380, 540))
        MainWindow.setBaseSize(QSize(380, 540))
        MainWindow.setContextMenuPolicy(Qt.DefaultContextMenu)
        icon = QIcon()
        icon.addFile(u":/icon/calculator.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"QWidget {\n"
"	color: white;\n"
"	background-color: #121212;\n"
"	font-family: Helvetica;\n"
"	font-size: 17pt;\n"
"	font-weight: 600;\n"
"}\n"
"\n"
"QPushButton {\n"
"	background-color: transparent;\n"
"	border: none;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: #666;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: #888;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setLayoutDirection(Qt.RightToLeft)
        self.label.setStyleSheet(u"color: #888;")
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy2)
        self.lineEdit.setStyleSheet(u"font-size: 45pt;\n"
"border: none;")
        self.lineEdit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lineEdit.setReadOnly(True)

        self.verticalLayout.addWidget(self.lineEdit)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.btn_4 = QPushButton(self.centralwidget)
        self.btn_4.setObjectName(u"btn_4")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.btn_4.sizePolicy().hasHeightForWidth())
        self.btn_4.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.btn_4, 3, 1, 1, 1)

        self.btn_sqrt = QPushButton(self.centralwidget)
        self.btn_sqrt.setObjectName(u"btn_sqrt")
        sizePolicy3.setHeightForWidth(self.btn_sqrt.sizePolicy().hasHeightForWidth())
        self.btn_sqrt.setSizePolicy(sizePolicy3)
        self.btn_sqrt.setCursor(QCursor(Qt.ArrowCursor))

        self.gridLayout.addWidget(self.btn_sqrt, 1, 2, 1, 1)

        self.btn_9 = QPushButton(self.centralwidget)
        self.btn_9.setObjectName(u"btn_9")
        sizePolicy3.setHeightForWidth(self.btn_9.sizePolicy().hasHeightForWidth())
        self.btn_9.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.btn_9, 2, 3, 1, 1)

        self.btn_delete = QPushButton(self.centralwidget)
        self.btn_delete.setObjectName(u"btn_delete")
        sizePolicy3.setHeightForWidth(self.btn_delete.sizePolicy().hasHeightForWidth())
        self.btn_delete.setSizePolicy(sizePolicy3)
        self.btn_delete.setCursor(QCursor(Qt.ArrowCursor))
        icon1 = QIcon()
        icon1.addFile(u":/icon/backspace.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_delete.setIcon(icon1)
        self.btn_delete.setIconSize(QSize(24, 24))

        self.gridLayout.addWidget(self.btn_delete, 0, 4, 1, 1)

        self.btn_right = QPushButton(self.centralwidget)
        self.btn_right.setObjectName(u"btn_right")
        sizePolicy3.setHeightForWidth(self.btn_right.sizePolicy().hasHeightForWidth())
        self.btn_right.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.btn_right, 5, 1, 1, 1)

        self.btn_mult = QPushButton(self.centralwidget)
        self.btn_mult.setObjectName(u"btn_mult")
        sizePolicy3.setHeightForWidth(self.btn_mult.sizePolicy().hasHeightForWidth())
        self.btn_mult.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.btn_mult, 3, 4, 1, 1)

        self.btn_div = QPushButton(self.centralwidget)
        self.btn_div.setObjectName(u"btn_div")
        sizePolicy3.setHeightForWidth(self.btn_div.sizePolicy().hasHeightForWidth())
        self.btn_div.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.btn_div, 2, 4, 1, 1)

        self.btn_clear = QPushButton(self.centralwidget)
        self.btn_clear.setObjectName(u"btn_clear")
        sizePolicy3.setHeightForWidth(self.btn_clear.sizePolicy().hasHeightForWidth())
        self.btn_clear.setSizePolicy(sizePolicy3)
        self.btn_clear.setCursor(QCursor(Qt.ArrowCursor))

        self.gridLayout.addWidget(self.btn_clear, 0, 0, 1, 1)

        self.btn_1 = QPushButton(self.centralwidget)
        self.btn_1.setObjectName(u"btn_1")
        sizePolicy3.setHeightForWidth(self.btn_1.sizePolicy().hasHeightForWidth())
        self.btn_1.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.btn_1, 4, 1, 1, 1)

        self.btn_8 = QPushButton(self.centralwidget)
        self.btn_8.setObjectName(u"btn_8")
        sizePolicy3.setHeightForWidth(self.btn_8.sizePolicy().hasHeightForWidth())
        self.btn_8.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.btn_8, 2, 2, 1, 1)

        self.btn_left = QPushButton(self.centralwidget)
        self.btn_left.setObjectName(u"btn_left")
        sizePolicy3.setHeightForWidth(self.btn_left.sizePolicy().hasHeightForWidth())
        self.btn_left.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.btn_left, 5, 0, 1, 1)

        self.btn_abs = QPushButton(self.centralwidget)
        self.btn_abs.setObjectName(u"btn_abs")
        sizePolicy3.setHeightForWidth(self.btn_abs.sizePolicy().hasHeightForWidth())
        self.btn_abs.setSizePolicy(sizePolicy3)
        self.btn_abs.setCursor(QCursor(Qt.ArrowCursor))

        self.gridLayout.addWidget(self.btn_abs, 1, 1, 1, 1)

        self.btn_6 = QPushButton(self.centralwidget)
        self.btn_6.setObjectName(u"btn_6")
        sizePolicy3.setHeightForWidth(self.btn_6.sizePolicy().hasHeightForWidth())
        self.btn_6.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.btn_6, 3, 3, 1, 1)

        self.btn_eq = QPushButton(self.centralwidget)
        self.btn_eq.setObjectName(u"btn_eq")
        sizePolicy3.setHeightForWidth(self.btn_eq.sizePolicy().hasHeightForWidth())
        self.btn_eq.setSizePolicy(sizePolicy3)
        self.btn_eq.setCursor(QCursor(Qt.ArrowCursor))
        self.btn_eq.setAutoExclusive(False)

        self.gridLayout.addWidget(self.btn_eq, 1, 4, 1, 1)

        self.btn_cdot = QPushButton(self.centralwidget)
        self.btn_cdot.setObjectName(u"btn_cdot")
        sizePolicy3.setHeightForWidth(self.btn_cdot.sizePolicy().hasHeightForWidth())
        self.btn_cdot.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.btn_cdot, 5, 3, 1, 1)

        self.btn_3 = QPushButton(self.centralwidget)
        self.btn_3.setObjectName(u"btn_3")
        sizePolicy3.setHeightForWidth(self.btn_3.sizePolicy().hasHeightForWidth())
        self.btn_3.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.btn_3, 4, 3, 1, 1)

        self.btn_plus = QPushButton(self.centralwidget)
        self.btn_plus.setObjectName(u"btn_plus")
        sizePolicy3.setHeightForWidth(self.btn_plus.sizePolicy().hasHeightForWidth())
        self.btn_plus.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.btn_plus, 5, 4, 1, 1)

        self.btn_2 = QPushButton(self.centralwidget)
        self.btn_2.setObjectName(u"btn_2")
        sizePolicy3.setHeightForWidth(self.btn_2.sizePolicy().hasHeightForWidth())
        self.btn_2.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.btn_2, 4, 2, 1, 1)

        self.btn_0 = QPushButton(self.centralwidget)
        self.btn_0.setObjectName(u"btn_0")
        sizePolicy3.setHeightForWidth(self.btn_0.sizePolicy().hasHeightForWidth())
        self.btn_0.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.btn_0, 5, 2, 1, 1)

        self.btn_degree = QPushButton(self.centralwidget)
        self.btn_degree.setObjectName(u"btn_degree")
        sizePolicy3.setHeightForWidth(self.btn_degree.sizePolicy().hasHeightForWidth())
        self.btn_degree.setSizePolicy(sizePolicy3)
        self.btn_degree.setCursor(QCursor(Qt.ArrowCursor))

        self.gridLayout.addWidget(self.btn_degree, 1, 3, 1, 1)

        self.btn_7 = QPushButton(self.centralwidget)
        self.btn_7.setObjectName(u"btn_7")
        sizePolicy3.setHeightForWidth(self.btn_7.sizePolicy().hasHeightForWidth())
        self.btn_7.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.btn_7, 2, 1, 1, 1)

        self.btn_5 = QPushButton(self.centralwidget)
        self.btn_5.setObjectName(u"btn_5")
        sizePolicy3.setHeightForWidth(self.btn_5.sizePolicy().hasHeightForWidth())
        self.btn_5.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.btn_5, 3, 2, 1, 1)

        self.btn_solve = QPushButton(self.centralwidget)
        self.btn_solve.setObjectName(u"btn_solve")
        sizePolicy3.setHeightForWidth(self.btn_solve.sizePolicy().hasHeightForWidth())
        self.btn_solve.setSizePolicy(sizePolicy3)
        self.btn_solve.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_solve.setStyleSheet(u"font: 34pt")

        self.gridLayout.addWidget(self.btn_solve, 0, 1, 1, 3)

        self.btn_minus = QPushButton(self.centralwidget)
        self.btn_minus.setObjectName(u"btn_minus")
        sizePolicy3.setHeightForWidth(self.btn_minus.sizePolicy().hasHeightForWidth())
        self.btn_minus.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.btn_minus, 4, 4, 1, 1)

        self.btn_x = QPushButton(self.centralwidget)
        self.btn_x.setObjectName(u"btn_x")
        sizePolicy3.setHeightForWidth(self.btn_x.sizePolicy().hasHeightForWidth())
        self.btn_x.setSizePolicy(sizePolicy3)
        self.btn_x.setCursor(QCursor(Qt.ArrowCursor))

        self.gridLayout.addWidget(self.btn_x, 1, 0, 1, 1)

        self.btn_pi = QPushButton(self.centralwidget)
        self.btn_pi.setObjectName(u"btn_pi")
        sizePolicy3.setHeightForWidth(self.btn_pi.sizePolicy().hasHeightForWidth())
        self.btn_pi.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.btn_pi, 4, 0, 1, 1)

        self.btn_le = QPushButton(self.centralwidget)
        self.btn_le.setObjectName(u"btn_le")
        sizePolicy3.setHeightForWidth(self.btn_le.sizePolicy().hasHeightForWidth())
        self.btn_le.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.btn_le, 3, 0, 1, 1)

        self.btn_qe = QPushButton(self.centralwidget)
        self.btn_qe.setObjectName(u"btn_qe")
        sizePolicy3.setHeightForWidth(self.btn_qe.sizePolicy().hasHeightForWidth())
        self.btn_qe.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.btn_qe, 2, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u" Calculator", None))
        self.label.setText("")
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.btn_4.setText(QCoreApplication.translate("MainWindow", u"4", None))
#if QT_CONFIG(shortcut)
        self.btn_4.setShortcut(QCoreApplication.translate("MainWindow", u"4", None))
#endif // QT_CONFIG(shortcut)
        self.btn_sqrt.setText(QCoreApplication.translate("MainWindow", u"\u221a", None))
#if QT_CONFIG(shortcut)
        self.btn_sqrt.setShortcut(QCoreApplication.translate("MainWindow", u"S", None))
#endif // QT_CONFIG(shortcut)
        self.btn_9.setText(QCoreApplication.translate("MainWindow", u"9", None))
#if QT_CONFIG(shortcut)
        self.btn_9.setShortcut(QCoreApplication.translate("MainWindow", u"9", None))
#endif // QT_CONFIG(shortcut)
        self.btn_delete.setText("")
#if QT_CONFIG(shortcut)
        self.btn_delete.setShortcut(QCoreApplication.translate("MainWindow", u"Backspace", None))
#endif // QT_CONFIG(shortcut)
        self.btn_right.setText(QCoreApplication.translate("MainWindow", u")", None))
#if QT_CONFIG(shortcut)
        self.btn_right.setShortcut(QCoreApplication.translate("MainWindow", u")", None))
#endif // QT_CONFIG(shortcut)
        self.btn_mult.setText(QCoreApplication.translate("MainWindow", u"\u00d7", None))
#if QT_CONFIG(shortcut)
        self.btn_mult.setShortcut(QCoreApplication.translate("MainWindow", u"*", None))
#endif // QT_CONFIG(shortcut)
        self.btn_div.setText(QCoreApplication.translate("MainWindow", u"\u00f7", None))
#if QT_CONFIG(shortcut)
        self.btn_div.setShortcut(QCoreApplication.translate("MainWindow", u"/", None))
#endif // QT_CONFIG(shortcut)
        self.btn_clear.setText(QCoreApplication.translate("MainWindow", u"AC", None))
#if QT_CONFIG(shortcut)
        self.btn_clear.setShortcut(QCoreApplication.translate("MainWindow", u"C", None))
#endif // QT_CONFIG(shortcut)
        self.btn_1.setText(QCoreApplication.translate("MainWindow", u"1", None))
#if QT_CONFIG(shortcut)
        self.btn_1.setShortcut(QCoreApplication.translate("MainWindow", u"1", None))
#endif // QT_CONFIG(shortcut)
        self.btn_8.setText(QCoreApplication.translate("MainWindow", u"8", None))
#if QT_CONFIG(shortcut)
        self.btn_8.setShortcut(QCoreApplication.translate("MainWindow", u"8", None))
#endif // QT_CONFIG(shortcut)
        self.btn_left.setText(QCoreApplication.translate("MainWindow", u"(", None))
#if QT_CONFIG(shortcut)
        self.btn_left.setShortcut(QCoreApplication.translate("MainWindow", u"(", None))
#endif // QT_CONFIG(shortcut)
        self.btn_abs.setText(QCoreApplication.translate("MainWindow", u"|x|", None))
#if QT_CONFIG(shortcut)
        self.btn_abs.setShortcut(QCoreApplication.translate("MainWindow", u"|", None))
#endif // QT_CONFIG(shortcut)
        self.btn_6.setText(QCoreApplication.translate("MainWindow", u"6", None))
#if QT_CONFIG(shortcut)
        self.btn_6.setShortcut(QCoreApplication.translate("MainWindow", u"6", None))
#endif // QT_CONFIG(shortcut)
        self.btn_eq.setText(QCoreApplication.translate("MainWindow", u"=", None))
#if QT_CONFIG(shortcut)
        self.btn_eq.setShortcut(QCoreApplication.translate("MainWindow", u"=", None))
#endif // QT_CONFIG(shortcut)
        self.btn_cdot.setText(QCoreApplication.translate("MainWindow", u".", None))
#if QT_CONFIG(shortcut)
        self.btn_cdot.setShortcut(QCoreApplication.translate("MainWindow", u".", None))
#endif // QT_CONFIG(shortcut)
        self.btn_3.setText(QCoreApplication.translate("MainWindow", u"3", None))
#if QT_CONFIG(shortcut)
        self.btn_3.setShortcut(QCoreApplication.translate("MainWindow", u"3", None))
#endif // QT_CONFIG(shortcut)
        self.btn_plus.setText(QCoreApplication.translate("MainWindow", u"+", None))
#if QT_CONFIG(shortcut)
        self.btn_plus.setShortcut(QCoreApplication.translate("MainWindow", u"+", None))
#endif // QT_CONFIG(shortcut)
        self.btn_2.setText(QCoreApplication.translate("MainWindow", u"2", None))
#if QT_CONFIG(shortcut)
        self.btn_2.setShortcut(QCoreApplication.translate("MainWindow", u"2", None))
#endif // QT_CONFIG(shortcut)
        self.btn_0.setText(QCoreApplication.translate("MainWindow", u"0", None))
#if QT_CONFIG(shortcut)
        self.btn_0.setShortcut(QCoreApplication.translate("MainWindow", u"0", None))
#endif // QT_CONFIG(shortcut)
        self.btn_degree.setText(QCoreApplication.translate("MainWindow", u"^", None))
#if QT_CONFIG(shortcut)
        self.btn_degree.setShortcut(QCoreApplication.translate("MainWindow", u"^", None))
#endif // QT_CONFIG(shortcut)
        self.btn_7.setText(QCoreApplication.translate("MainWindow", u"7", None))
#if QT_CONFIG(shortcut)
        self.btn_7.setShortcut(QCoreApplication.translate("MainWindow", u"7", None))
#endif // QT_CONFIG(shortcut)
        self.btn_5.setText(QCoreApplication.translate("MainWindow", u"5", None))
#if QT_CONFIG(shortcut)
        self.btn_5.setShortcut(QCoreApplication.translate("MainWindow", u"5", None))
#endif // QT_CONFIG(shortcut)
        self.btn_solve.setText(QCoreApplication.translate("MainWindow", u"Solve", None))
#if QT_CONFIG(shortcut)
        self.btn_solve.setShortcut(QCoreApplication.translate("MainWindow", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.btn_minus.setText(QCoreApplication.translate("MainWindow", u"-", None))
#if QT_CONFIG(shortcut)
        self.btn_minus.setShortcut(QCoreApplication.translate("MainWindow", u"-", None))
#endif // QT_CONFIG(shortcut)
        self.btn_x.setText(QCoreApplication.translate("MainWindow", u"x", None))
#if QT_CONFIG(shortcut)
        self.btn_x.setShortcut(QCoreApplication.translate("MainWindow", u"X", None))
#endif // QT_CONFIG(shortcut)
        self.btn_pi.setText(QCoreApplication.translate("MainWindow", u"pi", None))
#if QT_CONFIG(shortcut)
        self.btn_pi.setShortcut(QCoreApplication.translate("MainWindow", u"P", None))
#endif // QT_CONFIG(shortcut)
        self.btn_le.setText(QCoreApplication.translate("MainWindow", u"<", None))
#if QT_CONFIG(shortcut)
        self.btn_le.setShortcut(QCoreApplication.translate("MainWindow", u"<", None))
#endif // QT_CONFIG(shortcut)
        self.btn_qe.setText(QCoreApplication.translate("MainWindow", u">", None))
#if QT_CONFIG(shortcut)
        self.btn_qe.setShortcut(QCoreApplication.translate("MainWindow", u">", None))
#endif // QT_CONFIG(shortcut)
    # retranslateUi

