# ToKEi: Temporal Knowledge Graph Embeddings with Arbitrary Time Precision

This is the implementation of the ToKEi models for Temporal Knowledge Graph 
Embeddings (TKGE) with arbitrary time precision. This code is based on the
is original [RotatE](https://github.com/DeepGraphLearning/KnowledgeGraphEmbedding)
toolkit.

# Requirements
The model is implemented in Python 3, using the PyTorch library.
Other library requirements are listed in `requirements.txt`.
To load them into your preference virtual execution environment, use:

    pip install -r requirements.txt

# Data

Each dataset in stored under a single directory, featuring:
  - entities.dict  # Key values pairs for entities
  - relations.dict # Key values pairs for relations
  - temporal       # Facts with validity annotations
  - non-temporal   # Optional non-temporal facts.

# Usage

## Pre-training
```
    CUDA_VISIBLE_DEVICES=0 python RotatE/run.py                \
            --cuda                                             \
            --do_train                                         \
            --do_valid                                         \
            --do_test                                          \
            --data_path data/RotatE/wikidata12k                \
            --model RotatE                                     \
            -n 256 -b 1024 -d 1000                             \
            -g 24.0 -a 1.0 -adv                                \
            -lr 0.0001 --max_steps 150000                      \
            -save models/RotatE_WD12k --test_batch_size 16 -de
```
For a complete list of options, try:

    python run.py --help


## Training temporal models

```
    CUDA_VISIBLE_DEVICES=0 python train.py 
            --seed 0 --data_path data/wikidata12k              \
            -n 128 -b 1024 -p 15000 -wu 5000                   \
            -a 1.0 -lr 0.0001 --max_steps 45000                \
            -save models/RotatE_WD12k_CDY --test_batch_size 16 \
            -scope d1100_1_1,d2019_6_30,CDY
```
For more options, try:

    python train.py --help

## Testing pre-trained temporal models 

```
    CUDA_VISIBLE_DEVICES=0 python test.py 
            --data_path data/wikidata12k                       \
            -n 128 -b 1024 -p 15000 -wu 5000                   \
            -a 1.0 -lr 0.0001 --max_steps 45000                \
            -save models/RotatE_WD12k_CDY --test_batch_size 16 \
            -scope d1100_1_1,d2019_6_30,CDY                    \
	    --test_levels --test_time --test_scoping --test_ranking
```

For more options, try:

    python test.py --help

# Citation
```latex
@inproceedings{
  author    = {Julien Leblay and Melisachew Wudage Chekol and Xin Liu},
  title     = {Towards Temporal Knowledge Graph Embeddings with Arbitrary Time Precision},
  booktitle = {Proceedings of the 29th {ACM} International Conference on Information and Knowledge Management ({CIKM} '20), October 19--23, 2020, Virtual Event, Ireland},
  publisher = {{ACM}},
  year      = {2020},
  url       = {https://doi.org/10.1145/3340531.3412028},
  doi       = {10.1145/3340531.3412028},
}
```
