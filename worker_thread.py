from image_processing import process_image
from PyQt6.QtCore import pyqtSignal
from modules import *


class WorkerThread(QThread):
    finished = pyqtSignal()

    def __init__(self, img_path, saving_path):
        super().__init__()
        self.img_path = img_path
        self.saving_path = saving_path

    def run(self):
        process_image(self.img_path, self.saving_path)
        self.finished.emit()

    def create_operation_dialog(img_path, saving_path):
        dialog_stylesheet = """
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
                    """
        dialog = QDialog()
        dialog.setWindowTitle("Operation En Cours")
        dialog.setStyleSheet(dialog_stylesheet)
        dialog.setModal(True)
        label = QLabel()
        label.setText("Operation En Cours ...")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(label)
        dialog.setLayout(layout)
        dialog.resize(400, 180)
        opacity_effect = QGraphicsOpacityEffect(label)
        label.setGraphicsEffect(opacity_effect)
        animation = QPropertyAnimation(opacity_effect, b"opacity")
        animation.setDuration(1700)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setLoopCount(-1)
        animation.start()
        worker = WorkerThread(img_path, saving_path)
        worker.finished.connect(dialog.accept)
        worker.start()
        result = dialog.exec()
