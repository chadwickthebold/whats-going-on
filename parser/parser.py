from bs4 import BeautifulSoup

class BaseParser:
    """
    A parsing interface
    """

    def __init__(self) -> None:
        self.data = {}

class HTMLParser(BaseParser):
    """
    A parser with HTML convenience methods
    """