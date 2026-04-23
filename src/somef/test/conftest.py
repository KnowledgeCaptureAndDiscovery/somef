import pytest
from ..parser import pom_xml_parser

@pytest.fixture(autouse=True)
def reset_pom_parser_state():
    pom_xml_parser.processed_pom = False