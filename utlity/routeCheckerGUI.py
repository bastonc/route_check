import json
import math
import subprocess
import sys
import traceback

from PyQt5.QtCore import pyqtSlot, QThread
from PyQt5.QtGui import QIcon

from utlity.check_route_thread import CsvWorker, CheckerRouteThread, OutputCsv
from PyQt5.QtWidgets import QFileDialog, QApplication, QMessageBox

from utlity.main_wnd_route import CheckRouteWnd


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    text += ''.join(traceback.format_tb(tb))
    print(text)
    QMessageBox.critical(None, 'Error', text)
    quit()
sys.excepthook = log_uncaught_exceptions


class GUI_worker(CheckRouteWnd):
    def __init__(self):
        super().__init__(app=app)
        self.csv_file_name = None
        self.csv_ready = False
        self.skin_values = {}
        self.read_config_data()
        self.exclude_url_list = []
        self.exclude_route = []
        self.all_articles_list = []
        self.thread_analyze = []
        self.thread_list = {}
        self.output_file_path = ""
        self.console_counter = 0
        self.init_data()

    def init_data(self):
        self.csv_button.setIcon(QIcon("image/csv.png"))
        self.csv_button.setFixedWidth(150)
        self.csv_button.setFixedHeight(30)
        self.csv_button.clicked.connect(self.file_dialog)
        self.csv_label.setText("CSV file")
        self.csv_label.setFixedWidth(150)
        self.skin_label.setText("Skin")
        self.skin_combo.setFixedWidth(140)
        self.skin_combo.setFixedHeight(28)
        self.fill_skin_combo()
        self.route_exclude_plain_text.setFixedWidth(150)
        self.route_exclude_plain_text.setFixedHeight(80)
        self.url_bc_plain_text.setFixedHeight(80)
        self.threads_count_spin_box.setFixedWidth(30)
        self.go_button.setText("GO")
        self.go_button.setEnabled(False)
        self.go_button.clicked.connect(self.start_analyze_route)
        self.stop_button.hide()
        self.stop_button.setText("STOP")
        self.stop_button.clicked.connect(self.stop_worker_thread)
        self.stop_button.setStyleSheet("font-weight: bold; color: white; background-color: #a60000;")
        self.threads_count_spin_box.setMaximum(5)
        self.threads_count_spin_box.setMinimum(1)
        self.result_button.clicked.connect(self.open_result_directory)
        self.store_prev_session()

    def read_config_data(self):
        with open("cr_config.cfg", "r") as f:
            for string in f:
                if string[0] == "#" or string == "":
                    continue
                values = string.split("=", 1)
                if values[0] == "skin_value":
                    value_split = values[1].split("|")
                    self.skin_values.update({value_split[0]: {"url_pattern": value_split[1],
                                                              "bc_class_link": value_split[2],
                                                              "regex_pattern": str(value_split[3]).strip()}
                                             })

    def fill_skin_combo(self):
        for item in self.skin_values.keys():
            self.skin_combo.addItem(item)

    def store_prev_session(self):
        with open("history.json", "r") as f:
            json_obj = json.load(f)
        if "skin_combo" in json_obj:
            self.skin_combo.setCurrentText(json_obj["skin_combo"])
        if "excluded_route" in json_obj:
            self.route_exclude_plain_text.appendPlainText(json_obj["excluded_route"])
        if "exclude_urls" in json_obj:
            self.url_bc_plain_text.appendPlainText(json_obj["exclude_urls"])

    def start_analyze_route(self):
        self.go_button.setText("PROCESSING...")
        self.console_counter = 0
        self.console.clear()
        self.not_ready_go_button()
        self.stop_button.show()
        self.exclude_url_list = self.url_bc_plain_text.toPlainText().split("\n")
        self.exclude_route = self.route_exclude_plain_text.toPlainText().split("\n")
        self.console.appendPlainText("** Start processing in {self.thread_num} thread(s) **")
        self.save_data()

        # Init output file
        file_path_split = str(self.csv_file_name).split("/")
        self.output_file_path = "".join(item_path + "/" for item_path in file_path_split[:len(file_path_split) - 1])
        self.output_cvs_thread = QThread()
        self.output_csv = OutputCsv(
            str(self.output_file_path) + file_path_split[-1].replace(".csv", "") + "-routeCheker-out.csv")
        self.output_cvs_thread.started.connect(self.output_csv.init_output_csv)
        self.output_cvs_thread.start()

        # Get all articles
        self.csv_thread = QThread()
        self.csv_worker_thread = CsvWorker(self.csv_file_name)
        self.csv_worker_thread.articles_list_signal.connect(self.fill_csv_list)
        self.csv_worker_thread.console_message.connect(self.output_message_to_console)
        self.csv_worker_thread.moveToThread(self.csv_thread)
        self.csv_thread.started.connect(self.csv_worker_thread.get_article_from_scv)
        self.csv_thread.start()

    @pyqtSlot(list)
    def fill_csv_list(self, article_list):
        self.all_articles_list = article_list
        self.csv_thread.exit(0)
        self.start_threads()

    @pyqtSlot(object)
    def finish_processing(self, thread_id):
        self.console.appendPlainText(f"** Finished processing (Thread {self.thread_list[thread_id[0]]} ) **")
        thread_id[1].terminate()
        self.thread_list.pop(thread_id[0])
        if len(self.thread_list) == 0:
            self.output_cvs_thread.terminate()
            self.csv_thread.terminate()
            self.thread_analyze.clear()
            self.ready_go_button()
            self.stop_button.hide()

    @pyqtSlot(str)
    def output_to_console(self, message):
        self.console_counter += 1
        self.console.appendPlainText(f"# {self.console_counter} {message}")

    @pyqtSlot(str)
    def output_message_to_console(self, message):
        self.console.appendPlainText(message)

    def stop_worker_thread(self):
        for thread in self.thread_analyze:
            thread.terminate()
        self.console.appendPlainText("** Stopped processing **")
        self.output_cvs_thread.terminate()
        self.csv_thread.terminate()
        self.thread_analyze.clear()
        self.thread_list.clear()
        self.ready_go_button()
        self.stop_button.hide()

    def start_threads(self):
        stop_position_for_slice = 0
        len_article_list = len(self.all_articles_list)
        self.thread_analyze.clear()

        # Create threads workers
        count_articles_for_thread = len_article_list / int(self.threads_count_spin_box.text())
        for item in range(int(self.threads_count_spin_box.text())):
            start_position_for_slice = stop_position_for_slice if stop_position_for_slice is not None else len_article_list
            stop_position_for_slice = None if (start_position_for_slice + math.ceil(count_articles_for_thread)) > len_article_list else start_position_for_slice + math.ceil(count_articles_for_thread)
            print(f"start: {start_position_for_slice}, stop: {stop_position_for_slice}")
            if start_position_for_slice < len_article_list:
                self.thread_analyze.append(CheckerRouteThread(articles_list=self.all_articles_list[start_position_for_slice:stop_position_for_slice],
                                                              exclude_route=self.exclude_route,
                                                              exclude_url_list=self.exclude_url_list,
                                                              skin=self.skin_values[self.skin_combo.currentText()]["url_pattern"],
                                                              class_name=self.skin_values[self.skin_combo.currentText()]["bc_class_link"],
                                                              output_csv_name="result_gui_3.csv",
                                                              regex_pattern=self.skin_values[self.skin_combo.currentText()]["regex_pattern"],
                                                              output_to_csv=self.output_csv.save_to_report_file)
                                           )

        # Start threads workers
        for index, thread in enumerate(self.thread_analyze, start=1):
            self.thread_list.update({id(thread): index})
            thread.finish_processing.connect(self.finish_processing)
            thread.console.connect(self.output_to_console)
            thread.console_message.connect(self.output_message_to_console)
            thread.start()

    def save_data(self):
        data = {"excluded_route": self.route_exclude_plain_text.toPlainText(),
                "exclude_urls": self.url_bc_plain_text.toPlainText(),
                "skin_combo": self.skin_combo.currentText()}
        with open("history.json", "w") as f:
            json.dump(data, f)

    def file_dialog(self):
        csv_path = QFileDialog.getOpenFileName(self, 'Select CSV file with articleID', '', 'CSV file (*.csv)')[0]
        if csv_path:
            self.csv_file_name = csv_path
            file_name = str(csv_path).split("/")[-1]
            self.csv_label.setText(f"✓ {file_name}")
            self.csv_ready = True
            self.go_enable()

    def go_enable(self):
        if self.csv_ready:
            self.ready_go_button()
        else:
            self.not_ready_go_button()

    def ready_go_button(self):
        self.go_button.setText("GO")
        self.go_button.setEnabled(True)
        self.go_button.setStyleSheet("font-weight: bold; color: white; background-color: #265226;")

    def not_ready_go_button(self):
        self.go_button.setEnabled(False)
        self.go_button.setStyleSheet("font-weight: normal; color: 828282; background-color: #CBCBCB; outline-color: #BEBEBE;  border: 0;")

    def open_result_directory(self):
        output_file_path = self.output_file_path.replace("/", "\\")
        subprocess.Popen(f'explorer {output_file_path}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_wnd = GUI_worker()
    sys.exit(app.exec_())
