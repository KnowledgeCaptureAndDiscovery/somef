# Reggae: Dipole modes from `PBjam`

<a href="https://pb-reggae.readthedocs.io/en/latest/?badge=latest"><img src="https://readthedocs.org/projects/pb-reggae/badge/?version=latest" alt="readthedocs status" /></a>

<a href="https://doi.org/10.5281/zenodo.12730547"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.12730547.svg" alt="DOI"></a>

<a href="https://joss.theoj.org/papers/e6adb7a3b7cabe398f6c23297da1d3b3"><img src="https://joss.theoj.org/papers/e6adb7a3b7cabe398f6c23297da1d3b3/status.svg"></a>

<!-- index.rst blurb start -->

Reggae is a diagnostic tool for generating optimal parameters describing dipole mixed modes under the nonasymptotic matrix-coupling scheme of [Ong & Basu (2020)](https://ui.adsabs.harvard.edu/abs/2020ApJ...898..127O/abstract) used in the second release of [PBjam](https://github.com/grd349/PBjam) (see [Nielsen et al. 2021](https://ui.adsabs.harvard.edu/abs/2021AJ....161...62N/abstract)).

Since the primary samples of the [PLATO mission](https://ui.adsabs.harvard.edu/abs/arXiv:2406.05447) consist mainly of main-sequence and subgiant stars, PBjam implements a parameterisation of dipole modes suitable to these stars, outside the red-giant "asymptotic" regime. Reggae assists in the task of manually fine-tuning the dipole-mode model, and checking the quality of both our initial guesses and fitted solutions. An important part of this tuning is visual assessment of how well the data matches posterior samples for these parameters. Such asteroseismic visualisations often use the échelle power diagram near $\nu_{\mathrm{max}}$ as a diagnostic tool, with clearly-defined ridges emerging on this diagram for p-modes, such as in main-sequence stars.

We found Reggae very helpful both for these tuning and visualisation tasks, and also as a didactic aid to understanding the dipole mixed-mode parameters. As such, we release it publicly in advance of the second PBjam version, as we believe the community will benefit from access to such a visualisation tool. This will also assist future users of PBjam in devising ad-hoc prior constraints on the mixed-mode parameters, should they wish not to rely on the prior included with it.

<!-- index.rst blurb end -->

<a href="https://pb-reggae.readthedocs.io/en/latest/">For more details, please read our documentation here.</a>

## Installation

`reggae` is not yet available on PyPI. We recommend you install it in a virtual environment, from a local copy of the repository. For example:

```
git clone git@github.com:darthoctopus/reggae.git
cd reggae
python -m venv venv
. venv/bin/activate
pip install -e .
```

Please check [our documentation](https://pb-reggae.readthedocs.io/en/latest/installation.html) for more detailed installation and troubleshooting instructions.

## Usage

Reggae may be operated in many ways. It may be easiest to run the GUI with the command

```
python -m reggae
```

For more detailed usage instructions, please refer to our [documentation](https://pb-reggae.readthedocs.io/en/latest/usage.html).

## Generative model for mode frequencies

<!-- index.rst science start -->

We implement a generative model for dipole gravitoacoustic mixed modes using the parameterisation of [Ong & Basu (2020)](https://ui.adsabs.harvard.edu/abs/2020ApJ...898..127O/abstract). At present, the frequency-dependent coupling strength is described with two parameters (one for each of the two matrices entering into the parameterisation), with a conversion to the asymptotic $q$ provided by an expression in [Ong & Gehan (2023)](https://ui.adsabs.harvard.edu/abs/2023ApJ...946...92O/abstract). This expression is in turn used to generate stretched echelle power plots for diagnostic purposes.

In full, the generative model accepts the following parameters:

- $\Delta\Pi_0$, the notional period spacing of the g-mode cavity; this is related to the period spacing of any given $\ell$ as $\Delta\Pi_\ell = \Delta\Pi_0 / \sqrt{\ell(\ell + 1)}$.
- $p_L$ and $p_D$, the two coupling parameters described above.
- $\epsilon_g$, a g-mode phase offset.
- $\log \left(\delta\omega_\mathrm{rot, g} / \mathrm{\mu Hz}\right)$ and $\log \left(\delta\omega_\mathrm{rot, p} / \mathrm{\mu Hz}\right)$ --- the implementation of the PSD model (below) accepts separate values of the core (g-mode) and envelope (p-mode) rotational splittings. The pure p- and g-modes are split into multiplets separately before mode-coupling calculations are performed, thereby fully accounting for near-degeneracy asymmetric rotational splittings.
- $\delta_{01}$, an additional phase offset for the dipole p-modes relative to the asymptotic solution found by pbjam.
- $\alpha_g$, a curvature parameter for the g-modes (mirroring that of the p-modes in pbjam's asymptotic parameterisation).
- $i$, the inclination of the rotational axis.

<!-- index.rst science end -->

## PSD Model

The above parameters generate a set of dipole-mode frequencies. These parameters are fitted to the power spectrum in a fashion analogous to pbjam's "asymptotic peakbagging" step, whereby the generative model is used to construct a model power spectrum which is compared directly to the observational power spectrum, in order to constrain the model parameters. In order to make the likelihood function more amenable to optimisation and sampling, the linewidths of this artifical model PSD are deliberately broadened in a uniform manner (by default, by $1/200 \Delta\nu$) --- this has the effect of smoothing out the likelihood landscape, thereby alleviating the issue of trapping in tight local minima caused by the very narrow linewidths of the g-dominated mixed modes.

## GUI

In addition to a `DipoleStar` class (analogous to `star` in `pbjam`), we provide a GUI console for fine-tuning an initial guess to these asymptotic parameters. The primary use case for this is to refine the search space (i.e. reduce size of the prior volume) for more expensive computational methods, such as nested sampling. Simple tasks, such as simplex and genetic-algorithm optimisation, can also be performed from within the GUI.

![Screenshot of the GUI in operation, showing frequency and period-échelle power diagrams](screenshots/echelle.png)

## Contributing

<!-- index.rst contributing start -->

Reggae is currently developed by the following team:

- Joel Ong (Mode frequency generative model + GUI)
- Martin B. Nielsen (PSD model)
- Guy R. Davies
- Emily Hatt

We welcome contributions from the community. Easy ways to get started include:

- Finding bugs in our code — please open GitHub issues for these.
- Implementing feature suggestions — we welcome pull requests!

<!-- index.rst contributing end -->

We expect contributors to adhere to our [code of conduct](CODE_OF_CONDUCT.md).

## License

Reggae is released under the MIT license.