import unittest
from pathlib import Path
from .. parser import authors_parser

test_data_repositories = Path(__file__).parent / "test_data" / "authors_files"

class TestExtractAuthors(unittest.TestCase):

    def test_extract_authors_files(self):

        """This test checks if a file ot authors containing the correct values"""
        for file_path in test_data_repositories.glob("*"):
            str_authors = ""
            if file_path.is_file():
                file_name = file_path.stem  
                prefix = file_name.split("_AUTHORS")[0]

                with open(file_path, "r", encoding="utf-8") as f:
                    str_authors = f.read()
                    authors_list = authors_parser.parse_author_file(str_authors)

                    if prefix == "docker":
                        assert len(authors_list) == 715, f"Expected 215 authors, got {len(authors_list)}"
                        first_author = authors_list[0]
                        assert first_author.get("given_name") == "Aanand", f"First author given_name incorrect: {first_author.get('given_name')}"
                        assert first_author.get("last_name") == "Prasad", f"First author last_name incorrect: {first_author.get('last_name')}"
                        assert first_author.get("email") == "aanand.prasad@gmail.com", f"First author email incorrect: {first_author.get('email')}"
                        assert any(a.get("name") == "Daan van Berkel" for a in authors_list), "Expected author 'Daan van Berkel' not found"
                        last_author = authors_list[-1]
                        assert last_author.get("email") == "jifeng.yin@gmail.com", f"Last author email incorrect: {last_author.get('email')}"
                    
                    elif prefix == "tensorFlow":
                        assert len(authors_list) == 3, f"Expected 3 authors, got {len(authors_list)}"
                        first_author = authors_list[0]
                        assert first_author.get("type") == "Organization", f"First author type incorrect: {first_author.get('type')}"
                        assert first_author.get("name") == "Google Inc.", f"First author name incorrect: {first_author.get('name')}"
                        found = False
                        for author in authors_list:
                            if (
                                author.get("email") == "terrytangyuan@gmail.com"
                                and author.get("last_name") == "Tang"
                            ):
                                found = True
                                break
                        assert found, "Expected author with email terrytangyuan@gmail.com and last_name Tang not found"
                    
                    elif prefix == "ireeOrg":
                        assert len(authors_list) == 3, f"Expected 3 authors, got {len(authors_list)}"

                        for i, author in enumerate(authors_list):
                            assert author.get("type") == "Organization", f"Author {i} is not an Organization: {author}"

                        last_author = authors_list[-1]
                        assert last_author.get("name") == "Advanced Micro Devices, Inc.", (
                            f"Last author name incorrect: {last_author.get('name')}"
                        )

                    elif prefix == "jetBrain":
                        assert len(authors_list) == 2, f"Expected 2 authors, got {len(authors_list)}"
                        first_author = authors_list[0]
                        assert first_author.get("last_name") == "Nurullin", f"First author last_name incorrect: {first_author.get('last_name')}"

                    elif prefix == "pluginsGLPI":
                        assert len(authors_list) == 1, f"Expected 1 authors, got {len(authors_list)}"
                        first_author = authors_list[0]
                        assert first_author.get("name") == "Julien Dombre", f"First author name incorrect: {first_author.get('last_name')}"





