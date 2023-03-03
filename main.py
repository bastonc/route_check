import datetime
import gzip
import re
import csv
from time import sleep

import pandas as pd

import requests as requests
import xmltodict as xmltodict
import xml.etree.ElementTree as ET


# Get Sitemap

def get_url_from_sitemap(url_header, directory_sitemap):
    pattern = '(.*?)\/'
    max_subsitemaps_crawl = 50
    file_names_list = []
    res = requests.get(url_header)
    raw_data = xmltodict.parse(res.text)
    df_sitemap = pd.DataFrame({'loc': []})
    print("--> Download sitemap files")
    for i, r in enumerate(raw_data["sitemapindex"]["sitemap"], start=1):
        file_name = f"item-{i}"
        print(r["loc"])
        res_single_sitemap = requests.get(r["loc"], stream=True)
        if res_single_sitemap.status_code == 200:
            data = gzip.decompress(res_single_sitemap.content)
            with open(f"{directory_sitemap}/{file_name}.xml", 'w') as f:
                f.write(data.decode('utf-8'))
            file_names_list.append(file_name)
    return file_names_list


def get_all_links_from_xml(sitemaps_name_list, directory_sitemap):
    files_content = {}
    for file in sitemaps_name_list:
        with open(f"{directory_sitemap}/{file}.xml", "r") as f:
            raw_xml = xmltodict.parse(f.read())
            urls = [elem["loc"] for elem in raw_xml["urlset"]["url"]]
            files_content.update({file: urls})
    return files_content


def get_article_id(links_dict, reg_pattern):
    articles_id_dict = {}
    for parent, links_list in links_dict.items():
        articles_id_list = []
        for link in links_list:
            p = reg_pattern
                #"(?<=-)\d+(?=\.)"
                #'-[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'

            if re.search(p, link) is not None:
                for catch in re.finditer(p, link):
                    articles_id_list.append(str(catch[0]).replace(".", "").replace("-", ""))  # match save in list
        articles_id_dict.update({parent: articles_id_list})
        print(f"--> ArticleID in {parent} file (quantity): {len(articles_id_list)}")
    return articles_id_dict


def get_article_from_csv(csv_name):
    with open( csv_name, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        article_id = [row[0] for row in spamreader if row is not None and str(row[0]).isdigit()]
    if len(article_id) > 1:
        print(f"--> In CSV file found articleID (quantity){len(article_id)} | First: {article_id[0]}, Last {article_id[-1]}")
    return article_id

def compare_articles(articles_from_sitemap_dict: dict, articles_from_csv: list):
    noindex_url_in_sitemap_dict = {}
    matches = []
    for parent, articles_from_sitemap_list in articles_from_sitemap_dict.items():
        print(f"\n--> Processing {parent} sitemap")
        matches_set = set(articles_from_csv).intersection(articles_from_sitemap_list)
        matches_list = list(matches_set)
        # matches = [found_article for found_article in articles_from_csv if str(found_article) in articles_from_sitemap_list]
        print(f"---> Found matches: {len(matches_list)} in {parent} sitemap file (all matches in report file)")
        #print({parent: matches_list})
        save_to_report_file("match", {parent: matches_list})
        # print(len(articles_from_csv))
        diff_csv_set = set(articles_from_csv) - matches_set
        articles_from_csv = list(diff_csv_set)
        print(f"---> Articles in CSV left: {len(articles_from_csv)}")
        diff_articles_sitemap = set(articles_from_sitemap_list) - matches_set
        print(f"---> Articles noindex in sitemap {len(diff_articles_sitemap)}")
        if len(diff_articles_sitemap) != 0:
            noindex_url_in_sitemap_dict.update({parent: diff_articles_sitemap})
            print(f"Noindeх articles:{diff_articles_sitemap}", "\n"*2, articles_from_sitemap_list, "\n"*2)


    #     for match in matches_list:
    #     #     print(".", end="\r")
    #          while match in articles_from_csv:
    #              articles_from_csv.remove(match)
    #          while match in articles_from_sitemap_list:
    #              articles_from_sitemap_list.remove(match)
    #     if articles_from_sitemap_list is not None:
    #          noindex_url_in_sitemap_dict.update({parent: articles_from_sitemap_list})
    # if articles_from_csv is not None:
    #     save_to_report_file("Not in sitemaps", articles_from_csv)
    if articles_from_csv:
        print(f"--> Not found in sitemaps: {len(articles_from_csv)} \n{articles_from_csv}")
        save_to_report_file("not_found", {"--": articles_from_csv})
    if noindex_url_in_sitemap_dict != {}:
        print("--> Noindex found in sitemaps:")
        for parent, url_list in noindex_url_in_sitemap_dict.items():
            print(f"\tFile sitemap: {parent}")
            for url in url_list:
                print(f"\t\tURL: {url}")
        save_to_report_file("noindex", noindex_url_in_sitemap_dict)
       # print(noindex_url_in_sitemap_dict)

def save_to_report_file(type, matches_dict):
    if type == "match":
        with open(f"matches.csv", "a", newline='') as csvfile:
            fieldnames = ['ArticleID', 'in Sitemap']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # writer.writeheader()
            for parent, articles_list in matches_dict.items():
                for articles in articles_list:
                    writer.writerow({"ArticleID": articles, "in Sitemap": parent})
    elif type == "noindex":
        with open(f"noindex.csv", "a", newline='') as csvfile:
            fieldnames = ['ArticleID', 'in Sitemap']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
           # writer.writeheader()
            for parent, articles_list in matches_dict.items():
                for articles in articles_list:
                    writer.writerow({"ArticleID": articles, "in Sitemap": parent})
    elif type == "not_found":
        with open(f"not-found.csv", "a", newline='') as csvfile:
            fieldnames = ['ArticleID', 'in Sitemap']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # writer.writeheader()
            for parent, articles_list in matches_dict.items():
                for articles in articles_list:
                    writer.writerow({"ArticleID": articles, "in Sitemap": parent})

            #article_id = str(link).findall(r'\d+')

    #
    #         print(res_single_sitemap.headers['Content-Type'])
    #         if res_single_sitemap.headers['Content-Type'] == 'application/gzip':
    #             res_single_sitemap.raw.decode_content = True
    #             res_single_sitemap = gzip.GzipFile(fileobj=res_single_sitemap.raw)
    #
    #         else:
    #             res_single_sitemap = res_single_sitemap.text
    #         # xml_content = resSingle
    #
    #         raw_single = xmltodict.parse(res_single_sitemap)
    #         # print(rawSingle)
    #         data_single = [[r_single["loc"]] for r_single in raw_single["urlset"]["url"]]
    #         df_single = pd.DataFrame(data_single, columns=["loc"])
    #         df_sitemap = pd.concat([df_sitemap, df_single])
    #         print(len(df_sitemap))
    #
    #     # except:
    #     #     print("something went wrong at: " + r["loc"])
    #
    #     breakcounter += 1
    #     if breakcounter == max_subsitemaps_crawl:
    #         break
    #     sleep(1)
    # return df_sitemap

if __name__ == "__main__":
    # directory_sitemap = "sitemaps_direkt"
    # url_headers = "https://www.autoteiledirekt.de/sitemap/F5BF48AA40CAD7891EB709FCF1FDE128/item-index.xml"
    # regex_pattern = "(?<=-)\d+(?=\.)"
    # csv_name = "dir.csv"
    # ------
    directory_sitemap = "sitemaps_ersatz"
    url_headers = "https://www.autoersatzteile.de/sitemap/F5BF48AA40CAD7891EB709FCF1FDE128/item-index.xml"
    regex_pattern = "(?<=\/)\d+(?=-)"
    csv_name = "ers.csv"

    sitemaps_name_list = get_url_from_sitemap(url_headers, directory_sitemap) # download all sitemaps from server
    # sitemaps_name_list = ["item-1", "item-2"]
    links_in_sitemap_dict = get_all_links_from_xml(sitemaps_name_list, directory_sitemap)  # Get all links in sitemaps files
    articles_from_sitemaps = get_article_id(links_in_sitemap_dict, regex_pattern)  # Get clean articles from urls
    articles_from_csv = get_article_from_csv(csv_name)  # get all articles from csv
    compare_articles(articles_from_sitemaps, articles_from_csv)

    #print(sitemaps_name_list)

    #url = 'https://www.autoteiledirekt.de/sitemap/F5BF48AA40CAD7891EB709FCF1FDE128/item-index.xml'


# urls_in_sitemaps = [url for url in dfSitemap['loc']]