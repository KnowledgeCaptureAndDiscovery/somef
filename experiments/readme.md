## Experiments

This folder contains the details for reproducing two significant portions of somef, which we separated in two different experiments.

The first experiment aimed at trianing four binary, sennce-based classifiers that would detect whether a candidate sentence is a description, an installation instruction, an invocation command or a citation. The `training_corpus` folder contains the materials used to train the different classifiers we tried. The `trained_models` folder contains the pickle files of the trained classifiers, and the `ranking` folder contains the scores of each classifier on each category. The best-performing classifiers for each category have been incorporated in the main somed application.

The second experiment aimed at counting what are the common header names developers and scientists use to describe their scientific software. The idea behind this analysis is that the header used in a readme file is a good indicator of the content of that section (e.g., "Getting started", "How to use", "How to contribute"), and we found that many different authors used similar headers to describe their own readme files. The `header_analysis` folder contains notebooks explaining how we actually derived the current categories we recognize in somef; as well as a notebook with the header analysis itself by looking for synonyms of the header of interest. 

The classifier work was performed by Allen Mao and Haripriya Dharmala.

The header analysis work was performed by Priya Dharlama and Jiaying Wang.