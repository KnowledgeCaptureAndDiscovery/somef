# DEviLOG: Dynamic Evidential Lidar Occupancy Grid Mapping

This repository provides the dataset as well as the training pipeline that was used in our paper:

> **Data-Driven Occupancy Grid Mapping using Synthetic and Real-World Data**
> [IEEE Xplore](https://ieeexplore.ieee.org/document/9988605), [arXiv](https://arxiv.org/abs/2211.08278)
>
> [Raphael van Kempen](https://www.ika.rwth-aachen.de/en/institute/staff/raphael-van-kempen-msc.html), [Bastian Lampe](https://www.ika.rwth-aachen.de/en/institute/staff/bastian-lampe-m-sc.html), [Lennart Reiher](https://www.ika.rwth-aachen.de/en/institute/staff/lennart-reiher-msc.html), [Timo Woopen](https://www.ika.rwth-aachen.de/en/institute/management/timo-woopen-msc.html), [Till Beemelmanns](https://www.ika.rwth-aachen.de/en/institute/staff/till-beemelmanns-msc.html), and [Lutz Eckstein](https://www.ika.rwth-aachen.de/en/institute/management/univ-prof-dr-ing-lutz-eckstein.html)  
> [Institute for Automotive Engineering (ika), RWTH Aachen University](https://www.ika.rwth-aachen.de/en/)
>
> _**Abstract**_ —  In perception tasks of automated vehicles (AVs) data-driven have often outperformed conventional approaches. This motivated us to develop a data-driven methodology to compute occupancy grid maps (OGMs) from lidar measurements. Our approach extends previous work such that the estimated environment representation now contains an additional layer for cells occupied by dynamic objects. Earlier solutions could only distinguish between free and occupied cells. The information whether an obstacle could move plays an important role for planning the behavior of an AV. We present two approaches to generating training data. One approach extends our previous work on using synthetic training data so that OGMs with the three aforementioned cell states are generated. The other approach uses manual annotations from the nuScenes [1] dataset to create training data. We compare the performance of both models in a quantitative analysis on unseen data from the real-world
dataset. Next, we analyze the ability of both approaches to cope with a domain shift, i.e. when presented with lidar measurements from a different sensor on a different vehicle. We propose using information gained from evaluation on real-world data to further close the reality gap and create better synthetic data that can be used to train occupancy grid mapping models for arbitrary sensor configurations.

[![Demo Video](./assets/TODO.gif)](https://www.youtube.com/watch?v=TODO)

We hope our paper and code can help in your research. If this is the case, please cite:

```
@INPROCEEDINGS{9988605,
  author={van Kempen, Raphael and Lampe, Bastian and Reiher, Lennart and Woopen, Timo and Beemelmanns, Till and Eckstein, Lutz},
  booktitle={2022 International Conference on Electrical, Computer, Communications and Mechatronics Engineering (ICECCME)}, 
  title={Data-Driven Occupancy Grid Mapping using Synthetic and Real-World Data}, 
  year={2022},
  doi={10.1109/ICECCME55909.2022.9988605}}
```

## Content

- [Installation](#installation)
- [Data](#data)
- [Training](#training)
- [Evaluation](#evaluation)

## Installation

We suggest to create a new **[conda](https://docs.conda.io/) environment** with all required packages. This will automatically install the GPU version of TensorFlow with CUDA and cuDNN if an NVIDIA GPU is available. It is also necessary to fix some system paths in order for TensorFlow to correctly locate CUDA. Afterwards the environment must be re-activated.

```bash
# DEviLOG/
conda env create -f environment.yml
conda activate devilog
conda env config vars set LD_PRELOAD="$CONDA_PREFIX/lib/libcudart.so:$CONDA_PREFIX/lib/libcublas.so:$CONDA_PREFIX/lib/libcublasLt.so:$CONDA_PREFIX/lib/libcufft.so:$CONDA_PREFIX/lib/libcurand.so:$CONDA_PREFIX/lib/libcusolver.so:$CONDA_PREFIX/lib/libcusparse.so:$CONDA_PREFIX/lib/libcudnn.so"
conda activate devilog
```

<u>Alternatively</u>, it is possible to install all package dependencies in a **Python 3.8** environment (e.g. by using _virtualenv_) with _pip_. Note that *CMake* must be installed to build the `point-pillars` package.

```bash
# DEviLOG/
pip install -r requirements.txt
```

## Data

This repository contains a [TensorFlow Datasets](https://www.tensorflow.org/datasets) wrapper for the nuScenes dataset. Samples consisting of lidar point clouds and occupancy grid maps will automatically be generated in the training pipeline.

The nuScenes dataset can be downloaded from [here](https://www.nuscenes.org/nuscenes#download) (registration required). You will need the "full dataset", the "map expansion pack" and the "lidar-panoptic" package. For testing purposes, you can just download the "mini" splits instead of the full "trainval" split. The extracted folder must be placed in the manual installation directory for TensorFlow Datasets, e.g. `~/tensorflow_datasets/downloads/manual/v1.0-mini`. After extracting all archives you should have the following directories:

```bash
tensorflow_datasets/downloads/manual/
  v1.0-mini/  # or 'v1.0-trainval'
    maps/
      basemap/
      expansion/
      prediction/
    panoptic/
    samples/
    sweeps/
    v1.0-mini/  # or 'v1.0-trainval'
```

### Training

You can train a model to predict occupancy grid maps from lidar point clouds using training data created from the nuScenes dataset.

Start training the model by passing the provided [config file](model/config.yml) to the [training script](model/train.py).

```bash
# DEviLOG/model/
export TF_FORCE_GPU_ALLOW_GROWTH=true  # try this if cuDNN fails to initialize
./train.py -c config.yml
```

You can visualize training progress by pointing *TensorBoard* to the output directory (`model/output` by default). Training metrics will also be printed to `stdout`.

### Evaluation

Before evaluating your trained model on the test data, set the parameter `model-weights` to point to the `best_weights.hdf5` file in the `Checkpoints` folder of its model directory.

```bash
# DEviLOG/model/
./evaluate.py -c config.yml --model-weights output/<YOUR-TIMESTAMP>/Checkpoints/best_weights.hdf5
```

The evaluation results will be exported to the `Evaluation` folder in your model directory.

## Acknowledgement

>This research is accomplished within the project ”UNICARagil” (FKZ 16EMO0284K). We acknowledge the financial support for the project by the Federal Ministry of Education and Research of Germany (BMBF).
