# node-qa-masker

This is a NodeJS port of [pymasker](https://github.com/haoliangyu/pymasker). It provides a convenient way to produce masks from the Quality Assessment band of Landsat 8 OLI images, as well as MODIS land products.

## Installation

``` bash
npm install qa-masker
```

## Use Example

### Landsat 8

The `LandsatMasker` class provides the functionality to load and generate masks from the Quality Assessment band of Landsat 8 OLI image.

``` javascript
var qm = require('qa-masker');
var Masker = qm.LandsatMasker;
var Confidence = qm.LandsatConfidence;

// read the band file to initialize
var masker = new Masker('LC80170302016198LGN00_BQA.TIF');

// generate mask in ndarray format
var mask = masker.getWaterMask(Confidence.high);

// save the mask as GeoTIFF
masker.saveAsTif(mask, 'test.tif');
```

Five methods are provided for masking:

* `getCloudMask(confidence)`

* `getCirrusMask(confidence)`

* `getWaterMask(confidence)`

* `getVegMask(confidence)` (for vegetation)

* `getSnowMask(confidence)`

* `getFillMask()` (for filled pixels)

The `LandsatConfidence` class provide the definition of the confidence that certain condition exists at the pixel:

* `LandsatConfidence.high` (66% - 100% confidence)

* `LandsatConfidence.medium` (33% - 66% confidence)

* `LandsatConfidence.low` (0% - 33% confidence)

* `LandsatConfidence.undefined`

For more detail about the definition, please visit [the USGS Landsat website](http://landsat.usgs.gov/qualityband.php);

These five methods would return a [ndarray](https://github.com/scijs/ndarray) mask.

If a mask that matches multiple conditions is desired, the function `getMultiMask()` could help:

``` javascript
var mask = masker.getMultiMask([
  { type: 'could', confidence: LandsatConfidence.high },
  { type: 'cirrus', confidence: LandsatConfidence.medium }
]);
```

### MODIS Land Products

By using the lower level `Masker` class, the masking of MODIS land product QA band is supported. Because [node-gdal](https://github.com/scijs/ndarray) doesn't support HDF format, you need to convert the QA band to a GeoTIFF first using like [QGIS](http://www.qgis.org/en/site/),

A handy class `ModisMasker` is provided for particularly masking the quality of land products:

``` javascript
var qm = require('qa-masker');
var Masker = qm.ModisMasker;
var Quality = qm.ModisQuality;

// read the band file to initialize
var masker = new Masker('MODIS_QC_Band.tif');

// generate mask in ndarray format
var mask = masker.getQaMask(Quality.high);

// save the mask as GeoTIFF
masker.saveAsTif(mask, 'mask.tif');
```

The `ModisQuality` provides the definition of pixel quality:

  * `ModisQuality.high`: corrected product produced at ideal quality for all bands

  * `ModisQuality.medium`: corrected product produced at less than ideal quality for some or all bands

  * `ModisQuality.low`: corrected product not produced due to some reasons for some or all bands

  * `ModisQuality.low_cloud`: corrected product not produced due to cloud effects for all bands

Masking other than the product quality is not directly provided because of the variety of bit structure for different products.

A low-level method is available to extract mask with the understand of bit structure:

``` javascript
var masker = new Masker('modis_qa_band.tif');
var mask = masker.getMask(0, 2, 2);
```

`getMask(bitPos, bitLen, value)` function use to bit mask to extract quality mask:

* `bitPos`: the start position of quality assessment bits

* `bitLen`: the length of all used quality assessment bits

* `value`: the desired bit value (in integer)

For the detail explanation, please read [MODIS Land Product QA Tutorial](https://lpdaac.usgs.gov/sites/default/files/public/modis/docs/MODIS_LP_QA_Tutorial-1b.pdf).

### Looking for command line tool?

If the command line tool is wanted, please use [pymasker](https://github.com/haoliangyu/pymasker).

### You are a GIS guy and want something GIS?

Take a look at the [arcmasker](https://github.com/haoliangyu/arcmasker), the ArcMap toolbox that uses the same mechanism.
