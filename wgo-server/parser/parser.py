from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from data.db_models import Event


class BaseParser(ABC):
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url

    @abstractmethod
    def parse(self, file_path: str) -> list[Event]:
        pass


class HTMLParser(BaseParser):
    def _load(self, file_path: str) -> BeautifulSoup:
        with open(file_path, "r", encoding="utf-8") as f:
            return BeautifulSoup(f, "lxml")
