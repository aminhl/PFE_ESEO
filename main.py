
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from widgets import *
from modules import *
from tkinter import filedialog
import numpy as np
import sys
import os
from worker_thread import WorkerThread

# FIX Problem for High DPI and Scale above 100%
os.environ["QT_FONT_DPI"] = "96"

# SET AS GLOBAL WIDGETS
widgets = None


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        title = "ESEO Dijon - Option E-Sante"
        description = "Detection Mutation Cancer Du Poumon"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        self.charts_added = False

        # TOGGLE MENU
        widgets.toggleButton.clicked.connect(
            lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_exit.clicked.connect(self.buttonClick)

        # IMAGE_TREATEMENT WIDGETS
        widgets.pushButton.clicked.connect(self.buttonClick)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SHOW APP
        self.show()

        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(
            UIFunctions.selectMenu(widgets.btn_home.styleSheet()))

    # BUTTONS CLICK
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        if btnName == "btn_exit":
            self.show_exit_dialog()

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

            if not self.charts_added:

                x1 = [1, 2, 8, 3, 6]
                y1 = [9, 3, 1, 6, 3]
                labels = ['Category 1', 'Category 2']
                sizes = [15, 30]
                fig = Figure()
                fig.set_facecolor('#c9c5c5')
                ax1 = fig.add_subplot(121)
                ax1.plot(x1, y1)
                ax1.set_title('Line Chart')
                ax1.set_xlabel('X-axis')
                ax1.set_ylabel('Y-axis')
                ax2 = fig.add_subplot(122)
                ax2.pie(sizes, labels=labels, autopct='%1.1f%%',
                        startangle=90, wedgeprops=dict(width=0.4))
                ax2.set_title('Donut Chart')
                canvas = FigureCanvas(fig)
                layout = widgets.new_page.layout()
                layout.addWidget(canvas)
                layout.update()
                self.charts_added = True

        if btnName == "pushButton":
            img_path = filedialog.askopenfilename()
            saving_path = filedialog.askdirectory(
                title="Sélection du dossier de sauvegarde")
            widgets.lineEdit.setText(img_path)
            WorkerThread.create_operation_dialog(img_path, saving_path)

    # RESIZE EVENTS
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

        # MOUSE CLICK EVENTS
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

    def show_exit_dialog(self):
        # Show the custom exit confirmation dialog
        exit_dialog = QDialog(self)
        exit_dialog.setStyleSheet("""
            QDialog {
                background-color: rgba(40, 44, 52, 1);
                border: 2px solid #555;
                color: #EEE;
                width: 400px;
                height: 200px;
            }

            QLabel {
                font-size: 14px;
                color: #EEE;
            }
        """)
        exit_dialog.setWindowTitle('Exit Confirmation')

        # Create and set up the label
        label = QLabel('Are you sure you want to exit?', exit_dialog)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create and set up the buttons
        yes_button = QPushButton('Yes', exit_dialog)
        yes_button.clicked.connect(exit_dialog.accept)

        no_button = QPushButton('No', exit_dialog)
        no_button.clicked.connect(exit_dialog.reject)

        # Set up the layout
        dialog_layout = QVBoxLayout(exit_dialog)
        dialog_layout.addWidget(label)
        dialog_layout.addWidget(yes_button)
        dialog_layout.addWidget(no_button)

        # Show the dialog and handle the result
        result = exit_dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            # User clicked "Yes," exit the application
            self.exit_accepted()

    def exit_accepted(self):
        # Exit the application
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec())
