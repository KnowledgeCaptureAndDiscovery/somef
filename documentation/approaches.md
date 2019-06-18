# Approaches
## Recap of problem
A good Github repository README (or similar documentation) file informs the user of the following:
1. What
    1. program does the repository hold?
    2. does this program do? (description)
2. How
    1. does the user install this program? (installation)
    2. does the user run this program? (invocation)
3. Whose efforts led to the creation of this program? (citation)

Other interesting github repository metadata that may be of interest include the following:

4. What programming languages build this repository's software?
5. Who has contributed to this repository? Who owns it?
6. How has the repository evolved from commit to commit?
7. How may I use this software? What license does it use?

## Leveraging Github's API
For problems 1.1 and 4-7, [Github's API](https://developer.github.com/v3/) provides us directly our desired information. 

## Description / Installation / Invocation / Citation 
However, tackling problems 1.2-3 is less straightforward and we may thus consider multiple approaches. As an example, let us consider the README of the [pyGeoPressure](https://github.com/whimian/pyGeoPressure) repository.

### A closer look at `pyGeoPressure` example
In this repository, descriptions include:
> A Python package for pore pressure prediction using well log data and seismic velocity data.

and

> # Features
>
> 1. Overburden (or Lithostatic) Pressure Calculation
> 2. Eaton's method and Parameter Optimization
> 3. Bowers' method and Parameter Optimization
> 4. Multivariate method and Parameter Optimization

Citation information includes:
> Yu, (2018). PyGeoPressure: Geopressure Prediction in Python. Journal of Open Source Software, 3(30), 992, https://doi.org/10.21105/joss.00992

and
> ```bibtex 
> @article{yu2018pygeopressure,
> title = {{PyGeoPressure}: {Geopressure} {Prediction} in {Python}},
> author = {Yu, Hao},
> journal = {Journal of Open Source Software},
> volume = {3},
> pages = {922}
> number = {30},
> year = {2018},
> doi = {10.21105/joss.00992},
>}
>```
The installation command is:
> ## Installation
>
> `pyGeoPressure` is on `PyPI`:
>
> ```bash
> pip install pygeopressure
> ```
and its invocation command is found in its `Example` section, i.e.
> ## Example
>
> ### Pore Pressure Prediction using well log data
>
> ```python
> import pygeopressure as ppp
>
> survey = ppp.Survey("CUG")
> 
> well = survey.wells['CUG1']
>
> a, b = ppp.optimize_nct(well.get_log("Velocity"),
>                  well.params['horizon']["T16"],
>                  well.params['horizon']["T20"])
> n = ppp.optimize_eaton(well, "Velocity", "Overburden_Pressure", a, b)
>
> pres_eaton_log = well.eaton(np.array(well.get_log("Velocity").data), n)
>
> fig, ax = plt.subplots()
> ax.invert_yaxis()
>
> pres_eaton_log.plot(ax, color='blue')
> well.get_log("Overburden_Pressure").plot(ax, 'g')
> ax.plot(well.hydrostatic, well.depth, 'g', linestyle='--')
> well.plot_horizons(ax)
> ```

### Observations and Discussions
Whereas sometimes a reader of documentation relies on headings to identify a text's function, i.e. description / installation / invocation / citation, sometimes this heading is missing and the reader must deduce the function from the text. In the previous example, an example of this would be the citation information. However, in other circumstances, a heading may prove indispensable to distinguish categories, let's say an installation from an invocation. For example, without the aid of a heading, the difference between `python3 setup.py` and `python3 run.py` may not be obvious enough to qualify as an installation or execution.

Given this information, the focus is on the following two approaches:

1. Identify the headers within a document and deduce from them the text's function. Possibly, also follow links within the text to find more information. For example, if the README links to an `INSTALLATION.md` file, this `INSTALLATION.md` is probably of interest.
2. Analyze a corpus of descriptions, installations, invocations, and citations to detect linguistic properties and signals that distinguish one from the others.

It may even be possible to eventually synthesize these two methods.