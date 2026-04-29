from bs4 import BeautifulSoup

TESTFILE_PATH = 'references/sites/drawingcenter_2.html'

html_doc = open(TESTFILE_PATH, 'r', encoding="utf-8")

drawing_soup = BeautifulSoup(html_doc, 'lxml')

"""
TODO Need a class for this
"""
scrape_result = {
    "upcoming": [],
    "passed": []
}

title = drawing_soup.title

if title:
    print(title.string)

onview_section = drawing_soup.find(id='onview')

"""
TODO figure out how to avoid pylance warnings for accessing NoneType objects from bs4 searches
"""
if onview_section:
    onview_exhibits = onview_section.find_all(class_='exhibit_module')

    for exhibit in onview_exhibits:

        """
        TODO add class for raw scraped exhibit data
        idea - each attempted parse of a new section should be wrapped in some safety block
        so that we can debug exactly where in the parse process we blew up
        e.g. if we structure the parse as
        [parse outer[parse inner 1, parse inner 2, parse inner 3[parse 3.1, 3.2]] we should
        be able to see if we failed at parent step, a child step, or a sibling step. And the parser
        Should gracefully recover from failures at each step. The overal parse process should attempt
        to parse what it can, and then leave data state normalization to another process
        """
        exhibit_data = {
            "time": exhibit.time['datetime'],
            "title": exhibit.h2.text.rstrip(),
            "href": exhibit.h2.find('a')['href']
        }
        scrape_result['upcoming'].append(exhibit_data)

print(scrape_result)