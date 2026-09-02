![MEL+TNNT](https://github.com/KGCP/MEL-TNNT/blob/master/docs/MEL+TNNT.png)


---
# MEL: Metadata Extractor & Loader

## What is MEL?
Implements a set of classes and functions to extract metadata (and textual content) from various file formats, as JSON objects.

## Core Features
- Comprehensive metadata extraction support of various file types/formats.
- File attributes extraction: general metadata.
- Filetype structure and properties: specific metadata.
- Structured data associated to the file: associated metadata.
- Content extraction: raw text and binary-to-text conversion.
- Analysis of the textual content: pattern matching and keyword extraction.
- Input: a file; output: a JSON file with the metadata sets and content.
- It can store the result in a document store (by default, CouchDB).
- Integrated with The NLP-NER Toolkit for Named Entity Recognition tasks.

## Supported File Types/Formats:
- `.pdf`: uses Tesseract-OCR and pdftotext tools.
- `.docx`, `.pptx`: MSO "core properties".
- `.doc`, `.xls`, `.ppt`, `.vsd`, `.mpp`: (generalized to OLE 2 files).
- `.msg`: uses Win32 MAPI (Messaging API for Windows) + (OLE 2 file).
- `.docm`: uses a C# (.NET) converter.
- `.xlsx`
- `.csv`
- `.rtf`
- `.txt` | `.xml`, `.html`, `.htm`, `.json`: (processed as raw text files)
- `.zip`
- Images: `.jpg`, `.png`, etc.

## MEL Architecture
![UML Class Diagram](https://github.com/KGCP/MEL-TNNT/blob/master/docs/MEL/MEL-UML.png)

**Processing Model**: the methods implemented in MEL are generic and can be applied to extract the content and metadata of all supported file types/formats.
![Processing Model](https://github.com/KGCP/MEL-TNNT/blob/master/docs/MEL/MEL-ProcessingModel.png)

## Overview Demo
- ISWC 2021 - Posters & Demos Track | KGC Tutorial 2022: [demo video](https://www.youtube.com/watch?v=hWMZ1O-PSjE)


---
# TNNT: The NLP-NER Toolkit

## What is TNNT?
Implements a pipeline task to automate the extraction of categorised named entities from the unstructured information encoded in the source documents, using diverse Natural Language Processing (NLP) models and tools.  TNNT is integrated with MEL.

## Core Features
- Implements 21 models from 9 NLP tools.
- Capability of processing sequentially several blocks of models based on the input settings.
- Keeps general processing stats of the models processed.
- Generates an integrated summary of all recognised entities from all the processed models.
- The results are generated in JSON files (one for each processed model):
  - Each model generates the list of categories of the identified entities.
  - For each recognised entity, the toolkit retrieves its context information: start index in the document text and sentence.
- Hybrid processing data flow supported, either from/to the document store (CouchDB) or via direct processing from files.
- All textual content extracted by MEL (with many supported file types/formats such as PDF, DOCX, MSG, and TXT) is processable for the NLP/NER Toolkit.
- A built-in RESTful API that provides basic functions to browse the JSON file results and expand/complement/co-relate the NER results by performing other NLP tasks, such as part-of-speech tagging, dependency parsing, co-reference resolution.

## Supported NLP-NER tools and models
- NLTK.
- Stanford NER tagger: class_3, class_4, class_7.
- Stanza.
- spaCy: en_core_web_sm, en_core_web_md, en_core_web_lg
- Allen NLP: ELMo_NER, fine-grained_NER.
- Deep Pavlov: standard_onto, bert_onto, standard_conll2003, bert_conll2003.
- Polyglot.
- Flair: standard, ontonotes, fast, fast_ontonotes, pooled.
- Google BERT.

## TNNT Architecture
![TNNT Architecture](https://github.com/KGCP/MEL-TNNT/blob/master/docs/TNNT/TNNT-Architecture.png)
![UML Class Diagram](https://github.com/KGCP/MEL-TNNT/blob/master/docs/TNNT/TNNT-UML.png)

**Processing Model**: TNNT has been fully integrated with MEL.  MEL settings establish the way how TNNT will process some specific block of NER models for the input dataset (either from content stored on CouchDB or from a direct document processing immediately after the metadata extraction).  The following diagram presents the toolkit’s processing model: the first two blocks are orchestrated by MEL.
![Processing Model](https://github.com/KGCP/MEL-TNNT/blob/master/docs/TNNT/TNNT-ProcessingModel.png)

## Recognised Categories
From the implemented models, the toolkit can recognised entities from the following categories:
- `PERSON`: People, including fictional.
- `NORP`: Nationalities or religious or political groups.
- `FAC`: Buildings, airports, highways, bridges, etc.
- `ORG`: Companies, agencies, institutions, etc.
- `GPE`: Countries, cities, states.
- `LOC`: Non-GPE locations, mountain ranges, bodies of water.
- `PRODUCT`: Objects, vehicles, foods, etc. (Not services.)
- `EVENT`: Named hurricanes, battles, wars, sports events, etc.
- `WORK_OF_ART`: Titles of books, songs, etc.
- `LAW`: Named documents made into laws.
- `LANGUAGE`: Any named language.
- `DATE`: Absolute or relative dates or periods.
- `TIME`: Times smaller than a day.
- `PERCENT`: Percentage, including “%“.
- `MONEY`: Monetary values, including unit.
- `QUANTITY`: Measurements, as of weight or distance.
- `ORDINAL`: "first", "second", etc.
- `CARDINAL`: Numerals that do not fall under another type.

![Category classification from the models' perspective](https://github.com/KGCP/MEL-TNNT/blob/master/docs/TNNT/TNNT-CategoryClassification-ModelsPerspective.png)

## Overview Demo
- K-CAP 2021 | KGC Tutorial 2022: [demo video](https://www.youtube.com/watch?v=D4DEULn8EtU)


---
# Contacts
- Sergio J. Rodríguez Méndez <`Sergio.RodriguezMendez [at] anu.edu.au`>

# License
{MEL+TNNT} is publicly available under an MIT license, as specified in the [LICENSE](https://github.com/KGCP/MEL-TNNT/blob/master/LICENSE) file.