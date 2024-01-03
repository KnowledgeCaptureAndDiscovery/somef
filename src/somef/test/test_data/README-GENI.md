
![Geni Logo](https://github.com/oeg-upm/GEnI/blob/main/figs/GEnI%20logo%20background.png)

# 🖊 Installation
GEnI is an explainability framework, which feeds from [PyKeen](https://github.com/pykeen/pykeen) embeddings and predictions. Its **goal** is to provide **explainations and insights** for the entity predictions made by KGE models. For that purpose, a three-phase, sequential workflow is followed, which ranges from the most general feasible explaination (rules) to the most specific (influential facts detection). 
![Overview of the GEnI workflow](https://github.com/oeg-upm/GEnI/blob/main/figs/overview.png)
# 🤔 How to use GEnI
First, you should clone this GitHub repository as follows:

    git clone https://github.com/oeg-upm/GEnI.git
    
Once you have clone the repo, set up a clean Python 3.9 environment, either using conda or venv. Install the required packages as follows:

    pip install -r requirements.txt

**WARNING‼️** If you are NOT working in a Linux environment, you may have some issues with the packages **jax** and **jaxlib**, which are dependencies for the package **fuzzy-c-means**. The easiest workaround this issue is to uninstall these three packages, and make a clean install of fuzzy-c-means for your operative system as described in [the documentation of fuzzy-c-means](https://pypi.org/project/fuzzy-c-means/). After this, everything should run smoothly.

As you can see in the figure above, GEnI comprises two main stages: embedding and prediction generation, and prediction explaination. While the second stage is performed intrinsically by GEnI, the first stage is external and is fully supported by PyKeen. 

## ⚙️ Generating the embeddings and predictions
A dedicated script *generate_pykeen_embeddings.py* is provided to generate GEnI compliant embeddings. However, you can also generate these embeddings directly using PyKeen's source code, and perform the transformation afterwards. Nonetheless, it is easier to use the provided script. Here you have a sample execution of this script, which will generate the embeddings for the *Nations* dataset using the KGE model *TransE*. 

    python generate_pykeen_embeddings.py -m TransE -d nations

The model and the dataset should always be specified. But don't worry, the script will also notify you when there's an issue with the input. You can find all the parameters and options as follows:

    $python generate_pykeen_embeddings.py -h
    $usage: generate_pykeen_embeddings.py [-h] [--dataset DATASET] [--model MODEL] [--epochs EPOCHS] [--dim DIM]
                                         [--split SPLIT [SPLIT ...]] [--goal GOAL] [--tmp]
    
    optional arguments:
      -h, --help            show this help message and exit
      --dataset DATASET, -d DATASET
                            Indicate a dataset to work with
      --model MODEL, -m MODEL
                            Indicate a valid KGE model
      --epochs EPOCHS, -e EPOCHS
                            Number of training epochs. If unspecified, it uses 100 by default
      --dim DIM             Embedding dimension. If unspecified, it uses 100 by default
      --split SPLIT [SPLIT ...]
                            Training/Test/Validation split ratios. If unspecified, it uses 0.8 0.1 0.1
      --goal GOAL, -g GOAL  Specify the type of predictions to generate -> 'o' for object (tail) predictions -> 's' for subject
                            (head) predictions -> 'b' for both. If no value is specified, both predictions are computed by default
      --tmp                 Whether the generated data is permanently stored or deleted once processed. It unspecified, data is
                            stored permantently

After this execution, you'll notice that, inside the *dataset* folder, a new subfolder appears containing all the generated data. You can check all supported datasets and models on [PyKeen's documentation](https://pykeen.readthedocs.io/en/stable/)

## 💬 Using GEnI to explain predictions
With all embeddings and predictions ready, it's time to start explaining some predictions. There are two ways to perform this operation: explain a single prediction, or explain **all** of the predictions. 

### ☝️ Explaining a single prediction
Let's continue with the dataset we've used before, *nations*. Once of the predictions made by DistMult on this dataset is *(china,ngoorgs3,uk)*. One of the key aspects of GEnI is that it does not evaluate whether a predictions right or wrong, but always takes it as a ground truth to be explained. We could ask about a feasible explaination for this fact as follows:

    python main.py -m DistMult -d nations -f china ngoorgs3 uk
Which in this case will return:

    -->CURRENT FACT: (china,ngoorgs3,uk)
    [SUCCESS!] Your fact can be inferred using the rule chain (china, aidenemy, usa) ^ (usa, independence, uk) -> (china,ngoorgs3,uk)

It worked, yay! However, this may not always be the case, as some predictions may be entirely randomly made, thus making it impossible to obtain an insight.

### 🔍 Explaining all predictions
Now that we've checked that GEnI works for a single prediction, let's try and find insights for all the predictions we previously obtained. For that, we could simply execute the following command:

    python main.py -m DistMult -d nations --all

As in the previous case, GEnI will output a human-readable sentence for each prediction of the dataset, and an error message otherwise. However, console outputs are fleeting, and difficult to analyze. But, don't worry! If indicated, GEnI creates a Python dictionary with all the insights about every prediction, so it can be further used or analyzed. There are many more parameters that can be specified, which can be found using the *-h* flag on the script:

    usage: main.py [-h] [--dataset DATASET] [--model MODEL] [--threshold THRESHOLD] [--fact FACT [FACT ...]] [--goal GOAL] [--all]
               [--save] [--tmp]

    optional arguments:
      -h, --help            show this help message and exit
      --dataset DATASET, -d DATASET
                            Indicate a dataset to work with
      --model MODEL, -m MODEL
                            Indicate a valid KGE model
      --threshold THRESHOLD, -th THRESHOLD
                            User threshold value. Default value is 0.6
      --fact FACT [FACT ...], -f FACT [FACT ...]
                            Explain a single prediction in the format h r t
      --goal GOAL, -g GOAL  s if the head entity is predicted, o if the tail entity is predicted. Default value is o
      --all                 Explain all stored predictions
      --save, -s            Save final results
      --tmp                 Whether the generated data is permanently stored or deleted once processed. It unspecified, data is
                            stored permantently

# 📄 How to cite GEnI

        @article{amador_2023_geni,
      author    = {Elvira Amador{-}Dom{\'{\i}}nguez and
                   Emilio Serrano and
                   Daniel Manrique},
      title     = {GEnI: {A} framework for the generation of explanations and insights
                   of knowledge graph embedding predictions},
      journal   = {Neurocomputing},
      volume    = {521},
      pages     = {199--212},
      year      = {2023},
      url       = {https://doi.org/10.1016/j.neucom.2022.12.010},
      doi       = {10.1016/j.neucom.2022.12.010},
      timestamp = {Tue, 03 Jan 2023 15:21:14 +0100},
      biburl    = {https://dblp.org/rec/journals/ijon/Amador-Dominguez23.bib},
      bibsource = {dblp computer science bibliography, https://dblp.org}
    }

# 👥 Acknowledgements
This research work has been funded by the “Universidad Politécnica de Madrid” under the program “Ayudas para Contratos Predoctorales para la Realización del Doctorado”, by the Knowledge Spaces project (Grant PID2020-118274RB-I00 funded by MCIN/AEI/ 10.13039/501100011033), and by the Autonomous Region of Madrid through the program CABAHLA-CM (GA No. P2018/TCS-4423).
