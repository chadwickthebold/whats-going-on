from bs4 import BeautifulSoup

TESTFILE_PATH = 'references/sites/drawingcenter_2.html'

html_doc = open(TESTFILE_PATH, 'r', encoding="utf-8")

drawing_soup = BeautifulSoup(html_doc, 'lxml')

print(drawing_soup.title)