from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lxml import etree
import os
import webbrowser

def scrap_data():
    process = CrawlerProcess(get_project_settings())
    process.crawl('ostriv')
    process.crawl('fishing')
    process.start()


def task1():
    print("Task #1")
    root = etree.parse("task1.xml")
    pages = root.xpath("//fragment[@type='text']")
    print("Average number of text tags read from a page: %s" % ((len(pages))//20))


def task2():
    print("Task #2")
    transform = etree.XSLT(etree.parse("templateTask2.xsl"))
    result = transform(etree.parse("task2.xml"))
    result.write("task2.xhtml", pretty_print=True, encoding="UTF-8")
    webbrowser.open('file://' + os.path.realpath("task2.xhtml"))


if __name__ == '__main__':
    scrap_data() # Scrapping data from sites
    while True:
        print("/" * 50)
        print("Input number of task to execute, or anything else to exit:")
        print("1. Task#1: www.ostriv.in.ua")
        print("2. Task#2: www.fishing-mart.com.ua")
        print("> ", end='', flush=True)
        number = input()
        if number == "1":
            task1()
        elif number == "2":
            task2()
        else:
            break
    print("End of program")
