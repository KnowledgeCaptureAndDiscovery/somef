---
editor_options: 
  markdown: 
    wrap: sentence
output: github_document
---

<!-- badges: start -->

[![R-CMD-check](https://github.com/gabrielblain/CropWaterBalance/actions/workflows/R-CMD-check.yaml/badge.svg)](https://github.com/gabrielblain/CropWaterBalance/actions/workflows/R-CMD-check.yaml) 
[![R-CMD-check](https://github.com/adamhsparks/CropWaterBalance/actions/workflows/R-CMD-check.yaml/badge.svg)](https://github.com/adamhsparks/CropWaterBalance/actions/workflows/R-CMD-check.yaml)
<!-- badges: end -->

# CropWaterBalance

Crop water balance accounting in the root zone for irrigation purposes.

# Basic Description

{CropWaterBalance} is an R package designed to assist users in irrigation scheduling based on the Water Balance Approach.
The package is capable of calculating reference evapotranspiration (ET0) through various methods and conducting crop water balance accounting.
Additionally, {CropWaterBalance} includes auxiliary functions for comparing different ET0 estimation methods, calculating descriptive statistics for ET0 and rainfall series, and estimating soil heat flux and water stress coefficient.
The functions `ET0_HS()`, `ET0_PT()`, and `ET0_PM()` are used to estimate daily ET0 amounts using the methods of Hargreaves-Samani, Priestley-Taylor, and FAO-56 Penman-Monteith, respectively.
The `Descriptive()` function is specifically designed to calculate descriptive statistics for ET0 and rainfall series, including sample mean, median, standard deviation, standard error, maximum value, minimum value, and frequency of zeros.
Additionally, the `Compare()` function may be used to calculate measures of accuracy and agreement between two ET0 or rainfall series.
The `Soil_Heat_Flux()` function uses average air temperature data to estimate the soil heat flux, and the `Water_Stress_Coef()` function calculates the water stress coefficient for a crop.
The package depends on R (\>= 2.10) and imports functions from the R packages {[PowerSDI](https://CRAN.R-project.org/package=PowerSDI/)} and {[lubridate](https://CRAN.R-project.org/package=lubridate)}.

# Installation

``` r
devtools::install_github("gabrielblain/CropWaterBalance")
```

# Basic Instructions



## Function ET0_PM()

Calculates daily reference evapotranspiration amounts using the Penman and Monteith method.

## Usage


``` r
ET0_PM(Tavg,
  Tmax,
  Tmin,
  Rn,
  RH,
  WS,
  G = NULL,
  Alt
)
```

## Arguments

-   Tavg: A vector, 1-column matrix or data frame with daily average air temperature.
-   Tmax: A vector, 1-column matrix or data frame with daily maximum air temperature in Celsius degrees.
-   Tmin: A vector, 1-column matrix or data frame with daily minimum air temperature in Celsius degrees.
-   Rn: A vector, 1-column matrix or data frame with daily net radiation in MJ M-2 DAY-1.
-   RH: A vector, 1-column matrix or data frame with daily relative Humidity in %.
-   WS: A vector, 1-column matrix or data frame with daily wind speed in M S-1.
-   G: Optional. A vector, 1-column matrix or data frame with daily soil heat flux in MJ M-2 DAY-1. Default is `NULL` and if `NULL` it is assumed to be zero. May be provided by Soil_Heat_Flux.
-   Alt: A single number defining the altitude at crop's location in metres.

## Value

Daily reference evapotranspiration amounts in millimetres.

## Examples


``` r
Tavg <- DataForCWB[, 2]
Tmax <- DataForCWB[, 3]
Tmin <- DataForCWB[, 4]
Rn <- DataForCWB[, 6]
WS <- DataForCWB[, 7]
RH <- DataForCWB[, 8]
G <- DataForCWB[, 9]
head(ET0_PM(Tavg, Tmax, Tmin, Rn, RH, WS, G, Alt = 700))
```

```
##        ET0_PM
## [1,] 2.440372
## [2,] 4.171917
## [3,] 4.290477
## [4,] 3.665459
## [5,] 4.848520
## [6,] 5.669878
```

## Function ET0_PT()

Calculates daily reference evapotranspiration amounts using the Priestley-Taylor method.

## Usage


``` r
ET0_PT(Tavg,
  Rn,
  G = NULL,
  Coeff = 1.26
)
```

## Arguments

-   Tavg: A vector, 1-column matrix or data frame with daily average air temperature.
-   Rn: A vector, 1-column matrix or data frame with daily net radiation in MJ M-2 DAY-1.
-   G: Optional. A vector, 1-column matrix or data frame with daily soil heat flux in MJ M-2 DAY-1. Default is `NULL` and if `NULL` it is assumed to be zero. May be provided by Soil_Heat_Flux
-   Coeff: Single number defining the Priestley-Taylor coefficient. Default is 1.26

## Value

Daily reference evapotranspiration amounts in millimetres.

## Examples


``` r
Tavg <- DataForCWB[, 2]
Rn <- DataForCWB[, 6]
G <- DataForCWB[, 9]
head(ET0_PT(Tavg, Rn, G))
```

```
##        ET0_PT
## [1,] 3.432709
## [2,] 5.849554
## [3,] 6.432616
## [4,] 5.695334
## [5,] 7.023900
## [6,] 7.817355
```

## Function ET0_HS()

Calculates daily reference evapotranspiration amounts using the Hargreaves-Samani method.

## Usage


``` r
ET0_HS(
  Ra,
  Tavg,
  Tmax,
  Tmin
)
```

## Arguments

-   Ra: A vector, 1-column matrix or data frame with daily net radiation in MJ M-2 DAY-1.
-   Tavg: A vector, 1-column matrix or data frame with daily average air temperature.
-   Tmax: A vector, 1-column matrix or data frame with daily maximum air temperature in Celsius degrees.
-   Tmin: A vector, 1-column matrix or data frame with daily minimum air temperature in Celsius degrees.

## Value

Daily reference evapotranspiration amounts in millimetres.

## Examples


``` r
Tavg <- DataForCWB[, 2]
Tmax <- DataForCWB[, 3]
Tmin <- DataForCWB[, 4]
Ra <- DataForCWB[, 5]
head(ET0_HS(
  Ra = Ra,
  Tavg = Tavg,
  Tmax = Tmax,
  Tmin = Tmin
))
```

```
##           ET0
## [1,] 4.703700
## [2,] 5.331592
## [3,] 5.664174
## [4,] 6.163377
## [5,] 5.291303
## [6,] 6.251883
```

## Function Soil_Heat_Flux()

Calculates the daily amounts of Soil Heat Flux.

## Usage


``` r
Soil_Heat_Flux(Tavg)
```

## Arguments

-   Tavg: A vector, 1-column matrix or data frame with daily average air temperature.

## Value

Daily amounts of soil Heat flux in MJ m-2 day-1.

## Examples


``` r
Tavg <- DataForCWB[, 2]
head(Soil_Heat_Flux(Tavg))
```

```
## Warning in Soil_Heat_Flux(Tavg): The first 3 G values were set to zero
```

```
##            [,1]
## [1,]  0.0000000
## [2,]  0.0000000
## [3,]  0.0000000
## [4,]  0.3806333
## [5,] -0.7796333
## [6,] -0.2007667
```

## Function Descriptive()

Calculates descriptive statistics for rainfall, evapotranspiration, or other variable.

## Usage


``` r
Descriptive(Sample)
```

## Arguments

-   Sample: A vector, 1-column matrix or data frame with rainfall, evapotranspiration, or other variable.
    ## Value

-   sample mean (Avg), sample median (Med), sample standard variation (SD), sample standard Error (SE), maximum value (MaxValue), minimum value (MinValue), and frequency of zeros (FreqZero%) \## Examples

## Examples


``` r
Rain <- DataForCWB[, 10]
Descriptive(Sample = Rain)
```

```
##   SampleSize  Avg  Med    SD   SE MaxValue MinValue FreqZero%
## 1        129 6.53 0.25 13.06 1.15    71.37        0     48.06
```

## Function Compare()

Calculates measures of accuracy and agreement.

## Usage


``` r
Compare(Sample1, Sample2)
```

## Arguments

-   Sample1: A vector, 1-column matrix or data frame with evapotranspiration or other variable.
-   Sample2: A vector, 1-column matrix or data frame with evapotranspiration or other variable.

## Value

-   Absolute mean error (AME), Square root of the mean squared error (RMSE), Willmott's indices of agreement: original (dorig), Modified (dmod) and refined (dref), Pearson determination coefficient (R2).

## Examples


``` r
Tavg <- DataForCWB[, 2]
Tmax <- DataForCWB[, 3]
Tmin <- DataForCWB[, 4]
Rn <- DataForCWB[, 6]
WS <- DataForCWB[, 7]
RH <- DataForCWB[, 8]
G <- DataForCWB[, 9]
Sample1 <-
  ET0_PM(
    Tavg = Tavg,
    Tmax = Tmax,
    Tmin = Tmin,
    Rn = Rn,
    RH = RH,
    WS = WS,
    G = G,
    Alt = 700
  )
Sample2 <- ET0_PT(Tavg = Tavg, Rn = Rn, G = G)
Compare(Sample1 = Sample1, Sample2 = Sample2)
```

```
##       AME     RMSE     dorig     dmod        dref     RQuad
## 1 1.69222 1.813449 0.6403158 0.376103 -0.05737454 0.8675223
```

## Function CWB()

Calculates several parameters of the crop water balance.
It also suggests when and how much to irrigate.

## Usage


``` r
CWB(
  Rain,
  ET0,
  AWC,
  Drz,
  Kc = NULL,
  Irrig = NULL,
  MAD = NULL,
  InitialD = 0,
  start.date
)
```

## Arguments

-   Rain: Vector, 1-column matrix or data frame with daily rainfall totals in millimetres.

-   ET0: Vector, 1-column matrix or data frame with daily reference evapotranspiration in millimetres.

-   AWC: Vector, 1-column matrix or data frame with the available water capacity of the soil, that is: the amount of water between field capacity and permanent wilting point in millimetres of water per centimetre of soil.

-   Drz: Vector, 1-column matrix or data frame defining the root zone depth in centimetres.

-   Kc: Vector, 1-column matrix or data frame defining the crop coefficient.
    If NULL its values are assumed to be 1.

-   Irrig: Vector, 1-column matrix or data frame with net irrigation amount infiltrated into the soil for the current day in millimetres.

-   MAD: Vector, 1-column matrix or data frame defining the management allowed depletion.
    Varies between 0 and 1.

-   InitialD Single number defining in millimetre, the initial soil water deficit.
    It is used to start the water balance accounting.
    Default value is 0, which assumes the root zone is at the field capacity.

-   start.date: Date at which the accounting should start.
    Formats: “YYYY-MM-DD”, “YYYY/MM/DD”.

## Value

-   Water balance accounting, including the soil water deficit.

## Examples


``` r
Tavg <- DataForCWB[, 2]
Tmax <- DataForCWB[, 3]
Tmin <- DataForCWB[, 4]
Rn <- DataForCWB[, 6]
WS <- DataForCWB[, 7]
RH <- DataForCWB[, 8]
G <- DataForCWB[, 9]
ET0 <- ET0_PM(Tavg, Tmax, Tmin, Rn, RH, WS, G, Alt = 700)
Rain <- DataForCWB[, 10]
Drz <- DataForCWB[, 11]
AWC <- DataForCWB[, 12]
MAD <- DataForCWB[, 13]
Kc <- DataForCWB[, 14]
Irrig <- DataForCWB[, 15]
head(CWB(
  Rain = Rain,
  ET0 = ET0,
  AWC = AWC,
  Drz = Drz,
  Kc = Kc,
  Irrig = Irrig,
  MAD = MAD,
  start.date = "2023-11-23"
))
```

```
##            DaysSeason Rain Irrig ET0 Kc WaterStressCoef_Ks ETc (P+Irrig)-ETc NonStandardCropEvap ET_Defict  TAW SoilWaterDeficit d_MAD D>=dmad
## 2023-11-22          1 45.5     0 2.4  1                  1 2.4          43.0                 2.4         0 45.7              0.0  13.7      No
## 2023-11-23          2  0.3     0 4.2  1                  1 4.2          -3.9                 4.2         0 45.7              3.9  13.7      No
## 2023-11-24          3  0.0     0 4.3  1                  1 4.3          -4.3                 4.3         0 45.7              8.2  13.7      No
## 2023-11-25          4 11.4     0 3.7  1                  1 3.7           7.8                 3.7         0 45.7              0.4  13.7      No
## 2023-11-26          5  0.3     0 4.8  1                  1 4.8          -4.6                 4.8         0 45.7              5.0  13.7      No
## 2023-11-27          6  0.0     0 5.7  1                  1 5.7          -5.7                 5.7         0 45.7             10.7  13.7      No
```

## Function CWB_FixedSchedule()

Calculates several parameters of the crop water balance.
It also suggests how much irrigate.

## Usage


``` r
CWB_FixedSchedule(
  Rain,
  ET0,
  AWC,
  Drz,
  Kc = NULL,
  Irrig = NULL,
  MAD = NULL,
  InitialD = 0,
  Scheduling,
  start.date
)
```

## Arguments

-   Rain: Vector, 1-column matrix or data frame with daily rainfall totals in millimetres.

-   ET0: Vector, 1-column matrix or data frame with daily reference evapotranspiration in millimetres.

-   AWC: Vector, 1-column matrix or data frame with the available water capacity of the soil, that is: the amount of water between field capacity and permanent wilting point in millimetre of water per centimetre of soil.

-   Drz: Vector, 1-column matrix or data frame defining the root zone depth in centimetres.

-   Kc: Vector, 1-column matrix or data frame defining the crop coefficient.
    If NULL its values are assumed to be 1.

-   Irrig: Vector, 1-column matrix or data frame with net irrigation amount infiltrated into the soil for the current day in millimetres.

-   MAD: Vector, 1-column matrix or data frame defining the management allowed depletion.
    Varies between 0 and 1.

-   InitialD Single number defining in millimetre, the initial soil water deficit.
    It is used to start the water balance accounting.
    Default value is 0, which assumes the root zone is at the field capacity.

-   Scheduling Single integer number defining the number of days between two consecutive irrigations.

-   start.date: Date at which the accounting should start.
    Formats: “YYYY-MM-DD”, “YYYY/MM/DD”.

## Value

-   Water balance accounting, including the soil water deficit.


``` r
Tavg <- DataForCWB[, 2]
Tmax <- DataForCWB[, 3]
Tmin <- DataForCWB[, 4]
Rn <- DataForCWB[, 6]
WS <- DataForCWB[, 7]
RH <- DataForCWB[, 8]
G <- DataForCWB[, 9]
ET0 <- ET0_PM(Tavg, Tmax, Tmin, Rn, RH, WS, G, Alt = 700)
Rain <- DataForCWB[, 10]
Drz <- DataForCWB[, 11]
AWC <- DataForCWB[, 12]
MAD <- DataForCWB[, 13]
Kc <- DataForCWB[, 14]
Irrig <- DataForCWB[, 15]
Scheduling <- 5
head(CWB_FixedSchedule(
  Rain = Rain,
  ET0 = ET0,
  AWC = AWC,
  Drz = Drz,
  Kc = Kc,
  Irrig = Irrig,
  MAD = MAD,
  Scheduling = Scheduling,
  start.date = "2023-11-23"
))
```

```
##            DaysSeason   Rain Irrig   ET0 Kc WaterStressCoef_Ks   ETc (P+Irrig)-ETc NonStandardCropEvap ET_Defict   TAW SoilWaterDeficit  d_MAD            Scheduling
## 2023-11-22          1 45.470     0 2.440  1                  1 2.440        43.030               2.440         0 45.72            0.000 13.716                    No
## 2023-11-23          2  0.254     0 4.172  1                  1 4.172        -3.918               4.172         0 45.72            3.918 13.716                    No
## 2023-11-24          3  0.000     0 4.290  1                  1 4.290        -4.290               4.290         0 45.72            8.208 13.716                    No
## 2023-11-25          4 11.430     0 3.665  1                  1 3.665         7.765               3.665         0 45.72            0.444 13.716                    No
## 2023-11-26          5  0.254     0 4.849  1                  1 4.849        -4.595               4.849         0 45.72            5.038 13.716 Time to Irrigate 5 mm
## 2023-11-27          6  0.000     0 5.670  1                  1 5.670        -5.670               5.670         0 45.72           10.708 13.716                    No
```

## DataForAWC: Soil texture and plant available water capacity (AWC).

AWC is the amount of water between field capacity and permanent wilting point.
Given in millimetre of water per centimetre of soil.
Extracted from: Irrigation Scheduling: The Water Balance Approach Fact Sheet No. 4.707 by A.
A. Andales, J. L. Chávez, T. A. Bauder..

## Usage


``` r
DataForAWC
```

## Format

-   Soil Texture Soil Texture
-   AWC Low Available water capacity in millimetre of water per centimetre of soil
-   AWC High Available water capacity in millimetre of water per centimetre of soil
-   AWC Average Available water capacity in millimetre of water per centimetre of soil

## Source

<https://extension.colostate.edu/topic-areas/agriculture/>.

## Examples


``` r
DataForAWC
```

```
##        Soil.Texture AWC.Low AWC.High AWC.Average
## 1      Coarse sands      50       70          60
## 2        Fine sands      70       80          80
## 3       Loamy sands      70      100          80
## 4       Sandy loams     100      130         120
## 5  Fine sandy loams     130      170         150
## 6  Sandy clay loams     130      180         160
## 7             Loams     180      210         200
## 8        Silt loams     170      210         190
## 9  Silty clay loams     130      170         150
## 10        Clay loam     130      170         150
## 11       Silty clay     130      140         130
## 12             Clay     110      130         120
```

## DataForCWB: Data for Water Balance Accounting.

Daily meteorological data from a weather station in Campinas, Brazil and other parameters required for calculating the crop water balance.
The meteorological data belongs to the Agronomic Institute of the state of Sao Paulo.

## Usage


``` r
DataForCWB
```

## Format

-   A data frame with 129 rows and 16 columns.
-   date date
-   tmed Average air temperature in Celsius degrees
-   tmax Maximum air temperature in Celsius degrees
-   tmin Minimum air temperature in Celsius degrees
-   Ra Extraterrestrial solar radiation in MJ M-2 DAY-1
-   Rn Net radiation in MJ M-2 DAY-1
-   W Wind speed in M S-1
-   RH Relative Humidity in %
-   G Soil Heat Flux in MJ M-2 DAY-1
-   Rain Rain in millimetres
-   Drz Depth of the root zone in centimetres
-   AWC available water capacity (amount of water between field capacity and permanent wilting point) in millimetre of water per centimetre of soil
-   MAD management allowed depletion (between 0 and 1)
-   Kc Crop coefficient (between 0 and 1)
-   Irrig Applied net irrigation in millimetres

## Source

<http://www.ciiagro.org.br/>.

## Examples


``` r
head(DataForCWB)
```

```
##         Date   tmed  tmax  tmin       Ra       Rn    W    RH     G   Rain    Drz AWC MAD Kc Irrig
## 1 11/23/2010 23.000 27.26 18.74 42.07246  6.04422 2.16 76.58 -0.64 45.470 0.3048 150 0.3  1     0
## 2 11/24/2010 23.730 29.00 18.46 42.12238 11.08968 2.57 64.50 -0.30  0.254 0.3048 150 0.3  1     0
## 3 11/25/2010 24.650 30.33 18.97 42.17043 12.71410 2.80 70.37  0.19  0.000 0.3048 150 0.3  1     0
## 4 11/26/2010 24.795 31.46 18.13 42.21660 11.46852 1.86 73.03  0.38 11.430 0.3048 150 0.3  1     0
## 5 11/27/2010 22.340 27.86 16.82 42.26093 12.89778 2.61 57.80 -0.78  0.254 0.3048 150 0.3  1     0
## 6 11/28/2010 23.400 30.70 16.10 42.30341 15.02158 2.42 48.06 -0.20  0.000 0.3048 150 0.3  1     0
```

## BugReports:

\<<https://github.com/gabrielblain/CropWaterBalance/issues> \>

## License:

MIT

## Authors:

Gabriel Constantino Blain, Graciela da Rocha Sobierajski, Regina Célia Matos Pires, Adam H. Sparks, Letícia L. Martins.
Maintainer: Gabriel Constantino Blain, [gabriel.blain\@sp.gov.br](mailto:gabriel.blain@sp.gov.br){.email}

## Acknowledgments:

The package uses data from the Fact Sheet number 4707 Irrigation Scheduling: The Water Balance Approach, by A.
A. Andales, J. L. Chávez, and T.
A. Bauder.
The authors greatly appreciate this initiative.

## References

Allen, R.G.; Pereira, L.S.; Raes, D.; Smith, M. Crop evapotranspiration.
In Guidelines for Computing Crop Water Requirements.
Irrigation and Drainage Paper 56; FAO: Rome, Italy, 1998; p. 300.

Andales, A.A.; Chávez, J.L.;Bauder, T.A.
2012.
Irrigation Scheduling: The Water Balance Approach.
Fact Sheet number 4707, crop series \| irrigation.
<https://extension.colostate.edu/docs/pubs/crops/04707.pdf>

Hargreaves, G.H.; Samani, Z.A.
1985.Reference crop evapotranspiration from temperature.
Appl.
Eng.
Agric,1, 96–99.

Package ‘lubridate', Version 1.9.3, Author Vitalie Spinu et al., <https://CRAN.R-project.org/package=lubridate>

Package ‘PowerSDI', Version 1.0.
0, Author Gabriel C. Blain et al., <https://CRAN.R-project.org/package=PowerSDI>

Priestley, C.H.B., Taylor, R.J., 1972.
On the Assessment of Surface Heat Flux and Evaporation Using Large-Scale Parameters.
Monthly Weather Review, 100 (2), 81–92.