import csv
import gzip
import os
import re

import pandas as pd
import requests
import xmltodict


class Sitemap_check(object):

    def __init__(self, head_url, regex_pattern, articles_filename, name_project):
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
            print(f"Directory {self.name_project} already exist")
        for file in self.report_file_list:
            with open(f"{self.name_project}/{file}.csv", "w", newline='') as csvfile:
                fieldnames = ['ArticleID', 'in Sitemap']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

    def download_sitemaps(self):
        self.download_child_sitemap()

    def start_analyze(self):
        self.get_all_sitemaps_filename()
        self.get_all_links_from_xml()
        self.get_article_id()
        self.get_article_from_csv()
        self.compare_articles()

    def get_all_sitemaps_filename(self):
        files = os.listdir(f"{self.name_project}/sitemaps")
        sorted(files)
        self.sitemap_files_list = [str(file).replace(".xml", "") for file in files]


    def download_child_sitemap(self):
        res = requests.get(self.head_url)
        raw_data = xmltodict.parse(res.text)
        print("--> Download sitemap files")
        for i, r in enumerate(raw_data["sitemapindex"]["sitemap"], start=1):
            file_name = f"item-{i}"
            print(r["loc"])
            res_single_sitemap = requests.get(r["loc"], stream=True)
            if res_single_sitemap.status_code == 200:
                data = gzip.decompress(res_single_sitemap.content)
                with open(f"{self.name_project}/sitemaps/{file_name}.xml", 'w') as f:
                    f.write(data.decode('utf-8'))
                #self.sitemap_files_list.append(file_name)

    def get_all_links_from_xml(self):
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
                # "(?<=-)\d+(?=\.)"
                # '-[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
                if re.search(p, link) is not None:
                    for catch in re.finditer(p, link):
                        articles_in_sitemaps.append(str(catch[0]).replace(".", "").replace("-", ""))  # match save in list
                        self.articles_in_sitemaps = articles_in_sitemaps
            self.articles_sitemaps_dict.update({parent: self.articles_in_sitemaps})
            print(f"--> ArticleID in {parent} file (quantity): {len(articles_in_sitemaps)}")

    def get_article_from_csv(self):
        with open(self.articles_filename, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            self.articles_in_csv = [row[0] for row in spamreader if row is not None and str(row[0]).isdigit()]
        if len(self.articles_in_csv) > 1:
            print(f"--> In CSV file found articleID (quantity){len(self.articles_in_csv)} | First: {self.articles_in_csv[0]}, Last {self.articles_in_csv[-1]}")

    def compare_articles(self):
        for parent, articles_from_sitemap_list in self.articles_sitemaps_dict.items():
            print(f"\n--> Processing {parent} sitemap")
            matches_set = set(self.articles_in_csv).intersection(articles_from_sitemap_list)
            print(f"---> Found matches: {len(matches_set)} in {parent} sitemap file (all matches in report file)")
            self.save_to_report_file("match", {parent: matches_set})
            article_in_csv_left = set(self.articles_in_csv) - matches_set
            self.articles_in_csv = list(article_in_csv_left)
            print(f"---> Articles in CSV left: {len(self.articles_in_csv)}")
            diff_articles_sitemap = set(articles_from_sitemap_list) - matches_set
            print(f"---> Articles noindex in sitemap {len(diff_articles_sitemap)}")
            if len(diff_articles_sitemap) != 0:
                self.noindex_url_in_sitemap_dict.update({parent: diff_articles_sitemap})
                print(f"Noindeх articles added to output report file")
        if self.articles_in_csv:
            print(f"--> Not found in sitemaps: {len(self.articles_in_csv)} (added to output report file)")
            self.save_to_report_file("not_found", {"--": self.articles_in_csv})
        if self.noindex_url_in_sitemap_dict != {}:
            print("--> Noindex found in sitemaps (added to output report file):")
            self.save_to_report_file("noindex", self.noindex_url_in_sitemap_dict)

    def save_to_report_file(self, type, matches_dict):
        if type == "match":
            with open(f"{self.name_project}/{self.report_file_list[0]}.csv", "a", newline='') as csvfile:
                fieldnames = ['ArticleID', 'in Sitemap']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                # writer.writeheader()
                for parent, articles_list in matches_dict.items():
                    for articles in articles_list:
                        writer.writerow({"ArticleID": articles, "in Sitemap": parent})
        elif type == "noindex":
            with open(f"{self.name_project}/{self.report_file_list[2]}.csv", "a", newline='') as csvfile:
                fieldnames = ['ArticleID', 'in Sitemap']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                # writer.writeheader()
                for parent, articles_list in matches_dict.items():
                    for articles in articles_list:
                        writer.writerow({"ArticleID": articles, "in Sitemap": parent})
        elif type == "not_found":
            with open(f"{self.name_project}/{self.report_file_list[1]}.csv", "a", newline='') as csvfile:
                fieldnames = ['ArticleID', 'in Sitemap']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                # writer.writeheader()
                for parent, articles_list in matches_dict.items():
                    for articles in articles_list:
                        writer.writerow({"ArticleID": articles, "in Sitemap": parent})

if __name__ == "__main__":
    directory_sitemap = "sitemaps_ersatz"
    url_headers = "https://www.autoersatzteile.de/sitemap/F5BF48AA40CAD7891EB709FCF1FDE128/item-index.xml"
    regex_pattern = "(?<=\/)\d+(?=-)"
    csv_name = "ers.csv"
    download = False
    sitemap_check = Sitemap_check(head_url=url_headers, regex_pattern=regex_pattern, articles_filename=csv_name, name_project="ersatz")
    if download:
        sitemap_check.download_sitemaps()
    sitemap_check.start_analyze()
