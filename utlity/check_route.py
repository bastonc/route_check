import csv
import datetime
import re
from time import sleep

import requests
from bs4 import BeautifulSoup

import const.const as const


def get_source_code(url, mob, redirect):
    while 1:
        try:
            response = requests.get(url, headers=const.MOBILE_HEADERS if mob else const.DESKTOP_HEADERS, allow_redirects=redirect)
            if response.status_code == 200:
                return response
            print(f"Error! Bad status code ({response.status_code}) for {url}")
            return response
        except BaseException:
            print(f"Error conection. Try again for {url}")


def get_route_name(source_code):
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


def generate_url(articles_list):
        return [{article: f"https://new.autoteiledirekt.de/beru-{article}.html"} for article in articles_list]
# https://www.autoteiledirekt.de/beru-1213.html

def get_article_from_scv(csv_name):
    with open(csv_name, newline='') as csvfile:
        #spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        spamreader_dict = csv.DictReader(csvfile, ['article'])
        # for article in spamreader_dict:
        #     print(article['article'])
        article_id = [article['article'] for article in spamreader_dict if article is not None and str(article['article']).isdigit()]
    if len(article_id) > 1:
        print(f"--> In CSV file found articleID (quantity){len(article_id)} | First: {article_id[0]}, Last {article_id[-1]}")
    return article_id


def check_breadcrumbs(source_code, exclude_url_list, name_class_bc):
    soup = BeautifulSoup(source_code, 'html.parser')
    all_a = soup.find_all("a", attrs={"class": name_class_bc})
    #print(len(all_a), all_a)
    if len(all_a) <= 1:
        print("NO BC")
        return True
    for a in all_a:
        if a.get("href") in exclude_url_list:
           return True
    return False


def article_in_url(url, regex_pattern):
    p = regex_pattern
    if re.search(p, url) is not None:
        for catch in re.finditer(p, url):
            article = str(catch[0]).replace(".", "").replace("-", "")
    return article


def processing_urls(url_list, check_route_name, class_name_bc, regex_pattern):
    num = 0
    route_name = None
    for url_dict in url_list:
        for article, url in url_dict.items():
            num += 1
            source_code = get_source_code(url, False, True)
            if source_code.status_code == 200:
                route_name = get_route_name(source_code.text)
                if article_in_url(source_code.history[0].url, regex_pattern) != article_in_url(source_code.url,
                                                                                               regex_pattern):
                    route_name += " - 301"

            else:
                save_to_report_file(type="append", matches_dict={article: source_code.status_code})
            if route_name == check_route_name and not check_breadcrumbs(source_code.text,
                                                                        exclude_url_list,
                                                                        class_name_bc):
                route_name += " - bad"
            print(f"# {num} {datetime.datetime.now().strftime('%m-%d %H:%M:%S')} Article {article} route:{route_name}")
            save_to_report_file(type="append", matches_dict={article: route_name})
            # article_type.update({article: route_name})
            sleep(0.5)


def save_to_report_file(type, matches_dict={}):
    if type == "append":
        with open(f"result.csv", "a", newline='') as csvfile:
            fieldnames = ['ArticleID', 'Route']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for articleID, route in matches_dict.items():
                    writer.writerow({"ArticleID": articleID, "Route": route})
    elif type == "init":
        with open(f"result.csv", "w", newline='') as csvfile:
            fieldnames = ['ArticleID', 'Route']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()


if __name__=="__main__":
    # 18955661
    # https://www.autoersatzteile.de/18955661-motul
    #url = "https://new.autoersatzteile.de/18955661-motul"
    exclude_url_list = ["https://www.autoteiledirekt.de/werkzeuge.html", "https://www.autoteiledirekt.de/autozubehoer.html", "https://www.autoteiledirekt.de/chemie-und-pflege.html"]
    csv_name = "Direkt_bad.csv"
        # "route_product_Direct.csv"
    article_type = {}
    # save_to_report_file(type="init")
    articles_list = get_article_from_scv(csv_name)
    #print(articles_list)
    article_url_list = generate_url(articles_list)
    processing_urls(article_url_list, "product", "breadcrumbs__item", "(?<=-)\d+(?=\.)")



   # print(source_code.text)
