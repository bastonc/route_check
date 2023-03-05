import csv
import datetime
import re
from time import sleep

import requests
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from bs4 import BeautifulSoup

import const.const as const


class CsvWorker(QObject):
    articles_list_signal = pyqtSignal(list)
    console_message = pyqtSignal(str)

    def __init__(self, csv_file_name):
        super(CsvWorker, self).__init__()
        self.csv_file_name = csv_file_name
        self.articles_list = []

    def get_article_from_scv(self):
        with open(self.csv_file_name, newline='') as csvfile:
            spamreader_dict = csv.DictReader(csvfile, ['article'])
            self.articles_list = [article['article'] for article in spamreader_dict if article is not None and str(article['article']).isdigit()]
        if len(self.articles_list) > 1:
            self.console_message.emit(f"- In CSV file found articleID (quantity){len(self.articles_list)} | First: {self.articles_list[0]}, Last {self.articles_list[-1]}")
            self.articles_list_signal.emit(self.articles_list)


class OutputCsv(QObject):

    def __init__(self, name_output_csv):
        super().__init__()
        self.name_output_csv = name_output_csv

    def init_output_csv(self):
        with open(self.name_output_csv, "w", newline='') as csvfile:
            fieldnames = ['ArticleID', 'Route']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    def save_to_report_file(self, matches_dict={}):
        with open(self.name_output_csv, "a", newline='') as csvfile:
            fieldnames = ['ArticleID', 'Route']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for articleID, route in matches_dict.items():
                writer.writerow({"ArticleID": articleID, "Route": route})


class CheckerRouteThread(QThread):

    finish_processing = pyqtSignal(object)
    console = pyqtSignal(str)
    console_message = pyqtSignal(str)

    def __init__(self,
                 articles_list: list,
                 exclude_route: list,
                 exclude_url_list: list,
                 skin: str,
                 class_name: str,
                 output_csv_name: str,
                 regex_pattern: str,
                 output_to_csv: classmethod):
        super().__init__()
        self.exclude_route = exclude_route
        self.exclude_url_list = [str(url).replace("https://new.", "").replace("https://www.", "").replace("https://m.", "") for url in exclude_url_list]
        self.articles_list = articles_list
        self.article_url_list = None
        self.skin = skin
        self.exclude_route_list = exclude_route
        self.class_name = class_name
        self.output_csv_file = output_csv_name
        self.regex_pattern = regex_pattern
        self.output_to_csv = output_to_csv

    def run(self):
        self.generate_url()
        self.processing_urls(self.article_url_list, self.class_name)

    def get_source_code(self, url, mob, redirect):
        while 1:
            try:
                response = requests.get(url, headers=const.MOBILE_HEADERS if mob else const.DESKTOP_HEADERS, allow_redirects=redirect)
                if response.status_code == 200:
                    return response
                return response
            except BaseException:
                self.console_message.emit(f"ERROR CONNECTION TO  {url}. Retrying the connection...")

    @staticmethod
    def get_route_name(source_code):
        search_string = source_code.find("routeName")
        if search_string == -1:
            return "No found routeName"
        route_string = ""
        i = 0
        flag = True
        quantity = 0
        while flag:
            pointer_symbol = search_string + i
            if source_code[pointer_symbol] != "\"":
                route_string += source_code[pointer_symbol]
            elif source_code[pointer_symbol] == "\"" and quantity != 2:
                quantity += 1
            elif source_code[pointer_symbol] == "\"" and quantity == 2:
                flag = False
            i += 1
        values = route_string.split(":")
        if len(values) > 1:
            return route_string.split(":")[1]
        return None

    def generate_url(self):
        url_prefix, url_postfix = self.skin.split("[]")
        self.article_url_list = [{article: f"{url_prefix}{article}{url_postfix}"} for article in self.articles_list]

    def check_breadcrumbs(self, source_code, exclude_url_list, name_class_bc):
        all_bc_link = self.get_breadcrumbs_links(source_code, name_class_bc)
        if len(all_bc_link) <= 1:
            return True
        for a in all_bc_link:
            if str(a.get("href")).replace("https://new.","").replace("https://www.","").replace("https://m.", "") in exclude_url_list:
                return True
        return False

    @staticmethod
    def get_breadcrumbs_links(source_code, name_class_bc):
        soup = BeautifulSoup(source_code, 'html.parser')
        all_link = soup.find_all("a", attrs={"class": name_class_bc})
        return all_link

    @staticmethod
    def get_article_from_url(url, regex_pattern):
        article = None
        if re.search(regex_pattern, url) is not None:
            for catch in re.finditer(regex_pattern, url):
                article = str(catch[0]).replace(".", "").replace("-", "")
        return article

    def processing_urls(self, url_list, class_name_bc):
        num = 0
        for url_dict in url_list:
            route_name = None
            for article, url in url_dict.items():
                num += 1
                redirect = False
                source_code = self.get_source_code(url, False, True)
                if source_code.status_code == 200:
                    route_name = self.get_route_name(source_code.text)
                    if route_name not in self.exclude_route and len(source_code.history) > 0 and  self.get_article_from_url(source_code.history[0].url, self.regex_pattern) != self.get_article_from_url(source_code.url,
                                                                                                                              self.regex_pattern):
                        route_name += f" 301 to {self.get_article_from_url(source_code.url, self.regex_pattern) if self.get_article_from_url(source_code.url, self.regex_pattern) is not None else route_name}"
                        redirect = True
                    if route_name not in self.exclude_route and \
                            not self.check_breadcrumbs(source_code.text, self.exclude_url_list, class_name_bc) and \
                            not redirect:
                        route_name += " valid"
                    self.output_to_csv(matches_dict={article: route_name})
                else:
                    self.output_to_csv(matches_dict={article: source_code.status_code})
                self.console.emit(f"(Thread: {id(self)}) {datetime.datetime.now().strftime('%d-%m %H:%M:%S')} Article {article} route:{route_name}")
                sleep(0.5)
        self.finish_processing.emit((id(self), self))
