from PyQt5.QtWidgets import QWidget, QPushButton, QMainWindow, QLayout, QApplication, QVBoxLayout, QHBoxLayout, QLabel, \
    QLineEdit, QRadioButton, QTableView, QTableWidget, QTableWidgetItem, QDialog, QFileDialog, QPlainTextEdit, QComboBox
from PyQt5.QtCore import Qt, QObject, QEvent, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon


class MainWnd(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.main_vertical_layer = QVBoxLayout()
        self.drive_block_layer = QHBoxLayout()
        self.select_csv_layer = QVBoxLayout()
        self.url_header_layer = QVBoxLayout()
        self.project_name_layer = QVBoxLayout()
        self.skin_layer = QVBoxLayout()
        self.go_layer = QHBoxLayout()
        self.console_layer = QHBoxLayout()
        self.result_layer = QHBoxLayout()
        self.select_csv_label = QLabel("Index articles")
        self.select_csv_button = QPushButton()
        self.header_sitemap_label = QLabel("Enter header sitemap URL")
        self.header_sitemap_lineedit = QLineEdit()
        self.project_name_label = QLabel("Project name")
        self.project_name_lineedit = QLineEdit()
        self.skin_label = QLabel("Skin")
        self.skin_combo = QComboBox()
        self.go_button = QPushButton("GO")
        self.stop_button = QPushButton("STOP")
        self.console = QPlainTextEdit()
        self.result_button = QPushButton("Open project directory")
        self.about_button = QPushButton("?")
        self.central_widget = QWidget()
        self.app = app
        self.init_ui()

    def init_ui(self):
        desktop = self.app.desktop()
        width_coordinate = (desktop.width() / 2) - 300
        height_coordinate = (desktop.height() / 2) - 400
        self.setGeometry(int(width_coordinate), int(height_coordinate), 600, 800)
        self.setWindowTitle('Sitemap checker')
        self.setWindowIcon(QIcon('image/logo.png'))
        self.setWindowOpacity(0.99)

        # csv layer
        self.select_csv_layer.addWidget(self.select_csv_label)
        self.select_csv_layer.addWidget(self.select_csv_button)
        self.select_csv_button.setIcon(QIcon("image/csv.png"))

        # header sitemap layer
        self.url_header_layer.addWidget(self.header_sitemap_label)
        self.url_header_layer.addWidget(self.header_sitemap_lineedit)

        # name project layer
        self.project_name_layer.addWidget(self.project_name_label)
        self.project_name_layer.addWidget(self.project_name_lineedit)

        # Skin layer
        self.skin_layer.addWidget(self.skin_label)
        self.skin_layer.addWidget(self.skin_combo)

        # Setup csv, header sitemap, project name layers on horizontal layer (drive layer)
        self.drive_block_layer.addLayout(self.select_csv_layer)
        self.drive_block_layer.addLayout(self.url_header_layer)
        self.drive_block_layer.addLayout(self.project_name_layer)
        self.drive_block_layer.addLayout(self.skin_layer)

        # Setup drive layer to main vertical layer
        self.main_vertical_layer.addLayout(self.drive_block_layer)

        # Setup GO button on horizontal layer
        self.go_layer.addWidget(self.go_button)
        self.stop_button.setStyleSheet("font-weight: bold; color: white; background-color: #a60000;")
        self.stop_button.hide()
        self.go_layer.addWidget(self.stop_button)

        # Setup GO layer to main vertical layer
        self.main_vertical_layer.addLayout(self.go_layer)

        # setup console textplain on horizontal layer
        self.console_layer.addWidget(self.console)

        # Setup console layer to main vertical layer
        self.main_vertical_layer.addLayout(self.console_layer)

        # Setup result buttons on horizontal layer
        self.result_layer.addWidget(self.about_button)
        self.result_layer.addWidget(self.result_button)

        # Setup result layer to main vertical layer
        self.main_vertical_layer.addLayout(self.result_layer)

        # self.setLayout(self.main_vertical_layer)
        self.central_widget.setLayout(self.main_vertical_layer)

        # set main layer to window
        self.setCentralWidget(self.central_widget)
        self.show()
