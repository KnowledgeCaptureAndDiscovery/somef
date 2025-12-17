![Demo figure](notebooks/paper_figures/Intro_NewLabels-2.png)


# ICON: Learning Regular Maps through Inverse Consistency

[<img src="https://github.com/uncbiag/ICON/actions/workflows/test-action.yml/badge.svg">](https://github.com/uncbiag/ICON/actions)
[<img src="https://img.shields.io/pypi/v/icon_registration.svg?color=blue">](https://pypi.org/project/icon-registration)
[<img src="https://readthedocs.org/projects/icon/badge/?version=master">](https://icon.readthedocs.io/en/master/)


This is the official repository for  

**ICON: Learning Regular Maps through Inverse Consistency.**   
Hastings Greer, Roland Kwitt, Francois-Xavier Vialard, Marc Niethammer.  
_ICCV 2021_ https://arxiv.org/abs/2105.04459

**GradICON: Approximate Diffeomorphisms via Gradient Inverse Consistency.**  
Lin Tian, Hastings Greer, Francois-Xavier Vialard, Roland Kwitt, Raúl San José Estépar, Marc Niethammer.  
_CVPR 2023_ https://arxiv.org/abs/2206.05897

**Inverse Consistency by Construction for Multistep Deep Registration.**
Hastings Greer, Lin Tian, Francois-Xavier Vialard, Roland Kwitt, Sylvain Bouix, Raul San Jose Estepar, Richard Rushmore and Marc Niethammer.
_MICCAI 2023_ https://arxiv.org/abs/2305.00087

## Cite this work
```
@InProceedings{Greer_2021_ICCV,
    author    = {Greer, Hastings and Kwitt, Roland and Vialard, Francois-Xavier and Niethammer, Marc},
    title     = {ICON: Learning Regular Maps Through Inverse Consistency},
    booktitle = {Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)},
    month     = {October},
    year      = {2021},
    pages     = {3396-3405}
}
```

```
@article{Tian_2022_arXiv,
  title={GradICON: Approximate Diffeomorphisms via Gradient Inverse Consistency},
  author={Tian, Lin and Greer, Hastings and Vialard, Fran{\c{c}}ois-Xavier and Kwitt, Roland and Est{\'e}par, Ra{\'u}l San Jos{\'e} and Niethammer, Marc},
  journal={arXiv preprint arXiv:2206.05897},
  year={2022}
}
```
```
@misc{greer2023inverseconsistencyconstructionmultistep,
      title={Inverse Consistency by Construction for Multistep Deep Registration}, 
      author={Hastings Greer and Lin Tian and Francois-Xavier Vialard and Roland Kwitt and Sylvain Bouix and Raul San Jose Estepar and Richard Rushmore and Marc Niethammer},
      year={2023},
      eprint={2305.00087},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2305.00087}, 
}
```


## uniGradICON and multiGradICON

If you are interested in general purpose deep learning registration approaches check out [uniGradICON and multiGradICON](https://github.com/uncbiag/uniGradICON). These networks were trained using the GradICON technology but over many different datasets allowing them to generalize to different unimodal and multimodal registration tasks. 

## Video Presentation

[<img src="https://img.youtube.com/vi/7kZsJ3zWDCA/maxresdefault.jpg" width="50%">](https://youtu.be/7kZsJ3zWDCA)


## Running our code

We are available on PyPI!
```bash
pip install icon-registration
```


To run our pretrained model in the cloud on sample images from OAI knees, visit [our knee google colab notebook](https://colab.research.google.com/drive/1svftgw-vYWnLp9lSf3UkrG547atjbIrg?usp=sharing)

To run our pretrained model for lung CT scans on an example from COPDgene, visit [our lung google colab notebook](https://colab.research.google.com/github/uncbiag/ICON/blob/master/notebooks/ICON_lung_demo.ipynb)

----------------

To train from scratch on the synthetic triangles and circles dataset:

```bash
git clone https://github.com/uncbiag/ICON
cd ICON

pip install -e .

python training_scripts/2d_triangles_example.py
```

