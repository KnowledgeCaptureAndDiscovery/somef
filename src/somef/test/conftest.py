import pytest
from somef.parser import pom_xml_parser

@pytest.fixture(autouse=True)
def reset_pom_parser_state():
    # print("\n[DEBUG] Resetting pom_xml_parser...")
    pom_xml_parser.processed_pom = False