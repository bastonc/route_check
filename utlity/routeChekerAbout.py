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
        self.general_info_label.setText("<br><h3>ОБЩАЯ ИНФОРМАЦИЯ</h3>"
                                        "<p>После перегенирации sitemap необходимо проверить корректность обновленных карт сайтов.<br>"
                                        "Важно проверить что:</p>"
                                        "<ul><li>включенные в sitemap продукты не имеют редиректов</li>"
                                        "<li>страницы продуктов отдают код 200</li>"
                                        "<li>в карту сайта включены все (и только) индексируемые продукты</li></ul>"
                                        "<p>Т.к. объем индексируемых артикулов составялет ~ 3 млн, проверить вручную корректность генерации sitemap - <br> не представляется возможным. Помочь данной проверке призваны приложения Sitemap Cheker и Route Checker"
                                        "<p>Route checker позволяет определить валидность продуктов которые были включены/исключены в sitemap, продукты которые<br>выполянют редирект или отдают код отличный от 200.</p>"
                                        "<p>Проверка делается следующим образом:</p>"
                                        "<ol><li>Получаем артикулы которые входят и отсуствуют в sitemap с помощью Sitemap checker</li>"
                                        "<li>В Route checker указываем файл с артикуалми котрые не найдены в сайтмапах</li>"
                                        "<li>Указываем какие руты не должны входить в карту сайта (например tyre_item)</li>"
                                        "<li>Указываем URL категорий товары из которых не должны входить в карту сайта (например инстурменты, аксессуары и т.п.)</li>"
                                        "<li>После завершения проверки получаем csv файл в котором для каждого артикула будет указан рут к которому он принадлежит,<br>"
                                        "редирект (если таковой имеется), ошибочный код ответа сервера (в случае если продукт битый)<br>"
                                        "Если продукт не входит в перечень указанных для исклчения рутов и категорий (из п.3, 4), т.е. данный артикул <br>"
                                        "должен быть включен в сайтмап - он помечается как \"valid\"<br> "
                                        "В последствии по данному столбцу удобно фильтровать и быстро получать кол-во не включенных в карту сайта товаров</li>"
                                        "<li>Похожим образом выполянется проверка входящих в sitemap артикулов - указывается файл с входящими в сайтмап артикулами<br>"
                                        "на выходе получаем какой артикул к какому руту принадлежит, или продукт \"битый\", или имеет редирект (такие артикулы<br>"
                                        "необходимо исключить из sitemap). При проверке продуктов входящих в sitemap на постфикс 'valid' внимания не обращаем</li></ol>"
                                        )

        # interface image
        self.csv_inf_layer.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        csv_image = QPixmap("image/route_checker_1.png")
        self.csv_image_label.setPixmap(csv_image)
        self.header_sitemap_layer.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)



        # Header sitemap info
        self.header_sitemap_label.setText("<h3>ИНТЕРФЕЙС УПРАВЛЕНИЯ</h3>"
                                          "<p>1 - Кнопка выбора файла с артикулами полученными от Sitemap checker<br>"
                                          "2 - Выбор скина для которого будет проверка<br>"
                                          "3 - Перечень рутов которые <strong>не должны</strong> входить в sitemap<br>"
                                          "4 - Перечень URL категорий товары из которых <strong>не должны</strong> входить в sitemap<br>"
                                          "5 - Кол-во потоков в которое будут парсится страницы продуктов (чем больше потоков - тем быстрее процесс парсинга,<br>но и больше нагрузка на сервер,"
                                          " поэтому ограничил максимум 5-ю потоками). Каждый поток между запросами делает паузу в пол секунды<br>"
                                          "6 - Консоль в которой отражается ход выполнения процесса<br>"
                                          "7 - Кнопка которая открывает папку с csv-файлом в котром представлен результат анализа (данный файл появится<br>рядом с файлом который был указан в п 1 с именем 'имя указанного файла'-routeChecker-result.csv)<br></p>"
                                          )

        # Project name info
        self.project_info_layer.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.name_project_label.setText("<h3>ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ</h3>"
                                        "<p>Возможно дополнение скинов путем добавления в файл cr_config строк в формате<br>"
                                        "skin_value=Ersatz product|https://new.autoersatzteile.de/[]-motul|breadcrumbs__link|(?&lt;=\/)\d+(?=-)<br>"
                                        "где: <br>"
                                        "Ersatz product - название которое будет отображаться в выпадающем списке скинов<br>"
                                        "https://new.autoersatzteile.de/[]-motul любой URL продукта, место где должен быть артикул указывается как '[]'<br>"
                                        "breadcrumbs__link - класс ссылки хлебных крошек (по хлебным крошкам определяется принадлежность продукта к категории)<br>"
                                        "(?&lt;=\/)\d+(?=-) - регулярка для извлечения артикула из URL (нужна в процессе работы)<br></p>")

        # Skin info
        self.skin_info_layer.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.skin_info_label.setText("<h3>ПРИМЕЧАНИЯ</h3>"
                                     "<p>Запускать Route checker необходимо с включенным VPN, т.к. проверка выполянется на окружении NEW<br>"
                                     "Товары которые имеют меньше одной хлебной крошки - считаются не валидными для включения в sitemap (на Ersatz сейчас<br>"
                                     "таким образом выводятся аксессуары, поэтому для проверки Ersatz нет необходимости указывать URL категории аксессуаров)</p><br>")

        # Copyright layer
        self.copyright_layer.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.copyright_label.setText("<p style='font-size: 10px;'>Если, что-то не работает, возникли пожелания, предложения пишите <a href='mailto:s.baston@autodoc.eu'>s.baston@autodoc.eu</a> "
                                     "или в слаке Sergey Baston</p><center>© Sergey Baston 2023</center>")

