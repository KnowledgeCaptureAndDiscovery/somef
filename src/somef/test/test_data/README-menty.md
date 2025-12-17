<p align="center">
  <img src="https://github.com/mentpy/mentpy/blob/main/docs/_static/logo.png?raw=true" alt="MentPy: A Measurement-Based Quantum computing simulator." width="70%">
</p>

<div align="center">
    <a href="https://pypi.org/project/mentpy">
        <img src="https://img.shields.io/pypi/v/mentpy">
    </a>
    <a href="https://pypi.org/project/mentpy">
        <img src="https://img.shields.io/pypi/wheel/mentpy">
    </a>
    <a href='https://docs.mentpy.com/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/mentpy/badge/?version=latest' alt='Documentation Status' />
    </a>
    <a href="https://codecov.io/gh/mentpy/mentpy" > 
        <img src="https://codecov.io/gh/mentpy/mentpy/graph/badge.svg?token=3EM0A3Q4MG"/> 
    </a>
    <a href="https://x.com/mentpy">
        <img alt="X (formerly Twitter) Follow" src="https://img.shields.io/twitter/follow/mentpy">
    </a>
    <a href="https://discord.gg/HNA36hmEE5">
      <img alt="Discord" src="https://img.shields.io/discord/1158882999551676586?logo=discord&label=Chat&labelColor=ffffff">
    </a>
</div>

The `mentpy` library is an open-source software for simulations of 
measurement-based quantum computing circuits. Currently, this package is in its alpha version and many features are still in development.

## Installation

You can install the stable release of `mentpy` from PyPI using:

```bash
pip install mentpy
```

For the latest, potentially unstable version, you can install directly from the source:

```bash
pip install git+https://github.com/mentpy/mentpy.git
```

If you're contributing to `mentpy` and need to install development dependencies, you can do so using:

```bash
git clone https://github.com/mentpy/mentpy.git
cd mentpy
pip install -e '.[dev]'
```

This command installs `mentpy` in editable mode with its additional development dependencies.

## Usage
To simulate a measurement pattern, you can use the `mp.PatternSimulator`.
```python
import mentpy as mp

st = mp.templates.grid_cluster(2,4)
ps = mp.PatternSimulator(st)
output = ps(np.random.rand(len(st.outputc)))
```

For visualization of circuits, you can use the `mp.draw(st)` function

![image](https://user-images.githubusercontent.com/52287586/230715389-bf280971-c841-437d-8772-bf59557b0875.png)

To calculate the lie algebra of a model $G_\theta$, you can use the `mp.utils.calculate_lie_algebra` function

```python
lie_alg = mp.utils.calculate_lie_algebra(st)
len(lie_alg)
>> 16
```

## Documentation

The documentation for `mentpy` can be found <a href="https://mentpy.readthedocs.io/en/latest/" target="_blank">here</a>.

## Contributing

We welcome contributions to `mentpy`! Please see our [contributing guidelines](./CONTRIBUTING.md) for more information.

## How to cite

If you use `mentpy` in your research, please cite it as follows:

```
@software{mantilla2023mentpy,
    title = {{MentPy: A Python package for parametrized MBQC circuits}},
    author = {Mantilla Calderón, Luis},
    year = {2023},
    url = {https://github.com/mentpy/mentpy},
}
```