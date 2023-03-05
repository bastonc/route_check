from PyQt5 import QtCore
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QScrollArea


class About_window(QWidget):

    def __init__(self, parent_wnd):
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

        #self.main_layer.addWidget(self.scrol_lay)
        # self.setFixedWidth(800)
        # self.setWindowIcon()
        # self.setWindowTitle("About Sitemap cheker")
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
        self.scroll_lay.setWindowIcon(QIcon("image/logo.ico"))
        self.scroll_lay.setWindowTitle("About Sitemap checker")



    def init_data(self):
        # Caption
        self.pixmap = QPixmap("image/logo.ico")
        pixmap = self.pixmap.scaled(70, 70, QtCore.Qt.KeepAspectRatio)
        self.logo_label.setPixmap(pixmap)
        self.caption_label.setText("<h1>Sitemap checker</h1><p><strong>v.1.0</strong></p>")
        #self.caption_layer.setGeometry(QRect(200,500,400, 600))
        self.caption_layer.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # General info
        self.general_info_layer.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.general_info_label.setText("<br><h3>ОБЩАЯ ИНФОРМАЦИЯ</h3><p>Sitemap checker позволяет выполнять проверку перегениерации карт сайта после обновления индексируемых товаров,<br>наличия индексируемых/неиндексируемых продуктов (articleID) в сайтмапах</p>"
                                        "<p>Для проверки необходимо:</p>"
                                        "<ul><li>указать <strong>файл с индексируемыми артикулами</strong>, который можно получить после перегенерации индексируемых товаров</li>"
                                        "<li>указать <strong>путь к заголвочному файлу Sitemap</strong> (можно получить в search console)</li>"
                                        "<li>указать <strong>название проекта</strong> - оно может быть любым, например Ersatz DE product.</li></ul>"
                                        "<p> Алгоритм извлекает артикулы из URL продуктовых страниц и сравнивает их со списком индексируемых артикулов.<br>"
                                        "Cовпадения, артикулы не вошедшие в sitemap и артикулы которые есть в файлах sitemap но<br>"
                                        "отсутствуют в списке индексируемых (noindex артикулы) заносятся в соответсвтующие csv файлы отчетов</p>"
                                        "<p>В результате анализа, в каталоге с программой будет новая папка с именем проекта.<br>"
                                        "Открывается папка с проектом по кнопке \"Open project directory\""
                                        " в котрой будут хранится:</p><ul><li>match.csv - в этом файле указаны какие индексируемые артикулы в каких файлах sitemap находятся;</li>"
                                        "<li>not-found.csv - в нем указаны артикулы которые есть в списке индексируемых, но отсутствуют в сайтмапах;</li>"
                                        "<li>noindex.csv - артикулы которые обнаружены в сайтмапах но их нет в списке индексируемых (noindex продукты);</li>"
                                        "<li>в подпапке sitemaps - будут сохранены все сайтмапы в формате xml.</li><ul>")

        # CSV file info
        self.csv_inf_layer.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.csv_label.setText("<h3>ФАЙЛ С ИНДЕКСИРУЕМЫМИ АРТИКУЛАМИ</h3>"
                               "<p>В файле должен быть один столбец с индексируемыми артикулами.<br>"
                               "Заголовок столбца с артикулами - может быть любым или вообще отсутствовать</p>")
        csv_image = QPixmap("image/csv_table.png")
        self.csv_image_label.setPixmap(csv_image)
        self.header_sitemap_layer.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        # Header sitemap info
        self.header_sitemap_label.setText("<h3>ЗАГОЛОВОЧНЫЙ ФАЙЛ SITEMAP</h3><p>Файл sitemap в котором содержаться URL дочерних карт с адресами страниц сайта.<br> "
                                          "Адрес заголвочного файла желательно брать из search console, так можно быть точно увереным, что выполняется <br>"
                                          "проверка именно того сайтмап который видит Google.</p>")

        # Project name info
        self.project_info_layer.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.name_project_label.setText("<h3>НАЗВАНИЕ ПРОЕКТА</h3><p>В результате анализа в рабочей директории создается папка с именем<br> проекта в которой содержаться файлы "
                                        "отчетов (совпадения, не найденные<br>артикулы в сайтмапах, noindex-артикулы).</p><p> Такой подход позволяет выполнить<br> неколько проверок без риска "
                                        "потерять результат предыдущей проверки <br>Перезапись данных в проекте возможна только после подтверждения на перезапись проекта</p>")
        project_image = QPixmap("image/proj.png")
        self.name_project_image_label.setPixmap(project_image)

        # Skin info
        self.skin_info_layer.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.skin_info_label.setText("<h3>ВЫБОР СКИНА</h3><p>Выбор скина необходим для правильного парсинга артикула из URL'ов расположеных в sitemap файлах.<br> На данный "
                                     "момент можно выбрать Ersatz product и Direkt product.<br>Можно добавлять свои собственные пункты.<br>"
                                     "Для этого в файле config.cfg добавляется новая строка в формате<br>"
                                     "skin_value=Название:регулярное выражение<br>"
                                     "где:<br>- Название - название которое будет отображаться в выпадающем списке skin в интерфейсе программы<br>"
                                     "- регулярное выражение - регулярка которая позволяет извлекать артикулы из URL (или другую необходимую часть URL)</p><br>")

        # Console info layer
        self.console_layer.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.console_label.setText("<h3>КОНСОЛЬ</h3><p>В консоли отображается ход выполнения анализа, из нее можно почерпнуть информацию<br>о кол-ве артикулов в каждом файле сайтмапа,"
                                   "общем кол-ве индексируемых артикулов, <br>о том сколько найдено совпадений и неиндексируемых артикулов в каждом сайтмапе</p><br>")

        # Copyright layer
        self.copyright_layer.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.copyright_label.setText("<p style='font-size: 10px;'>Если, что-то не работает, возникли пожелания, предложения пишите <a href='mailto:s.baston@autodoc.eu'>s.baston@autodoc.eu</a> "
                                     "или в слаке Sergey Baston</p><center>© Sergey Baston 2023</center>")

