import csv
import gzip
import os
import re

import requests
import xmltodict
from PyQt5.QtCore import QThread, pyqtSignal


class Sitemap_check(QThread):
    console_message = pyqtSignal(str)
    finish_flag = pyqtSignal()
    stop_exception = pyqtSignal(str)

    def __init__(self, head_url, regex_pattern, articles_filename, name_project):
        super().__init__()
        self.head_url = head_url
        self.regex_pattern = regex_pattern
        self.articles_filename = articles_filename
        self.name_project = name_project
        self.report_file_list = ["match", "not_found", "noindex"]
        self.sitemap_files_list = []
        self.urls_in_sitemap = {}
        self.articles_sitemaps_dict = {}  # All articlesID in all sitemaps. Key is a parent file
        self.articles_in_sitemaps = []
        self.articles_in_csv = []
        self.noindex_url_in_sitemap_dict = {}
        self.init_report_file()

    def init_report_file(self):
        try:
            os.makedirs(f"{self.name_project}/sitemaps")
        except OSError:
            self.console_message.emit(f"Directory {self.name_project} already exist")
            # print(f"Directory {self.name_project} already exist")

        for file in self.report_file_list:
            with open(f"{self.name_project}/{file}.csv", "w", newline='') as csvfile:
                fieldnames = ['ArticleID', 'in Sitemap']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

    def run(self):
        self.download_child_sitemap()
        self.get_all_links_from_xml()
        self.get_article_id()
        self.get_article_from_csv()
        self.compare_articles()

    # def get_all_sitemaps_filename(self):
    #     files = os.listdir(f"{self.name_project}/sitemaps")
    #     sorted(files)
    #     self.sitemap_files_list = [str(file).replace(".xml", "") for file in files]

    def download_child_sitemap(self):
        self.console_message.emit("- Download sitemap files")
        # print("- Download sitemap files")
        try:
            res = requests.get(self.head_url)
            if res.status_code == 200:
                raw_data = xmltodict.parse(res.text)
            else:
                self.console_message.emit(f"- ERROR status code header sitemap {res.status_code}")
        except BaseException:
            # print("- ERROR connection check URL header sitemap or internet connection")
            self.stop_exception.emit("Check connection")
            self.sleep(1)
            self.terminate()

        for i, r in enumerate(raw_data["sitemapindex"]["sitemap"], start=1):
            file_name = f"item-{i}"
            self.console_message.emit(f" - {r['loc']}")
            # print(r["loc"])
            res_single_sitemap = requests.get(r["loc"], stream=True)
            if res_single_sitemap.status_code == 200:
                data = gzip.decompress(res_single_sitemap.content)
                with open(f"{self.name_project}/sitemaps/{file_name}.xml", 'w') as f:
                    f.write(data.decode('utf-8'))
                self.sitemap_files_list.append(file_name)

    def get_all_links_from_xml(self):
        self.console_message.emit(f"Reading URLs from sitemaps\nWait...\n")
        for file in self.sitemap_files_list:
            with open(f"{self.name_project}/sitemaps/{file}.xml", "r") as f:
                raw_xml = xmltodict.parse(f.read())
                urls = [elem["loc"] for elem in raw_xml["urlset"]["url"]]
                self.urls_in_sitemap.update({file: urls})

    def get_article_id(self):
        for parent, links_list in self.urls_in_sitemap.items():
            articles_in_sitemaps = []
            for link in links_list:
                p = self.regex_pattern
                if re.search(p, link) is not None:
                    for catch in re.finditer(p, link):
                        articles_in_sitemaps.append(str(catch[0]).replace(".", "").replace("-", ""))  # match save in list
                        self.articles_in_sitemaps = articles_in_sitemaps
            self.articles_sitemaps_dict.update({parent: self.articles_in_sitemaps})
            self.console_message.emit(f"- ArticleID in {parent} file (quantity): {len(articles_in_sitemaps)}")
            # print(f"--> ArticleID in {parent} file (quantity): {len(articles_in_sitemaps)}")

    def get_article_from_csv(self):
        with open(self.articles_filename, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            self.articles_in_csv = [row[0] for row in spamreader if row is not None and str(row[0]).isdigit()]
        if len(self.articles_in_csv) > 1:
            self.console_message.emit(f"\n- In CSV file found articleID (quantity){len(self.articles_in_csv)} | First: {self.articles_in_csv[0]}, Last {self.articles_in_csv[-1]}\n")
            # print(f"--> In CSV file found articleID (quantity){len(self.articles_in_csv)} | First: {self.articles_in_csv[0]}, Last {self.articles_in_csv[-1]}")

    def compare_articles(self):
        for parent, articles_from_sitemap_list in self.articles_sitemaps_dict.items():
            self.console_message.emit(f"- Processing {parent} sitemap")
            # print(f"\n--> Processing {parent} sitemap")
            matches_set = set(self.articles_in_csv).intersection(articles_from_sitemap_list)
            self.console_message.emit(f" - Found matches: {len(matches_set)} in {parent} sitemap file (all matches in report file)")
            # print(f"---> Found matches: {len(matches_set)} in {parent} sitemap file (all matches in report file)")
            self.save_to_report_file("match", {parent: matches_set})
            article_in_csv_left = set(self.articles_in_csv) - matches_set
            self.articles_in_csv = list(article_in_csv_left)
            self.console_message.emit(f" - Articles in CSV left: {len(self.articles_in_csv)}")
            # print(f"---> Articles in CSV left: {len(self.articles_in_csv)}")
            diff_articles_sitemap = set(articles_from_sitemap_list) - matches_set
            self.console_message.emit(f" - Articles noindex in sitemap {len(diff_articles_sitemap)}\n")
            # print(f"---> Articles noindex in sitemap {len(diff_articles_sitemap)}")
            if len(diff_articles_sitemap) != 0:
                self.noindex_url_in_sitemap_dict.update({parent: diff_articles_sitemap})
                self.console_message.emit(f"- Noindeх articles added to output report file")
                # print(f"Noindeх articles added to output report file")
        if self.articles_in_csv:
            self.console_message.emit(f"- Not found in sitemaps: {len(self.articles_in_csv)} (added to output report file)")
            # print(f"--> Not found in sitemaps: {len(self.articles_in_csv)} (added to output report file)")
            self.save_to_report_file("not_found", {"--": self.articles_in_csv})
        if self.noindex_url_in_sitemap_dict != {}:
            self.console_message.emit("- Noindex found in sitemaps (added to output report file):")
            # print("--> Noindex found in sitemaps (added to output report file):")
            self.save_to_report_file("noindex", self.noindex_url_in_sitemap_dict)
        self.finish_flag.emit()

    def save_to_report_file(self, type, matches_dict):
        if type == "match":
            with open(f"{self.name_project}/{self.report_file_list[0]}.csv", "a", newline='') as csvfile:
                fieldnames = ['ArticleID', 'in Sitemap']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                for parent, articles_list in matches_dict.items():
                    for articles in articles_list:
                        writer.writerow({"ArticleID": articles, "in Sitemap": parent})
        elif type == "noindex":
            with open(f"{self.name_project}/{self.report_file_list[2]}.csv", "a", newline='') as csvfile:
                fieldnames = ['ArticleID', 'in Sitemap']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                for parent, articles_list in matches_dict.items():
                    for articles in articles_list:
                        writer.writerow({"ArticleID": articles, "in Sitemap": parent})
        elif type == "not_found":
            with open(f"{self.name_project}/{self.report_file_list[1]}.csv", "a", newline='') as csvfile:
                fieldnames = ['ArticleID', 'in Sitemap']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                for parent, articles_list in matches_dict.items():
                    for articles in articles_list:
                        writer.writerow({"ArticleID": articles, "in Sitemap": parent})