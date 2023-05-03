import wikipedia, requests, argparse, logging , re, json, os
from bs4 import BeautifulSoup

def parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", help="указывайте заголовок страницы wikipedia", type=str)
    parser.add_argument("-d", help="указывате глубину вложенности страниц", type=int)
    page_title = parser.parse_args().p
    page_deep = parser.parse_args().d
    return page_title  if page_title else "Erdős number", \
           page_deep  if page_deep else 3


def is_valid(tag):
    return tag is not None \
        and tag.get("title") is not None


def get_links(url: str, prev_urls: set = set(), title: str = "Erdős number", data: list = [], deep: int = 3, counter = [0]):
    prev_urls.add(url)
    if deep != 0:
        counter[0] += 1
        logging.info(url)
        req_page = requests.get(url)
        bs = BeautifulSoup(req_page.content, "html.parser")
        tags_div = bs.find_all("div", id="mw-content-text", recursive=True)
        tags_a = tags_div[0].find_all("a", href=True)
        data.append({"title": title, "url": url, "members" : []})
        for tag in tags_a:
            if is_valid(tag) and re.search("^\/wiki\/.*", tag["href"]):
                url_join = "https://en.wikipedia.org" + tag["href"]
                if counter[0] == 1000:
                    break
                if url_join not in prev_urls:
                    get_links(url_join, prev_urls, tag["title"], data[-1]["members"], deep - 1, counter)
                else:
                    data[-1]["members"].append({"title": tag["title"], "url": url_join, "members" : []})
                    counter[0] += 1


def main():
    logging.basicConfig(level=logging.INFO)
    page_title, page_deep = parsing()
    data: list = []
    page = wikipedia.page(page_title)
    get_links(url=page.url, title=page_title, data=data, deep=page_deep)
    with open("wiki.json", "w") as file:
        file.write(json.dumps(data, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    try:
        main()
    except BaseException as e:
        logging.info(e)
