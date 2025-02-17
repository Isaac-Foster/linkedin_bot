from os import getenv
from pathlib import Path
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Vars:
    LOGIN: str = getenv("login")
    PASSWD: str = getenv("passwd")
    ROOT_PATH: str = Path(__file__).parent.parent
    DIR_NAME: str = getenv("dir_name")
    SEARCH: str = getenv("search")
    MODE: int = int(getenv("mode"))
    TEMPLATE: str = getenv("template")
    QUERY_ATTR_VALUE = ""

    def __post_init__(self):
        if not self.DIR_NAME or self.DIR_NAME == "":
            self.DIR_NAME = (
                self.LOGIN.split("@")[0].replace(".","_").
                replace("-","")
            )
        self.TEMPLATE = self.TEMPLATE.strip()

        if self.MODE == 1 or self.MODE == 2:
            self.QUERY_ATTR_VALUE = "Pesquisar"
        
        if self.MODE == 3:
            self.QUERY_ATTR_VALUE = "Pesquisar cargo, competência ou empresa"

VARS = Vars()