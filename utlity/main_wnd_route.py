from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QPushButton, QMainWindow, QLayout, QApplication, QVBoxLayout, QHBoxLayout, QLabel, \
    QLineEdit, QRadioButton, QTableView, QTableWidget, QTableWidgetItem, QDialog, QFileDialog, QPlainTextEdit, \
    QComboBox, QSpinBox
from PyQt5.QtCore import Qt, QObject, QEvent, QThread, pyqtSignal, pyqtSlot, QRect
from PyQt5.QtGui import QIcon


class CheckRouteWnd(QMainWindow):

    def __init__(self, app):
        super().__init__()
        self.app = app
        # Layers
        self.main_vertical_layer = QVBoxLayout()
        self.csv_lay = QVBoxLayout()
        self.skin_lay = QVBoxLayout()
        self.route_lay = QVBoxLayout()
        self.bc_lay = QVBoxLayout()
        self.thread_lay = QHBoxLayout()
        self.csv_skin_lay = QHBoxLayout()
        self.route_bc_lay = QHBoxLayout()
        self.result_lay = QHBoxLayout()
        self.drive_lay = QHBoxLayout()


        # Widgets
        self.csv_label = QLabel()
        self.csv_button = QPushButton()
        self.skin_label = QLabel()
        self.skin_combo = QComboBox()
        self.route_exclude_label = QLabel("Excluded routes from sitemap")
        self.route_exclude_label.setFixedHeight(15)
        self.route_exclude_plain_text = QPlainTextEdit()
        self.url_bc_label = QLabel("Excluded categories (URL) from sitemap")
        self.url_bc_label.setFixedHeight(15)
        self.url_bc_plain_text = QPlainTextEdit()
        self.threads_count_label = QLabel("Count threads")
        self.threads_count_label.setFixedHeight(20)
        self.threads_count_label.setFixedWidth(70)
        self.threads_count_spin_box = QSpinBox()
        self.go_button = QPushButton()
        self.stop_button = QPushButton()
        self.console = QPlainTextEdit()
        self.console.setMinimumHeight(380)
        self.result_button = QPushButton("Open result directory")
        self.about_button = QPushButton("?")
        self.about_button.setFixedWidth(20)
        self.central_widget = QWidget()



        self.init_ui()

    def init_ui(self):
        desktop = self.app.desktop()
        width_coordinate = (desktop.width() / 2) - 300
        height_coordinate = (desktop.height() / 2) - 400
        self.setGeometry(int(width_coordinate), int(height_coordinate), 600, 600)
        # self.setFixedHeight(600)
        #self.setFixedWidth(400)
        self.setWindowTitle('Route checker')
        self.setWindowIcon(QIcon('image/logo.png'))
        self.setWindowOpacity(0.99)
        # CSV lay
        self.csv_lay.addWidget(self.csv_label)
        self.csv_lay.addWidget(self.csv_button)
        self.csv_lay.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # Skin lay
        self.skin_lay.addWidget(self.skin_label)
        self.skin_lay.addWidget(self.skin_combo)
        self.skin_lay.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # Routes lay
        self.route_lay.addWidget(self.route_exclude_label)
        self.route_lay.addWidget(self.route_exclude_plain_text)
        #self.route_lay.setGeometry(QRect(0, 0, 300, 80))
        self.route_lay.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # BC lay
        self.bc_lay.addWidget(self.url_bc_label)
        self.bc_lay.addWidget(self.url_bc_plain_text)
        self.bc_lay.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        # Thread lay
        self.thread_lay.addWidget(self.threads_count_label)
        self.thread_lay.addWidget(self.threads_count_spin_box)

        # Setup drive lay
        self.drive_lay.addLayout(self.thread_lay)
        self.drive_lay.addWidget(self.go_button)
        self.drive_lay.addWidget(self.stop_button)
        self.drive_lay.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Setup CSV and skin lay
        self.csv_skin_lay.addLayout(self.csv_lay)
        self.csv_lay.addSpacing(5)
#        self.csv_lay.add
        self.csv_skin_lay.addLayout(self.skin_lay)
        self.csv_skin_lay.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        # Setup route and breadcrumb lay
        self.route_bc_lay.addLayout(self.route_lay)
        self.route_bc_lay.addLayout(self.bc_lay)

        # Setup result button lay
        self.result_lay.addWidget(self.about_button)
        self.result_lay.addWidget(self.result_button)

        # Setup main layout
        self.main_vertical_layer.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.main_vertical_layer.addLayout(self.csv_skin_lay)
        self.main_vertical_layer.addLayout(self.route_bc_lay)
        self.main_vertical_layer.addLayout(self.drive_lay)
        self.main_vertical_layer.addWidget(self.console)
        self.main_vertical_layer.addLayout(self.result_lay)
        self.central_widget.setLayout(self.main_vertical_layer)
        #self.central_widget.setFixedHeight(600)
        self.setCentralWidget(self.central_widget)
        self.show()




