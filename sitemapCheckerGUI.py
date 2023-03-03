import os
import subprocess
import sys

from PyQt5.QtCore import pyqtSlot

from about import About_window
from utlity.main_wnd import MainWnd
from PyQt5.QtWidgets import QFileDialog, QApplication, QMessageBox
from checker_thread import Sitemap_check


class GUI_worker(MainWnd):
    def __init__(self):
        super().__init__(app=app)
        # self.app = app
        # Data variable
        self.csv_path = ""
        self.project_name = ""
        self.csv_ready = False
        self.header_url_ready = False
        self.project_name_ready = False
        self.regex_patern = {}
        self.read_config_data()
        self.init_data()

    def read_config_data(self):
        with open("config.cfg", "r") as f:
            for string in f:
                if string[0] == "#" or string == "":
                    continue
                values = string.split("=", 1)
                if values[0] == "skin_value":
                    value_split = values[1].split(":", 1)
                    self.regex_patern.update({value_split[0]: value_split[1]})

    def init_data(self):
        self.result_button.setEnabled(False)
        self.not_ready_go_button()
        self.go_button.clicked.connect(self.start_check_sitemap)
        self.result_button.clicked.connect(self.open_result)
        self.select_csv_button.clicked.connect(self.csv_dialog)
        self.select_csv_button.setFixedWidth(100)
        self.select_csv_label.setFixedWidth(100)
        self.about_button.setFixedWidth(30)
        self.about_button.clicked.connect(self.about_window)
        self.header_sitemap_lineedit.textChanged.connect(self.check_correct_url)
        self.header_sitemap_lineedit.setFixedHeight(24)
        self.project_name_lineedit.textChanged.connect(self.check_name_project)
        self.project_name_lineedit.setFixedWidth(100)
        self.project_name_lineedit.setFixedHeight(24)
        self.skin_combo.currentTextChanged.connect(self.go_enable)
        self.fill_skin_combo()
        self.skin_combo.setFixedHeight(24)

    def fill_skin_combo(self):
        for item in self.regex_patern.keys():
            self.skin_combo.addItem(item)

    def check_correct_url(self):
        if self.header_sitemap_lineedit.text().startswith("https://"):
            self.header_sitemap_label.setText("Header sitemap URL")
            self.header_url_ready = True
            self.go_enable()
        elif self.header_sitemap_lineedit.text() == "":
            self.header_sitemap_label.setText("Enter header sitemap URL")
            self.header_url_ready = False
            self.go_enable()
        else:
            self.header_sitemap_label.setText("Incorrect URL")
            self.header_url_ready = False
            self.go_enable()

    def check_name_project(self):
        if self.project_name_lineedit.text() != "":
            self.project_name = self.project_name_lineedit.text()
            self.project_name_ready = True
            self.go_enable()
        else:
            self.project_name_ready = False
            self.go_enable()

    def csv_dialog(self):
        csv_path = QFileDialog.getOpenFileName(self, 'Select CSV file with index articleID', '', 'CSV file (*.csv)')[0]
        if csv_path:
            self.csv_path = csv_path
            file_name = str(csv_path).split("/")[-1]
            self.select_csv_label.setText(f"✓ {file_name}")
            self.csv_ready = True
            self.go_enable()

    def ready_go_button(self):
        self.go_button.setStyleSheet("font-weight: bold; color: white; background-color: #265226;")
        self.go_button.setText("GO")
        self.go_button.setEnabled(True)

    def not_ready_go_button(self):
        self.go_button.setStyleSheet("font-weight: normal; color: 828282; background-color: #CBCBCB; outline-color: #BEBEBE;  border: 0;")
        self.go_button.setEnabled(False)

    def go_enable(self):
        if self.header_url_ready and self.csv_ready and self.project_name_ready:
            self.ready_go_button()
        else:
            self.not_ready_go_button()

    def open_result(self):
        if os.path.exists(self.project_name_lineedit.text().strip()):
            subprocess.Popen(f'explorer {os.curdir}\\{self.project_name}')
        else:
            self.result_button.setText(f"{self.project_name} project does not exist")
            self.result_button.setEnabled(False)

    def check_project_name(self):
        if os.path.exists(self.project_name_lineedit.text().strip()):
            reply = QMessageBox.question(self,
                                         "Project",
                                         f"Project \"{self.project_name_lineedit.text().strip()}\" already exist.\nRewrite project?",
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.NoButton)
            if reply == QMessageBox.No:
                return False
            else:
                return True
        return True

    def start_check_sitemap(self):
        if self.check_project_name():
            self.stop_button.show()
            self.stop_button.clicked.connect(self.stop_checker_thread)
            self.go_button.setText("PROCESSING...")
            self.disable_drive()
            self.console.clear()
            self.console.appendPlainText(f"** Start process for {self.project_name} project **")
            self.sitemap_check_thread = Sitemap_check(self.header_sitemap_lineedit.text().strip(),
                          self.regex_patern[self.skin_combo.currentText()],
                          self.csv_path,
                          self.project_name_lineedit.text().strip())
            self.sitemap_check_thread.console_message.connect(self.output_to_console)
            self.sitemap_check_thread.finish_flag.connect(self.finish_analyze)
            self.sitemap_check_thread.stop_exception.connect(self.stop_by_exception)
            self.sitemap_check_thread.start()

    @pyqtSlot(str)
    def output_to_console(self, in_string):
        self.console.appendPlainText(in_string)

    @pyqtSlot()
    def finish_analyze(self):
        self.enable_drive()
        self.console.appendPlainText("\n ** Finish **\nOpen project directory with report files\n")
        self.result_button.setEnabled(True)
        self.stop_button.hide()
        self.result_button.setText(f"Open project directory")

    @pyqtSlot(str)
    def stop_by_exception(self, message):
        self.console.appendPlainText(f"\n ERROR! {message}\n")
        self.sitemap_check_thread.terminate()
        self.stop_button.hide()
        self.enable_drive()

    def stop_checker_thread(self):
        self.sitemap_check_thread.wait(3)
        self.sitemap_check_thread.terminate()
        self.enable_drive()
        self.stop_button.hide()

    def enable_drive(self):
        self.select_csv_button.setEnabled(True)
        self.header_sitemap_lineedit.setEnabled(True)
        self.project_name_lineedit.setEnabled(True)
        self.skin_combo.setEnabled(True)
        self.ready_go_button()

    def disable_drive(self):
        self.select_csv_button.setEnabled(False)
        self.header_sitemap_lineedit.setEnabled(False)
        self.project_name_lineedit.setEnabled(False)
        self.skin_combo.setEnabled(False)
        self.not_ready_go_button()

    def about_window(self):
        self.about_window = About_window(self)


# Main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_wnd = GUI_worker()
    sys.exit(app.exec_())
