# Practical Hilbert space approximate Bayesian Gaussian processes for probabilistic programming
Approximate eigendecomposition of the covariance function of a Gaussian process (GP). The method is based on interpreting the covariance function as the kernel of a pseudo-differential operator and approximating it using Hilbert space methods. This results in a reduced-rank approximation for the covariance function (Solin and Särkkä, 2020).

We denote this reduced rank GP model as the Hilbert space approximate Gaussian process (HSGP).

# Contents
This repo contains three folders:
## 1. Paper
This contains the main manuscript of the work, the supplemental material associated to the main manuscript and a poster presentated at StanCon 2020 conference. Additionally, this folder contains the Stan codes for every case study developed in the paper.
## 2. uni_dimensional
This contains a first R-notebook presenting the method for some examples and comparison to exact GPs and splines. Furthermore, this folder contains some initial material of the investigation with R-code and Stan code for some univariate data sets. There are the Stan codes for implementing the approximate GP (HSGP) model, the exact GP model and a spline model on the data sets. 
## 2. multi_dimensional
This contains some initial material of the investigation with R-code and Stan code for some multivariate data sets. There are the Stan codes for implementing the approximate GP (HSGP) model, the exact GP model and a spline model on the data sets.
