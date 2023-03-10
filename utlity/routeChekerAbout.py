from PyQt5 import QtCore
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QScrollArea


class AboutRouteChecker(QWidget):

    def __init__(self):
        super().__init__()
        # Layouts
        self.caption_layer = QHBoxLayout()
        self.general_info_layer = QHBoxLayout()
        self.csv_inf_layer = QHBoxLayout()
        self.header_sitemap_layer = QHBoxLayout()
        self.project_info_layer = QHBoxLayout()
        self.skin_info_layer = QHBoxLayout()
        self.console_layer = QHBoxLayout()
        self.copyright_layer = QHBoxLayout()
        self.main_layer = QVBoxLayout()
        self.main_widget = QWidget()
        self.scroll_lay = QScrollArea()

        # Labels
        self.logo_label = QLabel()
        self.caption_label = QLabel()
        self.general_info_label = QLabel()
        self.csv_label = QLabel()
        self.csv_image_label = QLabel()
        self.header_sitemap_label = QLabel()
        self.name_project_label = QLabel()
        self.name_project_image_label = QLabel()
        self.skin_info_label = QLabel()
        self.console_label = QLabel()
        self.copyright_label = QLabel()

        self.init_ui()

    def init_ui(self):

        # Caption layer
        self.caption_layer.addWidget(self.logo_label)
        self.caption_layer.addWidget(self.caption_label)

        # General info layer
        self.general_info_layer.addWidget(self.general_info_label)

        # CSV info layer
        self.csv_inf_layer.addWidget(self.csv_label)
        self.csv_inf_layer.addWidget(self.csv_image_label)

        # Header sitemap layer
        self.header_sitemap_layer.addWidget(self.header_sitemap_label)

        # Name project layer
        self.project_info_layer.addWidget(self.name_project_label)
        self.project_info_layer.addWidget(self.name_project_image_label)

        # Skin info layer
        self.skin_info_layer.addWidget(self.skin_info_label)

        # Console info layer
        self.console_layer.addWidget(self.console_label)

        # Copyright layer
        self.copyright_layer.addWidget(self.copyright_label)

        # Setup all layers to main layer
        self.main_layer.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_layer.addLayout(self.caption_layer)
        self.main_layer.addLayout(self.general_info_layer)
        self.main_layer.addLayout(self.csv_inf_layer)
        self.main_layer.addLayout(self.header_sitemap_layer)
        self.main_layer.addLayout(self.project_info_layer)
        self.main_layer.addLayout(self.skin_info_layer)
        self.main_layer.addLayout(self.console_layer)
        self.main_layer.addLayout(self.copyright_layer)
        self.setLayout(self.main_layer)
        self.init_data()

        self.main_widget.setLayout(self.main_layer)

        self.scroll_lay.setWidget(self.main_widget)
        self.scroll_lay.resize(800, 700)
        self.scroll_lay.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.scroll_lay.setWindowIcon(QIcon("image/logo.png"))
        self.scroll_lay.setWindowTitle("About Route checker")

    def init_data(self):
        # Caption
        self.pixmap = QPixmap("image/logo.png")
        pixmap = self.pixmap.scaled(70, 70, QtCore.Qt.KeepAspectRatio)
        self.logo_label.setPixmap(pixmap)
        self.caption_label.setText("<h1>Route checker</h1><p><strong>v.1.0</strong></p>")
        self.caption_layer.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # General info
        self.general_info_layer.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.general_info_label.setText("<br><h3>?????????? ????????????????????</h3>"
                                        "<p>?????????? ?????????????????????????? sitemap ???????????????????? ?????????????????? ???????????????????????? ?????????????????????? ???????? ????????????.<br>"
                                        "?????????? ?????????????????? ??????:</p>"
                                        "<ul><li>???????????????????? ?? sitemap ???????????????? ???? ?????????? ????????????????????</li>"
                                        "<li>???????????????? ?????????????????? ???????????? ?????? 200</li>"
                                        "<li>?? ?????????? ?????????? ???????????????? ?????? (?? ????????????) ?????????????????????????? ????????????????</li></ul>"
                                        "<p>??.??. ?????????? ?????????????????????????? ?????????????????? ???????????????????? ~ 3 ??????, ?????????????????? ?????????????? ???????????????????????? ?????????????????? sitemap - <br> ???? ???????????????????????????? ??????????????????. ???????????? ???????????? ???????????????? ???????????????? ???????????????????? Sitemap Cheker ?? Route Checker"
                                        "<p>Route checker ?????????????????? ???????????????????? ???????????????????? ?????????????????? ?????????????? ???????? ????????????????/?????????????????? ?? sitemap, ???????????????? ??????????????<br>?????????????????? ???????????????? ?????? ???????????? ?????? ???????????????? ???? 200.</p>"
                                        "<p>???????????????? ???????????????? ?????????????????? ??????????????:</p>"
                                        "<ol><li>???????????????? ???????????????? ?????????????? ???????????? ?? ???????????????????? ?? sitemap ?? ?????????????? Sitemap checker</li>"
                                        "<li>?? Route checker ?????????????????? ???????? ?? ???????????????????? ???????????? ???? ?????????????? ?? ??????????????????</li>"
                                        "<li>?????????????????? ?????????? ???????? ???? ???????????? ?????????????? ?? ?????????? ?????????? (???????????????? tyre_item)</li>"
                                        "<li>?????????????????? URL ?????????????????? ???????????? ???? ?????????????? ???? ???????????? ?????????????? ?? ?????????? ?????????? (???????????????? ??????????????????????, ???????????????????? ?? ??.??.)</li>"
                                        "<li>?????????? ???????????????????? ???????????????? ???????????????? csv ???????? ?? ?????????????? ?????? ?????????????? ???????????????? ?????????? ???????????? ?????? ?? ???????????????? ???? ??????????????????????,<br>"
                                        "???????????????? (???????? ?????????????? ??????????????), ?????????????????? ?????? ???????????? ?????????????? (?? ???????????? ???????? ?????????????? ??????????)<br>"
                                        "???????? ?????????????? ???? ???????????? ?? ???????????????? ?????????????????? ?????? ?????????????????? ?????????? ?? ?????????????????? (???? ??.3, 4), ??.??. ???????????? ?????????????? <br>"
                                        "???????????? ???????? ?????????????? ?? ?????????????? - ???? ???????????????????? ?????? \"valid\"<br> "
                                        "?? ?????????????????????? ???? ?????????????? ?????????????? ???????????? ?????????????????????? ?? ???????????? ???????????????? ??????-???? ???? ???????????????????? ?? ?????????? ?????????? ??????????????</li>"
                                        "<li>?????????????? ?????????????? ?????????????????????? ???????????????? ???????????????? ?? sitemap ?????????????????? - ?????????????????????? ???????? ?? ?????????????????? ?? ?????????????? ????????????????????<br>"
                                        "???? ???????????? ???????????????? ?????????? ?????????????? ?? ???????????? ???????? ??????????????????????, ?????? ?????????????? \"??????????\", ?????? ?????????? ???????????????? (?????????? ????????????????<br>"
                                        "???????????????????? ?????????????????? ???? sitemap). ?????? ???????????????? ?????????????????? ???????????????? ?? sitemap ???? ???????????????? 'valid' ???????????????? ???? ????????????????</li></ol>"
                                        )

        # interface image
        self.csv_inf_layer.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        csv_image = QPixmap("image/route_checker_1.png")
        self.csv_image_label.setPixmap(csv_image)
        self.header_sitemap_layer.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)



        # Header sitemap info
        self.header_sitemap_label.setText("<h3>?????????????????? ????????????????????</h3>"
                                          "<p>1 - ???????????? ???????????? ?????????? ?? ???????????????????? ?????????????????????? ???? Sitemap checker<br>"
                                          "2 - ?????????? ?????????? ?????? ???????????????? ?????????? ????????????????<br>"
                                          "3 - ???????????????? ?????????? ?????????????? <strong>???? ????????????</strong> ?????????????? ?? sitemap<br>"
                                          "4 - ???????????????? URL ?????????????????? ???????????? ???? ?????????????? <strong>???? ????????????</strong> ?????????????? ?? sitemap<br>"
                                          "5 - ??????-???? ?????????????? ?? ?????????????? ?????????? ???????????????? ???????????????? ?????????????????? (?????? ???????????? ?????????????? - ?????? ?????????????? ?????????????? ????????????????,<br>???? ?? ???????????? ???????????????? ???? ????????????,"
                                          " ?????????????? ?????????????????? ???????????????? 5-?? ????????????????). ???????????? ?????????? ?????????? ?????????????????? ???????????? ?????????? ?? ?????? ??????????????<br>"
                                          "6 - ?????????????? ?? ?????????????? ???????????????????? ?????? ???????????????????? ????????????????<br>"
                                          "7 - ???????????? ?????????????? ?????????????????? ?????????? ?? csv-???????????? ?? ???????????? ?????????????????????? ?????????????????? ?????????????? (???????????? ???????? ????????????????<br>?????????? ?? ???????????? ?????????????? ?????? ???????????? ?? ?? 1 ?? ???????????? '?????? ???????????????????? ??????????'-routeChecker-result.csv)<br></p>"
                                          )

        # Project name info
        self.project_info_layer.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.name_project_label.setText("<h3>???????????????????????????? ??????????????????</h3>"
                                        "<p>???????????????? ???????????????????? ???????????? ?????????? ???????????????????? ?? ???????? cr_config ?????????? ?? ??????????????<br>"
                                        "skin_value=Ersatz product|https://new.autoersatzteile.de/[]-motul|breadcrumbs__link|(?&lt;=\/)\d+(?=-)<br>"
                                        "??????: <br>"
                                        "Ersatz product - ???????????????? ?????????????? ?????????? ???????????????????????? ?? ???????????????????? ???????????? ????????????<br>"
                                        "https://new.autoersatzteile.de/[]-motul ?????????? URL ????????????????, ?????????? ?????? ???????????? ???????? ?????????????? ?????????????????????? ?????? '[]'<br>"
                                        "breadcrumbs__link - ?????????? ???????????? ?????????????? ???????????? (???? ?????????????? ?????????????? ???????????????????????? ???????????????????????????? ???????????????? ?? ??????????????????)<br>"
                                        "(?&lt;=\/)\d+(?=-) - ?????????????????? ?????? ???????????????????? ???????????????? ???? URL (?????????? ?? ???????????????? ????????????)<br></p>")

        # Skin info
        self.skin_info_layer.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.skin_info_label.setText("<h3>????????????????????</h3>"
                                     "<p>?????????????????? Route checker ???????????????????? ?? ???????????????????? VPN, ??.??. ???????????????? ?????????????????????? ???? ?????????????????? NEW<br>"
                                     "???????????? ?????????????? ?????????? ???????????? ?????????? ?????????????? ???????????? - ?????????????????? ???? ?????????????????? ?????? ?????????????????? ?? sitemap (???? Ersatz ????????????<br>"
                                     "?????????? ?????????????? ?????????????????? ????????????????????, ?????????????? ?????? ???????????????? Ersatz ?????? ?????????????????????????? ?????????????????? URL ?????????????????? ??????????????????????)</p><br>")

        # Copyright layer
        self.copyright_layer.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.copyright_label.setText("<p style='font-size: 10px;'>????????, ??????-???? ???? ????????????????, ???????????????? ??????????????????, ?????????????????????? ???????????? <a href='mailto:s.baston@autodoc.eu'>s.baston@autodoc.eu</a> "
                                     "?????? ?? ?????????? Sergey Baston</p><center>?? Sergey Baston 2023</center>")

