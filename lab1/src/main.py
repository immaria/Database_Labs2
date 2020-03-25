from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lxml import etree
import os
import webbrowser


def cleanup():
    try:
        os.remove("task1.xml")
        os.remove("task2.xml")
        os.remove("task2.xhtml")
    except OSError:
        pass


def scrap_data():
    process = CrawlerProcess(get_project_settings())
    process.crawl('kpi')
    process.crawl('rozetka')
    process.start()


def task1():
    print("- Task №1")
    root = etree.parse("task1.xml")
    pages = root.xpath("//page")
    print("Maximal number of text fragments for scrapped documents:")
    for page in pages:
        url = page.xpath("@url")[0]
        count = page.xpath("count(fragment[@type='text'])")
        print("%s: %d" % (url, count))


def task2():
    print("- Task №2")
    transform = etree.XSLT(etree.parse("task2.xsl"))
    result = transform(etree.parse("task2.xml"))
    result.write("task2.xhtml", pretty_print=True, encoding="UTF-8")
    print("XHTML page will be opened in web-browser...")
    webbrowser.open('file://' + os.path.realpath("task2.xhtml"))


if __name__ == '__main__':
    print("Laboratory work №1")
    print("--Cleaning files", end='', flush=True)
    cleanup()
    print("--Scrapping data from sites...", end='', flush=True)
    scrap_data()
    while True:
        print("-" * 70)
        print("---- To execute task input it's number (1 or 2), to exit - anything else")
        print("-- 1. Task № 1")
        print("-- 2. Task № 2")
        print("Your input: ", end='', flush=True)
        number = input()
        if number == "1":
            task1()
        elif number == "2":
            task2()
        else:
            break
    print("Exit")
