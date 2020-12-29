from somef.cli import extract_bibtex

def test_extract_bibtex():
    test_txt = """
Author: Daniel Garijo Verdejo (@dgarijo)
Contributors: María Poveda, Idafen Santana, Almudena Ruiz, Miguel Angel García, Oscar Corcho, Daniel Vila, Sergio Barrio, Martin Scharm, Maxime Lefrancois, Alfredo Serafini, @kartgk.
Citing WIDOCO: If you used WIDOCO in your work, please cite the ISWC 2017 paper: https://iswc2017.semanticweb.org/paper-138
bib
@inproceedings{garijo2017widoco,
  title={WIDOCO: a wizard for documenting ontologies},
  author={Garijo, Daniel},
  booktitle={International Semantic Web Conference},
  pages={94--102},
  year={2017},
  organization={Springer, Cham},
  doi = {10.1007/978-3-319-68204-4_9},
  funding = {USNSF ICER-1541029, NIH 1R01GM117097-01},
  url={http://dgarijo.com/papers/widoco-iswc2017.pdf}
}
If you want to cite the latest version of the software, you can do so by using: https://zenodo.org/badge/latestdoi/11427075.
    """
    c = extract_bibtex(test_txt)
    # Only one element is returned.
    assert "@inproceedings" in c[0]
