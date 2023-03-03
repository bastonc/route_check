import csv
import datetime
import re
import sys
import traceback
from time import sleep

import requests
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from PyQt5.QtWidgets import QMessageBox
from bs4 import BeautifulSoup

import const.const as const

def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    #import traceback
    text += ''.join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, 'Error', text)
    quit()
sys.excepthook = log_uncaught_exceptions


class CsvWorker(QObject):
    articles_list_signal = pyqtSignal(list)
    console = pyqtSignal(str)

    def __init__(self, csv_file_name):
        super(CsvWorker, self).__init__()
        self.csv_file_name = csv_file_name
        self.articles_list = []

    def get_article_from_scv(self):
        with open(self.csv_file_name, newline='') as csvfile:
            spamreader_dict = csv.DictReader(csvfile, ['article'])
            self.articles_list = [article['article'] for article in spamreader_dict if article is not None and str(article['article']).isdigit()]
        if len(self.articles_list) > 1:
            self.console.emit(f"- In CSV file found articleID (quantity){len(self.articles_list)} | First: {self.articles_list[0]}, Last {self.articles_list[-1]}")
            print(f"--> In CSV file found articleID (quantity){len(self.articles_list)} | First: {self.articles_list[0]}, Last {self.articles_list[-1]}")
            self.articles_list_signal.emit(self.articles_list)

class CheckRouteThread(QThread):

    finish_processing = pyqtSignal()
    console = pyqtSignal(str)

    def __init__(self,  csv_name, exclude_route, exclude_url_list, skin, class_name, output_csv_name, regex_pattern):
        super().__init__()
        self.exclude_route = exclude_route
        self.exclude_url_list = exclude_url_list
        self.csv_name = csv_name
        self.article_url_list = None
        self.skin = skin
        self.exclude_route_list = exclude_route
        self.class_name = class_name
        self.output_csv_file = output_csv_name
        self.regex_pattern = regex_pattern

    def run(self):
        print("start")
        self.get_article_from_scv(self.csv_name)
        self.generate_url()
        self.processing_urls(self.article_url_list,
                             self.exclude_route_list,
                             self.class_name,
                             self.regex_pattern)

    def init_output_csv(self):
        self.save_to_report_file(type="init")

    def get_source_code(self, url, mob, redirect):
        while 1:
            try:
                response = requests.get(url, headers=const.MOBILE_HEADERS if mob else const.DESKTOP_HEADERS, allow_redirects=redirect)
                if response.status_code == 200:
                    return response
                print(f"Error! Bad status code ({response.status_code}) for {url}")
                return response
            except BaseException:
                print(f"Error conection. Try again for {url}")

    def get_route_name(self, source_code):
        search_string = source_code.find("routeName")
        if search_string == -1:
            return "No found routeName"
        route_string = ""
        i = 0
        flag = True
        quantity = 0
        while flag:
            cyr = search_string + i
            if source_code[cyr] != "\"":
                route_string += source_code[cyr]
            elif source_code[cyr] == "\"" and quantity != 2:
                quantity += 1
            elif source_code[cyr] == "\"" and quantity == 2:
                flag = False
            i += 1
        print(f"current route_string {route_string}")
        values = route_string.split(":")
        if len(values) > 1:
            return route_string.split(":")[1]
        return None

    def generate_url(self):
            url_prefix, url_postfix = self.skin.split("[]")
            # print(f"url prefix {url_prefix} url postfix {url_postfix}")
            self.article_url_list = [{article: f"{url_prefix}{article}{url_postfix}"} for article in self.articles_list]
    # https://www.autoteiledirekt.de/beru-1213.html

    def get_article_from_scv(self, csv_name):
        with open(csv_name, newline='') as csvfile:
            spamreader_dict = csv.DictReader(csvfile, ['article'])
            self.articles_list = [article['article'] for article in spamreader_dict if article is not None and str(article['article']).isdigit()]
        if len(self.articles_list) > 1:
            self.console.emit(f"- In CSV file found articleID (quantity){len(self.articles_list)} | First: {self.articles_list[0]}, Last {self.articles_list[-1]}")
            print(f"--> In CSV file found articleID (quantity){len(self.articles_list)} | First: {self.articles_list[0]}, Last {self.articles_list[-1]}")

    @staticmethod
    def check_breadcrumbs(source_code, exclude_url_list, name_class_bc):
        soup = BeautifulSoup(source_code, 'html.parser')
        all_a = soup.find_all("a", attrs={"class": name_class_bc})
        if len(all_a) <= 1:
            print("Breadcrumbs level <= 1")
            return True
        for a in all_a:
            if a.get("href") in exclude_url_list:
                return True
        return False

    def get_article_from_url(self, url, regex_pattern):
        print(f"URL: {url} regex: {regex_pattern}")
        article = None
        #print("re.search(p, url)", re.search("(?<=-)\d+(?=\.)", url))
        if re.search(regex_pattern, url) is not None:
            #print(re.search(p, url))
            for catch in re.finditer(regex_pattern, url):
                print("catch", catch)
                article = str(catch[0]).replace(".", "").replace("-", "")
        print(f"article: {article}")
        return article

    def processing_urls(self, url_list, route_list, class_name_bc, regex_pattern):
        num = 0

        for url_dict in url_list:
            route_name = None
            for article, url in url_dict.items():
                num += 1
                source_code = self.get_source_code(url, False, True)
                if source_code.status_code == 200:
                    route_name = self.get_route_name(source_code.text)
                    if route_name not in self.exclude_route and len(source_code.history) > 0 and  self.get_article_from_url(source_code.history[0].url, self.regex_pattern) != self.get_article_from_url(source_code.url,
                                                                                                                              self.regex_pattern):
                        route_name += f" - 301 to {self.get_article_from_url(source_code.url, self.regex_pattern) if self.get_article_from_url(source_code.url, self.regex_pattern) is not None else route_name}"
                    if route_name not in self.exclude_route and not self.check_breadcrumbs(source_code.text, self.exclude_url_list, class_name_bc):
                            route_name += " - bad"
                    self.save_to_report_file(type="append", matches_dict={article: route_name})
                else:
                    self.save_to_report_file(type="append", matches_dict={article: source_code.status_code})

                self.console.emit(f"# {num} {datetime.datetime.now().strftime('%m-%d %H:%M:%S')} Article {article} route:{route_name}")
                print(f"# {num: 5} {datetime.datetime.now().strftime('%m-%d %H:%M:%S')} Article {article} route:{route_name}")
                sleep(0.5)
        print("Finish_process")
        self.finish_processing.emit()

    def save_to_report_file(self, type, matches_dict={}):
        if type == "append":
            with open(self.output_csv_file, "a", newline='') as csvfile:
                fieldnames = ['ArticleID', 'Route']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                for articleID, route in matches_dict.items():
                        writer.writerow({"ArticleID": articleID, "Route": route})
        elif type == "init":
            with open(self.output_csv_file, "w", newline='') as csvfile:
                fieldnames = ['ArticleID', 'Route']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()


class CheckerRouteThread(QThread):

    finish_processing = pyqtSignal(object)
    console = pyqtSignal(str)

    def __init__(self,  articles_list, exclude_route, exclude_url_list, skin, class_name, output_csv_name, regex_pattern):
        super().__init__()
        self.exclude_route = exclude_route
        self.exclude_url_list = exclude_url_list
        self.articles_list = articles_list
        self.article_url_list = None
        self.skin = skin
        self.exclude_route_list = exclude_route
        self.class_name = class_name
        self.output_csv_file = output_csv_name
        self.regex_pattern = regex_pattern

    def run(self):
        print("start")
        self.generate_url()
        self.processing_urls(self.article_url_list,
                             self.exclude_route_list,
                             self.class_name,
                             self.regex_pattern)

    def init_output_csv(self):
        self.save_to_report_file(type="init")

    def get_source_code(self, url, mob, redirect):
        while 1:
            try:
                response = requests.get(url, headers=const.MOBILE_HEADERS if mob else const.DESKTOP_HEADERS, allow_redirects=redirect)
                if response.status_code == 200:
                    return response
                print(f"Error! Bad status code ({response.status_code}) for {url}")
                return response
            except BaseException:
                print(f"Error conection. Try again for {url}")

    def get_route_name(self, source_code):
        search_string = source_code.find("routeName")
        if search_string == -1:
            return "No found routeName"
        route_string = ""
        i = 0
        flag = True
        quantity = 0
        while flag:
            cyr = search_string + i
            if source_code[cyr] != "\"":
                route_string += source_code[cyr]
            elif source_code[cyr] == "\"" and quantity != 2:
                quantity += 1
            elif source_code[cyr] == "\"" and quantity == 2:
                flag = False
            i += 1
        print(f"current route_string {route_string}")
        values = route_string.split(":")
        if len(values) > 1:
            return route_string.split(":")[1]
        return None

    def generate_url(self):
            url_prefix, url_postfix = self.skin.split("[]")
            # print(f"url prefix {url_prefix} url postfix {url_postfix}")
            self.article_url_list = [{article: f"{url_prefix}{article}{url_postfix}"} for article in self.articles_list]
    # https://www.autoteiledirekt.de/beru-1213.html

    @staticmethod
    def check_breadcrumbs(source_code, exclude_url_list, name_class_bc):
        soup = BeautifulSoup(source_code, 'html.parser')
        all_a = soup.find_all("a", attrs={"class": name_class_bc})
        if len(all_a) <= 1:
            print("Breadcrumbs level <= 1")
            return True
        for a in all_a:
            if a.get("href") in exclude_url_list:
                return True
        return False

    def get_article_from_url(self, url, regex_pattern):
        print(f"URL: {url} regex: {regex_pattern}")
        article = None
        #print("re.search(p, url)", re.search("(?<=-)\d+(?=\.)", url))
        if re.search(regex_pattern, url) is not None:
            #print(re.search(p, url))
            for catch in re.finditer(regex_pattern, url):
                print("catch", catch)
                article = str(catch[0]).replace(".", "").replace("-", "")
        print(f"article: {article}")
        return article

    def processing_urls(self, url_list, route_list, class_name_bc, regex_pattern):
        num = 0

        for url_dict in url_list:
            route_name = None
            for article, url in url_dict.items():
                num += 1
                source_code = self.get_source_code(url, False, True)
                if source_code.status_code == 200:
                    route_name = self.get_route_name(source_code.text)
                    if route_name not in self.exclude_route and len(source_code.history) > 0 and  self.get_article_from_url(source_code.history[0].url, self.regex_pattern) != self.get_article_from_url(source_code.url,
                                                                                                                              self.regex_pattern):
                        route_name += f" - 301 to {self.get_article_from_url(source_code.url, self.regex_pattern) if self.get_article_from_url(source_code.url, self.regex_pattern) is not None else route_name}"
                    if route_name not in self.exclude_route and not self.check_breadcrumbs(source_code.text, self.exclude_url_list, class_name_bc):
                            route_name += " - bad"
                    self.save_to_report_file(type="append", matches_dict={article: route_name})
                else:
                    self.save_to_report_file(type="append", matches_dict={article: source_code.status_code})

                self.console.emit(f"Thread{id(self)}# {num} {datetime.datetime.now().strftime('%m-%d %H:%M:%S')} Article {article} route:{route_name}")
                print(f"# {num: 5} {datetime.datetime.now().strftime('%m-%d %H:%M:%S')} Article {article} route:{route_name}")
                sleep(0.5)
        print("Finish_process")
        self.finish_processing.emit((id(self), self))

    def save_to_report_file(self, type, matches_dict={}):
        if type == "append":
            with open(self.output_csv_file, "a", newline='') as csvfile:
                fieldnames = ['ArticleID', 'Route']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                for articleID, route in matches_dict.items():
                        writer.writerow({"ArticleID": articleID, "Route": route})
        elif type == "init":
            with open(self.output_csv_file, "w", newline='') as csvfile:
                fieldnames = ['ArticleID', 'Route']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()



# if __name__ == "__main__":
#     exclude_url_list = ["https://www.autoteiledirekt.de/werkzeuge.html",
#                         "https://www.autoteiledirekt.de/autozubehoer.html",
#                         "https://www.autoteiledirekt.de/chemie-und-pflege.html"]
#     skin = "https://www.autoersatzteile.de/[]-motul"
#     check_thread = CheckRouteThread(csv_name="route_product_Direct.csv",
#                                     exclude_url_list=exclude_url_list,
#                                     skin=skin,
#                                     found_route="product",
#                                     class_name="breadcrumbs__item",
#                                     output_csv_name="result.csv")
#     check_thread.start_analyze()
